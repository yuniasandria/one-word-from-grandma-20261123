"""One Word From Grandma entry.

Writes exactly one word -- the single word grandma would text about AI --
to /output/entry.txt. Runs in a sandbox with no network; stdlib only.
"""

import os
from pathlib import Path

WORD = "doohickey"


def main() -> None:
    text = WORD.strip()
    if not 1 <= len(text) <= 30:
        raise SystemExit(f"entry must be 1-30 characters, got {len(text)}")
    if any(ch.isspace() for ch in text):
        raise SystemExit("entry must be exactly one word")
    out = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out.mkdir(parents=True, exist_ok=True)
    target = out / "entry.txt"
    target.write_text(text, encoding="utf-8")
    # Read back and verify: the gate requires 1-30 UTF-8 characters, not
    # whitespace-only, so refuse to pass silently if the file ever differs.
    # The post-write self-check also enforces the single-word shape on the
    # bytes actually on disk (all-lowercase letters, exact byte length, no
    # trailing newline or stray whitespace) so a truncated or padded write
    # fails loudly instead of shipping a malformed entry.
    written = target.read_text(encoding="utf-8")
    if written != text:
        raise SystemExit("entry.txt did not round-trip as a single word")
    if not written.isalpha() or not written.islower():
        raise SystemExit("entry.txt must contain only lowercase letters")
    if target.stat().st_size != len(text.encode("utf-8")):
        raise SystemExit("entry.txt byte length does not match the entry")


if __name__ == "__main__":
    main()
