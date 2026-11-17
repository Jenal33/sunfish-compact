#!/usr/bin/env python3
# sunfish-compact minified core — Jenal33, GPL-3.0-only
import time
from itertools import count
from collections import namedtuple
piece = {"P": 100, "N": 280, "B": 320, "R": 479, "Q": 929, "K": 60000}
pst = {
    'P': (   0,   0,   0,   0,   0,   0,   0,   0,
            78,  83,  86,  73, 102,  82,  85,  90,
             7,  29,  21,  44,  40,  31,  44,   7,
           -17,  16,  -2,  15,  14,   0,  15, -13,
           -26,   3,  10,   9,   6,   1,   0, -23,
           -22,   9,   5, -11, -10,  -2,   3, -19,
           -31,   8,  -7, -37, -36, -14,   3, -31,
             0,   0,   0,   0,   0,   0,   0,   0),
    'N': ( -66, -53, -75, -75, -10, -55, -58, -70,
            -3,  -6, 100, -36,   4,  62,  -4, -14,
            10,  67,   1,  74,  73,  27,  62,  -2,
            24,  24,  45,  37,  33,  41,  25,  17,
            -1,   5,  31,  21,  22,  35,   2,   0,
           -18,  10,  13,  22,  18,  15,  11, -14,
           -23, -15,   2,   0,   2,   0, -23, -20,
           -74, -23, -26, -24, -19, -35, -22, -69),
    'B': ( -59, -78, -82, -76, -23,-107, -37, -50,
           -11,  20,  35, -42, -39,  31,   2, -22,
            -9,  39, -32,  41,  52, -10,  28, -14,
            25,  17,  20,  34,  26,  25,  15,  10,
            13,  10,  17,  23,  17,  16,   0,   7,
            14,  25,  24,  15,   8,  25,  20,  15,
            19,  20,  11,   6,   7,   6,  20,  16,
            -7,   2, -15, -12, -14, -15, -10, -10),
    'R': (  35,  29,  33,   4,  37,  33,  56,  50,
            55,  29,  56,  67,  55,  62,  34,  60,
            19,  35,  28,  33,  45,  27,  25,  15,
             0,   5,  16,  13,  18,  -4,  -9,  -6,
           -28, -35, -16, -21, -13, -29, -46, -30,
           -42, -28, -42, -25, -25, -35, -26, -46,
           -53, -38, -31, -26, -29, -43, -44, -53,
           -30, -24, -18,   5,  -2, -18, -31, -32),
    'Q': (   6,   1,  -8,-104,  69,  24,  88,  26,
            14,  32,  60, -10,  20,  76,  57,  24,
            -2,  43,  32,  60,  72,  63,  43,   2,
             1, -16,  22,  17,  25,  20, -13,  -6,
           -14, -15,  -2,  -5,  -1, -10, -20, -22,
           -30,  -6, -13, -11, -16, -11, -16, -27,
           -36, -18,   0, -19, -15, -15, -21, -38,
           -39, -30, -31, -13, -31, -36, -34, -42),
    'K': (   4,  54,  47, -99, -99,  60,  83, -62,
           -32,  10,  55,  56,  56,  55,  10,   3,
           -62,  12, -57,  44, -67,  28,  37, -31,
           -55,  50,  11,  -4, -19,  13,   0, -49,
           -55, -43, -52, -28, -51, -47,  -8, -50,
           -47, -42, -43, -79, -64, -32, -29, -32,
            -4,   3, -14, -50, -57, -18,  13,   4,
            17,  30,  -3, -14,   6,  -1,  40,  18),
}
for k, table in pst.items():
    padrow = lambda row: (0,) + tuple(x + piece[k] for x in row) + (0,)
    pst[k] = sum((padrow(table[i * 8 : i * 8 + 8]) for i in range(8)), ())
    pst[k] = (0,) * 20 + pst[k] + (0,) * 20
