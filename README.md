# AI Document Convertor

This project is a lightweight starter for an AI-powered document conversion tool. It provides a simple Python CLI that can convert text-based files between common formats such as TXT, MD, HTML, and JSON.

## Features
- Convert text files between simple formats
- Basic command-line interface
- Extensible design for future AI-powered document processing
- Ready for adding OCR, PDF parsing, or LLM integrations

## Project structure
- `main.py` — CLI entry point
- `requirements.txt` — Python dependencies
- `.gitignore` — common ignore rules

## Quick start

1. Clone the repository
2. Create a virtual environment
3. Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# or .venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

4. Run the converter

```bash
python main.py input.txt output.md
```

## Example conversions

```bash
python main.py sample.txt sample.html
python main.py sample.md sample.txt
python main.py sample.json sample.md
```

## Notes
This is a starter project intended to give you a working foundation. The conversion logic is intentionally simple and can be expanded with AI features, OCR, file validation, and richer format handling.
