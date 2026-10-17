"""Configuration constants for the LLM batch runner."""

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DEFAULT_INPUT_FILE = PROJECT_ROOT / "data" / "text.txt"
DEFAULT_OUTPUT_FILE = PROJECT_ROOT / "output" / "responses.json"

# Gemma models are served through the Gemini API; swap for any other model name.
DEFAULT_MODEL = "gemma-4-31b-it"
API_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models"
API_KEY_ENV_VAR = "GEMINI_API_KEY"

REQUEST_TIMEOUT_SECONDS = 60
MAX_RETRIES = 3
RETRY_BACKOFF_SECONDS = 2


def get_api_key() -> str:
    """Read the API key from the environment (never hard-code it)."""
    key = os.environ.get(API_KEY_ENV_VAR, "").strip()
    if not key:
        raise RuntimeError(
            f"Missing API key. Set the {API_KEY_ENV_VAR} environment variable "
            "(get a free key at https://aistudio.google.com/apikey)."
        )
    return key
