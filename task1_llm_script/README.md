# LLM Batch Runner

Reads prompts from a text file, sends each to an LLM API (Gemma 4 via the Gemini API),
and saves every response to a JSON file.

## Structure
- `src/config.py`     - constants, API key lookup (from environment)
- `src/file_io.py`    - read prompts / write JSON
- `src/llm_client.py` - API call with retries
- `src/main.py`       - command-line entry point
- `data/text.txt`     - input (replace with the provided text.txt)
- `output/responses.json` - generated output

## Setup
1. `pip install -r requirements.txt`
2. Get a free API key: https://aistudio.google.com/apikey
3. `export GEMINI_API_KEY="your-key"` (Windows: `set GEMINI_API_KEY=your-key`)
4. Put the provided `text.txt` in `data/`
5. `python src/main.py`

Each non-empty line is one prompt. Use `--whole-file` to send the file as one prompt.

## Naming conventions used (PEP 8)
`snake_case` for files, functions, variables; `PascalCase` for classes; `UPPER_CASE` for constants.
