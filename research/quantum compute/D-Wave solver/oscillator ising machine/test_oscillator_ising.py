"""Correctness tests for the oscillator Ising sampler.
Run: python test_oscillator_ising.py      (prints PASS/FAIL per check)"""
import itertools
import warnings
import numpy as np
import networkx as nx
import dimod
from oscillator_ising import OscillatorIsingSampler, continuous_energy, phases_of

warnings.filterwarnings("ignore", category=DeprecationWarning)
import dwave_networkx as dnx

ok = []
def check(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

S = OscillatorIsingSampler()
rng = np.random.default_rng(0)

def random_bqm(n, seed, field=True):
    g = nx.random_regular_graph(3, n, seed=seed); r = np.random.default_rng(seed)
    J = {e: float(r.choice([-1, 1])) for e in g.edges()}
    h = {i: float(r.choice([-0.5, 0.5])) if field else 0.0 for i in range(n)}
    return dimod.BQM.from_ising(h, J)

# ---- the continuous energy is the Ising energy on locked phases
good = True
for seed in range(20):
    bqm = random_bqm(12, seed)
    s = dict(zip(range(12), rng.choice([-1, 1], 12)))
    good &= np.isclose(continuous_energy(bqm, {v: 0.0 if x > 0 else np.pi for v, x in s.items()}), bqm.energy(s))
check("H(phi) equals the Ising energy whenever every phase is 0 or pi (20 random models)", good)

# ---- the noiseless dynamics descend H (gradient flow), checked on the engine itself
bqm = random_bqm(40, 3)
H = [continuous_energy(bqm, phases_of(S.sample(bqm, num_reads=1, steps=k, dt=0.01, ks_max=0.0, noise=0.0, seed=5)))
     for k in range(0, 2001, 100)]
check("with no noise and no locking, H never increases along the run (21 checkpoints)",
      all(b <= a + 1e-9 for a, b in zip(H, H[1:])) and H[-1] < H[0])

# ---- second-harmonic locking drives every phase to 0 or pi
ph = S.sample(random_bqm(60, 4), num_reads=5, steps=6000, noise=0.0, seed=1).info["phases"]
dist = np.minimum(np.abs(np.sin(ph)), 1.0)
check(f"locking drives every phase to 0 or pi (max |sin phi| = {dist.max():.1e})", dist.max() < 1e-2)

# ---- sign conventions
one = lambda h: S.sample(dimod.BQM.from_ising({0: h}, {}), num_reads=3, seed=0).first.sample[0]
check("a single spin with field h = +1 settles at s = -1, and with h = -1 at s = +1", one(1.0) == -1 and one(-1.0) == 1)
chain = dimod.BQM.from_ising({}, {(i, i + 1): -1.0 for i in range(9)})
fm = S.sample(chain, num_reads=5, seed=0).first
check("a ferromagnetic chain (J = -1) aligns, energy -9", np.isclose(fm.energy, -9))
afm = dimod.BQM.from_ising({}, {(i, i + 1): +1.0 for i in range(9)})
check("an antiferromagnetic chain (J = +1) alternates, energy -9", np.isclose(S.sample(afm, num_reads=5, seed=0).first.energy, -9))

# ---- exact ground states with fields
hits = 0
for seed in range(10):
    bqm = random_bqm(14, 100 + seed)
    hits += np.isclose(S.sample(bqm, num_reads=20, steps=4000, seed=seed).first.energy,
                       dimod.ExactSolver().sample(bqm).first.energy)
check(f"finds the exact ground state of 14-spin glasses with fields ({hits}/10)", hits == 10)

# ---- dimod interface
qubo = dimod.BQM.from_qubo({(0, 0): -1, (1, 1): -1, (2, 2): -1, (0, 1): 2, (1, 2): 2, (0, 2): 2})
ss = S.sample(qubo, num_reads=8, seed=0)
check("QUBO in, QUBO out: vartype BINARY, values in {0, 1}, ground energy -1",
      ss.vartype is dimod.BINARY and set(np.unique(ss.record.sample)) <= {0, 1} and np.isclose(ss.first.energy, -1))
dimod.testing.assert_sampleset_energies(ss, qubo)
labelled = dimod.BQM.from_ising({"a": 0.5}, {("a", "b"): -1.0, ("b", "c"): 1.0})
ls = S.sample(labelled, num_reads=4, seed=0)
dimod.testing.assert_sampleset_energies(ls, labelled)
check("reported energies match the model, for integer and string variable labels",
      set(ls.variables) == {"a", "b", "c"} and np.isclose(ls.first.energy, dimod.ExactSolver().sample(labelled).first.energy))
check("an empty model returns an empty sample set", len(S.sample(dimod.BQM(dimod.SPIN))) == 0)

# ---- plugs into D-Wave's own problem library
G = nx.petersen_graph()
cut = dnx.maximum_cut(G, S, num_reads=20, seed=0)
cut_size = sum((u in cut) != (v in cut) for u, v in G.edges())
best = max(sum((u in c) != (v in c) for u, v in G.edges())
           for r in range(11) for c in map(set, itertools.combinations(G.nodes, r)))
check(f"dwave_networkx.maximum_cut with this sampler finds the optimal cut of the Petersen graph ({cut_size}/{best})", cut_size == best)
col = dnx.min_vertex_color(nx.cycle_graph(5), S, num_reads=20, seed=0)
check("dwave_networkx.min_vertex_color with this sampler 3-colours the 5-cycle validly",
      all(col[u] != col[v] for u, v in nx.cycle_graph(5).edges()) and len(set(col.values())) == 3)

print(f"\n{sum(ok)}/{len(ok)} checks passed")
