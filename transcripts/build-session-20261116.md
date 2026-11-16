# Build Transcript — sunfish-compact v2 (python-valid self-extractor)
Date: 2026-11-16 (continued)
Repo: https://github.com/Jenal33/sunfish-compact @ 33ad918809ba3d765f65c55e2efbca26d4cb0aea

## What changed from v1 (42a238a, bash extractor — FAILED intake)
main.py was a bash self-extractor; the competition executes main.py with
`python3.13 -P -s`, so a bash file cannot parse. Rebuilt as a **valid Python
self-extracting file of 4074 bytes**:

- lzma payload (3815 bytes, preset 9e pb=0) after stripping three search
  features for size (null-move pruning, RFP, LMR — MTD-bi + TT + killer +
  quiescence retained),
- payload encoded with a yEnc-style scheme (offset 42, escapes for NUL/LF/CR/
  quote/backslash) so every byte is latin-1 printable and the file parses,
- 95-byte Python decoder head/tail reconstructs the bytes and exec()s the
  decompressed engine.

## Evidence
- `python3 -W ignore -m py_compile main_py_self.py` → COMPILE_OK
- live practice trial vs local env (depth-2/3/4 gauntlet): **4 wins, 2 losses,
  0 draws** — same scoreline as the pre-strip build.

## License
GPL-3.0-only (Sunfish derivative, © Thomas Dybdahl Ahle) — see LICENSE.
