"""
D-Wave-style benchmark for the oscillator Ising sampler.

Instance sets
  A. 16-spin glasses with fields on random 3-regular graphs; exact ground states (dimod.ExactSolver).
  B. Planted-solution frustrated-loop problems on D-Wave's own qubit graphs, Chimera C(4) (128 spins)
     and Pegasus P(4) (264 spins); the planted state is a ground state by construction.
  C. 500-spin +-J glasses on random 3-regular graphs, without and with fields h = +-0.5; reference is the
     best energy found by any solver or by a long simulated-annealing run (1000 reads x 5000 sweeps).

Solvers (20 reads each)
  GFD oscillator (original)   ../gfd_oscillator.py, K = -J, best sign readout of the SVD modes per run.
                              It has no field input, so fields are dropped; energy is scored on the true model.
  Oscillator Ising sampler    oscillator_ising.py, default schedule (8000 steps).
  D-Wave SA                   dwave.samplers.SimulatedAnnealingSampler, default schedule (1000 sweeps).
  D-Wave tabu                 dwave.samplers.TabuSampler, default settings.
  Steepest descent            dwave.samplers.SteepestDescentSolver from random starts (a floor).

Metrics
  p(GS)   fraction of reads that reach the ground state (A, B)
  TTS99   time per read x ln(0.01) / ln(1 - p): CPU time to reach the ground state with 99% confidence
  gap     energy above the reference, best read and mean read (C)

CPU times compare software implementations on this machine. They say nothing about analog hardware.

Run: python benchmark.py            (writes RESULTS.md; about 10 minutes)
"""
import os
import sys
import time
import warnings
import numpy as np
import networkx as nx
import dimod
from dimod.generators import frustrated_loop
from dwave.samplers import SimulatedAnnealingSampler, TabuSampler, SteepestDescentSolver

warnings.filterwarnings("ignore", category=DeprecationWarning)
import dwave_networkx as dnx

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
from oscillator_ising import OscillatorIsingSampler
from gfd_oscillator import GFDOscillator

READS = 20


class OriginalGFDSampler(dimod.Sampler):
    """The original engine as a dimod sampler: one read = one run_phase at depth 4, best SVD-sign readout."""
    parameters = {"num_reads": [], "seed": []}
    properties = {}

    def sample(self, bqm, num_reads=10, seed=0, **kw):
        spin = bqm.change_vartype(dimod.SPIN, inplace=False)
        labels = list(spin.variables); idx = {v: k for k, v in enumerate(labels)}; n = len(labels)
        K = np.zeros((n, n))
        for (u, v), J in spin.quadratic.items():
            K[idx[u], idx[v]] = K[idx[v], idx[u]] = -J
        osc = GFDOscillator(dt=0.01, steps=4000); g = osc.encode_weighted(n, K)
        out = []
        for r in range(num_reads):
            st = osc.run_phase(g, depth=4, seed=seed + 100 * r)
            cands = [np.where(sg * st.Vt[m] > 0, 1, -1) for m in range(min(st.n_active, 4)) for sg in (1, -1)]
            out.append(min(cands, key=lambda s: spin.energy(dict(zip(labels, s)))))
        return dimod.SampleSet.from_samples_bqm((np.array(out), labels), spin).change_vartype(bqm.vartype)


class RandomStartDescent(dimod.Sampler):
    parameters = {"num_reads": [], "seed": []}
    properties = {}

    def sample(self, bqm, num_reads=10, seed=0, **kw):
        rng = np.random.default_rng(seed); labels = list(bqm.variables)
        init = dimod.SampleSet.from_samples_bqm((rng.choice([-1, 1], (num_reads, len(labels))), labels), bqm)
        return SteepestDescentSolver().sample(bqm, initial_states=init)


SOLVERS = [("GFD oscillator (original)", OriginalGFDSampler()),
           ("Oscillator Ising sampler", OscillatorIsingSampler()),
           ("D-Wave SA", SimulatedAnnealingSampler()),
           ("D-Wave tabu", TabuSampler()),
           ("Steepest descent", RandomStartDescent())]


