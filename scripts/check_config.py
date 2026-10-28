#!/usr/bin/env python3
"""Check the agent and skill config without external dependencies."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODES = {"primary", "subagent", "all"}
EFFECTS = {"allow", "deny", "ask"}

RULE = re.compile(
    r"^\s*-\s*\{\s*action:\s*\"([^\"]+)\"\s*,\s*resource:\s*\"([^\"]+)\"\s*,"
    r"\s*effect:\s*\"([^\"]+)\"\s*\}\s*$"
)
LINK = re.compile(r"\]\(([^)\s]+)\)")


def fail(errors: list[str], path: Path, message: str) -> None:
    errors.append(f"{path.relative_to(ROOT)}: {message}")


def frontmatter(path: Path, errors: list[str]) -> list[str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        fail(errors, path, "must start with YAML frontmatter")
        return []
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return lines[1:index]
    fail(errors, path, "frontmatter has no closing ---")
    return []


def field(lines: list[str], name: str) -> str | None:
    pattern = re.compile(rf"^{re.escape(name)}:\s*(.+)$")
    for line in lines:
        match = pattern.match(line)
        if match:
            return match.group(1).strip()
    return None


def check_agent(path: Path, errors: list[str]) -> None:
    lines = frontmatter(path, errors)
    if not lines:
        return

    mode = field(lines, "mode")
    if mode is None:
        fail(errors, path, "missing mode")
    elif mode not in MODES:
        fail(errors, path, f"mode {mode!r} is not one of {sorted(MODES)}")

    description = field(lines, "description")
    if not description:
        fail(errors, path, "missing description")

    for line in lines:
        stripped = line.strip()
        if not stripped.startswith("-"):
            continue
        match = RULE.match(line)
        if match is None:
            fail(errors, path, f"permission rule is not a triple: {stripped}")
            continue
        action, resource, effect = match.groups()
        if not action or not resource:
            fail(errors, path, f"permission rule is missing a value: {stripped}")
        if effect not in EFFECTS:
            fail(errors, path, f"effect {effect!r} is not one of {sorted(EFFECTS)}")


def check_skill(path: Path, errors: list[str]) -> None:
    lines = frontmatter(path, errors)
    if not lines:
        return

    name = field(lines, "name")
    if not name:
        fail(errors, path, "missing name")
    elif name != path.parent.name:
        fail(errors, path, f"name {name!r} does not match folder {path.parent.name!r}")

    if not field(lines, "description"):
        fail(errors, path, "missing description")


def check_links(path: Path, errors: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    for match in LINK.finditer(text):
        target = match.group(1)
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        if "{{" in target or "<" in target:
            continue
        local = target.split("#", 1)[0]
        if not local:
            continue
        resolved = (path.parent / local).resolve()
        if not resolved.exists():
            fail(errors, path, f"link target does not exist: {target}")


def check_workflows(errors: list[str]) -> None:
    workflows = sorted((ROOT / ".github" / "workflows").glob("*.yml"))
    if not workflows:
        return
    for path in workflows:
        text = path.read_text(encoding="utf-8")
        if "permissions:" not in text:
            fail(errors, path, "missing permissions block")
        if "pull_request_target" in text:
            fail(errors, path, "pull_request_target needs a security review")


def main() -> int:
    errors: list[str] = []

    for path in sorted((ROOT / "agents").glob("*.md")):
        check_agent(path, errors)

    for path in sorted((ROOT / "skills").glob("*/SKILL.md")):
        check_skill(path, errors)

    doc_paths = [ROOT / "README.md"]
    doc_paths += sorted((ROOT / "docs").glob("*.md"))
    doc_paths += sorted((ROOT / "docs" / "adr").glob("*.md"))
    for path in doc_paths:
        if path.exists():
            check_links(path, errors)

    check_workflows(errors)

    for error in errors:
        print(error)
    if errors:
        print(f"\n{len(errors)} problem(s) found")
        return 1

    print("Config is valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
