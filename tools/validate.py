"""Repository checks for X-RAY. Standard library only.

Usage: python tools/validate.py [repo_root]

Checks:
  1. SKILL.md frontmatter follows the Agent Skills spec (rules mirror skills-ref).
  2. SKILL.md stays under the line limit set in AGENTS.md.
  3. Every relative Markdown link and #anchor resolves.
  4. Tier names and evidence states are spelled consistently.
Exits 1 if any check fails.
"""

import re
import sys
import unicodedata
from pathlib import Path

# From the Agent Skills spec and skills-ref's validator.
ALLOWED_FIELDS = {"name", "description", "license", "allowed-tools", "metadata", "compatibility"}
MAX_NAME = 64
MAX_DESCRIPTION = 1024
MAX_COMPATIBILITY = 500
# The spec allows 500 lines; AGENTS.md targets well under 200.
MAX_SKILL_LINES = 200

# Misspellings of the four evidence states and three tiers.
TERM_ERRORS = [
    r"\bCONFIRM\b", r"\bINFER\b", r"\bUNKOWN\b", r"\bCONTRADICT\b",
    r"\bLight-weight\b", r"\bIntergrated\b",
]

FENCE = re.compile(r"^(```|~~~).*?^\1", re.S | re.M)


def frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    fields, key = {}, None
    for line in m.group(1).splitlines():
        top = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if top:
            key = top.group(1)
            fields[key] = top.group(2).strip()
        elif key and line.startswith((" ", "\t")):
            fields[key] += "\n" + line.strip()
    return fields


def check_skill(root, errors):
    skill = root / "SKILL.md"
    if not skill.is_file():
        errors.append("Missing required file: SKILL.md")
        return
    text = skill.read_text(encoding="utf-8")
    fields = frontmatter(text)
    if fields is None:
        errors.append("SKILL.md: no YAML frontmatter")
        return
    for key in fields.keys() - ALLOWED_FIELDS:
        errors.append(f"SKILL.md: unexpected frontmatter field '{key}'")

    name = unicodedata.normalize("NFKC", fields.get("name", "").strip().strip("\"'"))
    if not name:
        errors.append("SKILL.md: 'name' is required")
    else:
        if len(name) > MAX_NAME:
            errors.append(f"SKILL.md: name longer than {MAX_NAME} characters")
        if name != name.lower() or not all(c.isalnum() or c == "-" for c in name):
            errors.append("SKILL.md: name must be lowercase letters, digits, and hyphens")
        if name.startswith("-") or name.endswith("-") or "--" in name:
            errors.append("SKILL.md: name has a leading, trailing, or doubled hyphen")
        if unicodedata.normalize("NFKC", root.resolve().name) != name:
            errors.append(f"Directory name '{root.resolve().name}' must match skill name '{name}'")

    desc = fields.get("description", "").strip()
    if not desc:
        errors.append("SKILL.md: 'description' is required")
    elif len(desc) > MAX_DESCRIPTION:
        errors.append(f"SKILL.md: description is {len(desc)} characters (max {MAX_DESCRIPTION})")
    if re.search(r"<[A-Za-z/][^>]*>", desc):
        errors.append("SKILL.md: description contains XML-like tags")

    if "compatibility" in fields and len(fields["compatibility"]) > MAX_COMPATIBILITY:
        errors.append(f"SKILL.md: compatibility longer than {MAX_COMPATIBILITY} characters")

    lines = len(text.splitlines())
    if lines > MAX_SKILL_LINES:
        errors.append(f"SKILL.md: {lines} lines (target under {MAX_SKILL_LINES})")
    print(f"SKILL.md: name={name!r}, description={len(desc)} chars, {lines} lines")


def slug(heading):
    heading = re.sub(r"[^\w\- ]", "", heading.strip().lower())
    return heading.replace(" ", "-")


def anchors(path, cache):
    if path not in cache:
        body = FENCE.sub("", path.read_text(encoding="utf-8"))
        cache[path] = {slug(h) for h in re.findall(r"^#{1,6} (.*)$", body, re.M)}
    return cache[path]


def check_links(root, errors):
    cache, count = {}, 0
    for md in sorted(root.rglob("*.md")):
        if any(part.startswith(".") and part != ".github" for part in md.relative_to(root).parts):
            continue
        body = FENCE.sub("", md.read_text(encoding="utf-8"))
        for target in re.findall(r"\]\(([^)\s]+)\)", body):
            if re.match(r"^[a-z]+:", target):
                continue
            count += 1
            path, _, anchor = target.partition("#")
            dest = (md.parent / path).resolve() if path else md
            rel = md.relative_to(root).as_posix()
            if not dest.exists():
                errors.append(f"{rel}: broken link '{target}'")
            elif anchor and dest.is_file() and anchor not in anchors(dest, cache):
                errors.append(f"{rel}: missing anchor '{target}'")
    print(f"Links: {count} relative links checked")


def check_terms(root, errors):
    for md in sorted(root.rglob("*.md")):
        text = md.read_text(encoding="utf-8")
        for pattern in TERM_ERRORS:
            for m in re.finditer(pattern, text):
                line = text.count("\n", 0, m.start()) + 1
                errors.append(f"{md.relative_to(root).as_posix()}:{line}: inconsistent term '{m.group(0)}'")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    errors = []
    check_skill(root, errors)
    check_links(root, errors)
    check_terms(root, errors)
    for e in errors:
        print(f"ERROR {e}")
    print("OK" if not errors else f"{len(errors)} error(s)")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
