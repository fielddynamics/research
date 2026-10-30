#!/usr/bin/env python3
"""
Octahedral Resonance Node and Lattice: Python port
===================================================

A faithful port of OctahedralResonance.cs (Stephen Nelson, Field Dynamics
Research): a coupled oscillator built on the eight corners of the cube,
the eight points of the stellated octahedron.

    Architecture: 24 (TetA) + 16 (shared vertex) + 24 (TetB) = 64 parameters
    Three subcycles per oscillation:
        1. Forward        (TetA + shared): waves pass into the vertex
        2. Backward       (TetB + shared): the forward mix is received back
        3. Reconciliation (all 64): the two meet; the shared couplings learn
    Readout: the Walsh-Hadamard decomposition of the reconciled vertex state.

The port keeps the C# arithmetic, ordering, clamps and constants unchanged,
so the test suite at the bottom reproduces the C# program's tests. One test is
added at the start: the node as an analyser, which feeds a full truth table
across the eight vertices and reads the Walsh coefficients directly.

Run: python octahedral_node.py
"""
import math

N = 8
SIGNS = [(+1, +1, +1), (+1, +1, -1), (+1, -1, +1), (+1, -1, -1),
         (-1, +1, +1), (-1, +1, -1), (-1, -1, +1), (-1, -1, -1)]
PARITY = [+1, -1, -1, +1, -1, +1, +1, -1]
# TetA is the xyz = +1 tetrahedron in every convention used in this archive.
# The C# source maps bit 1 -> -1, so TetA has even-popcount indices here;
# Letter 1 and the README map bit 1 -> +1, which gives the same corners the
# odd-popcount addresses {001, 010, 100, 111}.
TETA_IDX = [0, 3, 5, 6]          # as in the C# source
TETB_IDX = [1, 2, 4, 7]


def _build_h():
    """H[k][c]: the 8 Walsh functions (const, x, y, z, xy, xz, yz, xyz) at corner k."""
    h = []
    for sx, sy, sz in SIGNS:
        h.append([1, sx, sy, sz, sx * sy, sx * sz, sy * sz, sx * sy * sz])
    return h


H = _build_h()
OVERLAP = [[sum(SIGNS[k][d] * SIGNS[j][d] for d in range(3)) for j in range(N)] for k in range(N)]


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def sign(v):
    """C# Math.Sign: -1, 0 or +1."""
    return (v > 0) - (v < 0)


def _finite(v):
    return not (math.isnan(v) or math.isinf(v))


