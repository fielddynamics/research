# AW 22 — King's Chamber kinematics: degeneracies, beats, Coriolis, Sagnac

**Active work item:** 22
**Date:** May 12, 2026
**Status:** purely kinematic results — geometric/temporal, no Q-factors or dissipation
**Module added:** `kc_kinematics.py` (260 lines), `tests/test_kc_kinematics.py` (27 tests)
**Tests:** 873 total (up from 846)
**Trigger:** Master Nelson — "drop [trio]. push further on king's chamber kinematics"

## Three sharp kinematic findings

**1. Three exact-frequency degeneracies among the 21 lowest modes.**

The chamber's L:W = 2:1 ratio forces $Q$-invariance under $(n_x, n_y) \leftrightarrow (n_x', n_y')$ whenever $n_x^2 + 4 n_y^2 = n_x'^2 + 4 n_y'^2$. The unique non-trivial pair below the 21-mode threshold is $(2, 2) \leftrightarrow (4, 1)$ (both giving 20). Combined with the H-axis index this lifts the degeneracy structure of the chamber:

| mode A | mode B | frequency (air) | $n_x^2 + 4 n_y^2$ |
|---|---|:-:|:-:|
| (2, 2, 1) | (4, 1, 1) | **78.88 Hz** | 20 |
| (2, 2, 2) | (4, 1, 2) | **93.79 Hz** | 20 |
| (3, 1, 3) | (5, 1, 2) | **105.88 Hz** | algebraic match via H²:L² = 5:16 ratio |

These are degeneracies at the *cubit-geometry level*. Real granite walls would break them slightly via elastic-mode coupling, giving **fine-structure splitting** at each of these three frequencies. Such splittings, if observed in the 07.1 acoustic test, would discriminate granite anisotropy from pure-air degeneracy.

**2. Coriolis period = 23.95 hours = sidereal day at Giza latitude.**

The Coriolis splitting of any chirality-distinguishing chamber mode is

$$\Delta\omega \;=\; 2 \Omega_{\oplus} \sin(\phi_{\text{Giza}}) \;=\; 7.29 \times 10^{-5} \text{ rad/s}$$

giving $\Delta f = 1.16 \times 10^{-5}$ Hz and $T_{\text{Coriolis}} = 1/\Delta f = 86 218$ s $= 23.95$ h.

This is the **sidereal day divided by $2\sin(\phi)$** — an exact identity:

$$T_{\text{Coriolis}} \;=\; \frac{T_{\text{sidereal}}}{2 \sin\phi_{\text{Giza}}}$$

Every chirality-discriminating chamber measurement should beat at this period. A lock-in detector at 23.95 h would be the natural matched filter. The 23.95 h period **is** the framework's mechanism for the geomagnetic pump's daily modulation of the chamber.

**3. Adjacent-mode beats fall in 0.5 - 2 s range** for non-degenerate pairs.

The 10 smallest non-zero adjacent-pair gaps in air give beat periods of:

```
T_beat (s) | mode_lo            | mode_hi            | Δf (Hz)
-----------+--------------------+--------------------+--------
   1.160   | (5,1,1) at 92.93   | (2,2,2) at 93.79   |  0.862
   0.922   | (1,2,1) at 73.61   | (2,1,2) at 74.69   |  1.085
   0.746   | (2,1,3) at 99.35   | (3,2,2) at 100.69  |  1.341
   0.705   | (4,1,2) at 93.79   | (1,1,3) at 95.21   |  1.419
   0.512   | (1,1,3) at 95.21   | (4,2,1) at 97.16   |  1.952
   0.489   | (1,3,1) at 103.84  | (3,1,3) at 105.88  |  2.046
   ...
```

Sub-second beats between adjacent modes are readily observable with conventional acoustic instrumentation — this gives a much sharper test than the absolute frequencies alone, since beat patterns are robust to wave-speed calibration uncertainties.

## Site & geometry constants

