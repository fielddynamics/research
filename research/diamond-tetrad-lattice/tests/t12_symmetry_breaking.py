"""T12. Symmetry breaking when x != 1.
For each of the 48 signed permutation matrices R, ask whether p -> R p + tau maps the diamond
sites onto themselves for some translation tau (diamond's space group is nonsymmorphic, so
tau is tried over every vector taking the origin to a nearby site). With V3 = 0 an operation is a symmetry if it maps
the diamond sites onto themselves (labels may swap: both ends are alike). With V3 != 0 the
labels must be kept. Pass: 48 and 24, and the lost operations are exactly those that swap
the sublattices (the parity coset -I . Td)."""
import itertools
import numpy as np
from exact_common import verdict
from fractions import Fraction as Fr
R48 = []
for p in itertools.permutations(range(3)):
    for s in itertools.product((1, -1), repeat=3):
        Rm = np.zeros((3, 3), int)
        for i in range(3):
            Rm[i, p[i]] = s[i]
        R48.append(Rm)
r = 6
A = {p for p in itertools.product(range(-r, r + 1), repeat=3) if all(c % 2 == 0 for c in p) and sum(p) % 4 == 0}
B = {p for p in itertools.product(range(-r, r + 1), repeat=3) if all(c % 2 for c in p) and sum(p) % 4 == 3}
lab = {**{p: 1 for p in A}, **{p: -1 for p in B}}
inner = [p for p in lab if max(map(abs, p)) <= r - 3]


taus = [np.array(q) for q in lab if max(map(abs, q)) <= 4]


def maps(Rm, tau, keep):
    seen = set()
    for p in inner:
        q = tuple(int(c) for c in Rm @ np.array(p) + tau)
        if q not in lab:
            return None
        seen.add(lab[q] == lab[p])
    if len(seen) != 1:
        return None
    kept = seen.pop()
    if keep and not kept:
        return None
    return "keeps" if kept else "swaps"


def classify(Rm, keep):
    for tau in taus:
        m = maps(Rm, tau, keep)
        if m:
            return m
    return None


res0 = [classify(Rm, False) for Rm in R48]
res1 = [classify(Rm, True) for Rm in R48]
n0 = sum(x is not None for x in res0); n1 = sum(x is not None for x in res1)
lost = [i for i in range(48) if res0[i] and not res1[i]]
TA = {(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)}
Td = [i for i, Rm in enumerate(R48) if {tuple(Rm @ np.array(v)) for v in TA} == TA]
coset = {i for i, Rm in enumerate(R48) if any((Rm == -R48[j]).all() for j in Td)}
print(f"V3 = 0: {n0} operations; V3 != 0: {n1}; lost {len(lost)}")
print("kept ones are Td (preserve the TetA star):", set(i for i in range(48) if res1[i]) == set(Td))
print("lost ones swap the sublattices:", all(res0[i] == "swaps" for i in lost), "| and are -I . Td:", set(lost) == coset)
ok = n0 == 48 and n1 == 24 and all(res0[i] == "swaps" for i in lost) and set(lost) == coset
verdict("T12", ok, "the polar bond (x != 1) halves the symmetry, from diamond's 48 to zincblende's 24; the lost half is parity")
