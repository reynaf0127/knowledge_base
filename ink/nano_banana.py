import time
import requests
import pandas as pd
from typing import List, Dict, Any, Optional

from common import get_credentials, get_ai_client, get_model_id, get_secret, DATASET_ID, global_style


# -----------------------
# Global setup
# -----------------------
dataset_id = DATASET_ID

credentials = get_credentials()
ai_client = get_ai_client()
model_id = get_model_id()

nanobanana_token = get_secret(dataset_id, "nanobanana", secret_type="string")

BASE_URL = "https://api.nanobananaapi.ai/api/v1/nanobanana"

HEADERS = {
    "Authorization": f"Bearer {nanobanana_token}",
    "Content-Type": "application/json",
}


# -----------------------
# NanoBanana API helpers
# -----------------------
def create_task(prompt: str,
                image_size: str = "9:16",
                num_images: int = 1,
                callback_url: str = "https://example.com/callback") -> str:
    payload = {
        "prompt": prompt,
        "numImages": num_images,
        "type": "TEXTTOIAMGE",
        "image_size": image_size,
        "callBackUrl": callback_url,
    }
    r = requests.post(f"{BASE_URL}/generate", headers=HEADERS, json=payload, timeout=60)
    r.raise_for_status()
    # return r.json()["data"]["taskId"]
    return r


def wait_for_result(task_id: str, poll_seconds: float = 2.0, max_polls: int = 60) -> str:
    """
    Poll NanoBanana until the task completes. Returns a single image URL.
    """
    for _ in range(max_polls):
        r = requests.get(
            f"{BASE_URL}/record-info",
            headers=HEADERS,
            params={"taskId": task_id},
            timeout=60,
        )

        try:
            r.raise_for_status()
        except requests.HTTPError as e:
            raise RuntimeError(f"NanoBanana /record-info HTTP {r.status_code}: {r.text}") from e

        try:
            j = r.json()
        except Exception as e:
            raise RuntimeError(f"NanoBanana /record-info returned non-JSON: {r.text}") from e

        data = j.get("data") or {}
        success_flag = data.get("successFlag")

        if success_flag == 1:
            resp = data.get("response") or {}
            url = resp.get("resultImageUrl")
            if not url:
                raise RuntimeError(f"Success but no resultImageUrl. Full JSON: {j}")
            return url

        if success_flag in (2, 3):
            raise RuntimeError(f"Task failed: {data.get('errorCode')} {data.get('errorMessage')}")

        time.sleep(poll_seconds)

    raise TimeoutError(f"Timed out waiting for task {task_id}")


# -----------------------
# CSV -> images pipeline
# -----------------------
def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize to a common schema when possible:
      - question -> title
      - answer   -> response
    """
    rename_map = {}
    if "title" not in df.columns and "question" in df.columns:
        rename_map["question"] = "title"
    if "response" not in df.columns and "answer" in df.columns:
        rename_map["answer"] = "response"

    return df.rename(columns=rename_map) if rename_map else df


def build_prompt(section_text: str, style: str) -> str:
    # Keep it short and consistent; avoid long text in-image unless you really want it
    return (
        f"{style}. "
        f"Create a single, clear visual concept representing the following content. "
        f"Content: '{section_text}'. "
        f"If you include text, keep it short and readable."
    )


def generate_images_from_topic_csv(
    csv_path: str,
    style: str,
    image_size: str = "9:16",
    num_images_per_section: int = 1,
    output_csv: str = "output_with_images.csv",
    sleep_between_tasks_s: float = 0.5,
) -> pd.DataFrame:
    
    df = pd.read_csv(csv_path)
    df = normalize_columns(df)

    rows: List[Dict[str, Any]] = []

    for _, r in df.iterrows():
        title = str(r["title"]).strip()
        section_text = str(r["response"]).strip()
        section_index = r["section_index"] if "section_index" in df.columns else None

        prompt = build_prompt(section_text, style)
        task_id = create_task(
            prompt=prompt,
            image_size=image_size,
            num_images=num_images_per_section,
        )
        image_url = wait_for_result(task_id)

        rows.append({
            "title": title,
            "section_index": section_index,
            "section_text": section_text,
            "prompt": prompt,
            "task_id": task_id,
            "image_url": image_url,
        })

        time.sleep(sleep_between_tasks_s)

    out_df = pd.DataFrame(rows)
    out_df.to_csv(output_csv, index=False)
    return out_df


def test_csv(
    csv_path: str,
    style: str,
    image_size: str = "9:16",
    num_images_per_section: int = 1,
    output_csv: str = "output_with_images.csv",
    sleep_between_tasks_s: float = 0.5,
) -> pd.DataFrame:
    
    df = pd.read_csv(csv_path)
    df = normalize_columns(df)

    rows: List[Dict[str, Any]] = []

    for _, r in df.iterrows():
        title = str(r["title"]).strip()
        section_text = str(r["response"]).strip()
        section_index = r["section_index"] if "section_index" in df.columns else None
        prompt = build_prompt(section_text, style)
        task_id = create_task(
            prompt=prompt,
            image_size=image_size,
            num_images=num_images_per_section,
        )
        rows.append({
            "title": title,
            "section_index": section_index,
            "section_text": section_text,
            "prompt": prompt,
            "task_id": task_id,
        })
    
    out_df = pd.DataFrame(rows)
    print(out_df.head())

# -----------------------
# Entrypoint
# -----------------------
if __name__ == "__main__":
    # out_df = generate_images_from_topic_csv(
    #     csv_path="topic_answers.csv",
    #     style=global_style,
    #     image_size="9:16",
    #     num_images_per_section=1,
    #     output_csv="output_with_images.csv",
    #     sleep_between_tasks_s=0.5,
    # )
    # print(out_df.head())
    test_csv("topic_answers.csv", global_style)