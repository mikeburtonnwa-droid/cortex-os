#!/usr/bin/env python3
"""hook_simulator.py

Runs a hook script against a JSON payload and reports the result.
Used to verify that a hook fires correctly without a full Claude
Code session.

Usage:
    python hook_simulator.py <hook_script> <fixture_json>
    python hook_simulator.py _shared/.claude/hooks/pre-tool-use.sh \\
        runtime/fixtures/pretooluse_bash_destructive.json

A fixture is a JSON file shaped like a Claude Code hook input. See
runtime/fixtures/ for sample fixtures.

Reports the hook's exit code, stdout, and stderr. Exit code 0 from
this script means the simulation ran; the hook's own exit code is
in the report. Exit code 1 from this script means the simulation
could not run (missing hook, malformed fixture).
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def simulate(hook_script: Path, fixture: Path) -> int:
    if not hook_script.is_file():
        print(f"hook_simulator: hook script not found: {hook_script}", file=sys.stderr)
        return 1
    if not fixture.is_file():
        print(f"hook_simulator: fixture not found: {fixture}", file=sys.stderr)
        return 1

    try:
        payload = json.loads(fixture.read_text())
    except json.JSONDecodeError as e:
        print(f"hook_simulator: fixture is not valid JSON: {e}", file=sys.stderr)
        return 1

    # Render the payload as a single JSON string on stdin.
    payload_json = json.dumps(payload)

    proc = subprocess.run(
        ["bash", str(hook_script)],
        input=payload_json,
        capture_output=True,
        text=True,
        timeout=30,
    )

    print(f"Hook: {hook_script}")
    print(f"Fixture: {fixture}")
    print(f"Exit code: {proc.returncode}")
    print(f"Verdict: {'ALLOW' if proc.returncode == 0 else 'BLOCK' if proc.returncode == 2 else 'ERROR'}")

    if proc.stdout:
        print("\n--- stdout ---")
        print(proc.stdout)
    if proc.stderr:
        print("\n--- stderr ---")
        print(proc.stderr)

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Simulate a Claude Code hook firing against a JSON fixture.",
    )
    parser.add_argument("hook_script", type=Path, help="Path to the hook bash script.")
    parser.add_argument("fixture", type=Path, help="Path to the JSON fixture for stdin.")
    args = parser.parse_args()

    return simulate(args.hook_script, args.fixture)


if __name__ == "__main__":
    sys.exit(main())
