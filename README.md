# sunfish-compact

Entry for the make.fun **tiny-chess-01** bounty: a chess engine in **one file ≤ 4096 bytes**.

`main.py` is a self-extracting artifact: a small bash head + an LZMA-compressed
Python payload. The payload contains:

- the **sunfish** MTD-bi search core (iterative deepening, killer moves,
  transposition table, null-move pruning, quiescence) — derived from
  [Sunfish](https://github.com/thomasahle/sunfish) by Thomas Dybdahl Ahle,
- the classic sunfish piece-square tables,
- a compact make.fun env client (BD/FEN parse, 180° board mirror, HTTP game/move loop).

## Run

```bash
MAKEFUN_ENV_URL=http://localhost:8090 ./main.py
```

The engine connects to the env server, plays each game in the gauntlet, and
respects a 4.5s move deadline (2.5s soft cutoff once a move is found).

## License

GPL-3.0 — see LICENSE. Derived from Sunfish (GPL-3.0) © Thomas Dybdahl Ahle.
