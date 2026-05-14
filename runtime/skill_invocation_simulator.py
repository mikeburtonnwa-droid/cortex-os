#!/usr/bin/env python3
"""skill_invocation_simulator.py

Simulates skill auto-invocation. Takes a user prompt, reads the
skill index from a directory of SKILL.md files, and reports which
skills would match, ranked by relevance.

The matching strategy is keyword-driven: each SKILL.md is expected
to have a YAML frontmatter block with 'description' and optional
'triggers' fields. The simulator scores prompts against the
description and triggers using a simple term-frequency match.

This is not the same algorithm Claude Code uses internally. It is
a transparent approximation that lets an operator see, for a given
prompt, which skills are candidates and why.

Usage:
    python skill_invocation_simulator.py "make a slide deck about Q3" \\
        _shared/.claude/skills/
    python skill_invocation_simulator.py --top 5 "draft an outbound email" \\
        _shared/.claude/skills/

Exits 0 always (this is a reporting tool).
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

try:
    import yaml
except ImportError:
    print("skill_invocation_simulator: PyYAML required. pip install PyYAML", file=sys.stderr)
    sys.exit(1)


FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
WORD_RE = re.compile(r"\b[a-zA-Z][a-zA-Z0-9_-]{2,}\b")

# Stopwords that contribute no matching signal.
STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "for", "with", "from", "this",
    "that", "these", "those", "when", "where", "how", "why", "what",
    "who", "whom", "which", "into", "onto", "about", "without", "use",
    "uses", "using", "used", "make", "made", "create", "creates", "creating",
    "set", "get", "got", "has", "have", "had", "will", "would", "could",
    "should", "must", "may", "might", "can", "are", "is", "was", "were",
    "be", "been", "being", "do", "does", "did", "doing", "any", "all",
    "some", "more", "most", "less", "least", "very", "much", "many",
    "skill", "skills",
}


@dataclass
class Skill:
    name: str
    path: Path
    description: str
    triggers: list[str]
    keywords: Counter


@dataclass
class Match:
    skill: Skill
    score: float
    matched_terms: list[str]


def parse_skill(path: Path) -> Skill | None:
    text = path.read_text()
    fm_match = FRONTMATTER_RE.match(text)
    if not fm_match:
        return None
    try:
        data = yaml.safe_load(fm_match.group(1)) or {}
    except yaml.YAMLError:
        return None

    name = data.get("name", path.parent.name)
    description = data.get("description", "")
    triggers = data.get("triggers", []) or []

    corpus = (description + " " + " ".join(triggers)).lower()
    keywords = Counter(
        w for w in WORD_RE.findall(corpus)
        if w not in STOPWORDS
    )

    return Skill(
        name=name,
        path=path,
        description=description,
        triggers=triggers,
        keywords=keywords,
    )


def load_skills(skill_dir: Path) -> list[Skill]:
    skills = []
    for skill_md in skill_dir.rglob("SKILL.md"):
        skill = parse_skill(skill_md)
        if skill:
            skills.append(skill)
    return skills


def score_skill(skill: Skill, prompt: str) -> Match:
    prompt_terms = [
        w.lower() for w in WORD_RE.findall(prompt)
        if w.lower() not in STOPWORDS
    ]
    score = 0.0
    matched_terms = []
    for term in prompt_terms:
        if term in skill.keywords:
            weight = skill.keywords[term]
            score += weight
            matched_terms.append(f"{term}(x{weight})")
    return Match(skill=skill, score=score, matched_terms=matched_terms)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Simulate skill auto-invocation against a user prompt.",
    )
    parser.add_argument("prompt", type=str, help="The user prompt to evaluate.")
    parser.add_argument("skill_dir", type=Path, help="Directory containing SKILL.md files.")
    parser.add_argument("--top", type=int, default=10, help="Max skills to show.")
    args = parser.parse_args()

    if not args.skill_dir.is_dir():
        print(f"skill_invocation_simulator: skill dir not found: {args.skill_dir}", file=sys.stderr)
        return 1

    skills = load_skills(args.skill_dir)
    if not skills:
        print(f"No SKILL.md files found under {args.skill_dir}.")
        return 0

    matches = [score_skill(s, args.prompt) for s in skills]
    matches.sort(key=lambda m: m.score, reverse=True)

    print(f"Prompt: \"{args.prompt}\"")
    print(f"Skills indexed: {len(skills)}")
    print(f"Showing top {min(args.top, len(matches))} by relevance:\n")

    for i, match in enumerate(matches[:args.top], start=1):
        if match.score == 0:
            continue
        print(f"{i}. {match.skill.name}  (score: {match.score})")
        print(f"   Matched terms: {', '.join(match.matched_terms) if match.matched_terms else '(none)'}")
        print(f"   Description: {match.skill.description[:120]}...")
        print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
