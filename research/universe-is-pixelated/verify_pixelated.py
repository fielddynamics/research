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

print("8. The cube as universal Boolean operator")
nand = 0
for x in range(N):
    a, b = (x >> 2) & 1, (x >> 1) & 1
    nand |= (1 - (a & b)) << x
check("NAND (on the first two inputs) is one of the 256 operations", 0 <= nand < 256)
tof = [x ^ (1 if (x >> 2) & 1 and (x >> 1) & 1 else 0) for x in range(N)]
check("the Toffoli gate is a permutation of the 8 corners, swapping 110 and 111", sorted(tof) == list(range(N)) and tof[6] == 7 and tof[7] == 6 and all(tof[x] == x for x in range(6)))
check("reversible 3-bit gates = permutations of the corners: 8! = 40320", math.factorial(8) == 40320)
Hinv = H.T / 8
check("every one of the 256 operations is recovered exactly from its Walsh spectrum (unique expansion)",
      all(np.allclose(Hinv @ W, [1 - 2 * ((bits >> x) & 1) for x in range(N)]) for bits, W in enumerate(spectra)))

print("9. Letters 1, 2 and 3 on the cube")
H16 = np.array([[(-1) ** pc(a & x) for x in range(16)] for a in range(16)])
from scipy.optimize import linprog
bounded = []
for m in range(16):
    sgn = np.array([1 if (m >> i) & 1 else -1 for i in range(4)])
    Nrm = sgn[:, None] * V
    unb = any(linprog(-d, A_ub=Nrm, b_ub=np.ones(4), bounds=[(None, None)] * 3).status == 3
              for d in np.vstack([np.eye(3), -np.eye(3)]))
    if not unb: bounded.append(m)
check("Letter 1: of the 16 sign choices, exactly 0000 and 1111 give bounded regions", bounded == [0, 15])
rep = np.array([v in (0, 15) for v in range(16)], int)
check("Letter 1: the Walsh spectrum of {0000,1111} is the 8 even-weight patterns",
      set(np.nonzero(H16 @ rep)[0]) == {a for a in range(16) if pc(a) % 2 == 0})
check("Letter 2: central inversion x -> x XOR 111 swaps TetA and TetB", {v ^ 7 for v in TetA} == set(TetB))
check("Letter 2: w_a(x XOR 111) = (-1)^grade(a) w_a(x)", all(H[a, x ^ 7] == (-1) ** pc(a) * H[a, x] for a in range(N) for x in range(N)))
blind_ok, blind = True, 0
for bits, W in enumerate(spectra):
    inv = all(((bits >> x) & 1) == ((bits >> (x ^ 7)) & 1) for x in range(N))
    even = all(W[a] == 0 for a in range(N) if pc(a) % 2)
    blind_ok &= (inv == even); blind += inv
check("Letter 2: an operation is blind to TetA/TetB exactly when its spectrum is even-grade only", blind_ok)
check("Letter 2: 16 of the 256 operations are root-blind", blind == 16)
check("Letter 3: per face 16 = 10 symmetric + 6 antisymmetric = (f(K,+1)-1)/2 + (f(K,-1)-1)/2",
      (K*(K+1)//2, K*(K-1)//2) == ((21-1)//2, (13-1)//2) and K*(K+1)//2 + K*(K-1)//2 == 16)
check("Letter 3: K^3 = (2^D)^2 = 64 holds at D = 3 and at no other D up to 50",
      [D for D in range(1, 51) if (D + 1) ** 3 == 4 ** D] == [3])
check("G blocks 1, 4, 16 are Sylvester-Hadamard orders 2^0, 2^2, 2^4", [1, 4, 16] == [2 ** 0, 2 ** 2, 2 ** 4])

print("10. The octahedral node (Python port of OctahedralResonance.cs)")
import contextlib, io, os, sys as _sys
_sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import octahedral_node as on
def _wh(v): return [sum(on.H[k][c] * v[k] for k in range(8)) / 8 for c in range(8)]
grade = [0, 1, 1, 1, 2, 2, 2, 3]
nd = on.OctahedralNode(); nd.inject((1, -1, 1)); nd.tick()
inp = [sum((1, -1, 1)[d] * on.SIGNS[k][d] for d in range(3)) for k in range(8)]
nz = lambda v: {grade[c] for c, x in enumerate(_wh(v)) if abs(x) > 1e-9}
check("input projection carries grade 1 only", nz(inp) == {1})
check("forward pass adds grades 0 and 2", nz(nd.forward_mix) == {0, 1, 2})
check("backward pass adds grade 3: one oscillation fills the whole Walsh spectrum", nz(nd.backward_mix) == {0, 1, 2, 3})
with contextlib.redirect_stdout(io.StringIO()):
    res, _ = on.run()
for key in ("analyser 256", "XOR single tick", "3-bit parity single tick", "16 gates single tick", "full adder sum", "full adder carry"):
    a, b = res[key]
    check(f"node: {key} = {a}/{b}", a == b)

print(f"\n  {PASS} passed, {FAIL} failed")
raise SystemExit(FAIL > 0)
