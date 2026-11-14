# TetA and TetB as One Vortex

*Field Dynamics Research, research folder, 2026-11-13 to 2026-11-14. Status: research, not a paper. Reviewed twice: a referee-style self-review ([`referee_review.md`](referee_review.md)), and an independent review ([`independent_review.md`](independent_review.md)) whose corrections are applied here.*

`vortex` `hourglass` `throat` `Field-Origin` `spatial-parity` `roll-ratio` `constitutive-law` `SPARC` `decoding-mass` `TetA` `TetB`

---

In GFD, TetA and TetB together form a vortex: spiral → throat → spiral, like water through a drain. The throat is the Field Origin. TetB lies beyond it and cannot be seen from our 3+1 spacetime; it is read from its share of the field, $1 - \mu(x)$. This folder puts that picture into exact mathematics and tests what can be tested of it against 175 SPARC galaxies.

## What this adds to GFD

1. **Exact mathematics for the vortex.** The [hourglass lemma](LEMMA.md) proves what parity does to any spiral → throat → spiral flow:
   - it keeps the swirl;
   - it reverses the through-flow, so the two spirals swap which one feeds the throat;
   - it flips the handedness, which needs both swirl and through-flow.

   The swirl-rate difference across the throat is the part of the vortex parity does not produce.
