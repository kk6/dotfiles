#!/usr/bin/env python3
"""Claude Code statusline script.

Outputs a single-line status string for Claude Code's statusLine feature.
Reads JSON from stdin (provided by Claude Code) and renders:
  model | directory | git branch | usage metrics (ctx, 5h, 7d)

Usage:
    Configure in ~/.claude/settings.json:
    { "statusLine": { "type": "command", "command": "~/.claude/statusline.py" } }
"""

import json
import subprocess
import sys
from pathlib import Path

RESET = "\033[0m"
DIM = "\033[2m"
BOLD = "\033[1m"

# Ring meter characters mapped to 0-100% in 25% steps
RINGS = "○◔◑◕●"

# (label, key-path) pairs for usage metrics to display
METRICS = [
    ("ctx", ("context_window", "used_percentage")),
    ("5h", ("rate_limits", "five_hour", "used_percentage")),
    ("7d", ("rate_limits", "seven_day", "used_percentage")),
]


def gradient(pct: float) -> str:
    """Return a Truecolor ANSI escape that shifts green -> yellow -> red."""
    r = min(int(pct * 5.1), 255) if pct < 50 else 255
    g = max(200 - int((pct - 50) * 4), 0) if pct >= 50 else 200
    b = 60 if pct >= 50 else 80
    return f"\033[38;2;{r};{g};{b}m"


def resolve(data: dict, keys: tuple[str, ...]) -> float | None:
    """Safely traverse nested dicts by a sequence of keys.

    Returns the leaf value if all keys exist, otherwise None.
    """
    current = data
    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def fmt(label: str, pct: float) -> str:
    """Format a single metric as 'label ring pct%' with gradient color."""
    ring = RINGS[min(int(pct / 25), 4)]
    return f"{DIM}{label}{RESET} {gradient(pct)}{ring} {round(pct)}%{RESET}"


def get_git_branch() -> str:
    """Return the current git branch name, or empty string if not in a repo."""
    try:
        return subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            timeout=2,
        ).stdout.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return ""


def main() -> None:
    """Build and print the statusline from Claude Code's JSON input."""
    data = json.load(sys.stdin)

    model = resolve(data, ("model", "display_name")) or "Claude"
    parts = [f"󰚩  {BOLD}{model}{RESET}"]

    parts.append(f"\uf07c  {Path.cwd().name}")

    branch = get_git_branch()
    if branch:
        parts.append(f"\U000F062C {branch}")

    metrics = []
    for label, keys in METRICS:
        pct = resolve(data, keys)
        if pct is not None:
            metrics.append(fmt(label, pct))

    if metrics:
        parts.append(f"\U000F04C5 {' '.join(metrics)}")

    print(" | ".join(parts), end="")


if __name__ == "__main__":
    main()
