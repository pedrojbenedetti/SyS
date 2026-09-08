from pathlib import Path
import re

README = Path("README.md")
START = "<!-- TOC START -->"
END = "<!-- TOC END -->"


def github_slug(text: str, seen: dict[str, int]) -> str:
    """Approximate GitHub's heading anchors for README headings."""
    text = re.sub(r"<[^>]+>", "", text).strip().lower()
    text = re.sub(r"[^\w\- ]", "", text, flags=re.UNICODE)
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")

    count = seen.get(text, 0)
    seen[text] = count + 1
    return text if count == 0 else f"{text}-{count}"


def build_toc(markdown: str) -> str:
    seen: dict[str, int] = {}
    lines: list[str] = []
    in_code_block = False

    for line in markdown.splitlines():
        if line.lstrip().startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        match = re.match(r"^(#{2,3})\s+(.+?)\s*$", line)
        if not match:
            continue

        level = len(match.group(1))
        title = match.group(2).strip()

        if title == "Índice":
            continue

        slug = github_slug(title, seen)
        indent = "  " * (level - 2)
        lines.append(f"{indent}- [{title}](#{slug})")

    return "\n".join(lines)


def main() -> None:
    markdown = README.read_text(encoding="utf-8")

    if START not in markdown or END not in markdown:
        raise SystemExit(
            f"README.md must contain both {START!r} and {END!r} markers."
        )

    toc = build_toc(markdown)
    replacement = f"{START}\n{toc}\n{END}"
    updated = re.sub(
        re.escape(START) + r".*?" + re.escape(END),
        replacement,
        markdown,
        flags=re.DOTALL,
    )

    README.write_text(updated, encoding="utf-8")


if __name__ == "__main__":
    main()
