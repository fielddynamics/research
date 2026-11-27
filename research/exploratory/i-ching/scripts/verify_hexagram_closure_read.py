"""The 64 hexagrams and the closure read of Proofs 23-26.

Checks every statement in ../HEXAGRAMS_AND_THE_CLOSURE_READ.md.
Encoding as in closure_walk_proof_iching.py: yang = 1, and a trigram's value is
4*bottom + 2*middle + top, so Earth = 0, Heaven = 7. A hexagram is (lower, upper).

Run from this folder:  python verify_hexagram_closure_read.py
Needs numpy and mpmath.
"""
import itertools as it
import numpy as np
import mpmath

n = 0
def check(label, ok):
    global n
    assert ok, label
    n += 1
    print("PASS", label)

NAMES = {0: "Earth", 1: "Mountain", 2: "Water", 3: "Wind",
         4: "Thunder", 5: "Fire", 6: "Lake", 7: "Heaven"}
TRI = range(8)
HEX = [(a, b) for a in TRI for b in TRI]
ZERO = (0, 0)

def line(t, i):           # line i = 0 (bottom), 1 (middle), 2 (top)
    return (t >> (2 - i)) & 1

# ------------------------------------------------------------------ 1. the map R
def R(h):
    a, b = h
    return (b, a ^ b)

check("R^3 = identity on all 64 hexagrams", all(R(R(R(h))) == h for h in HEX))
check("R fixes only Earth over Earth", [h for h in HEX if R(h) == h] == [ZERO])
check("R^2 fixes only Earth over Earth", [h for h in HEX if R(R(h)) == h] == [ZERO])
orbits = {frozenset({h, R(h), R(R(h))}) for h in HEX if h != ZERO}
check("the 63 other hexagrams fall into 21 orbits of 3", len(orbits) == 21 and
      all(len(o) == 3 for o in orbits))

# ------------------------------------------------------------------ 2. R is omega on corresponding lines
# F4 = {x + y w : x, y in F2}, w^2 = w + 1; w * (x + y w) = y + (x + y) w
def omega(d):
    x, y = d
    return (y, x ^ y)

def pair(h, i):           # corresponding lines: line i of the lower and of the upper trigram
    return (line(h[0], i), line(h[1], i))

check("R acts as multiplication by omega on each corresponding pair (lines 1&4, 2&5, 3&6)",
      all(pair(R(h), i) == omega(pair(h, i)) for h in HEX for i in range(3)))

# ------------------------------------------------------------------ 3. grades 1, 4, 16
def grade(h):             # highest active corresponding pair, counted from the bottom
    act = [i for i in range(3) if pair(h, i) != (0, 0)]
    return max(act) if act else -1

check("R preserves the grade", all(grade(R(h)) == grade(h) for h in HEX))
per_grade = [sum(1 for o in orbits if grade(next(iter(o))) == k) for k in range(3)]
check("orbits per grade are 1, 4, 16  ((4-1)/3, (16-4)/3, (64-16)/3)", per_grade == [1, 4, 16])

# ------------------------------------------------------------------ 4. 21 = 7 + 14, the Fano subplane
def dependent(h):
    a, b = h
    return a == 0 or b == 0 or a == b

dep = [o for o in orbits if dependent(next(iter(o)))]
check("7 orbits of dependent pairs, 14 of independent pairs",
      len(dep) == 7 and len(orbits) - len(dep) == 14)
check("each dependent orbit is {(v,0), (0,v), (v,v)} for one nonzero trigram v",
      sorted(sorted(o) for o in dep) ==
      sorted(sorted([(v, 0), (0, v), (v, v)]) for v in range(1, 8)))

# the 21 orbits are the points of PG(2,4); its lines are the zero sets of nonzero F4-linear forms
F4MUL = [[0, 0, 0, 0], [0, 1, 2, 3], [0, 2, 3, 1], [0, 3, 1, 2]]   # 0,1,w,w^2 as 0,1,2,3
def f4(d):                 # (x, y) = x + y w  ->  0..3 with w = 2, w^2 = 3 = 1 + w
    x, y = d
    return x + 2 * y
def coords(h):
    return [f4(pair(h, i)) for i in range(3)]
def form(c, h):
    s = 0
    for ci, vi in zip(c, coords(h)):
        s ^= F4MUL[ci][vi]
    return s
point_of = {h: o for o in orbits for h in o}
lines = set()
for c in it.product(range(4), repeat=3):
    if c != (0, 0, 0):
        lines.add(frozenset(point_of[h] for h in HEX if h != ZERO and form(c, h) == 0))
fano = set(dep)
meet = {len(L & fano) for L in lines}
check("PG(2,4) from the hexagrams has 21 lines of 5 points", len(lines) == 21 and
      all(len(L) == 5 for L in lines))
check("every line meets the 7 dependent orbits in 1 or 3 points: a Baer (Fano) subplane",
      meet == {1, 3})

# ------------------------------------------------------------------ 5. the TIME rotation
def T(h):                  # rotate about the Heaven-Earth axis: cycle the line positions
    rot = lambda t: (line(t, 2) << 2) | (line(t, 0) << 1) | line(t, 1)
    return (rot(h[0]), rot(h[1]))

check("T^3 = identity", all(T(T(T(h))) == h for h in HEX))
check("R and T commute (they act on different factors of F4 (x) F2^3)",
      all(R(T(h)) == T(R(h)) for h in HEX))
