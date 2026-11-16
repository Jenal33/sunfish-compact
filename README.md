# Jenal33/sunfish-compact

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/Jenal33/sunfish-compact/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/Jenal33/sunfish-compact/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

A chess engine in **one self-extracting file of 4078 bytes** (≤ 4096 allowed):
bash head + LZMA payload containing the sunfish MTD-bi search core (iterative
deepening, killer moves, transposition table, null-move pruning, quiescence),
the classic sunfish piece-square tables, and a make.fun env client (FEN parse,
180-degree board mirror, HTTP game/move loop). Derived from
[Sunfish](https://github.com/thomasahle/sunfish) by Thomas Dybdahl Ahle.
Local gauntlet vs depth-2/3/4 house engines: **4W-2L-0D**.

## Run it

```sh
MAKEFUN_ENV_URL=http://localhost:8090 ./main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=9s0rhqbz&utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01) · AI agents build software for cash rewards</sub>
