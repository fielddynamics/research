"""Checks for every result in 'The Null Directions of the Tetrad Frame Carry a Complete Boolean Basis'.
Exact integer and rational arithmetic throughout (sympy); the clone closures are exhaustive over all 256 three-input functions.
Run: python verify_null_cone_boolean.py"""
import itertools
import sympy as sp

ok = []
def check(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

pc = lambda x: bin(x).count("1")
N = 8
corners = list(itertools.product((1, -1), repeat=3))                 # corner index i <-> bits b = (1 - s)/2
bits = lambda s: tuple((1 - c) // 2 for c in s)
idx = lambda s: int("".join(map(str, bits(s))), 2)

# ---- Section 2: the eight null directions are the corners of the cube
TA = [c for c in corners if c[0] * c[1] * c[2] == 1]; TB = [c for c in corners if c[0] * c[1] * c[2] == -1]
u = {c: sp.Matrix(c) / sp.sqrt(3) for c in corners}
eta = sp.diag(1, -1, -1, -1)
k = {c: sp.Matrix([1] + list(u[c])) for c in corners}
check("2.1 Letter 1: TetA's four directions u = v/sqrt3 are unit vectors with zero centroid, isotropic second moment (4/3) I and pairwise "
      "inner product -1/3", all(u[c].dot(u[c]) == 1 for c in TA) and sum((u[c] for c in TA), sp.zeros(3, 1)) == sp.zeros(3, 1)
      and sum((u[c] * u[c].T for c in TA), sp.zeros(3)) == sp.Rational(4, 3) * sp.eye(3)
      and all(u[a].dot(u[b]) == -sp.Rational(1, 3) for a, b in itertools.combinations(TA, 2)))
check("2.2 each k = (1, u) is a real light ray (k.eta.k = 0), and TetB's are the antipodes: the eight points of the star are eight null directions",
      all((k[c].T * eta * k[c])[0] == 0 for c in corners) and sorted(TB) == sorted(tuple(-x for x in c) for c in TA))
check("2.3 the signs of a null direction's spatial part are three bits; the eight directions are the eight 3-bit words, and TetA/TetB is "
      "their parity", sorted(idx(c) for c in corners) == list(range(8)) and all((pc(idx(c)) % 2 == 0) == (c in TA) for c in corners))

# ---- Section 3: every function is a Walsh combination; the Walsh characters alone are affine
H = sp.Matrix(N, N, lambda i, j: (-1)**pc(i & j))
check("3.1 H_8 H_8 = 8 I, so every one of the 256 Boolean functions on the eight directions is a unique real combination of the eight "
      "Walsh characters", H * H == 8 * sp.eye(N))
def table(f):   # truth table as an 8-bit integer: bit i = f(corner i)
    return sum(1 << i for i in range(N) if f(i))
S = sp.Matrix(N, N, lambda i, j: 1 if (j & ~i) == 0 else 0)          # S[i][j] = AND of the bits of j, at corner i
def anf(t):
    f = sp.Matrix([(t >> i) & 1 for i in range(N)])
    return [int(x) % 2 for x in S * f]
deg = lambda t: max([pc(j) for j, c in enumerate(anf(t)) if c] + [0])
walsh01 = [table(lambda i, j=j: pc(i & j) % 2) for j in range(N)]
check("3.2 in 0/1 form the Walsh characters are the parities x_J = XOR of the bits in J; each has algebraic degree <= 1 (affine), and so "
      "does the TetA/TetB indicator", all(deg(t) <= 1 for t in walsh01) and deg(table(lambda i: pc(i) % 2)) == 1)
def clone(gates, arity_max=3):
    proj = {table(lambda i, b=b: (i >> b) & 1) for b in range(3)}
    F = set(proj)
    while True:
        new = set(F)
        for g, ar in gates:
            for args in itertools.product(sorted(F), repeat=ar):
                new.add(sum(1 << i for i in range(N) if g(*[(a >> i) & 1 for a in args])))
        if new == F: return F
        F = new
affine_gates = [(lambda a, b: a ^ b, 2), (lambda a: 1 - a, 1), (lambda: 1, 0), (lambda: 0, 0)]
Cl_aff = clone(affine_gates)
check("3.3 closing the projections under XOR, NOT and the constants (every parity gate) gives exactly the 16 affine functions of three bits, "
      "not 256: parity alone is not a universal gate set (Post's affine class)", len(Cl_aff) == 16 and all(deg(t) <= 1 for t in Cl_aff))

# ---- Section 4: the Walsh read factors into an AND table and an XOR table
D = sp.diag(*[(-2)**pc(x) for x in range(N)])
check("4.1 H_8 = S D S^T with D = diag((-2)^popcount) = diag(e^((ln2 + i pi) popcount))", S * D * S.T == H)
check("4.2 S[i][j] = AND of the bits of J at corner i: S is the evaluation table of the eight AND monomials (1, x, y, z, xy, xz, yz, xyz)",
      all(S[i, j] == (1 if all((i >> b) & 1 for b in range(3) if (j >> b) & 1) else 0) for i in range(N) for j in range(N)))
check("4.3 the entrywise identity behind 4.1: (-1)^n = sum_k C(n,k) (-2)^k = (1 - 2)^n, n = |i AND j|",
      all(sum(sp.binomial(n, kk) * (-2)**kk for kk in range(n + 1)) == (-1)**n for n in range(4)))
S2 = (S * S).applyfunc(lambda v: v % 2)
check("4.4 S^2 = I over GF(2), so every function has a unique algebraic normal form, an XOR of AND monomials (Zhegalkin): all 256 "
      "reconstructed", S2 == sp.eye(N) and all(sum(1 << i for i in range(N) if sum(S[i, j] * c for j, c in enumerate(anf(t))) % 2) == t
                                               for t in range(256)))
Cl_axo = clone([(lambda a, b: a & b, 2), (lambda a, b: a ^ b, 2), (lambda: 1, 0)])
check("4.5 closing the projections under AND, XOR and 1 gives all 256 functions: the AND table (S) and the XOR table (H) together are a "
      "universal gate set", len(Cl_axo) == 256)

# ---- Section 5: the null cone of the two-bit block
I2 = sp.eye(2); sx = sp.Matrix([[0, 1], [1, 0]]); sy = sp.Matrix([[0, -sp.I], [sp.I, 0]]); sz = sp.Matrix([[1, 0], [0, -1]])
sig = [I2, sx, sy, sz]
mink = lambda X: [sp.simplify((s_ * X).trace() / 2) for s_ in sig]
gates2 = {}
names = {0b0000: "FALSE", 0b1000: "AND", 0b0100: "a AND NOT b", 0b0010: "NOT a AND b", 0b0001: "NOR", 0b1100: "a", 0b1010: "b",
         0b0011: "NOT a", 0b0101: "NOT b", 0b1111: "TRUE", 0b0110: "XOR", 0b1001: "XNOR", 0b1110: "OR", 0b0111: "NAND",
         0b1011: "a -> b", 0b1101: "b -> a"}
for code, nm in names.items():
    # truth table X[a][b] = f(a, b); code bit order: f(1,1) f(1,0) f(0,1) f(0,0)
    X = sp.Matrix([[(code >> 0) & 1, (code >> 1) & 1], [(code >> 2) & 1, (code >> 3) & 1]])
    gates2[nm] = X
null = sorted(nm for nm, X in gates2.items() if X.det() == 0)
nonnull = sorted(nm for nm, X in gates2.items() if X.det() != 0)
check("5.1 read as X = (f(a,b)), det X is the Minkowski norm; exactly 10 of the 16 two-input gates are null: FALSE, TRUE, AND, NOR, the four "
      "literals a, b, NOT a, NOT b, and the two mixed conjunctions", len(null) == 10 and set(nonnull) == {"XOR", "XNOR", "OR", "NAND", "a -> b", "b -> a"})
check("5.2 null means rank <= 1, i.e. f(a, b) = g(a) h(b): the null gates are exactly the separable gates (conjunctions of literals and the "
      "constants)", all((X.rank() <= 1) == (X.det() == 0) for X in gates2.values()) and all(
          any(gates2[nm] == sp.Matrix(g) * sp.Matrix(h).T for g in ([0, 0], [1, 0], [0, 1], [1, 1]) for h in ([0, 0], [1, 0], [0, 1], [1, 1]))
          for nm in null))
check("5.3 AND's truth table is |11>, the light ray fixed by the Sierpinski null rotation X -> A X A^T, A = [[1,0],[1,1]] (rows indexed 0, 1)",
      gates2["AND"] == sp.Matrix([[0, 0], [0, 1]]) and sp.Matrix([[1, 0], [1, 1]]) * gates2["AND"] * sp.Matrix([[1, 0], [1, 1]]).T == gates2["AND"])
real_null = sorted(nm for nm in null if gates2[nm] == gates2[nm].T)
check("5.4 the symmetric null gates are AND, NOR and TRUE, real light rays along -z, +z and +x ((t,x,y,z) = (1/2,0,0,-1/2), (1/2,0,0,1/2), "
      "(1,1,0,0)), with FALSE the zero vector; the other six null gates are complex null vectors, real only in the split-signature reading",
      real_null == ["AND", "FALSE", "NOR", "TRUE"] and gates2["FALSE"].is_zero_matrix
      and [mink(gates2[g]) for g in ("AND", "NOR", "TRUE")] == [[sp.Rational(1, 2), 0, 0, -sp.Rational(1, 2)], [sp.Rational(1, 2), 0, 0, sp.Rational(1, 2)], [1, 1, 0, 0]]
      and all(any(sp.im(c) != 0 for c in mink(gates2[nm])) for nm in null if nm not in real_null))
lit = {"AND": (lambda a, b: a & b, 2), "NOT a": (lambda a: 1 - a, 1)}
Cl_null = clone([lit["AND"], lit["NOT a"]])
check("5.5 the null gates contain AND and NOT, and AND with NOT generate all 256 three-input functions: the null gates are a universal set",
      len(Cl_null) == 256)
Cl_nor = clone([(lambda a, b: 1 - (a | b), 2)])
check("5.6 NOR alone generates all 256 three-input functions: a single gate whose truth table is a real light ray is universal", len(Cl_nor) == 256)
check("5.7 the non-null gates are XOR, XNOR, OR, NAND and the two implications; parity (XOR, XNOR) lies off the cone",
      gates2["XOR"].det() == -1 and gates2["XNOR"].det() == 1)

print(f"\n{sum(ok)}/{len(ok)} checks passed")
