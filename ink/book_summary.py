import pandas as pd
import json
import time
import random
import re
from google.api_core.exceptions import DeadlineExceeded, ServiceUnavailable, ResourceExhausted, InternalServerError
from common import get_credentials, get_ai_client, get_model_id, get_secret, DATASET_ID, N_SENTENCE, N_QUOTES, MAX_QUOTE_WORDS, MAX_WORD_COUNT

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


PROMPT_TEMPLATE = """
Summarize the book "{title}" in exactly {n_sentence} short paragraphs (no more than {max_word_count} words total).

Then provide {n_quotes} short memorable quotes from the book (each under {max_quote_words} words).

Return ONLY valid JSON. Do not use markdown.

{{
  "summary": ["section1", "section2", "section3", "section4", "section5"],
  "quotes": ["...", "..."]
}}
"""

def extract_text(response):
    if getattr(response, "text", None):
        return response.text.strip()
    try:
        return response.candidates[0].content.parts[0].text.strip()
    except Exception:
        return None

def summarize_one_book(ai_client, model_id, title):
    prompt = PROMPT_TEMPLATE.format(
        title=title,
        n_sentence=N_SENTENCE,
        n_quotes=N_QUOTES,
        max_quote_words=MAX_QUOTE_WORDS,
        max_word_count=MAX_WORD_COUNT,
    )

    response = generate_with_retry(ai_client, model_id, prompt, max_retries=5)
    text = extract_text(response)
    if not text:
        return None, None

    cleaned = clean_json_text(text)

    try:
        data = json.loads(cleaned)
        return data.get("summary"), data.get("quotes")
    except json.JSONDecodeError:
        print("⚠️ JSON parse failed for:", title)
        print("Cleaned output was:\n", cleaned)
        return None, None

def build_book_dataframe(book_titles):
    ai_client = get_ai_client()
    model_id = get_model_id()

    rows = []

    for title in book_titles:
        summary, quotes = summarize_one_book(ai_client, model_id, title)

        rows.append({
            "book_title": title,
            "summary": summary,
            "quotes": quotes,
        })

    df = pd.DataFrame(rows)
    return df