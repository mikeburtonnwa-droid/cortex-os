#!/usr/bin/env python3
"""cascade_walker.py

Prints the cascade of CLAUDE.md files that would load when Claude Code
opens a given directory. Walks up the filesystem tree from the target
path to the repository root, collecting CLAUDE.md files at each level.

Usage:
    python cascade_walker.py <path>
    python cascade_walker.py reference/business-example/functions/research/
    python cascade_walker.py --verbose .

The cascade order is shallowest first. The deepest CLAUDE.md is the
last to load and conceptually overrides shallower files on points
of contradiction.

Exits 0 on success, 1 if the target path does not exist, 2 if no
CLAUDE.md is found anywhere in the chain.
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class CascadeEntry:
    path: Path
    depth: int
    word_count: int


def find_repo_root(start: Path) -> Path:
    """Walk up until a .git directory is found, or fall back to filesystem root."""
    current = start.resolve()
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    return start.resolve()


def walk_cascade(target: Path, repo_root: Path) -> list[CascadeEntry]:
    """Collect CLAUDE.md files from repo_root down to target."""
    target = target.resolve()
    repo_root = repo_root.resolve()

    # Validate target is at or under repo_root.
    try:
        target.relative_to(repo_root)
    except ValueError:
        # Target is outside the repo; walk from target's filesystem
        # ancestors instead.
        repo_root = Path(target.anchor)

    entries: list[CascadeEntry] = []
    chain: list[Path] = []

    # Build the chain from target up to repo_root.
    current = target if target.is_dir() else target.parent
    while True:
        chain.append(current)
        if current == repo_root or current == current.parent:
            break
        current = current.parent

    # Reverse so we go shallowest-first.
    chain.reverse()

    for depth, directory in enumerate(chain):
        candidate = directory / "CLAUDE.md"
        if candidate.is_file():
            word_count = len(candidate.read_text().split())
            entries.append(CascadeEntry(
                path=candidate,
                depth=depth,
                word_count=word_count,
            ))

    return entries


def format_entries(entries: list[CascadeEntry], repo_root: Path, verbose: bool) -> str:
    if not entries:
        return "No CLAUDE.md files found in the cascade."

    lines = []
    lines.append(f"Cascade for working directory: {entries[-1].path.parent}")
    lines.append(f"Repo root: {repo_root}")
    lines.append("")
    lines.append("Load order (shallowest first, deepest wins):")
    lines.append("")

    for i, entry in enumerate(entries):
        relative = entry.path.relative_to(repo_root)
        indent = "  " * i
        marker = "↳" if i > 0 else " "
        lines.append(f"{indent}{marker} {relative}  ({entry.word_count} words)")

    if verbose:
        lines.append("")
        lines.append("Total files in cascade: {}".format(len(entries)))
        lines.append("Total words loaded: {}".format(sum(e.word_count for e in entries)))

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print the CLAUDE.md cascade for a target directory.",
    )
    parser.add_argument(
        "path",
        type=Path,
        help="Target directory (or file) whose cascade should be resolved.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print word totals and cascade statistics.",
    )
    args = parser.parse_args()

    if not args.path.exists():
        print(f"cascade_walker: path does not exist: {args.path}", file=sys.stderr)
        return 1

    repo_root = find_repo_root(args.path)
    entries = walk_cascade(args.path, repo_root)

    print(format_entries(entries, repo_root, args.verbose))

    if not entries:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
