import pandas as pd
import json
import time
import random
import re
from typing import List, Dict, Any
from google.api_core.exceptions import DeadlineExceeded, ServiceUnavailable, ResourceExhausted, InternalServerError
from common import get_credentials, get_ai_client, get_model_id, get_secret, DATASET_ID

dataset_id = DATASET_ID

credentials = get_credentials()
ai_client = get_ai_client()
model_id = get_model_id()

google_user_token = get_secret(dataset_id, "google_user_token", secret_type="json")
airtable_api = get_secret(dataset_id, "airtable_api_personal", secret_type="string")

# modify timeout:
RETRIABLE = (DeadlineExceeded, ServiceUnavailable, ResourceExhausted, InternalServerError)

def generate_with_retry(ai_client, model_id, contents, max_retries=5):
    last_err = None

    for attempt in range(max_retries):
        try:
            # Some google-genai versions accept a 'timeout' kwarg; some don't.
            # We'll try with timeout first, then fall back without it.
            try:
                return ai_client.models.generate_content(
                    model=model_id,
                    contents=contents,
                    timeout=120,  # seconds (if supported by your installed version)
                )
            except TypeError:
                return ai_client.models.generate_content(
                    model=model_id,
                    contents=contents,
                )

        except RETRIABLE as e:
            last_err = e
            # exponential backoff + jitter
            sleep_s = min(2 ** attempt, 32) + random.uniform(0, 1.5)
            print(f"⚠️ Retryable error ({type(e).__name__}): {e} — sleeping {sleep_s:.1f}s (attempt {attempt+1}/{max_retries})")
            time.sleep(sleep_s)

    raise last_err


def clean_json_text(text: str) -> str:
    if not text:
        return text

    t = text.strip()

    # Remove ```json ... ``` or ``` ... ```
    if t.startswith("```"):
        # remove the first line ```json or ```
        t = re.sub(r"^```[a-zA-Z0-9_-]*\s*\n", "", t)
        # remove trailing ```
        t = re.sub(r"\n```$", "", t).strip()

    # If model added extra text, keep only the first JSON object
    # Find the first '{' and last '}' and slice
    first = t.find("{")
    last = t.rfind("}")
    if first != -1 and last != -1 and last > first:
        t = t[first:last+1]

    return t


def extract_text(response):
    if getattr(response, "text", None):
        return response.text.strip()
    try:
        return response.candidates[0].content.parts[0].text.strip()
    except Exception:
        return None


PROMPT_TEMPLATE = """
Answer the following question: "{question}"

Requirements:
- Write exactly {n_paragraphs} paragraphs.
- Keep the total response under 1000 words.
- Each paragraph must be divided into exactly 5 sections.
- Return ONLY valid JSON (no markdown, no extra text).

Output JSON schema:
{{
  "answer": ["section1", "section2", "section3", "section4", "section5"]
}}
"""


def answer_question_5_sections(ai_client, model_id: str, question: str, n_paragraphs: int = 1) -> List[str]:
    """Return exactly 5 answer sections as a list of strings."""
    prompt = PROMPT_TEMPLATE.format(question=question, n_paragraphs=n_paragraphs)

    response = generate_with_retry(ai_client, model_id, prompt, max_retries=5)
    text = extract_text(response)
    if not text:
        raise ValueError("Empty model response text")

    cleaned = clean_json_text(text)

    try:
        payload = json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise ValueError(f"Model did not return valid JSON. Cleaned output:\n{cleaned}") from e

    sections = payload.get("answer")
    if not isinstance(sections, list) or len(sections) != 5 or not all(isinstance(s, str) for s in sections):
        raise ValueError(f"Expected 'answer' to be a list of 5 strings. Got:\n{payload}")

    return sections


def build_answer_dataframe(topic_titles: List[str], n_paragraphs: int = 1) -> pd.DataFrame:
    rows: List[Dict[str, Any]] = []

    for q in topic_titles:
        try:
            sections = answer_question_5_sections(ai_client, model_id, q, n_paragraphs=n_paragraphs)
            for i, section in enumerate(sections, start=1):
                rows.append({"title": q, "response": section, "section_index": i})
        except Exception as e:
            # keep 5 rows even on failure (optional behavior)
            for i in range(1, 6):
                rows.append({"title": q, "response": None, "section_index": i})
            print(f"Error for title '{q}': {e}")

    return pd.DataFrame(rows)