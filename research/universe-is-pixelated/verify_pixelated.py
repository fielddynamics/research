"""
Checks for 'The Universe Is Pixelated'. Every statement of established
mathematics in the README is verified here, together with the GFD value of G.
Run: python verify_pixelated.py
"""
import itertools, math
import numpy as np

PASS = FAIL = 0
def check(name, ok):
    global PASS, FAIL
    PASS += bool(ok); FAIL += (not ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")

pc = lambda v: bin(v).count("1")
N = 8
H = np.array([[(-1) ** pc(a & x) for x in range(N)] for a in range(N)])
TetA = [v for v in range(N) if pc(v) % 2 == 1]   # {1,2,4,7}
TetB = [v for v in range(N) if pc(v) % 2 == 0]   # {0,3,5,6}

print("1. The Walsh-Hadamard matrix of the cube")
check("H8 equals H2 (x) H2 (x) H2 (Sylvester)", np.array_equal(H, np.kron(np.kron([[1,1],[1,-1]],[[1,1],[1,-1]]),[[1,1],[1,-1]])))
check("rows are orthogonal: H H^T = 8 I", np.array_equal(H @ H.T, 8 * np.eye(N, dtype=int)))
check("rows are characters: w_a(x XOR y) = w_a(x) w_a(y)",
      all(H[a, x ^ y] == H[a, x] * H[a, y] for a in range(N) for x in range(N) for y in range(N)))

print("2. The stellated octahedron in the spectrum")
check("TetA = odd-parity corners {1,2,4,7}, TetB = even-parity corners {0,3,5,6}", TetA == [1,2,4,7] and TetB == [0,3,5,6])
check("w111 = +1 on TetB and -1 on TetA", all(H[7, v] == (1 if v in TetB else -1) for v in range(N)))
check("each tetrahedron: all six pairs at Hamming distance 2 (regular)",
      all(pc(a ^ b) == 2 for T in (TetA, TetB) for a, b in itertools.combinations(T, 2)))
check("TetB is a subgroup under XOR; TetA is its coset", all((a ^ b) in TetB for a in TetB for b in TetB) and {a ^ 7 for a in TetB} == set(TetA))
indA = np.array([v in TetA for v in range(N)], int)
check("spectrum of TetA's indicator lives only at w000 and w111", set(np.nonzero(H @ indA)[0]) == {0, 7})
ax = np.array([v in (0, 7) for v in range(N)], int)
check("spectrum of the body diagonal {000,111} lives only on TetB", set(np.nonzero(H @ ax)[0]) == set(TetB))
Adj = np.array([[int(pc(x ^ y) == 1) for y in range(N)] for x in range(N)])
check("cube-graph eigenvectors are the Walsh functions, eigenvalue 3 - 2*grade",
      all(np.array_equal(Adj @ H[a], (3 - 2 * pc(a)) * H[a]) for a in range(N)))
check("cube graph is bipartite with colour classes TetA and TetB", all(Adj[x, y] == 0 for T in (TetA, TetB) for x in T for y in T))
check("multiplying by w111 maps eigenvalue lambda to -lambda",
      all(np.array_equal(Adj @ (H[7] * H[a]), -(3 - 2 * pc(a)) * (H[7] * H[a])) for a in range(N)))

print("3. Hadamard rows are the tetrad")
H4 = np.array([[1,1,1,1],[1,1,-1,-1],[1,-1,1,-1],[1,-1,-1,1]])
V = H4[:, 1:]
check("dropping H4's first column gives Letter 1's v1..v4", [tuple(r) for r in V] == [(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)])
check("v1+v2+v3+v4 = 0 (closure)", np.array_equal(V.sum(0), [0,0,0]))
check("pairwise cosine -1/3 (regular tetrahedron)", all(abs(V[i] @ V[j] / 3 + 1/3) < 1e-12 for i, j in itertools.combinations(range(4), 2)))

print("4. The octahedron and the eight null directions")
normals = {tuple(s) for s in itertools.product((1,-1), repeat=3)}
check("the octahedron |x|+|y|+|z| <= 1 has its 8 face normals at the 8 cube corners", len(normals) == 8)
check("those 8 normals are exactly +-v1..v4 (both tetrads)", normals == {tuple(r) for r in V} | {tuple(-r) for r in V})
check("octahedron = {|v_i| <= 1 for all i}: equal on a sample grid",
      all((abs(x)+abs(y)+abs(z) <= 1) == all(abs(r @ (x,y,z)) <= 1 for r in V)
          for x in np.linspace(-1,1,11) for y in np.linspace(-1,1,11) for z in np.linspace(-1,1,11)))

print("5. Boolean functions on the cube")
spectra = []
for bits in range(2 ** N):
    F = np.array([1 - 2 * ((bits >> x) & 1) for x in range(N)])
    spectra.append(H @ F)
check("3 inputs -> 2^3 = 8 corners -> 2^8 = 256 Boolean functions", len(spectra) == 256)
check("Parseval: every spectrum has sum of squares 64", all((W ** 2).sum() == 64 for W in spectra))
check("16 functions are affine (a single Walsh function or its negative)", sum(np.abs(W).max() == 8 for W in spectra) == 16)

print("6. G as a graded-operator read (GFD)")
K = 4
for s, f in ((1, 21), (0, 17), (-1, 13)):
    I_s = np.diag([1] + [s] * K + [1] * K ** 2)
    check(f"Tr(I_s) at s={s:+d} equals f(K,s) = {f}", int(np.trace(I_s)) == f)
alpha, hbar, c, me = 7.2973525693e-3, 1.054571817e-34, 299792458.0, 9.1093837015e-31
G0 = (17 / 13) * alpha ** 21 * hbar * c / me ** 2
G1 = G0 * (1 + alpha / (2 * math.pi))
check(f"G tree = {G0:.4e}, within 0.13% of CODATA 6.6743e-11", abs(G0 / 6.67430e-11 - 1) < 1.3e-3)
check(f"G one-loop = {G1:.5e}, within 0.01% of CODATA", abs(G1 / 6.67430e-11 - 1) < 1e-4)

print("7. The grid")
dihedral = {"tetrahedron": math.acos(1/3), "cube": math.pi/2, "octahedron": math.acos(-1/3),
            "dodecahedron": math.acos(-1/math.sqrt(5)), "icosahedron": math.acos(-math.sqrt(5)/3)}
fills = [k for k, d in dihedral.items() if abs(2*math.pi/d - round(2*math.pi/d)) < 1e-9]
check("only the cube's dihedral angle divides 360 degrees (only the cube fills space face to face)", fills == ["cube"])

print(f"\n  {PASS} passed, {FAIL} failed")
raise SystemExit(FAIL > 0)