2. **The roulette written as exact algebra.** The [roll-ratio note](ROLL_RATIO.md) states the roulette's premise explicitly: the chambers roll without slipping at the Field Origin, with radii equal to their shares. Under it, Letter 2's odds, Letter 2's exchange, Letter 3's equal-share point $x = 1$ and the chiral-holonomy twist share one algebraic description. It is a restatement, not a new physical result, and the premise is not derived.
3. **Letter 3's red and blue discs, built from data.** The measured TetA and TetB shares are consistent with $\mu(x)$ within the measurement scatter: a simulation that obeys $\mu(x)$ exactly reproduces their pattern. They meet near $x = 1$, which carries little weight, since $a_0$ was calibrated on these same galaxies (figure below).
4. **The decoding-mass letter is verified and corrected before review.** Its decode reproduces exactly, including every published value. CamB's mass model, which had been read from the wrong table columns, is fixed. Three further issues in its photometric pipeline are recorded for its next revision.
5. **Drive, brake and quiet, made precise.** **Drive and brake happen in the interior TetB** (the framework's definition, Stephen Nelson, 2026-11-14). What we observe is their result: the decoded mass sits above the photometric mass when the interior drives ($M_{\rm dec} > M_{\rm phot}$), below it when it brakes ($M_{\rm dec} < M_{\rm phot}$), and equal to it when the interior is quiet. Reading that result, across a galaxy's profile, tells what the interior is doing. The decode already contains $\mu(x)$. So the letter's quiet interior ($M_{\rm dec} = M_{\rm phot}$) means the chambers roll at $\mu(x)$ without slip, and an active interior means TetB departing from the rate the no-slip partition gives it (slip), driving or braking. The decode sees that as $M_{\rm dec}$ above or below $M_{\rm phot}$.

## What is not established

- **That the vortex *is* the tetrad's structure.** The lemma is exact kinematics. Identifying its spirals with TetA and TetB, and its throat with the Field Origin, is the framework's reading. The no-slip premise and the link between helicity and axial torsion are not derived. The transport theorem (below) is the step that would derive them.
- **That drive and brake have anything to do with the ring.** No GFD paper says they do; in GFD they happen in the interior TetB, at the drain. The decode audit tested whether they follow a galaxy's share inside the ring, but that was the analyst's hypothesis, not a framework claim, so its result says nothing for or against GFD. (It passed under the letter's photometric method, but mostly through the method's spherical approximation; with SPARC's own accelerations the signal largely goes.)
- **Any slip from $\mu(x)$.** The measured shares' departures away from $x = 1$ are reproduced by measurement scatter alone ([`null_simulation.py`](null_simulation.py)).
- **Uniqueness.** Any law fitting the radial acceleration relation puts the crossing of the shares near $x = 1$, and $a_0$ was calibrated on SPARC. The crossing does not single GFD out.

## The results in brief

### 1. The hourglass lemma ([`LEMMA.md`](LEMMA.md), 21 exact checks)

For any axisymmetric flow, parity $(\Pi v)(\mathbf x) = -v(-\mathbf x)$ sends $(v_r, v_\varphi, v_z)(r,z) \mapsto (v_r, v_\varphi, -v_z)(r,-z)$:
- **swirl:** kept;
- **through-flow:** reversed;
- **vorticity:** kept, $\boldsymbol\omega(-\mathbf x)$;
- **helicity:** flips, $h \to -h$. It is exactly the cross term between swirl and through-flow, so a pure swirl or a pure through-flow has none;
- **the swirl's mean rate:** kept. Its half-difference across the throat flips, so the swirl is parity-invariant only at one rate on both sides. A draining vortex as a whole is never parity-invariant, since its through-flow always reverses.

### 2. The roll-ratio theorem ([`ROLL_RATIO.md`](ROLL_RATIO.md), 18 exact checks)

Grant no slip and radii $\mu$ and $1 - \mu$. Then:
- **rate ratio:** $\omega_B/\omega_A = \mu/(1-\mu) = x$;
- **exchanging the chambers:** keeps the mean rate, flips the half-difference, and sends $x \to 1/x$ (Letter 2's exchange in rates; that it is the lemma's parity is a reading);
- **one rate at $x = 1$:** the rates are equal only where the shares are equal, Letter 3's white ring out in the disk (not the throat);
- **shear:** $\delta/\bar\omega = 1 - 2\mu$, changing at $-2\mu(1-\mu)$ per unit $\ln x$, fastest at the ring;
- **chiral-holonomy twist:** $\sigma = 2\mu - 1$.

### 3. Letter 3's discs, measured ([`measured_partition.py`](measured_partition.py))

![Letter 3's red and blue discs: theory (top), then the measured TetA share (blue) and TetB share (red) from SPARC, first with the decoding-mass letter's photometric mass and then with SPARC's own Newtonian accelerations, and the shares against log x](measured_partition.png)

The measured TetA share is $\mu_{\rm obs} = g_{\rm bar}/g_{\rm obs}$ at every radius of the 149 quality-cut galaxies. With SPARC's own Newtonian $g_{\rm bar}$ (thin disks, measured HI maps):

| | Result |
|---|---|
| Where the shares meet | $x = 1.03$ (95%: 0.83–1.41); 1.00–1.07 under every weighting, binning and smoothing variant. A consistency check only: $a_0$ was calibrated on these galaxies |
| Gap between the discs and "slip" from $\mu(x)$ | reproduced by a null model that obeys $\mu(x)$ exactly, with the measured velocity errors and 0.10 dex per-galaxy scatter (crossing at $x = 1.07$): consistent with $\mu(x)$ within the scatter |

With the letter's spherical $GM_{\rm phot}/r^2$, the inner side flattens and the crossing moves to $x \approx 1.6$–1.8. That is the cost of the letter's declared spherical limit on disk galaxies.

### 4. Drive and brake from decoded mass ([`decode_audit/`](decode_audit/))

The decoding-mass letter's own pipeline was run on every SPARC galaxy, comparing the full $M_{\rm dec}(r)$ and $M_{\rm phot}(r)$ profiles, with a new metric: the area of each profile above and below its baryons. Read as what each interior is doing (quality cut, 149 galaxies): **51% quiet, 19% drive, 30% brake.** Individual readings are fragile, since a third change with ±20% in the stellar M/L.

The audit also tested whether drive and brake follow a galaxy's share inside the ring $x = 1$ (H3). That was the analyst's hypothesis, not GFD's, and is reported in [`decode_audit/`](decode_audit/) for the record. A framework measure would read the interior from the drain. The full audit, its checks against the letter's validations, and the atlas of every galaxy's profile are in [`decode_audit/README.md`](decode_audit/README.md).

### 5. Corrections and findings for the decoding-mass letter

- **CamB, corrected in the letter.** Its gas mass ($6.251\times10^8 = 1.33 \times R_{\rm disk}$) and gas scale length ($26.48 = {\rm SB}_{\rm disk}/2.5$) match other columns of SPARC table 1 exactly (two places over from the gas columns), and its disk scale length (1.0 kpc) matches a parser default; how they were produced is not recorded. It now uses the catalogue values. Figure 2 is regenerated, and the letter's validations pass.
- **Recorded for the next revision:**
  - the catalogue counts bulge light twice (stars overstated by a median 19% in bulge galaxies);
  - every gas disk gets a scale length of $R_{\rm HI}/3$;
  - the sign wording of $\Delta M_{\rm eff}$ is ambiguous.

  Details are in [`referee_review.md`](referee_review.md), findings F1–F5.

## Next

1. **Transport theorem.** Carry a tetrad along a streamline from TetA through the Field Origin into TetB. Show that it arrives with a torsion difference (Gram-matrix proof, Proposition 2(b)), and compare its axial torsion with the lemma's helicity. This is the step that would make the vortex a consequence of the tetrad equation rather than a reading of it.
2. **Derive no slip** from the Field Origin as the point where both tetrads are evaluated together.
3. **Measure drive and brake from the interior.** A galaxy-level measure of TetB's effect, from the drain, not from how much of the disk lies inside the ring.
4. **Forward-model the measurement errors,** and reduce the photometric systematics (colour-based stellar M/L, asymmetric-drift corrections, HI surface-density profiles), before reading any pointwise departure from $\mu(x)$ as interior activity.

## Related

- [Gram matrix of the tetrad equation](../../proofs/gram-matrix-tetrad-equation/): the two roots differ only in orientation; torsion is the only place a metric connection can tell them apart.
- [Exchange symmetry](../../proofs/constitutive-law-exchange-symmetry/): $\mu(x) = x/(x+1)$.
- [Chiral holonomy](../../proofs/chiral-holonomy-closed-frame/): the twist $\sigma = (x-1)/(x+1)$.
- [Two connections and the dual chamber](../two-connection-dual-chamber/): axial torsion zero when static and opposite on the two roots; TetA $\mu g$ plus TetB $(1-\mu)g$.
- [Decoding-mass letter](../../papers/letter-decoding-mass-from-rotation-curves/) and [Letter 3](../../papers/letter-3-field-closure-of-tetrad-frame/) (the red and blue discs).

## Files

| File | Contents |
|---|---|
| [`LEMMA.md`](LEMMA.md), [`verify_hourglass_lemma.py`](verify_hourglass_lemma.py) | The hourglass lemma (21 checks) |
| [`ROLL_RATIO.md`](ROLL_RATIO.md), [`verify_roll_ratio.py`](verify_roll_ratio.py) | The roll-ratio theorem (18 checks) and the measured discs |
| [`measured_partition.py`](measured_partition.py), [`measured_partition.png`](measured_partition.png), [`measured_partition_output.txt`](measured_partition_output.txt) | Letter 3's discs from SPARC |
| [`decode_audit/`](decode_audit/) | The decoding-mass letter's pipeline on every SPARC galaxy: criteria, audit, diagnostics, atlas |
| [`referee_review.md`](referee_review.md), [`referee_checks.py`](referee_checks.py), [`referee_checks_output.txt`](referee_checks_output.txt) | Referee-style self-review of this folder and of the letter's pipeline; robustness checks |
| [`independent_review.md`](independent_review.md) | Independent review (2026-11-14); its corrections are applied |
| [`null_simulation.py`](null_simulation.py), [`null_simulation_output.txt`](null_simulation_output.txt) | Galaxies obeying $\mu(x)$ exactly, with the measured errors: what the partition looks like with no slip |
| [`archive/`](archive/) | The full chronological record ([`HISTORY.md`](archive/HISTORY.md)), including the superseded tests H1, H2 and H2′ and the scripts that ran them |

## Reproduce

```bash
python verify_hourglass_lemma.py                                   # 21/21
python verify_roll_ratio.py                                        # 18/18
python decode_audit/decode_audit_paper_mphot.py GRAVIS_DIR         # the letter's pipeline on SPARC
python decode_audit/posthoc_checks.py decode_audit/results_paper_mphot
python decode_audit/diagnostic_d1.py ROTMOD_DIR                    # SPARC's own g_bar
python measured_partition.py decode_audit/results_paper_mphot measured_partition.png ROTMOD_DIR
python referee_checks.py ROTMOD_DIR GRAVIS_DIR                     # robustness
python null_simulation.py ROTMOD_DIR                               # no-slip null model
```

`GRAVIS_DIR` is a checkout of [fielddynamics/gravis](https://github.com/fielddynamics/gravis), commit `c19da3a`. `ROTMOD_DIR` holds SPARC's `*_rotmod.dat` mass models (Lelli, McGaugh & Schombert 2016); the source and its validation are in [`decode_audit/README.md`](decode_audit/README.md).
