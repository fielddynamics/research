# GFD Oscillator — Working Release

**Three primitives. Three universal kernels. Three jobs.**

`kuramoto-model` `ising-model` `qubo` `walsh-hadamard-transform` `boolean-functions` `optimization`

This package contains the verified working implementations of:

1. **GFD Oscillator** — universal coupling-matrix optimizer (Ising / QUBO ground-state search).
2. **Walsh bridge primitives** — Walsh-Hadamard transforms, composition rules, character algebra.
3. **π-walk Walsh recovery** — deterministic harmonic decomposition of truth tables, machine-precision-exact on all 256 three-input Boolean functions.

For the engineering synthesis with theory, mechanism, and architectural picture, see [`docs/SYNTHESIS.md`](docs/SYNTHESIS.md).

---

## What's in the box

```
src/
  bridge.py           Walsh primitives + composition rules + 8-test self-check
  gfd_oscillator.py   Kuramoto-based universal eigensolver / Ising ground-state finder
  walsh_recovery.py   π-walk Walsh recovery for 8-cell (3-input) functions

tests/
  test_oscillator_mechanics.py     10 tests demonstrating oscillator mechanics
  test_walsh_recovery.py            Standard-gate π-walk tests
  test_walsh_recovery_hard.py       12 hard tests: 256 3-input functions + Parseval + linearity + ...
  test_walsh_recovery_16cell.py     10 hard tests: 16-cell recovery, including bent function exact
  test_hopfield.py                  Hopfield associative memory — discrete + oscillator (ω=0)
  test_hopfield_bit_closure.py      Bit-level field closure — round 2 corrects round 1's mistakes
  test_hopfield_gauge.py            Diagnostic: gauge-vs-success in Hopfield retrieval
  test_hopfield_iterate.py          Iteration variants: state, K-update, voting, hybrid
  test_hopfield_restarts.py         Restart + tracking experiment for basin-edge regime
  mini_word_embedding.py            Toy unsupervised word embedding (~30 words)
  ontology_learner.py               100-fact ontology learner with online learning
  ontology_learner_large.py         272-fact, 115-entity ontology with multi-hop queries

docs/
  SYNTHESIS.md        Full engineering synthesis
```

---

## Quick start

```bash
# Walsh primitives self-check
cd src && python3 bridge.py

# All 256 three-input Boolean functions, machine-precision recovery (8 cells)
cd tests && python3 test_walsh_recovery_hard.py

# 16-cell recovery — 4-input functions, including bent
cd tests && python3 test_walsh_recovery_16cell.py

# Hopfield retrieval — discrete and oscillator-based
cd tests && python3 test_hopfield.py

# Bit-level field closure — round 2 corrects round 1
cd tests && python3 test_hopfield_bit_closure.py

# Unsupervised ontology learning, 115 entities
cd tests && python3 ontology_learner_large.py

# Oscillator mechanics — 10 tests building intuition from 2 nodes upward
cd tests && python3 test_oscillator_mechanics.py
```

Expected outputs:
- `bridge.py self-test: all 8 checks pass.`
- `12/12 tests passed` (8-cell Walsh recovery hard battery)
- `10/10 tests passed` (16-cell Walsh recovery, bent function exact)
- 10 demonstrations of attract/repel, frustration, depth gauge, etc.

---

## The 30-second pitch

**Spectral processor** (separate codebase) is the *forward* primitive:
load a Walsh bridge `B`, give it input bits, it evaluates `f(x)`. Universal Boolean function evaluator.

**GFD oscillator** (this codebase) is the *search* primitive:
load a coupling matrix `K`, run Kuramoto dynamics, read the SVD coordinates. Universal Ising/QUBO ground-state finder.

**π-walk + Hadamard** is the *recovery* primitive:
sample a truth table along the base-8 π address pattern, run a Hadamard transform, get the Walsh bridge. Universal Boolean function spectral analyzer.

Together: forward evaluation + combinatorial search + spectral analysis, all on one analog chip family, all with one kernel apiece.

---

## What's verified, what isn't

**Verified at machine precision in this release:**
- All 256 three-input Boolean functions recovered exactly via π-walk (8-cell bridges)
- 16,384 of 65,536 four-input Boolean functions recovered exactly (16-cell bridges, including bent)
- Parseval (`Σ B[c]² = 1`) holds for all sampled 8-cell and 16-cell functions
- Linearity, round-trip identity, sparse/dense recovery
- Oscillator mechanics: 10/10 mechanical demonstrations (attract, repel, frustration, locking, gauge)
- Coverage thresholds: step 21 for 8 cells, step 37 for 16 cells (sharp 0 → exact transitions at both)
- **Hopfield retrieval (associative memory): 45/45 on 3-pattern N=32 test via oscillator (ω=0); matches or beats discrete Hopfield on hard corruption regimes**
- **Bit-level field closure: ~13 percentage point gain in basin-edge regime over single-shot retrieval**
- **Unsupervised ontology learning: 115-entity ontology with abstract-attribute discovery (predator clusters with eagle/hawk/lion), online learning of new entities (squirrel/falcon/camel placed correctly without retraining)**

**Honest limits:**
- Oscillator with `K = B⊗B` recovers bridge sign patterns exactly but flattens magnitudes for non-uniform bridges. Use the π-walk + Hadamard primitive for full bridge recovery with magnitudes.
- Bent / maximally-degenerate-spectrum cases require either depth ≥ N in the oscillator, or the π-walk primitive.
- TSP encoding degrades above N ≈ 30.
- The oscillator covers the classical (symmetric/standard) sector of K-particle Heisenberg representation theory; the entangled (hook) sector is outside its reach.

For the full discussion see `docs/SYNTHESIS.md` §9.

---

## License

Code: MIT.
Documentation: CC BY 4.0.

Stephen Nelson / Field Dynamics Research / 2026.
