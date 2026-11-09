# Oscillator Ising Machine

*The GFD oscillator as a solver for D-Wave-class problems · Gravity Field Dynamics (GFD) · Field Dynamics Research*

`ising-model` `qubo` `oscillator-ising-machine` `kuramoto-model` `combinatorial-optimization` `d-wave` `dimod` `benchmark`

---

D-Wave's quantum annealers solve **Ising problems**: find spins $s_i = \pm 1$ that minimise

$$E(s) = \sum_i h_i s_i + \sum_{i<j} J_{ij} s_i s_j ,$$

with local fields $h_i$ and couplings $J_{ij}$. The same problems written in 0/1 variables are called QUBOs. Max-Cut, graph colouring, the travelling salesperson problem, scheduling and many others can all be written this way, which is why the format matters.

This folder turns the GFD oscillator into a solver for exactly these problems. It takes any problem in D-Wave's own format, returns answers in D-Wave's own format, and is benchmarked against D-Wave's own classical solvers on the kinds of instances D-Wave publishes results on. Everything here runs in software; nothing runs on D-Wave hardware.

## What changed from the original oscillator

The [original solver](../) couples oscillators with the Kuramoto law and reads answers from an SVD of the settled phases. Three things stop it from being a general Ising solver:

| Gap | Consequence |
|---|---|
| No input for the fields $h_i$ | Most D-Wave problems cannot be posed to it at all |
| Phases never settle to two values | Spins are recovered indirectly, from the sign of SVD modes |
| No annealing schedule | It settles into the nearest good state, not the best |

The new sampler keeps the Kuramoto coupling and adds the three standard ingredients of an *oscillator Ising machine*:

- a **field term**, so every Ising problem can be posed;
- **second-harmonic locking**, which pulls each phase to 0 or $\pi$, so each oscillator *is* a spin;
- an **annealing schedule**: noise that fades and locking that grows over the run.

Each oscillator's phase $\phi_i$ follows gradient flow on

$$H(\phi) = \sum_i h_i \cos\phi_i + \sum_{i<j} J_{ij} \cos(\phi_i - \phi_j) - \frac{k_s}{2} \sum_i \cos 2\phi_i ,$$

which equals the Ising energy exactly when every phase is 0 or $\pi$. The spin is read off as $s_i = \mathrm{sign}(\cos\phi_i)$.

## Using it

It is a standard D-Wave (dimod) sampler, so it drops in wherever a D-Wave sampler is used:

```python
import dimod, networkx as nx, dwave_networkx as dnx
from oscillator_ising import OscillatorIsingSampler

sampler = OscillatorIsingSampler()

# Any Ising problem, fields included
bqm = dimod.BQM.from_ising({0: 0.5, 1: -0.5}, {(0, 1): -1.0, (1, 2): 1.0})
print(sampler.sample(bqm, num_reads=20).first)

# Any QUBO
qubo = dimod.BQM.from_qubo({(0, 0): -1, (1, 1): -1, (0, 1): 2})
print(sampler.sample(qubo, num_reads=20).first)

# D-Wave's own problem library
cut = dnx.maximum_cut(nx.petersen_graph(), sampler, num_reads=20)
colours = dnx.min_vertex_color(nx.cycle_graph(5), sampler, num_reads=20)
```

Settings: `num_reads` (independent runs), `steps` (default 8000), `dt` (0.02), `ks_max` (final locking strength, 1.5), `noise` (starting noise, 1.0), `seed`.

## Is it correct?

`test_oscillator_ising.py` checks the engine itself, not only its answers (12/12):

- the continuous energy equals the Ising energy whenever every phase is 0 or $\pi$;
- without noise, the energy never rises during a run: the dynamics are a true gradient flow;
- the locking drives every phase to 0 or $\pi$, to within $10^{-13}$;
- fields push spins the right way, and ferromagnetic and antiferromagnetic chains order correctly;
- it finds the exact ground state of 14-spin glasses with fields, 10 out of 10;
- QUBO and Ising inputs, any variable labels, and reported energies all match D-Wave's conventions;
- it plugs into `dwave_networkx`: optimal Max-Cut of the Petersen graph, valid 3-colouring of the 5-cycle.

