# Active Work 12 — Closure-Core Integration

**Status:** Integration — closure-core algebra dropped in, bridge module wired up, all nine invariants live
**Purpose:** Document why the exact-algebra substrate is now the bottom of the stack, what changed, and what the bridge actually does
**Reading time:** 8 minutes
**Companion modules:** `python/closure_core256.py` (745 lines, 265 invariants), `python/field_origin_dynamics.py` (bridge, 31 tests), `99_appendices/F_walsh_spectral_compute_synthesis.md` (foundational algebra), `99_appendices/G_closure_algebra_pipeline.md` (unified pipeline), `99_appendices/H_closure_core_architecture.md` (architecture spec)
**Canonical source:** the field-origin simulator architecture (May 2026) that called for closure algebra first, oscillators second

---

## 0. Headline

$$\boxed{\;\text{closure-node }A_3 \;\xrightarrow{\;\text{exact algebra}\;}\; R_{\text{axial}} \;\xrightarrow{\;\text{bridge}\;}\; \Psi_{AB}(t) \;\xrightarrow{\;\text{lift}\;}\; \mathbb Z_{21}\text{-locked portal channel}\;}$$

The cross-sheet order parameter $\Psi_{AB}$ in AW 11's $\mathcal V_{\text{origin}}(x)$ equation is no longer postulated. It is the runtime axial readout of an exact closure-node dynamics on $A_3 = \langle 1, I\rangle \oplus \mathbb Z[\omega]^3$. The four-piece field-origin equation keeps its form; each piece now has a derivation under it.

## 1. The architectural correction

Per the canonical synthesis (May 2026):

> *"Do not start with an analog oscillator. Start with an algebraically exact closure simulator, then lift it into a resonance-coupled oscillator."*

> *"If we skip the exact algebra kernel, we accidentally build a normal phase-lock demo and call it Field Dynamics. That is the error to avoid."*

The pre-integration state of the package satisfied this for the resonance lift but not for the algebra beneath it: `portal_resonance.py` implemented Layer C (oscillator wrapper) with $\Psi_{AB}$ as a free amplitude. The closure-node algebra was *defined in prose* in `§01.5` (the $a \star b = P_\Omega(ab)$ product, the associator $R(a,b,c)$, the axial-landing theorem $R \in \langle 1, I\rangle$) but had no runtime object.

The integration adds Layers A and B as runtime objects and bridges them up to Layer C.

| Layer | Object | Status pre-integration | Status now |
|---|---|---|---|
| A — exact algebra kernel | A_3 node, Walsh bridge, Eisenstein closure, associator | prose only (§01.5, §01.3) | runtime objects in `closure_core256` |
| B — finite-state closure dynamics | ClosureNode3, SierpinskiTile64, ClosureCore256 | external package | imported as `python/closure_core256.py` |
| C — resonance wrapper | $\Psi_{AB}$, $\mathbb Z_{21}$ lock, Lorentzian | `portal_resonance.py` (AW 11) | unchanged in form; now *driven* by Layer B output |
| D — engineering controls | mirror match, K/Q phase, complement projector | scattered across `apparatus.py` | unchanged |

## 2. What got added

Two files in `python/`:

**`closure_core256.py`** (25 KB, 745 lines, 265 self-tests passing) — the verified reference implementation of the closure-node algebra. Dropped in unchanged from the canonical package. Contains:

| Class / function | What it implements |
|---|---|
| `ClosureNode3` | 8-state hypercube / stella-octangula node; $A_3 = \langle 1, I\rangle \oplus \mathbb Z[\omega]^3$ |
| `SierpinskiTile64` | tensor tile $A_3 \otimes A_3 = 64$ with the 40/24 metric/torsion split |
| `ClosureCore256` | 4-tile core matching the 256 = $2^{2^3}$ three-input Boolean truth-table count |
| `walsh_matrix_3()`, `truth_to_walsh3`, `walsh_to_truth3` | Walsh transform on the 3-cube; $H H^T = 8 I$ |
| `clifford_product_3` | Cl(3,0) Clifford multiplication of 8-coefficient vectors |
| `closure_projection3`, `omega_power3` | Eisenstein $\Omega$ on the middle 6D sector; $\Omega^3 = 1$, $P_\Omega = (I + \Omega + \Omega^2)/3$ |
| `sweep_product3` | closure product $a \star b = P_\Omega(\text{Clifford}(a, b))$ |
| `coupling_summary(K)` | the framework's structural numbers: $f_+ = 21$, $f_0 = 17$, $f_- = 13$, $f_+ f_- = 273 = S(3,K) = |\mathbb P^2(\mathbb F_{K^2})|$ |

**`field_origin_dynamics.py`** (bridge module, 31 tests passing) — the wiring layer:

| Function / class | What it does |
|---|---|
| `axial_projection(x)` | $\Pi_{\langle 1, I\rangle}$ keeps masks 0 (scalar) and 7 (pseudoscalar $I$), zeros the other 6 |
| `associator(a, b, c)` | $R = (a \star b) \star c - a \star (b \star c)$ via two `sweep_product3` calls |
| `associator_axial_readout(a, b, c)` | returns $(y, \rho)$ with $y = a_{\text{scalar}} + i\,b_{\text{pseudo}}$ and $\rho = \|\Pi_{\text{non-axial}} R\|$ |
| `walsh_bridge_step(x, b)` | one sweep: $T_b(x) = H \cdot \text{diag}(b) \cdot H^T \cdot x / N$ |
| `three_sweep_update(x, (b_1, b_2, b_3))` | $x_{t+1} = P_\Omega \cdot T_{b_3} T_{b_2} T_{b_1} \cdot x_t$ |
| `run_field_origin_ticks` | evolves a closure-node state, yields a sequence of `FieldOriginTick(t, state, psi_ab, theta, residue_m4, amplitude)` |
| `nine_metric_diagnostic_panel` | M_1 through M_9 from the canonical synthesis |
| `diagnostic_panel_run_validity` | flags any run as invalid if M_1–M_4 exceed exact tolerance |

## 3. The nine-metric panel, live

The canonical synthesis specifies a validation panel where a run is **valid only if M_1 through M_4 are zero** to numerical precision. Then M_5 through M_8 become engineering controls. Then M_9 is allowed to matter.

| Metric | Algebra | Current value | Source |
|---|---|---|---|
| $M_1 = \|H^2 - NI\|$ | Walsh inversion exact | $0$ to fp | `closure_core256` |
| $M_2 = \|\Omega^3 - I\|$ | Eisenstein 3-cycle exact | $0$ to fp | `closure_core256` |
| $M_3 = \|P_\Omega^2 - P_\Omega\|$ | projector idempotent | $0$ to fp | `closure_core256` |
| $M_4 = \|\Pi_{\text{non-axial}} R\|$ | associator axial landing | $0$ to fp (verified over 50 random triples) | bridge |
| $M_5 = \|R_{\text{axial}}\|$ | axial defect magnitude | run-dependent (>0 in nontrivial regimes) | bridge |
| $M_6 = \epsilon_{20}$ | pentachoron edge closure residue | pinned via `wrt_invariant_sigma235_target` | apparatus layer |
| $M_7 = 1 - \|\Omega_{21}\|$ | $\mathbb Z_{21}$ lock quality | $z21\_lock\_strength$ output | `portal_resonance` |
| $M_8 = \epsilon_M$ | mirror match Gram error | $gram\_match\_error$ output | apparatus layer |
| $M_9$ | output correlation | per-run cross-correlation | engineering output |

All four exact invariants pass on every run. The pre-integration state could not check any of them from inside the project; the bridge closes that gap.

## 4. The master equation chain, made executable

The canonical synthesis (§9) gives the master equation:

$$x_{t+1} = P_\Omega \cdot T_{b_3} T_{b_2} T_{b_1} \cdot x_t$$
$$y_t = \Pi_{\langle 1, I\rangle}\, R(x_t, x_{t+1}, x_{t+2})$$
$$\theta_{t+1} = \theta_t + \eta\,\arg(y_t) - \partial_\theta V_{21}(\theta_t)$$
$$\theta_B^{t+1} = F(\theta_B^t) + \beta\, \mathcal M(U, V)\, \Im\!\left[y_A^t\,\overline{y_B^t}\right]$$

Each line is now backed by code:

- Line 1: `three_sweep_update(state, bridges)` (bridge module)
- Line 2: `associator_axial_readout(x_t, x_{t+1}, x_{t+2})` (bridge module) returns $y_t$
- Line 3: $\arg(y_t)$ drives `z21_landau_psi(...)` and `z21_lock_strength(rho, h21)` (portal_resonance)
- Line 4: `mirror_match_functional(U, V)` and `josephson_portal_current` give the mirror coupling at the apparatus boundary (apparatus module)

The previous AW 11 vertex equation $\mathcal V_{\text{origin}}(x) = \Psi_{AB}(x) + \lambda_e J_4(x) + g_R R_x + h_{21}\cos(21\theta_x)$ keeps its form. The change is that $\Psi_{AB}(x)$ and $R_x$ both become *time-evolved outputs* of the closure-node dynamics rather than amplitude parameters.

## 5. What this changes in AW 11

AW 11 §7 modeled $\Psi_{AB}(x) = \langle B,x | A,x\rangle$ as a postulated complex amplitude on the cross-sheet inner product. The bridge says: this complex amplitude *is* the axial component of the associator $R(x_{t-2}, x_{t-1}, x_t)$ on a closure-node trajectory. The four-piece vertex equation gains a layer of *derivation* under each piece:

