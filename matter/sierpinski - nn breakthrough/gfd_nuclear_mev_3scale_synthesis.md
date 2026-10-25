# GFD Nuclear Binding Energy: Sierpiński Walk Decomposition

**Stephen Nelson · Field Dynamics · March 2026**
**Session Synthesis: From 256-dim walk vector to 3-scale MeV solve**

---

## Table of Contents

1. The Core Insight
2. The 256-Dimensional Walk Vector
3. The (3+1) Gate Structure
4. The Coupling Polynomial
5. Valence Shell Connection
6. The 3-Scale Decomposition (The Solve)
7. The Three Neural Networks
8. Results
9. The Universal Constants That Emerged
10. Files and Reproduction
11. What Comes Next

---

## 1. The Core Insight

Nuclear binding energy per nucleon (B/A in MeV) for all 83 stable elements can be decomposed into three contributions mapped onto a Sierpiński triangle — the fractal structure of the stellated octahedron.

The decomposition uses:
- A **256-dimensional binary fill vector** encoding mass number A
- Three projections of that vector at different scales (face, channel, subchannel)
- Three independent neural networks (4 hidden nodes each, 12 total)
- A fixed (3+1) gate exclusion at every level

Result: **R² = 0.9998, MAE = 0.9 keV/n, 77/77 elements within 0.5%**, reproducible across independent training runs with identical outputs.

---

## 2. The 256-Dimensional Walk Vector

### Construction

The stellated octahedron has 4 faces. Each face has 4 channels. Each channel has 4 subchannels. That's 4 × 4 × 4 = **64 positions per shell**.

The walk fills these positions in a fixed order defined by three nested loops:

```python
for face in [0, 1, 2, 3]:        # 4 faces
    for channel in [0, 1, 2, 3]:  # 4 channels per face
        for subchannel in [0, 1, 2, 3]:  # 4 subchannels per channel
            # position index = face*16 + channel*4 + subchannel
```

This produces walk positions 0 through 63. When all 64 are filled, the **shell closes** and the walk restarts at position 0 in the next shell.

With 4 possible shells, the full vector is **256 dimensions** (4 shells × 64 positions).

### Mapping mass number A to the vector

For an element with mass number A:

1. Compute `a64 = A mod 64` (if 0, set to 64)
2. Compute `n_complete = (A - a64) / 64` (number of complete shells)
3. Total filled positions = `n_complete × 64 + a64`
4. Vector: `v[i] = 1 if i < total_filled, else 0`

Example: Iron (Fe), A = 56
- a64 = 56, n_complete = 0
- 56 ones followed by 200 zeros
- Fills positions 0–55 in shell 0 (faces 0, 1, 2 complete + 8 positions into face 3)

Example: Bismuth (Bi), A = 209
- a64 = 17, n_complete = 3
- 209 ones followed by 47 zeros
- 3 complete shells + 17 positions into shell 3

### Why 256 and not 64?

The 64-dim vector (collapsing shells by summing) loses shell information. Elements at different shells but same a64 get identical vectors. The 256-dim preserves **which shell** each position was traversed in. This matters because later shells contribute less binding per nucleon (the B/A curve descends after Iron).

---

## 3. The (3+1) Gate Structure

### What is (3+1)?

In every group of 4 (faces, channels, subchannels), the first 3 are **spatial** and the 4th is the **gate** (the Sierpiński-excluded center). This is the fundamental structure of the stellated octahedron at every nesting level.

Visually on the Sierpiński triangle: three bright corners (spatial), one dark inverted center (gate).

### Gate Depth

Each of the 64 walk positions has a **gate depth** (gd) = how many of its indices are 3 (the gate index):

- **gd = 0**: face ∈ {0,1,2}, channel ∈ {0,1,2}, subchannel ∈ {0,1,2} → pure spatial
- **gd = 1**: exactly one index = 3 → one gate crossing
- **gd = 2**: exactly two indices = 3 → double gate (gate of gate)
- **gd = 3**: face=3, channel=3, subchannel=3 → triple gate (deepest center, position 63)

### Gate Depth Distribution

The counts follow the binomial expansion of (3+1)³:

| gd | Count | Formula | Role |
|----|-------|---------|------|
| 0  | **27** | 3³ | Spatial corners |
| 1  | **27** | 3 × 3² | Single gate crossings |
| 2  | **9**  | 3 × 3 | Double gate (face closures) |
| 3  | **1**  | 1 | Triple gate (total closure) |

27 + 27 + 9 + 1 = 64.

### Gate positions carry minimal binding energy