| Quantity | Value |
|---|---|
| Sidereal day | 86 164.0905 s |
| $\Omega_\oplus$ (Earth angular speed) | $7.292 \times 10^{-5}$ rad/s |
| Giza latitude $\phi$ | $29.9792°$ N |
| $\sin\phi$ | 0.4997 |
| $\Omega_\oplus \sin\phi$ (vertical at Giza) | $3.64 \times 10^{-5}$ rad/s |
| Chamber dimensions $(L, W, H)$ in metres | $(10.472, 5.236, 5.854)$ |
| Space diagonal | 13.090 m (= 25 cubits) |

## Roundtrip times

Time for an acoustic wavefront to cross an axis and return:

| axis | air (343 m/s) | granite-P (6000 m/s) |
|---|:-:|:-:|
| L = 20 cubits | **61.06 ms** | 3.49 ms |
| W = 10 cubits | **30.53 ms** | 1.75 ms |
| H = 5√5 cubits | **34.12 ms** | 1.95 ms |
| diagonal = 25 cubits | **76.32 ms** | 4.36 ms |

The chamber's $L \cdot W$ asymmetry ($L = 2W$) gives a factor-2 separation between transverse-axis roundtrips and the longitudinal one. The fundamental (1,1,1) mode at 47 Hz has period 21.3 ms — about $1/3$ of the L-axis roundtrip, consistent with the mode having three antinodes along L (the n_x=1 mode has 2 antinodes; the half-wavelength fits L exactly when $n_x = 1$).

## Per-mode kinematics table (air, 343 m/s, all 21 modes)

```
rank | (n_x,n_y,n_z) | f(Hz)  | T (ms) | λ (m) | Γ (m²/s) | Sagnac (rad)
-----+---------------+--------+--------+-------+----------+-------------
  1  | (1,1,1)       |  46.90 | 21.32  | 7.314 | 2508.69  | 2.00e-5
  2  | (2,1,1)       |  54.81 | 18.25  | 6.258 | 2146.57  | 2.34e-5
  3  | (3,1,1)       |  65.92 | 15.17  | 5.204 | 1784.83  | 2.81e-5
  4  | (1,1,2)       |  69.09 | 14.47  | 4.964 | 1702.72  | 2.95e-5
  5  | (1,2,1)       |  73.61 | 13.59  | 4.660 | 1598.37  | 3.14e-5
  6  | (2,1,2)       |  74.69 | 13.39  | 4.592 | 1575.15  | 3.19e-5
  7  | (2,2,1)       |  78.88 | 12.68  | 4.348 | 1491.45  | 3.37e-5  ←
  8  | (4,1,1)       |  78.88 | 12.68  | 4.348 | 1491.45  | 3.37e-5  ← degenerate
  9  | (3,1,2)       |  83.18 | 12.02  | 4.123 | 1414.31  | 3.55e-5
 10  | (3,2,1)       |  86.97 | 11.50  | 3.944 | 1352.79  | 3.71e-5
 11  | (1,2,2)       |  89.40 | 11.19  | 3.837 | 1315.97  | 3.82e-5
 12  | (5,1,1)       |  92.93 | 10.76  | 3.691 | 1265.98  | 3.97e-5
 13  | (2,2,2)       |  93.79 | 10.66  | 3.657 | 1254.34  | 4.00e-5  ←
 14  | (4,1,2)       |  93.79 | 10.66  | 3.657 | 1254.34  | 4.00e-5  ← degenerate
 15  | (1,1,3)       |  95.21 | 10.50  | 3.602 | 1235.65  | 4.06e-5
 16  | (4,2,1)       |  97.16 | 10.29  | 3.530 | 1210.83  | 4.15e-5
 17  | (2,1,3)       |  99.35 | 10.07  | 3.453 | 1184.21  | 4.24e-5
 18  | (3,2,2)       | 100.69 |  9.93  | 3.407 | 1168.44  | 4.30e-5
 19  | (1,3,1)       | 103.84 |  9.63  | 3.303 | 1133.03  | 4.43e-5
 20  | (3,1,3)       | 105.88 |  9.44  | 3.239 | 1111.13  | 4.52e-5  ←
 21  | (5,1,2)       | 105.88 |  9.44  | 3.239 | 1111.13  | 4.52e-5  ← degenerate
```