class OctahedralNode:
    def __init__(self, node_id=0, standing=False):
        self.id = node_id
        self.time = 0.0
        self.cycle = 0
        self.mu = 0.5
        self.mu_prev = 0.5
        # learnable parameters: 24 + 16 + 24
        self.amp_a = [0.0] * N
        self.amp_b = [0.0] * N
        self.freq_a = [1.0 + 0.01 * k for k in range(N)]
        self.freq_b = [1.0 + 0.01 * (N - 1 - k) for k in range(N)]
        self.phase_a = [2 * math.pi * k / N for k in range(N)]
        self.phase_b = [2 * math.pi * (k + 4) / N for k in range(N)]
        self.coupling_in = [1.0] * N
        self.coupling_out = [1.0] * N
        # state
        self.wave_a = [0.0] * N
        self.wave_b = [0.0] * N
        self.forward_mix = [0.0] * N
        self.backward_mix = [0.0] * N
        self.vertex = [0.0] * N
        self.coeffs = [0.0] * N
        self.input = [0.0] * N
        self.output = [0.0] * N
        self.omega = 0.0
        self.entropy = 0.0
        self.energy_a = self.energy_b = self.delta = 0.0
        # hyperparameters
        self.closure_rate = 0.02
        self.dt = 0.1
        self.vertex_gain = 0.2
        self.damping = 0.9          # declared in the C# source, not used by Tick()
        self.pair_links = []
        # standing=True: closure relaxation saturated by the constitutive law
        # mu(x) = x/(x+1), with the outward coupling held at its unit fixed point.
        # The original rule (standing=False) targets sqrt(mean energy), which feeds
        # back on itself and drives amplitudes and couplings to their clamps.
        self.standing = standing

    param_count = 24 + 16 + 24

    def _mix(self, wave):
        out = [0.0] * N
        for k in range(N):
            linear = self.coupling_in[k] * wave[k]
            cross = 0.0
            for j in range(N):
                if j != k:
                    cross += OVERLAP[k][j] * self.coupling_in[k] * wave[k] * self.coupling_in[j] * wave[j]
            v = linear + self.vertex_gain * cross / (N - 1)
            if not _finite(v):
                v = linear
            out[k] = clamp(v, -50, 50)
        return out

    def tick(self):
        self.mu_prev = self.mu
        # subcycle 1: forward (TetA + shared)
        for k in range(N):
            self.wave_a[k] = self.amp_a[k] * math.sin(self.freq_a[k] * self.time + self.phase_a[k]) + self.input[k]
        self.forward_mix = self._mix(self.wave_a)
        # subcycle 2: backward (TetB + shared)
        for k in range(N):
            self.wave_b[k] = (self.amp_b[k] * math.sin(self.freq_b[k] * self.time + self.phase_b[k])
                              + self.coupling_out[k] * self.forward_mix[k])
        self.backward_mix = self._mix(self.wave_b)
        # subcycle 3: reconciliation (all 64)
        self.energy_a = sum(v * v for v in self.forward_mix)
        self.energy_b = sum(v * v for v in self.backward_mix)
        self.delta = self.energy_a - self.energy_b
        for k in range(N):
            self.vertex[k] = self.coupling_out[k] * (self.forward_mix[k] + self.backward_mix[k]) / 2.0
        for c in range(N):
            self.coeffs[c] = sum(H[k][c] * self.vertex[k] for k in range(N)) / N
        self.omega = self.coeffs[7]
        c0 = self.coeffs[0]
        self.mu = clamp((1.0 + self.omega / c0) / 2.0, 0, 1) if abs(c0) > 1e-12 else 0.5
        m = self.mu
        self.entropy = (-m * math.log(m) - (1 - m) * math.log(1 - m)) if 1e-12 < m < 1 - 1e-12 else 0.0
        # self-training of the shared couplings
        for k in range(N):
            fwd, bwd = self.forward_mix[k], self.backward_mix[k]
            if math.isnan(fwd) or math.isnan(bwd):
                continue
            agreement = clamp(fwd * bwd, -10, 10)
            self.coupling_in[k] += self.closure_rate * sign(agreement) * (1.0 - abs(self.coupling_in[k]))
            self.coupling_in[k] = clamp(self.coupling_in[k], 0.01, 5.0)
            if self.standing:
                target_out = 1.0
            else:
                target_out = min(math.sqrt(max((self.energy_a + self.energy_b) / (2 * N), 1e-12)), 5.0)
            self.coupling_out[k] += self.closure_rate * (target_out - self.coupling_out[k])
            self.coupling_out[k] = clamp(self.coupling_out[k], 0.01, 5.0)
        mean_e = (self.energy_a + self.energy_b) / (2 * N)
        r = math.sqrt(max(mean_e, 1e-12))
        target_amp = r / (1.0 + r) if self.standing else min(r, 5.0)
        for k in range(N):
            self.amp_a[k] = clamp(self.amp_a[k] + self.closure_rate * (target_amp - self.amp_a[k]), 0.01, 5.0)
            self.amp_b[k] = clamp(self.amp_b[k] + self.closure_rate * (target_amp - self.amp_b[k]), 0.01, 5.0)
        self.output = list(self.vertex)
        self.input = [0.0] * N
        self.time += self.dt
        self.cycle += 1

    def inject(self, data):
        """Project up to 3 input values onto the 8 corners: input[k] += sum_d data[d] * sign_k[d]."""
        for k in range(N):
            self.input[k] += sum(data[d] * SIGNS[k][d] for d in range(min(len(data), 3)))


class PairConnection:
    def __init__(self, target, pair_index, strength=1.0):
        self.target, self.pair_index, self.strength = target, pair_index, strength


