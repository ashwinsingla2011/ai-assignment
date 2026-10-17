"""Minimal client for the Gemini / Gemma generateContent REST API."""

import time

import requests

from config import (
    API_BASE_URL,
    MAX_RETRIES,
    REQUEST_TIMEOUT_SECONDS,
    RETRY_BACKOFF_SECONDS,
)


class LLMClient:
    """Sends prompts to an LLM API and returns the generated text."""

    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
        self.url = f"{API_BASE_URL}/{model}:generateContent"

    def generate(self, prompt: str) -> str:
        """Send one prompt; retry on rate limits / server errors."""
        body = {"contents": [{"parts": [{"text": prompt}]}]}
        headers = {"Content-Type": "application/json", "x-goog-api-key": self.api_key}

        last_error = "unknown error"
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                resp = requests.post(
                    self.url, json=body, headers=headers, timeout=REQUEST_TIMEOUT_SECONDS
                )
            except requests.RequestException as exc:
                last_error = f"network error: {exc}"
            else:
                if resp.status_code == 200:
                    return self._extract_text(resp.json())
                last_error = f"HTTP {resp.status_code}: {resp.text[:200]}"
                if resp.status_code not in (429, 500, 502, 503, 504):
                    break  # not retryable (e.g. bad key, bad request)

            if attempt < MAX_RETRIES:
                time.sleep(RETRY_BACKOFF_SECONDS * attempt)

        raise RuntimeError(last_error)

    @staticmethod
    def _extract_text(data: dict) -> str:
        try:
            parts = data["candidates"][0]["content"]["parts"]
            # skip any "thought" parts some models return; keep only the final answer
            return "".join(
                p.get("text", "") for p in parts if not p.get("thought")
            ).strip()
        except (KeyError, IndexError, TypeError) as exc:
            raise RuntimeError(f"Unexpected response format: {data}") from exc