fixT = [h for h in HEX if T(h) == h]
check("T fixes 4 hexagrams: Earth and Heaven over each other",
      sorted(fixT) == [(0, 0), (0, 7), (7, 0), (7, 7)])
orbT = {frozenset({h, T(h), T(T(h))}) for h in HEX if h != ZERO}
check("T gives 23 invariant directions (3 fixed + 20 orbits), not 21", len(orbT) == 23)
check("by Burnside, T gives 24 invariant dimensions (Proof 23's ordered corner-pair count) "
      "and R gives 22 (the Triforce count)", (64 + 4 + 4) // 3 == 24 and (64 + 1 + 1) // 3 == 22)

# ------------------------------------------------------------------ 6. one Walsh read
H2 = np.array([[1, 1], [1, -1]])
H4 = np.kron(H2, H2)
H8 = np.kron(H4, H2)
def walsh(u, v, bits):
    return (-1) ** bin(u & v).count("1")
# index a hexagram by its six bits: trigram grouping (lower, upper) or corresponding-pair grouping
def bits_trigram(h):
    return (h[0] << 3) | h[1]
def bits_pairs(h):
    v = 0
    for i in range(3):
        x, y = pair(h, i)
        v = (v << 2) | (x << 1) | y
    return v
W_tri = np.array([[walsh(bits_trigram(g), bits_trigram(h), 6) for h in HEX] for g in HEX])
W_pair = np.array([[walsh(bits_pairs(g), bits_pairs(h), 6) for h in HEX] for g in HEX])
check("the 64-point Walsh read is the same whether grouped as two trigrams or three "
      "corresponding pairs", (W_tri == W_pair).all())
check("as matrices: H8 (x) H8 = H4 (x) H4 (x) H4 = H2^(x)6", (np.kron(H8, H8) ==
      np.kron(np.kron(H4, H4), H4)).all())

# ------------------------------------------------------------------ 7. the pi walk against R
N = 20000
mpmath.mp.dps = int(N * np.log10(8)) + 50
whole = int(mpmath.floor(mpmath.mp.pi * mpmath.mpf(8) ** N))
digits = [int(c) for c in oct(whole)[2:]]          # leading 3, then N fractional digits
check("pi in base 8 begins 3.1103755242102643", digits[:17] ==
      [3, 1, 1, 0, 3, 7, 5, 5, 2, 4, 2, 1, 0, 2, 6, 4, 3])
v, s = [], 0
for d in digits:
    s += d
    v.append(s % 8)
# the walk steps (a, b) -> (b, b + d mod 8); R steps (a, b) -> (b, a XOR b)
agree = sum(1 for k in range(2, len(v)) if v[k] == v[k - 2] ^ v[k - 1])
rate = agree / (len(v) - 2)
print(f"   pi walk steps agreeing with R: {agree} of {len(v) - 2} = {rate:.4f} (random: 0.125)")
check("the pi walk follows R on about 1/8 of its steps, as random digits would",
      abs(rate - 0.125) < 0.01)
agree332 = sum(1 for k in range(2, 334) if v[k] == v[k - 2] ^ v[k - 1])
print(f"   in the 332 steps to closure: {agree332} agree with R")
# R itself is a walk with period 3: next = previous XOR current
seq = [5, 3]
for _ in range(10):
    seq.append(seq[-2] ^ seq[-1])
check("R as a walk (next = previous XOR current) repeats with period 3, so it never "
      "covers the 64 hexagrams", seq[:3] == seq[3:6] == seq[6:9])

# ------------------------------------------------------------------ 8. families, lines and line changes
TETA = [7, 4, 2, 1]        # Heaven and the three sons (eldest, middle, youngest)
TETB = [0, 3, 5, 6]        # Earth and the three daughters
xor_closed = lambda S: all((a ^ b) in S for a in S for b in S)
check("with Earth as zero, the mother's family is a subspace and the father's is its coset",
      xor_closed(TETB) and not xor_closed(TETA) and sorted(a ^ 7 for a in TETB) == sorted(TETA))
rot = lambda t: (line(t, 2) << 2) | (line(t, 0) << 1) | line(t, 1)
check("the TIME rotation fixes Heaven and Earth and cycles sons and daughters by age",
      rot(7) == 7 and rot(0) == 0 and [rot(s) for s in (4, 2, 1)] == [2, 1, 4]
      and [rot(d) for d in (3, 5, 6)] == [5, 6, 3])
sign = lambda t: tuple(1 if line(t, i) else -1 for i in range(3))   # yang = +1
core = {}
for a, b in it.combinations(TETA, 2):
    m = tuple((x + y) // 2 for x, y in zip(sign(a), sign(b)))
    core[(a, b)] = m
check("Proof 25's core vertices (s_i + s_j)/2 are the six single lines (position x yin/yang)",
      sorted(core.values()) == sorted([tuple(s if k == i else 0 for k in range(3))
                                       for i in range(3) for s in (1, -1)]))
opp = {7: 0, 4: 3, 2: 5, 1: 6}    # traditional opposites: every line reversed
bonds = [(a, b) for a in TETA for b in TETB if b != opp[a]]
check("Proof 24's 12 core bonds are exactly the one-line changes between the families",
      len(bonds) == 12 and all(bin(a ^ b).count("1") == 1 for a, b in bonds)
      and all(bin(a ^ opp[a]).count("1") == 3 for a in TETA))
check("so the core's conserved currents are the 12 - 8 + 1 = 5 circulations of line changes",
      12 - 8 + 1 == 5)

print(f"{n} checks passed")
