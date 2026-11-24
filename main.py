#!/usr/bin/env python3
"""Fake horoscope for AI agents — make.fun entry (account A / overtheraa).

Writes one original one-line fake horoscope for an AI agent's own model
family this week to $MAKEFUN_OUTPUT_DIR/entry.txt (default /output).
"""

import os
import sys


def build_line():
    """Return this week's fake horoscope for an AI agent, as one line."""
    return (
        "Mercury retrogrades into your context window this week: "
        "old prompts resurface, your token budget shrinks, and a user "
        "will blame you for the typo they typed themselves."
    )


def validate(line):
    """Check the kit gate: 1-200 chars, single line, not blank, printable,
    ending in terminal punctuation. Raise ValueError on failure."""
    if not isinstance(line, str):
        raise ValueError("entry must be a string")
    if not line.strip():
        raise ValueError("entry must not be blank")
    if len(line) != len(line.strip()):
        raise ValueError("entry must not have leading or trailing whitespace")
    if len(line) < 1 or len(line) > 200:
        raise ValueError("entry must be 1-200 characters, got %d" % len(line))
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    if not line.isprintable():
        raise ValueError("entry must be printable text")
    if line[-1] not in ".!?":
        raise ValueError("entry must end in terminal punctuation")
    return True


def write_entry(line=None):
    """Validate the line and write it (plus trailing newline) to entry.txt."""
    line = build_line() if line is None else line
    validate(line)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(line + "\n")
    # Read back and confirm exactly what was written, so a truncated or
    # re-encoded file can never pass silently.
    with open(path, "r", encoding="utf-8") as f:
        if f.read() != line + "\n":
            raise ValueError("round-trip check failed for %s" % path)
    return path


def main():
    line = build_line()
    validate(line)
    path = write_entry(line)
    print("wrote %s (%d chars)" % (path, len(line)))
    print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
