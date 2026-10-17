import argparse
import json
import os
import re
from pathlib import Path

try:
    import markdown
except ImportError:  # pragma: no cover
    markdown = None


def read_text(path):
    return Path(path).read_text(encoding="utf-8")


def write_text(path, content):
    Path(path).write_text(content, encoding="utf-8")


def txt_to_md(content):
    lines = content.splitlines()
    if not lines:
        return ""
    return "\n".join(f"{line}" for line in lines)


def md_to_txt(content):
    # Very basic markdown cleanup for starter usage
    text = re.sub(r"`([^`]+)`", r"\1", content)
    text = re.sub(r"#+\s*", "", text)
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"\*(.*?)\*", r"\1", text)
    text = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def txt_to_html(content):
    escaped = (
        content
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
    paragraphs = [f"<p>{p}</p>" for p in escaped.splitlines() if p.strip()]
    return "<html><body>\n" + "\n".join(paragraphs) + "\n</body></html>"


def html_to_txt(content):
    return re.sub(r"<[^>]+>", "", content).replace("&nbsp;", " ").replace("&amp;", "&")


def json_to_txt(content):
    data = json.loads(content)
    if isinstance(data, dict):
        lines = []
        for key, value in data.items():
            lines.append(f"{key}: {value}")
        return "\n".join(lines)
    if isinstance(data, list):
        return "\n".join(str(item) for item in data)
    return str(data)


def txt_to_json(content):
    return json.dumps({"content": content}, indent=2, ensure_ascii=False)


def md_to_html(content):
    if markdown is None:
        raise RuntimeError("Markdown package is required for MD -> HTML conversions. Install dependencies with: pip install -r requirements.txt")
    return markdown.markdown(content)


def convert_file(input_path, output_path):
    input_ext = Path(input_path).suffix.lower()
    output_ext = Path(output_path).suffix.lower()

    content = read_text(input_path)

    converters = {
        (".txt", ".md"): txt_to_md,
        (".md", ".txt"): md_to_txt,
        (".txt", ".html"): txt_to_html,
        (".html", ".txt"): html_to_txt,
        (".json", ".txt"): json_to_txt,
        (".txt", ".json"): txt_to_json,
        (".md", ".html"): md_to_html,
    }

    conversion = converters.get((input_ext, output_ext))
    if conversion is None:
        raise ValueError(
            f"Unsupported conversion: {input_ext} -> {output_ext}. "
            "Supported conversions include: .txt to .md, .md to .txt, .txt to .html, .html to .txt, .json to .txt, .txt to .json, .md to .html."
        )

    converted = conversion(content)
    write_text(output_path, converted)
    print(f"Converted {input_path} -> {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Simple document converter")
    parser.add_argument("input_file", help="Path to the source file")
    parser.add_argument("output_file", help="Path to the destination file")
    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        raise FileNotFoundError(f"Input file not found: {args.input_file}")

    output_dir = os.path.dirname(args.output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    convert_file(args.input_file, args.output_file)


if __name__ == "__main__":
    main()