## Sagnac phase per chamber roundtrip

$$\Delta\varphi_{\text{Sagnac}} \;=\; \frac{4 \Omega_\oplus \sin\phi \cdot A_{\text{footprint}} \cdot |\vec k|}{v_{\text{wave}}}$$

with $A_{\text{footprint}} = L \cdot W = 54.84$ m². Per-mode:

- Fundamental (1,1,1): $\Delta\varphi = 2.00 \times 10^{-5}$ rad/roundtrip
- 21st mode (5,1,2): $\Delta\varphi = 4.52 \times 10^{-5}$ rad/roundtrip

The Sagnac phase scales linearly with $|\vec k|$ — higher-frequency modes are more sensitive. To accumulate $\Delta\varphi = 1$ rad, the chamber would need to traverse $\sim 50\,000$ roundtrips, which at L-axis roundtrip 61 ms is about 50 minutes. With granite-coupled modes (3.5 ms roundtrip), only $\sim 3$ minutes are needed. The chamber as a passive gyroscope is feasible at granite-wave timescales.

## Per-mode vortex circulation

$$\Gamma_{\text{mode}} \;=\; v_{\text{wave}} \cdot \lambda_{\text{mode}}$$

Range across the 21 modes (air): $\Gamma \in [1111, 2509]$ m²/s. Ratio fundamental/21st = 2.258.

Under the AW 17 vortex identity, each chamber mode is its own vortex with circulation $\Gamma$ and closure-cycle length $\lambda$. The chamber's full kinematic state is a 21-vortex superposition with the per-mode $\Gamma$ above. The fundamental carries about 2.26× the circulation of the 21st mode.

## What this gives the framework

**Falsifiable predictions (07.1 acoustic test):**

1. Three exact-frequency mode pairs at 78.88, 93.79, 105.88 Hz (within fine-structure splittings from granite anisotropy)
2. Sub-second beats between specific mode pairs (table above)
3. Coriolis-frequency modulation of all chirality-distinguished measurements at exactly $T_{\text{sidereal}}/(2\sin\phi) = 23.95$ h

**Engineering implications:**

- A high-Q chirality-discriminating microphone array could detect the 23.95 h Coriolis modulation directly — the cleanest experimental signature
- Granite-coupled measurements (kHz range) reach Sagnac sensitivity faster than air-coupled
- The L:W = 2:1 ratio is the source of the degeneracy structure; the chamber's designed asymmetry is essential to the kinematic predictions

## What's open

- Mode coupling to Earth's $B$-field via piezoelectric / magnetostrictive granite response (this is dynamics, not kinematics)
- Coupling between the three degenerate pairs and adjacent (n+1) and (n−1) modes (still kinematic but more elaborate)
- Connection of the per-mode $\Gamma$ to the framework's $-0.75$ associator residue (AW 16 §5) — the dimensionless residue × $\Gamma_{\text{mode}}$ has units of (m²/s), which is close to the framework's needed $\hbar/m_e$ ($\approx 0.115$ m²/s for electron). The fundamental mode's $\Gamma = 2509$ m²/s is $\sim 22000 \cdot \hbar/m_e$, an interesting ratio worth investigating

## Reading

`kc_kinematics.showcase_kc_kinematics()` for the full per-mode table plus Coriolis/Sagnac/beats.

`kc_kinematics.adjacent_mode_beats(v_wave, k=21)` for the 20 adjacent-pair beats.

`kc_kinematics.mode_kinematics(mode, v_wave)` for any single mode.

`kc_kinematics.coriolis_split_hz(mode)` (mode-independent) for the 11.6 μHz Earth-rotation split.