## What it achieves

`benchmark.py` compares five solvers, 20 reads each, on three kinds of instance. The full tables are in [`RESULTS.md`](RESULTS.md). The solvers are the original GFD oscillator, the new sampler, D-Wave's simulated annealing and tabu search, and steepest descent from random starts as a floor.

**Small spin glasses with fields, exact answers known (16 spins).** The new sampler reaches the ground state in 83% of runs, the same as D-Wave's simulated annealing (84%). The original oscillator reaches it in 47%, because it cannot see the fields.

**Large spin glasses (500 spins).** The new sampler's best run lands within 3–6 energy units of the best known solution, against 58–89 for the original oscillator. With fields on, it is close to D-Wave's tabu search (+3.3 against +2.0) and behind simulated annealing (+1.3).

**Planted problems on D-Wave's own chip graphs (Chimera, 128 spins; Pegasus, 264 spins).** These are built so the ground state is known, and they are the kind of instance D-Wave reports results on. Here the new sampler is weak: it reaches the ground state in 9% of runs on Chimera and 1% on Pegasus, against 62% and 71% for simulated annealing. Longer anneals and weaker locking raise the Chimera figure to 21%, so tuning helps, but there is a real gap still to close.

**Speed.** In software, the new sampler is roughly 30 to 50 times slower per run than D-Wave's simulated annealing, which is highly optimised compiled code. That comparison says little about the goal, which is hardware: an analog or FPGA oscillator network would integrate every spin at once. One run is 8000 steps of size 0.02, or 160 time units of the dynamics. On hardware, the time per run would be 160 × the network's coupling time constant: 160 µs at a 1 µs time constant, 160 ns at 1 ns. That is a projection, not a measurement; no hardware has been built.

## Summary

| | Original oscillator | Oscillator Ising sampler |
|---|---|---|
| Accepts any Ising or QUBO problem in D-Wave's format | No (no fields) | Yes |
| Exact ground states, 16 spins with fields | 47% of runs | 83% (D-Wave SA: 84%) |
| 500-spin glasses, best run above best known | +58 to +89 | +3 to +6 (SA: 0 to +1.3) |
| Planted problems on D-Wave chip graphs | 1–13% of runs | 1–9%, up to 21% tuned (SA: 62–71%) |

The new sampler is a working D-Wave-class solver, comparable to D-Wave's classical solvers on spin glasses and behind them on planted chip-graph problems.

## What comes next

1. **Close the gap on planted problems.** Tune the schedule per problem class, and try per-oscillator amplitude control and adaptive noise, which have helped other oscillator Ising machines.
2. **Measure scaling.** Time-to-solution as the number of spins grows, which is the figure D-Wave's results are judged on.
3. **Test the GFD elements directly.** Does the depth gauge predict which runs have found the ground state? Can the constitutive-law amplitude channel act as the per-oscillator amplitude control in step 1? If either helps, that is the distinctive GFD result. If not, the sampler stands as a standard oscillator Ising machine built on the GFD coupling.
4. **Hardware.** An FPGA implementation would turn the projection above into a measurement.

## Contents

| File | Contents |
|---|---|
| [`oscillator_ising.py`](oscillator_ising.py) | The sampler: a D-Wave (dimod) sampler for any Ising or QUBO problem |
| [`test_oscillator_ising.py`](test_oscillator_ising.py) | Correctness tests of the dynamics and the interface (12/12) |
| [`benchmark.py`](benchmark.py) | The D-Wave-style benchmark; writes `RESULTS.md` (about 8 minutes) |
| [`RESULTS.md`](RESULTS.md) | Full benchmark tables. "0 ms" there means under half a millisecond |

```bash
pip install numpy scipy networkx dimod dwave-samplers dwave-networkx
python test_oscillator_ising.py
python benchmark.py
```

Tested with dimod 0.12.23, dwave-samplers 1.8.0 and dwave-networkx 0.8.19. D-Wave is moving dwave-networkx into a new package, dwave-graphs; it still works but prints a deprecation notice.

---

*Stephen Nelson, Field Dynamics Research · MIT (code) / CC BY 4.0 (documentation)*
