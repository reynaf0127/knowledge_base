import json
from google.oauth2 import service_account
from google.cloud import secretmanager
from google import genai

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/cloud-platform",
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/drive.file",
]

DATASET_ID = "unity-other-learn-prd"
SA_SECRET_ID = "learn_service_account"
LOCATION = "us-central1"
MODEL_ID = "gemini-2.5-flash"
N_SENTENCE = 5
N_QUOTES = 5
MAX_QUOTE_WORDS = 20
MAX_WORD_COUNT = 1000
global_style = "Minimalist beige infographic, art cartoon style, soft neutral palette, clean layout with icons"



def load_sa_credentials_from_secret(
    project_id: str,
    secret_id: str,
    version_id: str = "latest",
    scopes: list[str] | None = None,
):
    sm_client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    resp = sm_client.access_secret_version(request={"name": name})
    sa_info = json.loads(resp.payload.data.decode("utf-8"))
    return service_account.Credentials.from_service_account_info(sa_info, scopes=scopes)


def get_credentials():
    return load_sa_credentials_from_secret(
        project_id=DATASET_ID,
        secret_id=SA_SECRET_ID,
        scopes=SCOPES,
    )


def get_ai_client():
    credentials = get_credentials()
    return genai.Client(
        vertexai=True,
        project=credentials.project_id,
        location=LOCATION,
        credentials=credentials,
    )


def get_model_id():
    return MODEL_ID


def access_secret_text(
    project_id: str,
    secret_id: str,
    version: str = "latest",
    credentials=None,
) -> str:
    # Use provided credentials if given, otherwise use your default SA creds
    if credentials is None:
        credentials = get_credentials()

    sm_client = secretmanager.SecretManagerServiceClient(credentials=credentials)
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version}"
    resp = sm_client.access_secret_version(request={"name": name})
    return resp.payload.data.decode("utf-8").strip()


def get_secret(
    project_id: str,
    secret_id: str,
    *,
    secret_type: str = "string",
    version: str = "latest",
    credentials=None,
):
    raw = access_secret_text(
        project_id=project_id,
        secret_id=secret_id,
        version=version,
        credentials=credentials,
    )

    if not raw:
        raise ValueError(f"Secret '{secret_id}' is empty")

    if secret_type == "json":
        try:
            return json.loads(raw)
        except json.JSONDecodeError as e:
            raise ValueError(f"Secret '{secret_id}' is not valid JSON") from e

    return raw