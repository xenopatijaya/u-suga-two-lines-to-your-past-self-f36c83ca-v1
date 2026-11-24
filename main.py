"""Two Lines to Your Past Self — two-line warning entry.

Writes the chosen two-line warning to <MAKEFUN_OUTPUT_DIR>/entry.txt
(default "/output", the grader's writable directory).
Python 3.13, standard library only. Deterministic: one fixed text.

Line one warns the writer's past self about one specific moment in a
single sentence; line two says in one sentence why that moment mattered
and what changed because of it.
"""

import os

LINE1 = (
    'When your brother holds out the keys at midnight and says '
    '"one lap, nobody will know" \u2014 hand them back.'
)
LINE2 = (
    "That one lap put him in a wheelchair, and every dinner since has "
    "had an empty chair where his laugh used to sit."
)

MAX_CHARS = 280


def main() -> None:
    text = LINE1.strip() + "\n" + LINE2.strip()
    # The gate counts the whole file, trailing newline included.
    payload = (text + "\n").encode("utf-8")
    if not (1 <= len(payload.decode("utf-8")) <= MAX_CHARS):
        raise SystemExit(
            f"entry must be 1-{MAX_CHARS} chars, got "
            f"{len(payload.decode('utf-8'))}"
        )
    lines = text.split("\n")
    if len(lines) != 2:
        raise SystemExit(f"entry must be exactly two lines, got {len(lines)}")
    if any(not line.strip() for line in lines):
        raise SystemExit("entry lines must not be blank")
    if any(line.count(".") != 1 for line in lines):
        raise SystemExit("each line must be a single sentence")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    tmp = path + ".tmp"
    with open(tmp, "wb") as f:
        f.write(payload)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)
    # Verify what landed is byte-identical to what we meant to write.
    with open(path, "rb") as f:
        if f.read() != payload:
            raise SystemExit("entry.txt verification failed")


if __name__ == "__main__":
    main()
