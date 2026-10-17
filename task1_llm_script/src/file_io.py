"""Helpers for reading prompts from a text file and writing results to JSON."""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def read_prompts(path: Path, whole_file: bool = False) -> list[str]:
    """Return prompts from a text file.

    By default every non-empty line is one prompt. With ``whole_file=True``
    the entire file is sent as a single prompt.
    """
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"Input file not found: {path}")

    text = path.read_text(encoding="utf-8").strip()
    if not text:
        raise ValueError(f"Input file is empty: {path}")

    if whole_file:
        return [text]
    return [line.strip() for line in text.splitlines() if line.strip()]


def save_results(results: list[dict[str, Any]], path: Path, model: str, source: Path) -> None:
    """Write results plus metadata to a JSON file (creates folders if needed)."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "metadata": {
            "model": model,
            "source_file": str(source),
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "total_prompts": len(results),
            "successful": sum(1 for r in results if r["error"] is None),
        },
        "results": results,
    }
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
