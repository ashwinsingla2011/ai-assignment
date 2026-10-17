"""Read prompts from a text file, query an LLM API, save responses to JSON.

Usage:
    export GEMINI_API_KEY="your-key"
    python src/main.py                       # uses data/text.txt -> output/responses.json
    python src/main.py -i my.txt -o out.json
    python src/main.py --whole-file          # send the entire file as one prompt
"""

import argparse
import sys
from pathlib import Path

import config
from file_io import read_prompts, save_results
from llm_client import LLMClient


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Send prompts from a text file to an LLM API.")
    p.add_argument("-i", "--input", type=Path, default=config.DEFAULT_INPUT_FILE)
    p.add_argument("-o", "--output", type=Path, default=config.DEFAULT_OUTPUT_FILE)
    p.add_argument("-m", "--model", default=config.DEFAULT_MODEL)
    p.add_argument("--whole-file", action="store_true",
                   help="treat the whole file as a single prompt")
    return p.parse_args()


def run(input_path: Path, output_path: Path, model: str, whole_file: bool = False) -> list[dict]:
    prompts = read_prompts(input_path, whole_file=whole_file)
    client = LLMClient(config.get_api_key(), model)

    results = []
    for index, prompt in enumerate(prompts, start=1):
        print(f"[{index}/{len(prompts)}] {prompt[:60]}")
        try:
            response, error = client.generate(prompt), None
        except RuntimeError as exc:
            response, error = None, str(exc)
            print(f"   failed: {error}", file=sys.stderr)
        results.append({"id": index, "prompt": prompt, "response": response, "error": error})

    save_results(results, output_path, model, input_path)
    print(f"Saved {len(results)} result(s) to {output_path}")
    return results


def main() -> None:
    args = parse_args()
    try:
        run(args.input, args.output, args.model, args.whole_file)
    except (FileNotFoundError, ValueError, RuntimeError) as exc:
        sys.exit(f"Error: {exc}")


if __name__ == "__main__":
    main()