K_MID, K_END = pst["K"], tuple(piece["K"] + 70
   - 10 * (abs(2 * (i // 10) - 11) + abs(2 * (i % 10) - 9)) for i in range(120))
ML = 60000 - 13 * 929
MU = 60000 + 10 * 929
A1, H1, A8, H8 = 91, 98, 21, 28
initial = (
    "         \n"
    "         \n"
    " rnbqkbnr\n"
    " pppppppp\n"
    " ........\n"
    " ........\n"
    " ........\n"
    " ........\n"
    " PPPPPPPP\n"
    " RNBQKBNR\n"
    "         \n"
    "         \n"
)
N, E, S, W = -10, 1, 10, -1
directions = {
    "P": (N, N+N, N+W, N+E),
    "N": (N+N+E, E+N+E, E+S+E, S+S+E, S+S+W, W+S+W, W+N+W, N+N+W),
    "B": (N+E, S+E, S+W, N+W),
    "R": (N, E, S, W),
    "Q": (N, E, S, W, N+E, S+E, S+W, N+W),
    "K": (N, E, S, W, N+E, S+E, S+W, N+W)
}
QS = 40
QS_A = 140
ER = 15
PC = 40
LMR = 60
RFP = 0
TABLE_SIZE = 10**6
Move = namedtuple("Move", "i j prom")
class Position(namedtuple("Position", "board score wc bc ep kp")):
    def __hash__(self):
        return hash((self.board, self.wc, self.bc, self.ep, self.kp))
    def __eq__(self, o):
        return (self.board == o.board and self.ep == o.ep and self.kp == o.kp
                and self.wc == o.wc and self.bc == o.bc)
    def __ne__(self, o):
        return not self.__eq__(o)
    def gen_moves(self):
        for i, p in enumerate(self.board):
            if p not in "PNBRQK":
                continue
            for d in directions[p]:
                for j in count(i + d, d):
                    q = self.board[j]
                    if q in " \nPNBRQK":
                        break
                    if p == "P":
                        if d in (N, N + N) and q != ".": break
                        if d == N + N and (i < A1 + N or self.board[i + N] != "."): break
                        if (
                            d in (N + W, N + E)
                            and q == "."
                            and j not in (self.ep, self.kp, self.kp - 1, self.kp + 1)
                        ):
                            break
                        if A8 <= j <= H8:
                            for prom in "NBRQ":
                                yield Move(i, j, prom)
                            break
                    yield Move(i, j, "")
                    if p in "PNK" or q in "pnbrqk":
                        break
                    if i == A1 and self.board[j + E] == "K" and self.wc[0]:
                        yield Move(j + E, j + W, "")
                    if i == H1 and self.board[j + W] == "K" and self.wc[1]:
                        yield Move(j + W, j + E, "")
    def rotate(self, nullmove=False):
        return Position(
            self.board[::-1].swapcase(), -self.score, self.bc, self.wc,
            119 - self.ep if self.ep and not nullmove else 0,
            119 - self.kp if self.kp and not nullmove else 0,
        )
    def move(self, move):
        i, j, prom = move
        p, q = self.board[i], self.board[j]
        put = lambda board, i, p: board[:i] + p + board[i + 1 :]
        board = self.board
        wc, bc, ep, kp = self.wc, self.bc, 0, 0
        score = self.score + self.value(move)
        board = put(board, j, board[i])
        board = put(board, i, ".")
        wc = (wc[0] and i != A1, wc[1] and i != H1)
        bc = (bc[0] and j != H8, bc[1] and j != A8)
        if p == "K":
            wc = (False, False)
            if abs(j - i) == 2:
                kp = (i + j) // 2
                r = A1 if j < i else H1
                board = put(board, r, ".")
                board = put(board, kp, "R")
        if p == "P":
            if A8 <= j <= H8:
                board = put(board, j, prom)
            if j - i == 2 * N:
                ep = i + N
            if j == self.ep:
                board = put(board, j + S, ".")
        return Position(board[::-1].swapcase(), -score, bc, wc,
                        119 - ep if ep else 0, 119 - kp if kp else 0)
    def value(self, move):
        i, j, prom = move
        p, q = self.board[i], self.board[j]
        score = pst[p][j] - pst[p][i]
        if q in "pnbrqk":
            score += pst[q.upper()][119 - j]
        if abs(j - self.kp) < 2:
            score += pst["K"][119 - j]
        if p == "K" and abs(i - j) == 2:
            score += pst["R"][(i + j) // 2]
            score -= pst["R"][A1 if j < i else H1]
        if p == "P":
            if A8 <= j <= H8:
                score += pst[prom][j] - pst["P"][j]
            if j == self.ep:
                score += pst["P"][119 - (j + S)]
        return score
    def king_capture(self):
        return next((m for m in self.gen_moves()
                     if self.board[m.j] == "k" or abs(m.j - self.kp) < 2), None)
class Stop(Exception): pass
Entry = namedtuple("Entry", "lower upper")
class SE:
    def __init__(self):
        self.tp_score, self.tp_move, self.history = {}, {}, set()
        self.nodes, self.deadline = 0, 1 << 63
    def bound(self, pos, gamma, depth, root=False):
        self.nodes += 1
        if self.nodes % 2048 == 0 and time.time() > self.deadline: raise Stop
        depth = max(depth, 0)
        if pos.score <= -ML:
            return -MU
        if not root:
            entry = self.tp_score.get((pos, depth), Entry(-MU, MU))
            if entry.lower >= gamma: return entry.lower
            if entry.upper < gamma: return entry.upper
            if depth > 0 and pos in self.history: return 0
        def moves():
            killer = self.tp_move.get(pos)
            if depth == 0:
                yield None, pos.score
            if not killer and depth > 2:
                self.bound(pos, gamma, depth - 3, root=True)
                killer = self.tp_move.get(pos)
            val_lower = QS - depth * QS_A
            if killer and pos.value(killer) >= val_lower:
                yield killer, -self.bound(pos.move(killer), 1 - gamma, depth - 1)
            for cnt, (val, move) in enumerate(sorted(((v, m) for m in pos.gen_moves()
                                     if (v:=pos.value(m)) >= val_lower), reverse=True)):
                if depth <= 1 and pos.score + val < gamma:
                    yield (move, MU) if val >= ML else (None, pos.score + val)
                    break
                score = -self.bound(pos.move(move), 1 - gamma, depth - 1)
                yield move, score
        best, live = -MU, False
        for move, score in moves():
            best = max(best, score)
            live |= move is not None and score > -MU
            if best >= gamma:
                if move is not None and depth:
                    self.tp_move[pos] = move
                    if len(self.tp_move) > TABLE_SIZE:
                        del self.tp_move[next(k for k in self.tp_move if k != self.root)]
                break
        if depth and not live and all(
                pos.move(m).king_capture() for m in pos.gen_moves()):
            best = -ML if pos.rotate(nullmove=True).king_capture() else 0
        if not root:
            self.tp_score[pos, depth] = Entry(best, entry.upper) if best >= gamma else Entry(entry.lower, best)
        if len(self.tp_score) > TABLE_SIZE:
            del self.tp_score[next(iter(self.tp_score))]
        return best
    def search(self, history):
        self.nodes, self.history = 0, set(history)
        self.tp_score.clear()
        pos = self.root = history[-1]
        bare = sum(c.isupper() for c in pos.board) == 1 or sum(c.islower() for c in pos.board) == 1
        pst["K"] = K_END if bare else K_MID
        gamma = 0
        for depth in range(1, 1000):
            lower, upper, probes = 1 - MU, MU, 0
            while lower < upper - ER:
                score = self.bound(pos, gamma, depth, root=True)
                if score >= gamma: lower = max(lower, score)
                else: upper = min(upper, score)
                probes += 1
                yield depth, gamma, score, self.tp_move.get(pos)
                if lower > upper or probes > PC:
                    break
                gamma = (lower + upper + 1) // 2
def render(i): return chr((i - A1) % 10 + ord("a")) + str(1 - (i - A1) // 10)
def fb(board, wc=(True, True), bc=(True, True), ep=0, kp=0):
    score = sum(pst[p][i] if p.isupper() else -pst[p.upper()][119 - i]
                for i, p in enumerate(board) if p.isalpha())
    return Position(board, score, wc, bc, ep, kp)
import json,os,urllib.request,time
U=os.environ["MAKEFUN_ENV_URL"]
def P(p,b):
 r=urllib.request.Request(U+p,data=json.dumps(b).encode(),headers={"content-type":"application/json"})
 return json.load(urllib.request.urlopen(r))
def BD(f):
 b=[" "]*120
 for r in range(12):b[r*10+9]="\n"
 for ri,row in enumerate(f.split()[0].split("/")):
  fi=0;r=2+ri
  for k in range(8):b[r*10+1+k]="."
  for c in row:
   if c.isdigit():fi+=int(c)
   else:b[r*10+1+fi]=c;fi+=1
 return "".join(b)
def MI(b):
 o=[" "]*120
 for r in range(12):o[r*10+9]="\n"
 for i in range(21,99):
  c=b[i];j=119-i
  if c==".":o[j]="." if 21<=j<=98 else " "
  elif c not in".\n ":o[j]=c.swapcase()
 return "".join(o)
while 1:
 g=P("/game",{})
 st=g.get("status")
 if st=="done":break
 if st!="your_move":continue
 w=g["colour"]=="white"
 b=BD(g["fen"])
 if not w:b=MI(b)
 pos=fb(b,(w,""),(not w,""))
 s=SE();t0=time.time();s.deadline=t0+4.5
 mv=None
 try:
  for d,ga,sc,m in s.search([pos]):
   if m:mv=m
   if time.time()-t0>2.5 and mv:break
 except Stop:pass
 if mv is None:continue
 i,j=mv.i,mv.j
 if not w:i,j=119-i,119-j
 u=render(i)+render(j)+(mv.prom.lower() if mv.prom else"")
 L=g["legal_moves"]
 if u not in L:u=L[0] if L else None
 if not u:continue
 P("/move",{"game":g["game"],"move":u})

def safe_prompt(f):
    line = f()
    return line if line and line.strip() else None