def run(sampler, bqm, seed):
    t = time.time(); ss = sampler.sample(bqm, num_reads=READS, seed=seed)
    return ss.record.energy, (time.time() - t) / READS


def tts99(p, t_read):
    if p >= 1.0: return t_read
    if p <= 0.0: return float("inf")
    return t_read * np.log(0.01) / np.log(1.0 - p)


def fmt_t(t):
    return "never" if not np.isfinite(t) else (f"{t * 1e3:.0f} ms" if t < 1 else f"{t:.1f} s")


def spin_glass(n, seed, field):
    g = nx.random_regular_graph(3, n, seed=seed); r = np.random.default_rng(seed)
    return dimod.BQM.from_ising({i: float(r.choice([-0.5, 0.5])) if field else 0.0 for i in range(n)},
                                {e: float(r.choice([-1, 1])) for e in g.edges()})


def planted(graph, seed):
    r = np.random.default_rng(seed); plant = {v: int(r.choice([-1, 1])) for v in graph.nodes}
    bqm = frustrated_loop(graph, num_cycles=int(0.3 * graph.number_of_nodes()), planted_solution=plant, seed=seed)
    return bqm, bqm.energy(plant)


def ground_state_table(title, instances):
    """instances: list of (bqm, ground_energy). Returns markdown lines."""
    lines = [f"### {title}", "", "| Solver | p(GS) per read | instances solved | time per read | TTS99 |",
             "|---|---|---|---|---|"]
    for name, sampler in SOLVERS:
        ps, ts, solved = [], [], 0
        for k, (bqm, gs) in enumerate(instances):
            e, t = run(sampler, bqm, k)
            hit = np.isclose(e, gs); ps.append(hit.mean()); ts.append(t); solved += hit.any()
        p, t = float(np.mean(ps)), float(np.mean(ts))
        lines.append(f"| {name} | {p:.2f} | {solved}/{len(instances)} | {fmt_t(t)} | {fmt_t(tts99(p, t))} |")
        print(lines[-1], flush=True)
    return lines + [""]


def gap_table(title, bqms):
    lines = [f"### {title}", "", "| Solver | gap, best read | gap, mean read | time per read |", "|---|---|---|---|"]
    results = {name: [run(s, b, k) for k, b in enumerate(bqms)] for name, s in SOLVERS}
    refs = [min(SimulatedAnnealingSampler().sample(b, num_reads=1000, num_sweeps=5000, seed=k).first.energy,
                *(results[name][k][0].min() for name, _ in SOLVERS)) for k, b in enumerate(bqms)]
    for name, _ in SOLVERS:
        best = np.mean([r[0].min() - ref for r, ref in zip(results[name], refs)])
        mean = np.mean([r[0].mean() - ref for r, ref in zip(results[name], refs)])
        t = np.mean([r[1] for r in results[name]])
        lines.append(f"| {name} | +{best:.1f} | +{mean:.1f} | {fmt_t(t)} |")
        print(lines[-1], flush=True)
    return lines + [""]


if __name__ == "__main__":
    t0 = time.time()
    out = ["# Benchmark results", "",
           f"Generated by `benchmark.py`, {READS} reads per solver per instance. "
           "CPU times are software on one machine and say nothing about analog hardware.", ""]
    A = [(b, dimod.ExactSolver().sample(b).first.energy) for b in (spin_glass(16, 200 + s, True) for s in range(20))]
    out += ground_state_table("A. 16-spin glasses with fields, exact ground states (20 instances)", A)
    for gname, G in (("Chimera C(4), 128 spins", dnx.chimera_graph(4)), ("Pegasus P(4), 264 spins", dnx.pegasus_graph(4))):
        out += ground_state_table(f"B. Planted frustrated loops on {gname} (5 instances)", [planted(G, s) for s in range(5)])
    for field in (False, True):
        out += gap_table(f"C. 500-spin glasses, fields {'h = +-0.5' if field else 'off'} (3 instances); "
                         "energy above the best known solution", [spin_glass(500, 300 + s, field) for s in range(3)])
    out.append(f"Total run time {time.time() - t0:.0f} s.")
    open(os.path.join(HERE, "RESULTS.md"), "w").write("\n".join(out) + "\n")
    print("\nwrote RESULTS.md")
