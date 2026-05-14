#!/usr/bin/env python3
"""current_reality_updater.py

Rewrites the Current Reality block in a CLAUDE.md file. Demonstrates
the state-persistence pattern: durable session state lives in
human-readable markdown, not in a vector store or database.

The Current Reality block is delimited by a heading match. The
script finds the heading, replaces the block content until the
next heading at the same or higher level, and updates the
"Updated: <date>" line at the top of the block.

Usage:
    python current_reality_updater.py <claude_md_path> <input_file>
    python current_reality_updater.py CLAUDE.md /tmp/session-end.md
    python current_reality_updater.py CLAUDE.md - <<EOF
    Phase 5 complete. Reference business shipped. Phase 6 next.
    EOF

The input file (or stdin if '-') contains the new Current Reality
content as freeform markdown. The script wraps it with the
"Updated: <today>" header and inserts it in place of the existing
block.

Exits 0 on success, 1 if the target file is malformed or the
heading cannot be found.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path


HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
UPDATED_RE = re.compile(r"^\*\*Updated:\s*\d{4}-\d{2}-\d{2}\*\*\s*$", re.MULTILINE)


def find_current_reality_block(text: str) -> tuple[int, int] | None:
    """Return (start_offset, end_offset) for the body of the Current Reality block."""
    headings = list(HEADING_RE.finditer(text))
    for i, match in enumerate(headings):
        title = match.group(2).strip().lower()
        if title.startswith("current reality") or title.startswith("current state"):
            block_start = match.end()
            heading_level = len(match.group(1))
            # Find the next heading at same or higher level.
            for next_match in headings[i + 1:]:
                next_level = len(next_match.group(1))
                if next_level <= heading_level:
                    return (block_start, next_match.start())
            return (block_start, len(text))
    return None


def render_block(content: str) -> str:
    today = date.today().isoformat()
    body = content.strip()
    return f"\n\n**Updated: {today}**\n\n{body}\n\n"


def update_file(target: Path, new_content: str) -> int:
    if not target.is_file():
        print(f"current_reality_updater: target not found: {target}", file=sys.stderr)
        return 1

    text = target.read_text()
    block = find_current_reality_block(text)

    if block is None:
        print(
            f"current_reality_updater: no '## Current Reality' or '## Current State' "
            f"heading found in {target}.",
            file=sys.stderr,
        )
        return 1

    start, end = block
    rendered = render_block(new_content)
    new_text = text[:start] + rendered + text[end:]
    target.write_text(new_text)

    print(f"current_reality_updater: updated {target}")
    print(f"  Block replaced from offset {start} to {end}.")
    print(f"  New block length: {len(rendered)} chars.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Replace the Current Reality block in a CLAUDE.md file.",
    )
    parser.add_argument("claude_md", type=Path, help="Path to the CLAUDE.md to update.")
    parser.add_argument("input", type=str, help="Path to file with new content, or '-' for stdin.")
    args = parser.parse_args()

    if args.input == "-":
        new_content = sys.stdin.read()
    else:
        input_path = Path(args.input)
        if not input_path.is_file():
            print(f"current_reality_updater: input file not found: {args.input}", file=sys.stderr)
            return 1
        new_content = input_path.read_text()

    return update_file(args.claude_md, new_content)


if __name__ == "__main__":
    sys.exit(main())
