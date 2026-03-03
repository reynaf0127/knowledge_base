import json
import time
import random
import re
from google.api_core.exceptions import DeadlineExceeded, ServiceUnavailable, ResourceExhausted, InternalServerError
from common import get_credentials, get_ai_client, get_model_id, get_secret, DATASET_ID
from google.genai import errors as genai_errors


dataset_id = DATASET_ID

credentials = get_credentials()
ai_client = get_ai_client()
model_id = get_model_id()

google_user_token = get_secret(dataset_id, "google_user_token", secret_type="json")

# --- Helpers ---
RETRYABLE = (
    DeadlineExceeded,
    ServiceUnavailable,
    ResourceExhausted,
    InternalServerError,
)

def extract_json_from_text(text: str):
    if not text:
        raise ValueError("Empty response")

    # Strip ```json fences
    text = re.sub(r"```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```", "", text)

    # Try whole string
    try:
        return json.loads(text)
    except Exception:
        pass

    # Try to locate JSON array
    m = re.search(r"($begin:math:display$\[\\s\\S\]\*$end:math:display$)", text)
    if m:
        return json.loads(m.group(1))

    raise ValueError(f"Could not parse JSON. Head: {text[:200]}")

def is_429(e: Exception) -> bool:
    return isinstance(e, genai_errors.ClientError) and getattr(e, "status_code", None) == 429

def call_gemini_with_long_backoff(prompt: str, max_retries: int = 8) -> str:
    """
    On 429, back off HARD (60s, 120s, 180s...), because short retries often fail.
    """
    for attempt in range(max_retries):
        try:
            resp = ai_client.models.generate_content(model=model_id, contents=prompt)
            return resp.text if hasattr(resp, "text") else str(resp)
        except Exception as e:
            if is_429(e) and attempt < max_retries - 1:
                # hard backoff + jitter, cap at 5 minutes
                sleep_s = min(300, 60 * (attempt + 1)) + random.random() * 5
                print(f"[429] RESOURCE_EXHAUSTED. Sleeping {sleep_s:.1f}s then retrying...")
                time.sleep(sleep_s)
                continue
            raise

def generate_topics(tags):
    tags = tags

    prompt = f"""
    Return ONLY valid JSON (no markdown, no extra text).

    For each tag in this list, generate exactly 2 recent news topics that are close to everyday life
    and good for deeper research.

    Tags: {tags}

    Output must be a single flat JSON array of objects.
    Each object must have exactly:
    - "tag": one of the tags above
    - "topic": a short, specific topic

    Total objects must be {len(tags) * 2}.
    Example:
    [
    {{"tag":"habits","topic":"..."}},
    {{"tag":"habits","topic":"..."}},
    {{"tag":"productivity","topic":"..."}}
    ]
    """.strip()

    raw = call_gemini_with_long_backoff(prompt)
    data = extract_json_from_text(raw)

    # Basic validation
    if not isinstance(data, list) or len(data) != len(tags) * 2:
        raise ValueError(f"Expected {len(tags)*2} items, got {len(data) if isinstance(data, list) else type(data)}")

    results = [{"tag": str(x["tag"]), "topic": str(x["topic"]).strip()} for x in data]
    return results