class OctahedralLattice:
    DIRS = [(+1, 0), (-1, 0), (0, +1), (0, -1)]   # right, left, down, up

    def __init__(self, width, height, gain=0.8, damping=0.5, standing=False):
        self.width, self.height, self.tick_count = width, height, 0
        self.grid = [[OctahedralNode(x * height + y, standing) for y in range(height)] for x in range(width)]
        for col in self.grid:
            for node in col:
                node.vertex_gain, node.damping = gain, damping
        for x in range(width):
            for y in range(height):
                for p, (dx, dy) in enumerate(self.DIRS):
                    nx, ny = x + dx, (y + dy) % height     # vertical wraps; horizontal open
                    if 0 <= nx < width:
                        self.grid[x][y].pair_links.append(PairConnection(self.grid[nx][ny], p))

    def tick(self):
        for x in range(self.width):
            for y in range(self.height):
                node = self.grid[x][y]
                for link in node.pair_links:
                    for k in range(N):
                        raw = link.strength * link.target.output[k]
                        node.input[k] += sign(raw) * abs(raw) / (abs(raw) + 1.0)   # mu(x) = x/(x+1)
        for col in self.grid:
            for node in col:
                node.tick()
        self.tick_count += 1

    def set_input(self, row, data):
        if 0 <= row < self.height:
            self.grid[0][row].inject(data)

    def read_outputs(self):
        return [self.grid[self.width - 1][y].mu for y in range(self.height)]

    def read_spectra(self):
        return [list(self.grid[self.width - 1][y].coeffs) for y in range(self.height)]

    def mean_entropy(self):
        return sum(n.entropy for col in self.grid for n in col) / (self.width * self.height)


# =============================================================================
# TEST SUITE (mirrors the C# Main, plus Test 0)
# =============================================================================

def f(v):
    return f"{'+' if v >= 0 else ''}{v:.4f}"