This was discovered empirically through the neural network analysis:
- Cu (A=63) to Zn (A=64): the last position filled is (F3,C3,S3), the triple gate. B/A changes by only +0.004 MeV/n.
- Re (A=187) to Os (A=192): filling 5 gate positions (all gd ≥ 2), B/A **drops** by 0.004 MeV/n.

Gates are **closure mechanisms**, not energy carriers. This matches the electron shell structure (see Section 5).

---

## 4. The Coupling Polynomial

### Definition

**f(K, s) = 1 + Ks + K²**

where K = 4 (unique solution of 2(D+1) = 2^D with D = 3) and s ∈ [-1, +1] is the coupling state.

### Key property: This is LINEAR in s

f(K, s) = K² + Ks + 1 = **17 + 4s**

It's a straight line through the Field Origin (F⁰ = 17) with slope K = 4.

### Three structural landmarks

| s | f(4, s) | Name | Meaning |
|---|---------|------|---------|
| +1 | **21 = F⁺** | Full coupling | All structural units active |
| 0 | **17 = F⁰** | Field Origin | Channels decoupled, scaffold intact |
| -1 | **13 = F⁻** | Anti-coupling | Channel cancellation |

Range: F⁺ - F⁻ = 2K = 8

### Terms map to Sierpiński levels

| Term | Value | Level | Coupling dependence |
|------|-------|-------|-------------------|
| **1** | 1 | Subchannel (innermost) | Constant |
| **Ks** | 4s | Channel (middle) | Varies with s |
| **K²** | 16 | Face (outermost) | Constant |

The K² = 16 face scaffold is **always present**. Only the channel layer (Ks) varies with coupling state. This is why the channel neural network collapsed to a constant — it's measuring the Ks term, which at the B/A scale is a geometric constant.

### Why NOT f = 1 + Ks + K²s²?

The quadratic version destroys F⁰ = 17. At s = 0, it gives 1 instead of 17. The 16-face scaffold vanishes. This is unphysical — the geometric structure doesn't disappear when channels decouple. The correct form preserves the scaffold at all coupling states.

### Walk quantization

The walk maps fill fraction (0 to 1) to coupling state s = 2×fill - 1 (-1 to +1). This gives five quantized states:

| fill | s | f |
|------|---|---|
| 0.00 | -1.0 | 13 |
| 0.25 | -0.5 | 15 |
| 0.50 | 0.0 | 17 |
| 0.75 | +0.5 | 19 |
| 1.00 | +1.0 | 21 |

The polynomial and the walk quantization are identical — the same linear function in two coordinate systems.

---

## 5. Valence Shell Connection

### The (3+1) hierarchy generates electron sub-shells

The spatial channels at each Sierpiński depth d map directly to electron angular momentum:

| Depth d | Spatial channels 3^d | SO(3) irrep | Sub-shell | Capacity 2(2l+1) |
|---------|---------------------|-------------|-----------|-----------------|
| 0 | 1 | l = 0 | **s** | 2 |
| 1 | 3 | l = 1 | **p** | 6 |
| 2 | 9 | l = 2 | **d** | 10 |
| 3 | 27 | l = 3 | **f** | 14 |

Total capacity: 2 + 6 + 10 + 14 = **32 = K³/2 = 64/2**

Half the walk carries energy. The other half is gate/closure structure.

### Electron shells map to walk cycles

The principal quantum shells map to the 3 Sierpiński nesting levels:

| Walk cycle | Level | Electron shells | Combined capacity |
|-----------|-------|----------------|------------------|
| Cycle 1 | Face | n = 1, 2 | 2 + 8 = 10 |
| Cycle 2 | Channel | n = 3, 4 | 18 + 32 = 50 |
| Cycle 3 | Subchannel | n = 5, 6 | 50 + 72 = 122 |

Each cycle reads f from 13→21 **twice** (spatial sweep + gate closure), giving 2 shells per cycle = 6 shells from 3 cycles.

### The critical connection

The gate carries **zero contribution** to valence structure because it's the Sierpiński-excluded center. The sub-shell capacities are 3^d (not 4^d) — the gate is removed at every depth. When we set the gate subchannel to 0 in the neural network, we enforced the same exclusion principle that generates the electron shells. This was confirmed empirically: gate positions contribute essentially zero binding energy.

The 16-channel output architecture (16 channels × 3 spatial subchannels, gate zeroed) is literally the same structure that generates the sub-shell filling order.

---

## 6. The 3-Scale Decomposition (The Solve)

### The key insight

The 256-dim walk vector has exactly one natural factorization that respects the (3+1) hierarchy at every level. It decomposes into three scales:

| Scale | Grouping | Dimensions | What it captures |
|-------|----------|-----------|-----------------|
| **Face** | 256 ÷ 16 = groups of 16 | 16 values | 4 faces × 4 shells, fill ratio per face |
| **Channel** | 256 ÷ 4 = groups of 4 | 64 values | 16 channels × 4 shells, fill ratio per channel |
| **Subchannel** | Raw binary | 256 values | Individual positions, 1 or 0 |

Each group's value is the fill ratio (sum ÷ group size) → 0.0 to 1.0.

### Why these three and no others?

The 256 vector factorizes as 4 × 4 × 4 × 4 (shells × faces × channels × subchannels). The only scale-respecting groupings that preserve (3+1) symmetry are by 16 (face), by 4 (channel), and by 1 (subchannel). Any other grouping (by 8, by 32) breaks the tetrahedral symmetry.

Three scales are forced by:
- D = 3 spatial dimensions
- 3 nesting levels of the Sierpiński triangle
- 3 cycles in the walk (face → channel → subchannel)
- 3 terms in the polynomial f = 1 + Ks + K²

### Shell structure is preserved

The grouping is consecutive chunking of the 256 vector. This means:
- Channel group 0 = shell 0, F0.C0 (first channel of first face, first shell)
- Channel group 16 = shell 1, F0.C0 (same channel, second shell)
- Face group 0 = shell 0, Face 0
- Face group 4 = shell 1, Face 0

The networks can distinguish which shell they're looking at.

---

## 7. The Three Neural Networks

### Architecture

```
NN_face:    16 inputs → 4 hidden (ReLU) → 1 output   (face MeV contribution)
NN_channel: 64 inputs → 4 hidden (ReLU) → 1 output   (channel MeV contribution)
NN_sub:    256 inputs → 4 hidden (ReLU) → 1 output   (subchannel MeV contribution)

B/A (predicted) = NN_face_out + NN_channel_out + NN_sub_out
```

### Why 4 hidden nodes each?

K = 4. The intrinsic dimensionality of the coupling structure is 4. This was verified by training networks with hidden sizes 4, 8, 16, 32 — all achieve the same R² ceiling (~0.999). More nodes don't help. 4 is sufficient because it matches the tetrahedral branching factor.

### Total parameter count

- NN_face: 16×4 + 4 + 4×1 + 1 = 73
- NN_channel: 64×4 + 4 + 4×1 + 1 = 265
- NN_sub: 256×4 + 4 + 4×1 + 1 = 1033

Total: **1,371 parameters** fitting 77 elements. But the architecture has **zero free structural parameters** — every dimension is dictated by the (3+1)³ geometry.

### Training

- Loss: MSE(predicted B/A, known B/A)
- Optimizer: Adam, lr=0.01 with step decay
- Epochs: 80,000
- Restarts: 10 (to escape local minima)
- Convergence: typically by epoch 20,000 (MAE = 1 keV)
- Excludes: He, Li, Be, B, F (light-element outliers, 5 elements)

### The (3+1) gate exclusion

In the 16-channel architecture variant, each channel's output tiles to 3 spatial subchannels and zeros the 4th (gate). This enforces perfect Triforce symmetry at every level — three identical corners, dark center.

---

## 8. Results

### Accuracy

| Metric | Value |
|--------|-------|
| R² | **0.999765** |
| MAE | **0.9 keV/n** |
| Max error | **22.0 keV/n** (Ar/Ca collision) |
| ≤ 0.5% | **77/77 elements** |

### Reproducibility

Two independent training runs produce **identical** outputs — same Face, Channel, Sub values for every element, same R², same universal constants. The decomposition is unique.

### The three scale contributions (element-dependent)

For Iron (Fe, A=56, B/A = 8.790):
```
Face:       3.687 MeV/n  (42%)
Channel:    0.820 MeV/n  (9%)
Subchannel: 4.284 MeV/n  (49%)
Total:      8.790 MeV/n  ✓
```

For Carbon (C, A=12, B/A = 7.680):
```
Face:       2.682 MeV/n  (35%)
Channel:    0.820 MeV/n  (11%)
Subchannel: 4.178 MeV/n  (54%)
Total:      7.680 MeV/n  ✓
```

For Bismuth (Bi, A=209, B/A = 8.041):
```
Face:       5.177 MeV/n  (64%)
Channel:    0.820 MeV/n  (10%)
Subchannel: 2.045 MeV/n  (25%)
Total:      8.041 MeV/n  ✓
```

Pattern: As elements get heavier, Face contribution rises, Subchannel falls, Channel stays fixed.

---

## 9. The Universal Constants That Emerged

### b = 0.0304 MeV/n (gate depth 1, universal)

The channel network output divided by 27 (the number of gd=1 positions) gives **exactly 0.0304** for every element. Zero variance. This is a geometric constant of the stellated octahedron — the energy per single-gate-crossing position.

