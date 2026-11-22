# The Mountain Scale in the SST: the Net-Field Rule From the Action

*Writing "read the law at the mountain's scale" into the action · Gravity Field Dynamics (GFD) · Field Dynamics Research*

[![Lean proof](https://github.com/fielddynamics/research/actions/workflows/lean-sst-mountain-scale.yml/badge.svg)](https://github.com/fielddynamics/research/actions/workflows/lean-sst-mountain-scale.yml)

`SST` `net-field-rule` `mountain-scale` `Jacobi-radius` `projector` `preferred-foliation` `action` `proof`

---

This folder holds a three-page proof, a script that checks it (17 checks), a 3D numerical solution, and a Lean 4 formalisation (3 theorems). It closes the step that the [time-leg](../sst-covariant-time-leg/), [net-field rule](../net-field-rule/) and [khronon](../sst-khronon-preferred-frame/) proofs all left open.

## The picture

A mountain stream looks flat close up; zoomed out, it runs down a mountain.

- **Inside a bound system** the host's field is a flat slope, and each body is a dimple with **no drain**: pure TetA.
- **Seen from outside**, the whole mountain shows, and the law acts on it.
- **The views meet at the Jacobi radius**, where the dimple stops standing out against the tide.

## What was open

The action applied the law wherever the time leg accelerates, including around the Sun. That gives every star a tail (a pull of a₀ on every planet), which is excluded. The net-field rule removed the tail by reading the law on the galaxy's coarse-grained field, but that was a rule added on top of the action.

## What this proof does

1. **It writes the mountain scale into the action.** The SST has a preferred foliation, a preferred "now", so on each slice of space there is a natural projector P onto modes longer than the mountain scale ℓ. It is defined from the slice's own geometry, so it respects the theory's symmetry. The action reads:
   - the **curvature term** (all of Newton and Einstein) at every point;
   - the **law's term** (the TetB share) on the mountain, P Φ.
2. **The field equation then splits exactly:**
   - **the dimple** obeys plain Poisson, ∇²(Φ − PΦ) = 4πG(1 − P)ρ: linear, bare G, pure TetA, and **the same whatever the law is**;
   - **the mountain** obeys the law at the mountain's scale, P∇·[μ∇PΦ] = 4πG Pρ.

   This is the net-field rule's split, now **derived** from the action instead of assumed.
3. **What follows:**
   - no tail;
   - γ = 1, with lensing unchanged;
   - galaxies unchanged;
   - the preferred frame has nothing inside a star system (the khronon proof's Theorem 6, now derived).
4. **The data fix the scale: each bound system's own Jacobi radius.**

   | System | Size | Its Jacobi radius | Result |
   |---|---|---|---|
   | Sun | planets out to ~0.0005 pc | 1.44 pc | dimple: pure TetA |
   | Pal 14 | 26 pc | ~160 pc | dimple: bare G, as its dispersion requires |
   | Pal 4 | 18 pc | ~270 pc | dimple: bare G |

   A single universal length fails: at the Sun's 1.4 pc, Pal 14's body would be read through the law. In its external-field regime that is G → G/μ, which its dispersion excludes at 8.9σ. So every bound system has its own mountain scale, exactly as the picture says.

## The 3D check

A galaxy and a compact "Sun" were solved in a periodic box, both ways:

![The tail read pointwise, and no tail at the mountain's scale](fig_demo.png)

- **Read pointwise**, the extra pull around the Sun is the tail, matching a₀μ(x) to 3%.
- **Read at the mountain's scale**, it is small and fades toward the Sun: only the smoothed sheet and the tide.
- The dimple equals plain Newton for (1 − P)ρ to 2 × 10⁻¹⁵.
- The galaxy's own field is unchanged once ℓ is small against it: 4 × 10⁻², 3 × 10⁻³ and 2 × 10⁻⁴ for ℓ at 2, 1 and ½ of the galaxy's width. In the Milky Way, ℓ/R ≈ 2 × 10⁻⁴.

## What it leaves open

- **Why the edge follows the tide.** The Jacobi radius comes from the picture and is confirmed by the data; it is not derived from a deeper principle.
- **The edges between systems.** P is exact within each system. At a Jacobi surface, where the scale changes, the departure is bounded by the tide (7 × 10⁻¹⁴ m/s² for the Sun), not shown to be zero.
- **Time-dependent binding**, in mergers and tidal stripping.
- **Curved slices.** P commutes with the slice's Laplacian exactly, and with the gradient to O(Φ/c²).

## Contents

| File | What it is |
|---|---|
| [`sst_mountain_scale.pdf`](sst_mountain_scale.pdf) | The proof (3 pages) |
| [`sst_mountain_scale.tex`](sst_mountain_scale.tex) | LaTeX source (IOP class, [`iopjournal.cls`](iopjournal.cls)) |
| [`verify_sst_mountain_scale.py`](verify_sst_mountain_scale.py) | 17 checks: the split in 1D (exact linear algebra, two laws), the projector on a curved slice, the numbers, and the 3D results |
| [`verify_output.txt`](verify_output.txt) | Its output |
| [`demo_mountain_scale.py`](demo_mountain_scale.py), [`demo_output.txt`](demo_output.txt) | The 3D solution (about 5 minutes) |
| [`galaxy_scaling.py`](galaxy_scaling.py), [`galaxy_scaling_output.txt`](galaxy_scaling_output.txt) | The galaxy's field against ℓ (about 5 minutes) |
| [`make_figure.py`](make_figure.py) | Draws [`fig_demo`](fig_demo.pdf) |
| [`lean/MountainScale.lean`](lean/MountainScale.lean) | Lean 4, 3 theorems, importing the [khronon](../sst-khronon-preferred-frame/lean/) formalisation |
| [`LEAN_AUDIT.md`](LEAN_AUDIT.md) | What the Lean proves and what is cited |

## Running the checks

```
python demo_mountain_scale.py > demo_output.txt
python galaxy_scaling.py > galaxy_scaling_output.txt
python verify_sst_mountain_scale.py
cd lean && lake exe cache get && lake build
```