def run():
    results = {}
    print("=" * 62)
    print("  OCTAHEDRAL RESONANCE NODE + LATTICE  (Python port)")
    print("  64 parameters: 24 (TetA) + 16 (shared vertex) + 24 (TetB)")
    print("=" * 62)

    # ---------------------------------------------------------------
    # TEST 0: the node as analyser. A full truth table on the 8 corners,
    # decomposed by the node's own H, gives the Walsh coefficients exactly.
    # ---------------------------------------------------------------
    print("\nTEST 0: Analyser mode, all 256 three-input functions")
    exact = 0
    for bits in range(256):
        truth = [1 - 2 * ((bits >> k) & 1) for k in range(N)]
        coeffs = [sum(H[k][c] * truth[k] for k in range(N)) / N for c in range(N)]
        rebuilt = [sum(H[k][c] * coeffs[c] for c in range(N)) for k in range(N)]
        exact += all(abs(rebuilt[k] - truth[k]) < 1e-12 for k in range(N))
    print(f"  truth table -> 8 Walsh coefficients -> truth table: {exact}/256 exact")
    results["analyser 256"] = (exact, 256)

    xor_in = [(-1, -1), (-1, +1), (+1, -1), (+1, +1)]
    xor_exp = [-1, +1, +1, -1]

    print("\nTEST 1: XOR (2-input, single tick)")
    ok = 0
    for i in range(4):
        node = OctahedralNode(0); node.inject(xor_in[i]); node.tick()
        xy = node.coeffs[4]; pred = -sign(xy)
        ok += pred == xor_exp[i]
        print(f"  {xor_in[i]} xy={f(xy)} pred={pred:+d} {'PASS' if pred == xor_exp[i] else 'FAIL'}")
    print(f"  XOR: {ok}/4"); results["XOR single tick"] = (ok, 4)

    p3_in = [(a, b, c) for a in (-1, 1) for b in (-1, 1) for c in (-1, 1)]
    p3_exp = [a * b * c for a, b, c in p3_in]

    print("\nTEST 2: 3-bit parity (grade-3 readout, single tick)")
    ok = 0
    for i in range(8):
        node = OctahedralNode(0); node.inject(p3_in[i]); node.tick()
        xyz = node.coeffs[7]; pred = sign(xyz)
        ok += pred == p3_exp[i]
        print(f"  {p3_in[i]} xyz={f(xyz)} pred={pred:+d} exp={p3_exp[i]:+d} {'PASS' if pred == p3_exp[i] else 'FAIL'}")
    print(f"  3-bit parity: {ok}/8"); results["3-bit parity single tick"] = (ok, 8)

    print("\nTEST 3: 3-bit parity over repeated cycles")
    for nc in (1, 5, 10, 25, 50, 100):
        ok = 0
        for i in range(8):
            node = OctahedralNode(0)
            for _ in range(nc):
                node.inject(p3_in[i]); node.tick()
            ok += sign(node.coeffs[7]) == p3_exp[i]
        print(f"  {nc:3d} cycles: {ok}/8 parity correct")
        results[f"parity {nc} cycles"] = (ok, 8)

    print("\nTEST 3b: The standing wave, read over one period")
    print("  closure bounded by mu(x)=x/(x+1); readout = Walsh coefficients averaged over the last period")
    period = int(round(2 * math.pi / 0.1))
    for nc in (1, 10, 100, 1000):
        ok_par = ok_xor = 0
        for i in range(8):
            node = OctahedralNode(0, standing=True); acc = 0.0; avg = min(period, nc)
            for t in range(nc):
                node.inject(p3_in[i]); node.tick()
                if t >= nc - avg:
                    acc += node.coeffs[7]
            ok_par += sign(acc) == p3_exp[i]
        for i in range(4):
            node = OctahedralNode(0, standing=True); acc = 0.0; avg = min(period, nc)
            for t in range(nc):
                node.inject(xor_in[i]); node.tick()
                if t >= nc - avg:
                    acc += node.coeffs[4]
            ok_xor += -sign(acc) == xor_exp[i]
        print(f"  {nc:4d} cycles: parity {ok_par}/8, XOR {ok_xor}/4   (amplitude settles at {node.amp_a[0]:.3f})")
        results[f"standing parity {nc} cycles"] = (ok_par, 8)
        results[f"standing XOR {nc} cycles"] = (ok_xor, 4)
    node = OctahedralNode(0)
    clips = 0
    for t in range(1000):
        node.inject(p3_in[7]); node.tick()
        clips += any(abs(v) >= 50 for v in node.forward_mix + node.backward_mix)
    print(f"  original closure rule, 1000 cycles: amplitude {node.amp_a[0]:.2f}, coupling_out {node.coupling_out[0]:.2f}, "
          f"clipped on {clips} of 1000 cycles")
    results["original rule clipped cycles"] = (clips, 1000)

    print("\nTEST 4: All 16 two-input Boolean functions (single tick)")
    fnames = ["FALSE", "AND", "A>B", "A", "B>A", "B", "XOR", "OR",
              "NOR", "XNOR", "!B", "A>=B", "!A", "B>=A", "NAND", "TRUE"]
    tt16 = [[-1, -1, -1, -1], [-1, -1, -1, +1], [-1, -1, +1, -1], [-1, -1, +1, +1],
            [-1, +1, -1, -1], [-1, +1, -1, +1], [-1, +1, +1, -1], [-1, +1, +1, +1],
            [+1, -1, -1, -1], [+1, -1, -1, +1], [+1, -1, +1, -1], [+1, -1, +1, +1],
            [+1, +1, -1, -1], [+1, +1, -1, +1], [+1, +1, +1, -1], [+1, +1, +1, +1]]
    H4 = [[1, -1, -1, +1], [1, -1, +1, -1], [1, +1, -1, -1], [1, +1, +1, +1]]
    total = 0
    for fi in range(16):
        truth = tt16[fi]
        hc = [sum(H4[j][c] * truth[j] for j in range(4)) / 4.0 for c in range(4)]
        fc = 0
        for j in range(4):
            node = OctahedralNode(0); node.inject(xor_in[j]); node.tick()
            dec = hc[0] * node.coeffs[0] + hc[1] * node.coeffs[1] + hc[2] * node.coeffs[2] + hc[3] * node.coeffs[4]
            fc += sign(dec) == truth[j]
        total += fc
        needs = "nonlin" if hc[3] != 0 else ("linear" if hc[1] or hc[2] else "const ")
        print(f"  {fnames[fi]:<5} [{needs}]: {fc}/4  h=({hc[0]:.1f},{hc[1]:.1f},{hc[2]:.1f},{hc[3]:.1f})")
    print(f"  Total: {total}/64"); results["16 gates single tick"] = (total, 64)

    print("\nTEST 5: Full adder (sum from grade 3, carry from grade 1)")
    s_ok = c_ok = 0
    for i in range(8):
        node = OctahedralNode(0); node.inject(p3_in[i]); node.tick()
        a, b, c = p3_in[i]
        bits = [(a > 0), (b > 0), (c > 0)]
        s_exp = 1 if sum(bits) % 2 else -1
        c_exp = 1 if sum(bits) >= 2 else -1
        s_ok += sign(node.coeffs[7]) == s_exp
        c_ok += sign(node.coeffs[1] + node.coeffs[2] + node.coeffs[3]) == c_exp
    print(f"  Sum: {s_ok}/8  Carry: {c_ok}/8")
    results["full adder sum"] = (s_ok, 8); results["full adder carry"] = (c_ok, 8)

    print("\nTEST 6: Vertex gain sweep (single tick)")
    print("    gain | parity | xor(xy)")
    gain_rows = []
    for g in (0.01, 0.05, 0.1, 0.15, 0.2, 0.3, 0.5, 0.8, 1.0, 1.5, 2.0):
        par = xr = 0
        for i in range(8):
            node = OctahedralNode(0); node.vertex_gain = g; node.inject(p3_in[i]); node.tick()
            par += sign(node.coeffs[7]) == p3_exp[i]
        for i in range(4):
            node = OctahedralNode(0); node.vertex_gain = g; node.inject(xor_in[i]); node.tick()
            xr += -sign(node.coeffs[4]) == xor_exp[i]
        gain_rows.append((g, par, xr))
        print(f"  {g:6.2f} |  {par}/8  |  {xr}/4")

    print("\nTEST 7: Full spectrum for input (+1,-1,+1)")
    node = OctahedralNode(0); node.inject((+1, -1, +1)); node.tick()
    names = ["const", "x", "y", "z", "xy", "xz", "yz", "xyz"]; grades = [0, 1, 1, 1, 2, 2, 2, 3]
    for c in range(N):
        print(f"    g{grades[c]} {names[c]:>5}: {f(node.coeffs[c])}  [{'even' if grades[c] % 2 == 0 else 'odd '}]")
    print(f"  mu={node.mu:.4f}  omega={node.omega:.4f}  entropy={node.entropy:.4f}")

    print("\nTEST 8: Lattice wiring (6 x 4)")
    lat = OctahedralLattice(6, 4)
    counts = {}
    for col in lat.grid:
        for n in col:
            counts[len(n.pair_links)] = counts.get(len(n.pair_links), 0) + 1
    print(f"  links per node -> count: {dict(sorted(counts.items()))}  (24 nodes, {24 * 64} parameters)")

    print("\nTEST 10: XOR through a 4 x 2 lattice (30 ticks)")
    ok = 0
    for i in range(4):
        lat = OctahedralLattice(4, 2)
        a, b = xor_in[i]
        for _ in range(30):
            for row in range(2):
                lat.set_input(row, (a, b, 0))
            lat.tick()
        xy = lat.read_spectra()[0][4]
        ok += -sign(xy) == xor_exp[i]
        print(f"  A={a:+d} B={b:+d} XOR={xor_exp[i]:+d}  xy={f(xy)}  {'PASS' if -sign(xy) == xor_exp[i] else 'FAIL'}")
    print(f"  XOR through lattice: {ok}/4"); results["XOR lattice 4x2"] = (ok, 4)

    print("\nTEST 11: XOR across lattice sizes (ticks = width + 3)")
    for w, h in ((2, 2), (3, 2), (4, 2), (6, 2), (4, 4), (8, 4), (10, 4)):
        ok = 0
        for i in range(4):
            lat = OctahedralLattice(w, h)
            a, b = xor_in[i]
            for _ in range(w + 3):
                for row in range(h):
                    lat.set_input(row, (a, b, 0))
                lat.tick()
            ok += -sign(lat.read_spectra()[0][4]) == xor_exp[i]
        print(f"  {w}x{h:<2} | {w + 3:3d} ticks | {ok}/4 | {w * h * 64} params")
        results[f"XOR lattice {w}x{h}"] = (ok, 4)

    print("\n" + "=" * 62)
    print("  SUMMARY")
    print("=" * 62)
    for k, (a, b) in results.items():
        print(f"  {k:<28} {a}/{b}")
    return results, gain_rows


if __name__ == "__main__":
    run()