Verification: 27 × 0.0304 = 0.820 = the channel network constant. ✓

### Channel = 0.820 MeV/n (universal)

The channel-scale network collapsed to a single constant. Every element gets exactly 0.820 MeV/n from the channel scale regardless of mass number, shell, or fill state. This is the Ks term of the coupling polynomial evaluated at the nuclear energy scale.

### Gate depth energies per element

| Depth | Symbol | Formula | Fe value | Range across elements | Role |
|-------|--------|---------|----------|----------------------|------|
| gd=0 | a | Face_MeV / 27 | 0.1365 | 0.099 – 0.192 | Spatial energy |
| gd=1 | b | Chan_MeV / 27 | 0.0304 | **0.0304 (constant)** | Gate coupling |
| gd=2 | c | Sub_MeV / 9 | 0.4760 | 0.227 – 0.491 | Closure energy |
| gd=3 | d | — | ≈ 0 | ≈ 0 | Triple gate (zero) |

### The a = 0.137 coincidence

For elements near Iron, the spatial energy per position a ≈ 0.137, which equals 1/α (the fine structure constant) to the available precision. This connection — spatial coupling energy equaling the electromagnetic coupling constant — warrants investigation but has not been proven causal.

---

## 10. Files and Reproduction

### Data generation

| File | Purpose |
|------|---------|
| `gen_3scale.py` | Generates `gfd_3scale_vectors.csv` from element data |
| `gfd_3scale_vectors.csv` | 82 elements × (Sym, A, B/A, Shell, Vec256, 16 face ratios, 64 channel ratios) |
| `gfd_sierpinski_256.csv` | Raw 256-dim vectors (earlier format) |

### Training

| File | Purpose |
|------|---------|
| `gfd_3scale_train.py` | Three-network training, produces JSON + CSV results |
| `gfd_3scale.json` | Per-element: face_mev, chan_mev, sub_mev, a, b, c |
| `gfd_3scale_results.csv` | Same in tabular form |
| `gfd_3scale_model.pt` | Saved PyTorch model weights |

### Visualization

| File | Purpose |
|------|---------|
| `gfd_weight_sierpinski.html` | Interactive Sierpiński triangle viewer |
| — | Modes: Weight Map, Element Fill, Energy Build, 3-Scale |
| — | Drop JSON files to load per-element data |
| — | Arrow keys cycle elements, hover for details |

### Earlier exploration files

| File | Purpose |
|------|---------|
| `gfd_nn_train.py` | Original 64→64→1 fully connected network (R²=0.9998) |
| `gfd_nn_contributions.py` | 16-channel (3+1) architecture with gate zeroing |
| `gfd_build_weight_map.py` | Generates effective weight analysis and HTML |
| `gfd_polynomial_tests.py` | 53 automated tests verifying the coupling polynomial |
| `gfd_polynomial_knowledge.md` | Reference document for f(K,s) = 1 + Ks + K² |

### Reproduction

```bash
pip install torch
python gen_3scale.py           # generates CSV
python gfd_3scale_train.py     # trains, exports JSON + CSV
# open gfd_weight_sierpinski.html, drag gfd_3scale.json onto drop zone
```

---

## 11. What Comes Next

### Immediate

- Zenodo DOI deposit: code + data + CSV results (locks priority)
- GitHub repo: full reproducible package with README
- J. Phys. G letter: kinematic result first (Section 1-2), then mechanism (Section 3)

### The base-8 π connection

The BBP formula generates π in base 8 from the same stellated octahedron face-reading mechanism. The step function that walks the Sierpiński triangle producing binding energies is the same walk that generates π. The walk that produces B/A and the walk that produces π share the same topology.

### The transformation polynomial

The coupling polynomial f(s) = 17 + 4s is linear, but the walk through it is nonlinear (coupon-collector curve at each cycle). The three neural networks implicitly learn this nonlinear transformation. Extracting it analytically — s_effective(step) as a function of walk position — would close the gap between the polynomial and the direct computation.

### The five excluded elements

He, Li, Be, B, F are excluded. These are light elements where the walk hasn't filled enough positions for the hierarchical structure to stabilize. A separate treatment (possibly the constitutive law μ(x) = x/(x+1)) may bring them in.

### The Z/A degeneracy

Elements with the same A but different Z (Ar/Ca at A=40, Mo/Tc at A=98) get identical predictions because the walk vector depends only on A, not Z. The maximum error from this is 22 keV/n. Incorporating Z/A as a constitutive modulation would break this degeneracy.

---

*© Stephen Nelson 2025–2026 · Field Dynamics · CC BY 4.0*