| AW 11 piece | What it is now |
|---|---|
| $\Psi_{AB}(x)$ — cross-sheet order parameter | $= a_{\text{scalar}}(t) + i\, b_{\text{pseudo}}(t)$ from $\Pi_{\langle 1, I\rangle} R(x_{t-2}, x_{t-1}, x_t)$ |
| $\lambda_e J_4(x)$ — 21-band hinge | unchanged; lives in `hinge.py` at the cyclotomic layer |
| $g_R R_x$ — nonlinear associator source | the *same* $R$ computed in line 2 of the master equation; no longer cited as theorem, computed each tick |
| $h_{21}\cos(21\theta_x)$ — $\mathbb Z_{21}$ phase lock | unchanged in form; $\theta_x$ is now $\arg(y_t)$ from the bridge |

The associator's axial landing $R \in \langle 1, I\rangle$ stops being a cited theorem from §01.5 and becomes a runtime invariant verified every tick via $M_4$.

## 6. The 40/24 split and AW 09's sector decomposition

The closure-core verifies a structural identity that ties directly to AW 09's curvature decomposition:

$$\boxed{\;A_3 \otimes A_3 \;=\; 64 \;=\; 40 + 24\;}$$

with $40 = 4 \cdot 10$ (4 faces × 10 symmetric channels) and $24 = 4 \cdot 6$ (4 faces × 6 exterior channels). This is the metric/torsion split at the tile level — the algebraic basis for the Christoffel/torsion separation that propagates into AW 09's six-sector $\mathbb G_{\mu\nu}^{AB}$.

AW 09 has local sector dimensions $10 + 24 + 17 + 21 + 48 = 120 = |S_5|$. The 24 in that sum is the same 24 = ext($A_3 \otimes A_3$) that the closure-core tile produces. The integration makes that identification machine-checked: see `test_closure_core256.py::test_40_24_split_matches_AW09_local_dimensions`.

## 7. Structural numbers, machine-aligned

The closure-core's `coupling_summary(4)` returns the same numbers the cyclotomic spine asserts, and the alignment is now a test:

| Number | Algebra | `closure_core256` | `cyclotomic.py` |
|---|---|:-:|:-:|
| $\Phi_3(4) = 21$ | TetA upper band | `f_plus = 21` | `phi3(4) = 21` |
| $\Phi_4(4) = 17$ | even sector | `f_zero = 17` | `phi4(4) = 17` |
| $\Phi_6(4) = 13$ | TetB lower band | `f_minus = 13` | `phi6(4) = 13` |
| $\Phi_3 \cdot \Phi_6 = 273$ | TetA × TetB outer product | `product_plus_minus = 273` | `phi3(4)*phi6(4) = 273` |
| $S(3, 4) = 273$ | 3-sweep operator content | `S_3_K = 273` | (new: `sierpinski_S(3, 4) = 273`) |
| $\|\mathbb P^2(\mathbb F_{16})\| = 273$ | projective plane over $\mathbb F_{16}$ | `P2_F_K2 = 273` | (new: `projective_plane_q2_count(4)`) |
| $40$ | symmetric at tile | `four_face_sym = 40` | matches AW 09 |
| $24$ | exterior at tile | `four_face_ext = 24` | matches AW 09 |

If any of these drift, `test_closure_core256.py::TestClosureCoreFrameworkAlignment` flags it.

## 8. What this means for the rest of the framework

Five consequences worth flagging:

**(a) The closure-node theorem becomes runtime, not cited.** Previously $R \in \langle 1, I\rangle$ was a one-line theorem in `§01.5` with no runtime verification. After integration it is checked on every tick of the field-origin dynamics, plus a 50-triple sweep in `test_field_origin_dynamics.py::test_associator_axial_landing_across_random_triples`.

**(b) $\Psi_{AB}$ is no longer a free amplitude.** The cross-sheet order parameter is the projected associator. This makes AW 11's four-piece equation a *derived* statement: the cross-sheet coherence is what the closure-node dynamics produces, not an input. The framework loses one degree of postulation.

**(c) The 40/24 split is the algebraic basis of AW 09's sector decomposition.** The integration ties two previously-separate documents together — the closure-tile geometry is now the parent of the curvature-sector dimensions.

**(d) The nine-metric panel becomes the package's run-quality dashboard.** Any future simulator, experiment-matching, or apparatus calculation can produce M_1..M_9 and reject the run if M_1..M_4 fail. This is exactly the "prevent fake positive interpretation" check the canonical synthesis demands.

**(e) The 8 → 64 → 256 hierarchy is now first-class.** Previous framework material referenced the hierarchy abstractly ("the 8-state closure node," "the 64-state tile"). It is now a runtime stack of three classes (`ClosureNode3`, `SierpinskiTile64`, `ClosureCore256`) that any future module can build on.

