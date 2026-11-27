"""The coupling polynomial at the prime two.

Checks every statement in ../THE_COUPLING_POLYNOMIAL_AT_TWO.md.
Run from this folder:  python verify_prime_two.py   (needs sympy)
"""
import itertools as it
import sympy as sp

n = 0
def check(label, ok):
    global n
    assert ok, label
    n += 1
    print("PASS", label)

t, K = sp.symbols("t K")
I2 = sp.eye(2)
# integer rotations of order 3, 4, 6: the companion matrices of the cyclotomic polynomials
C = {3: sp.Matrix([[0, -1], [1, -1]]), 4: sp.Matrix([[0, -1], [1, 0]]), 6: sp.Matrix([[0, -1], [1, 1]])}
PHI = {3: t**2 + t + 1, 4: t**2 + 1, 6: t**2 - t + 1}
mod = lambda M, p: M.applyfunc(lambda v: v % p)

# ------------------------------------------------------------------ 1. the coupling polynomial is det(K I - C_n)
for k, s in ((3, 1), (4, 0), (6, -1)):
    check(f"C_{k} has order {k}", C[k] ** k == I2 and all(C[k] ** j != I2 for j in range(1, k)))
    check(f"det(K I - C_{k}) = Phi_{k}(K) = 1 + ({s})K + K^2",
          sp.expand((K * I2 - C[k]).det() - (1 + s * K + K**2)) == 0)
    check(f"the state label s = {s} is minus the trace of C_{k}", -C[k].trace() == s)
check("at K = 4: 21, 17, 13", [(4 * I2 - C[k]).det() for k in (3, 4, 6)] == [21, 17, 13])

# ------------------------------------------------------------------ 2. the same numbers as norms
w = sp.Rational(-1, 2) + sp.sqrt(3) * sp.I / 2
N = lambda z: sp.nsimplify(sp.expand(z * sp.conjugate(z)))
check("21 = N(4 - w), 13 = N(4 + w) in Z[w]; 17 = N(4 - i) in Z[i]",
      (N(4 - w), N(4 + w), N(4 - sp.I)) == (21, 13, 17))
check("(4 - w)(4 + w) = 17 + w, so 273 = N(17 + w)",
      sp.simplify(sp.expand((4 - w) * (4 + w)) - (17 + w)) == 0 and N(17 + w) == 273)
check("273 = Phi_6(17) = Phi_3(16)", 17**2 - 17 + 1 == 273 == 16**2 + 16 + 1)
check("C_6 has the sign-reversed eigenvalues of C_3 (-w and its conjugate)",
      sp.expand(PHI[6] - PHI[3].subs(t, -t)) == 0)

# ------------------------------------------------------------------ 3. reduction at two
check("Phi_3 stays irreducible mod 2: 2 is inert in Z[w], residue field F_4 (so K = 4)",
      sp.factor_list(PHI[3], modulus=2)[1] == [(t**2 + t + 1, 1)])
check("Phi_4 = (t + 1)^2 mod 2: 2 ramifies in Z[i]", sp.factor_list(PHI[4], modulus=2)[1] == [(t + 1, 2)])
check("2 = -i (1 + i)^2 in Z[i]", sp.expand(-sp.I * (1 + sp.I) ** 2) == 2)
check("Phi_6 = Phi_3 mod 2", sp.Poly(PHI[6] - PHI[3], t, modulus=2).is_zero)

R = sp.Matrix([[0, 1], [1, 1]])      # (a, b) -> (b, a + b): the I Ching read
S = sp.Matrix([[0, 1], [1, 0]])      # (a, b) -> (b, a): trigram swap
L = sp.Matrix([[1, 0], [1, 1]])      # the Sierpinski generator of Proofs 26 and g-null-rotation
check("C_3 = R mod 2 and C_6 = R mod 2: TetA's and TetB's rotations both reduce to the I Ching read",
      mod(C[3], 2) == R and mod(C[6], 2) == R)
check("C_3 and C_6 differ mod 4: the root sign survives in the second binary digit",
      mod(C[3], 4) != mod(C[6], 4))
check("C_4 = S mod 2: the Field Origin's rotation reduces to the trigram swap", mod(C[4], 2) == S)
check("S is unipotent mod 2: (S - I)^2 = 0", mod((S - I2) ** 2, 2) == sp.zeros(2))
GL = [M for M in (sp.Matrix(2, 2, list(v)) for v in it.product([0, 1], repeat=4)) if M.det() % 2 == 1]
check("GL(2,2) has 6 elements", len(GL) == 6)
check("S is conjugate to the Sierpinski generator L in GL(2,2)",
      any(mod(P * S * P.inv_mod(2), 2) == L for P in GL))
gen, frontier = {tuple(I2)}, [I2]
while frontier:
    M = frontier.pop()
    for g in (R, S):
        Nn = mod(M * g, 2)
        if tuple(Nn) not in gen:
            gen.add(tuple(Nn)); frontier.append(Nn)
check("R and S generate all of GL(2,2) = S_3", len(gen) == 6)

# ------------------------------------------------------------------ 4. on the 64 hexagrams
V = list(range(8))
H = [(a, b) for a in V for b in V]
def apply(M, h):
    a, b = h
    pick = lambda c, x: x if c % 2 else 0
    return (pick(M[0, 0], a) ^ pick(M[0, 1], b), pick(M[1, 0], a) ^ pick(M[1, 1], b))
orbits = set()
for h in H:
    o = frozenset(apply(M, h) for M in (sp.Matrix(2, 2, list(g)) for g in gen))
    orbits.add(o)
sizes = sorted(len(o) for o in orbits)
check("GL(2,2) orbits on hexagrams: 1 + 7 x 3 + 7 x 6 (the Fano decomposition)",
      sizes == [1] + [3] * 7 + [6] * 7)
check("R alone: 21 orbits of 3 on the nonzero hexagrams (Proof 26's directions)",
      len({frozenset({h, apply(R, h), apply(R * R, h)}) for h in H if h != (0, 0)}) == 21)
check("S alone fixes the 8 hexagrams with equal trigrams and pairs the rest",
      sum(1 for h in H if apply(S, h) == h) == 8)

print(f"{n} checks passed")