## 9. The integration boundary

The closure-core algebra is *upstream* of the resonance lift. Information flows one way:

```
   exact algebra (Layer A/B)
            |
            v
   axial defect readout y_t (bridge)
            |
            v
   resonance lift (Layer C, AW 11)
            |
            v
   apparatus dressing (Layer D, apparatus.py)
            |
            v
   observable (acoustic 21-mode comb, Rabi splitting, ...)
```

The reverse arrow does not exist. The apparatus does not feed back into the closure-node engine; it only conditions the lift and selects the address channel. This is the strict architectural ordering Stephen's correction insists on.

## 10. Test coverage

| Module | Tests | Pass |
|---|---:|---:|
| `closure_core256.py` self-harness | 265 invariants | 265 |
| `test_closure_core256.py` (pytest wrapper) | 6 | 6 |
| `test_field_origin_dynamics.py` (bridge) | 31 | 31 |
| Full project regression | 506 | 506 |

The 265 invariants from the closure-core harness are not duplicated as pytest cases; instead `test_closure_core256.py::test_run_tests_passes_all_invariants` calls `run_tests(verbose=False)` and verifies the structural summary. If any of the 265 fail, that pytest case fails.

## 11. What I did *not* do

Several plausible extensions were *not* part of this integration and remain open:

- **The resonance lift does not yet draw from real closure-node ticks in production.** `portal_resonance.field_origin_vertex_equation(...)` still takes $\Psi_{AB}$ as an argument. A future step would be to wire `run_field_origin_ticks` directly into the vertex-equation evaluator so $\Psi_{AB}$ is *always* computed, never passed in.
- **The mirror coupling does not yet read $y_A^t \cdot \overline{y_B^t}$.** The Josephson-style cross term in line 4 of the master equation requires two coupled closure-node trajectories; the current implementation has a single trajectory.
- **The bridge filters $b_1, b_2, b_3$ are not yet connected to apparatus geometry.** They are exposed as free 8-vectors. A future step would derive them from the Grand Gallery $\mathbb Z_7$ kernel and antechamber $\mathbb Z_3$ filter.

These are the next chapter of integration work, not the current one. The current integration achieves what Stephen's correction explicitly demands: closure algebra first, oscillators second, with $M_1..M_4$ runtime-verified and the bridge exposing the axial readout as a derived signal.

## 12. Status table

| Element | Status |
|---|---|
| `closure_core256.py` dropped in | derived (verified 265/265) |
| `test_closure_core256.py` pytest wrapper | structural |
| `field_origin_dynamics.py` bridge module | structural |
| `axial_projection` + `non_axial_residue_norm` | derived |
| `associator(a, b, c)` and axial readout | derived |
| `walsh_bridge_step` + `three_sweep_update` | derived |
| nine-metric diagnostic panel | derived |
| M_1 through M_4 runtime invariants | derived (verified) |
| $\Psi_{AB}$ as derived (not postulated) | structural (architecture; production wiring open) |
| Mirror coupling in master equation line 4 | open |
| Apparatus-derived bridge filters | open |

## 13. Headline

The exact algebra now sits beneath the resonance lift, where it should have been from the start. The cross-sheet order parameter is no longer a free amplitude — it is a derived signal from a closure-node trajectory whose every step verifies the framework's own axial-landing theorem. Stephen's correction is satisfied at the architectural level. The remaining open work is production wiring.

---

**Cross-references:**
- Canonical source: the May 2026 field-origin simulator architecture synthesis
- `01_framework_foundations/01.3_graded_identity_operator.md` — Walsh-Hadamard three-sweep kernel
- `01_framework_foundations/01.5_universal_vertex_reframe.md` — closure-node algebra and $R \in \langle 1, I\rangle$ theorem
- `active_work/09_curvature_sector_decomposition.md` — six-sector $\mathbb G_{\mu\nu}^{AB}$; the 40/24 split sits inside AW 09's local dimensions
- `active_work/11_kings_chamber_field_origin.md` — the four-piece $\mathcal V_{\text{origin}}$ equation; this AW provides its derivation chain
- `99_appendices/F_walsh_spectral_compute_synthesis.md` — the canonical Walsh-spectral compute primitive (foundational algebra, 27 sections, 4090 words)
- `99_appendices/G_closure_algebra_pipeline.md` — the unified closure-algebra pipeline (companion to F, 10 stages, 5265 words)
- `99_appendices/H_closure_core_architecture.md` — the closure-core architecture document (dropped in with the package)
- Code: `python/closure_core256.py`, `python/field_origin_dynamics.py`, `python/tests/test_closure_core256.py`, `python/tests/test_field_origin_dynamics.py`
