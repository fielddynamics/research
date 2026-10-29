# Atomic and Compound Properties from the Vortex Radius

*An overdetermined test of the GFD atomic picture · Gravity Field Dynamics (GFD) · Field Dynamics Research*

`atomic-physics` `periodic-table` `polarizability` `chemical-bonding` `ionic-crystals` `lattice-energy` `materials-science`

---

## Summary

Gravity Field Dynamics describes an atom with the same structure it uses for a galaxy. The nucleus is a bound gravity-field configuration. Its electric field is a vortex extending into the surrounding unbound field. The electron is a region of that surrounding field, a *tile*, illuminated by the vortex. In this picture, the radius of an atom is the distance at which the outermost tile sits from the nucleus.

This folder asks a single question: **if the vortex radius is known, how many other properties of atoms and compounds follow from it?** Two test suites (40 tests, all passing) take the radius as the generating variable and propagate it, through standard physical relations, to geometry, polarizability, bonding, magnetism, chemical trends, materials classification, lattice energetics, optics and thermomechanical behaviour. The answer is that the system is strongly overdetermined: one radius per element reproduces many independently measured quantities, most to within a few per cent.

The work has a clear boundary. The effective nuclear charges that set the radius are taken from Clementi's tabulated screening values, and the downstream relations (Born–Landé, Clausius–Mossotti, Mulliken, Pearson) are established physics. What the suites test is the internal consistency of the vortex picture: that a single geometric quantity, interpreted as the vortex radius, carries this much of the chemistry. Deriving the screening itself from the $K = 4$, $D = 3$ geometry is the open problem that would make the chain parameter-free.

## The atomic picture

The companion folder [`atom-vortex-horizon/`](../atom-vortex-horizon/) (40 tests) establishes the starting point.

- **Same equation, two scales.** The galactic relation $v^4 = GM\,(v^2/r + a_0)$ and the atomic relation $v^4 = (kZe^2/m_e)\,(v^2/r + a_{0v})$ have the same form. Only the coupling constant and the transition acceleration differ.
- **The atomic transition scale.** At the Bohr radius, the Coulomb acceleration $ke^2/(m_e a_0^2)$ and the centripetal acceleration $v_{\mathrm{Bohr}}^2/a_0$ are equal. Both are $\alpha^3 m_e c^3/\hbar \approx 9.04 \times 10^{22}$ m/s². GFD identifies this as the atomic counterpart $a_{0v}$ of the galactic scale $a_0$.
- **The radius.** The outermost tile sits at $r = n^2 a_0 / Z_{\mathrm{eff}}$, with $n$ the shell number and $Z_{\mathrm{eff}}$ the net vortex flux reaching it. With Clementi's $Z_{\mathrm{eff}}$ this matches Clementi's calculated radii for $Z = 1$–20 to about 1%. That agreement holds largely by construction (see *Baselines* below): Clementi's radii are the maxima of Slater-type orbitals, which lie at exactly $n^2 a_0/Z_{\mathrm{eff}}$.

## Method

Each property is computed from the radius, or from quantities that follow from it, using a standard relation. Each test then compares the result with measured data and passes only if a stated threshold is met.

```
  Atomic number Z
       │
       ▼
  Net vortex flux Z_eff  (Clementi screening)
       │
       ▼
  Vortex radius r = n² a₀ / Z_eff ─────────────── ≈ 1% vs Clementi radii (by construction)
       │
       ├──→ Polarizability α ∝ r^2.57 ──────────── R² > 0.99
       │         ├──→ Refractive index (Clausius–Mossotti) ── 5.6%
       │         ├──→ C₆ dispersion ranking ────── ρ > 0.95
       │         └──→ Molar refractivity ───────── < 2% (noble gases)
       │
       ├──→ Chemical hardness η ∝ 1/r ───────────── r > 0.93
       │         └──→ metal / semiconductor / insulator
       │
       ├──→ Bond length d = a₀ √(2 Z_eff) / BO^¼ ─── < 1.5% (N–N family)
       │
       └──→ Ionic radii
                 ├──→ Lattice constant ─────────── 1.1%
                 ├──→ Lattice energy (Born–Landé)  4.5%
                 ├──→ Bulk modulus (1:1 salts) ─── 4.0%
                 └──→ Crystal structure from radius ratio
```

## Results

### Atomic properties: [`gfd_vortex_overdetermined_20.py`](gfd_vortex_overdetermined_20.py), 20/20

| Section | Finding |
|---|---|
| **K. Geometry** | Circumference, cross-section and volume follow from $r$. Atomic volume reproduces the periodic saw-tooth first noted by Lothar Meyer (1870): a jump at each alkali metal, contraction to each noble gas. |
| **L. Polarizability** | $\log\alpha$ against $\log r$ gives $R^2 > 0.99$ across $Z = 1$–20, with $\alpha \propto r^{p}$, $2.4 < p < 2.8$ (best fit 2.57). Ordering within every period is exact. |
| **M. Bond lengths** | $d(\mathrm{H{-}H}) = a_0\sqrt 2 = 74.8$ pm against 74.14 pm observed (0.9%). The nitrogen single, double and triple bonds are reproduced to within 1.5% from one $Z_{\mathrm{eff}}$ and the bond-order scaling $\mathrm{BO}^{-1/4}$, the same fourth-power law as the Tully–Fisher relation. |
| **N. Magnetism** | The Bohr magneton $e\hbar/2m_e$ equals the circulation moment $e\,v_{\mathrm{Bohr}}\,a_0/2$ exactly. The orbital moment at shell $n$ is $n\,\mu_B$, independent of $Z_{\mathrm{eff}}$. |
| **O. Chemical trends** | $Z_{\mathrm{eff}}/r^2$ correlates with Pauling electronegativity ($r > 0.89$). The radius alone assigns every element from $Z = 1$ to 20 to its reactivity class. |

### Compound properties: [`gfd_vortex_enterprise_20.py`](gfd_vortex_enterprise_20.py), 20/20

Tested against ten well-characterised rocksalt compounds.

| Property | Relation | Mean error |
|---|---|---|
| Lattice constant | $a = 2(r^+ + r^-)$ | 1.1% |
| Lattice energy | Born–Landé | 4.5% |
| Bulk modulus, singly charged ions | second derivative of Born–Landé | 4.0% |
| Refractive index | Clausius–Mossotti | 5.6% |
| Work function, alkali and alkaline-earth metals | $\approx 0.93 \times$ Mulliken electronegativity | about 5% |

The compound suite also verifies a set of correct orderings: band gaps (fluorides > chlorides > bromides; Li > Na > K salts), melting points (MgO > CaO > all 1:1 compounds), the anti-correlation of thermal expansion with melting point ($r > 0.95$), electrode potentials, hydration energies and the solubility of the sodium halides. A cross-property check confirms that the chain $r_{\mathrm{ion}} \to a \to U \to B \to n$ is self-consistent for each compound.

### Exact relations

Two results are identities rather than fits. The Bohr magneton equals the circulation moment of the ground-state vortex, and the Coulomb and centripetal accelerations at the Bohr radius coincide. Both hold within the Bohr model by construction; GFD's contribution is to read them as properties of the vortex.

## Baselines: what the vortex formulation adds

[`baseline_comparison.py`](baseline_comparison.py) scores each GFD result against standard alternatives, using reference data collected in [`data/atomic_reference.csv`](data/atomic_reference.csv) with sources in [`data/SOURCES.md`](data/SOURCES.md).

**Radii.** The suites compare $r = n^2 a_0/Z_{\mathrm{eff}}$ with Clementi's calculated radii. For a Slater-type orbital the radial density peaks at $r = n/\zeta = n^2 a_0/Z_{\mathrm{eff}}$, and Clementi's radii are defined as that peak, so the 1% agreement is a consistency check, not an independent prediction. Against an independent, empirical radius scale (the covalent radii of Cordero et al. 2008), with one scale factor fitted for each model:

| Model | Typical deviation (log-RMS) | Rank correlation |
|---|---|---|
| $n^2 a_0/Z_{\mathrm{eff}}$ with Clementi's $Z_{\mathrm{eff}}$ (GFD) | 0.24 | 0.955 |
| Slater's rules (1930), effective $n^*$ | 0.29 | 0.961 |
| Slater's rules, integer $n$ | 0.32 | 0.961 |

The GFD formulation tracks the independent radii somewhat better than Slater's rules. That advantage comes from Clementi's self-consistent-field screening, which the formula takes as input.

**Polarisability.** A power law in the radius, $\alpha = 4.49\,r^{2.57}$ (two fitted parameters), describes all twenty elements with a typical deviation of 14%. A classical $\alpha = r^3$ with no fitted parameter fails badly; a fitted $s\,r^3$ gives 29%. In a hold-out test, fitting on $Z = 1$–10 and predicting $Z = 11$–20, the power law gives 21% against 45% for $s\,r^3$. The relation is real and predictive, but it would hold for any accurate radius; it is not specific to GFD.

**The H–H bond.** $a_0\sqrt 2 = 74.84$ pm is 0.94% from the measured 74.14 pm. Of 129 comparably simple expressions $a_0\,(p/q)^k$ ($p, q \le 8$; $k = 1, \tfrac12, \tfrac13$), two come as close, and $a_0 \cdot 7/5$ is closer. The result is distinctive but not unique, so it carries weight only together with the threshold argument ($x = K$) that selects it.

**What this means.** As it stands, the chain's predictive content enters through Clementi's screening constants. The vortex picture organises the results coherently, but the step that would make them GFD's own is deriving $Z_{\mathrm{eff}}$, or the screening, from $K = 4$, $D = 3$ geometry. That is the programme's central open target.

## Limitations

The suites are explicit about where the radius stops being sufficient.

- **Screening is an input.** $Z_{\mathrm{eff}}$ comes from Clementi's tables. The values that reproduce radii differ from those that reproduce ionisation energies, by a factor falling from 1.0 at hydrogen to about 0.4 at neon. That ratio encodes how the outer structure relaxes when a tile is removed, and until it is derived, ionisation energies, and the hardness and Mulliken electronegativity built on them, depend on measured inputs.
- **Lattice dynamics.** The static dielectric constant is overestimated by about 67%, because it depends on ionic displacement in the lattice, which a sum of polarisabilities cannot capture.
- **Doubly charged ions.** Born–Landé overestimates the bulk modulus of MgO and CaO by 66–70%.
- **Quantitative melting points and band gaps.** Both are ranked correctly, but magnitudes are off by about 20%. They depend on liquid-phase entropy and on band structure, which a ground-state radius does not contain.
- **Coverage.** Validation spans $Z = 1$–20 and ionic compounds. Transition metals, covalent networks and metallic alloys remain untested.

## Running the tests

```bash
python gfd_vortex_overdetermined_20.py     # 20/20: atomic properties
python gfd_vortex_enterprise_20.py         # 20/20: compound properties
python baseline_comparison.py              # GFD against standard baselines
python ../atom-vortex-horizon/gfd_vortex_horizon_20.py       # 20/20: the vortex picture
python ../atom-vortex-horizon/gfd_vortex_horizon_ext_20.py   # 20/20: extended horizon
```

All four suites were run for this README and pass (80/80). A second atomic suite referred to in the synthesis, `gfd_vortex_overdetermined_p2_20.py` (materials classification, dispersion, lattice energies and reaction energetics; sections P–T), is not present in the repository.

## Contents

| File | Contents |
|---|---|
| [`gfd_overdetermined_synthesis.md`](gfd_overdetermined_synthesis.md) | Full synthesis of the overdetermined programme: every section, the industrial pipeline, results and gaps |
| [`gfd_vortex_overdetermined_20.py`](gfd_vortex_overdetermined_20.py) | Atomic-property suite, sections K–O |
| [`gfd_vortex_enterprise_20.py`](gfd_vortex_enterprise_20.py) | Compound-property suite, sections U–Y |
| [`baseline_comparison.py`](baseline_comparison.py) | Scores the GFD results against Slater's rules, independent covalent radii, $r^3$ baselines, a hold-out test and a look-elsewhere test |
| [`data/atomic_reference.csv`](data/atomic_reference.csv) | All reference values in one file, with [`data/SOURCES.md`](data/SOURCES.md) giving the source of each column |

## Context within the GFD programme

The atomic results sit among the programme's broader claims, each developed elsewhere in the archive:

| Claim | Where it is developed |
|---|---|
| Galaxy rotation curves from the constitutive law, without dark matter | [`papers/letter-radial-acceleration-relation-sparc/`](../../papers/letter-radial-acceleration-relation-sparc/) |
| The weakness of gravity as coupling depth, $G = (17/13)\,\alpha^{21}\,\hbar c/m_e^2$ | [`g_from_topology/`](../g_from_topology/), Paper VI |
| Three spatial dimensions selected by $2(D+1) = 2^D$ | [`field-closure/`](../field-closure/), Paper IX |
| Nuclear magic numbers and binding energies from tetrahedral packing | Papers XI and XIII; [`bound-gravity-and-packing/`](../bound-gravity-and-packing/) |
| The same law governing galaxies and atoms | this folder and [`atom-vortex-horizon/`](../atom-vortex-horizon/) |
| The electron as an illuminated tile; shell capacity $2n^2$ | this folder; [`valance-shells-nailed/`](../valance-shells-nailed/) |
| The fine-structure constant and the cosmological constant from $K = 4$ | exploratory notes, not validated here |

---

## References

- Born, M. and Landé, A. (1918). Über die absolute Berechnung der Kristalleigenschaften mit Hilfe Bohrscher Atommodelle. *Sitzungsber. Preuss. Akad. Wiss.*, 1048.
- Clementi, E. and Raimondi, D. L. (1963). Atomic screening constants from SCF functions. *J. Chem. Phys.* 38, 2686.
- Cordero, B. et al. (2008). Covalent radii revisited. *Dalton Trans.*, 2832.
- Clementi, E., Raimondi, D. L. and Reinhardt, W. P. (1967). Atomic screening constants from SCF functions. II. *J. Chem. Phys.* 47, 1300.
- Meyer, L. (1870). Die Natur der chemischen Elemente als Function ihrer Atomgewichte. *Ann. Chem. Pharm.* Suppl. 7, 354.
- Mulliken, R. S. (1934). A new electroaffinity scale. *J. Chem. Phys.* 2, 782.
- Parr, R. G. and Pearson, R. G. (1983). Absolute hardness: companion parameter to absolute electronegativity. *J. Am. Chem. Soc.* 105, 7512.
- Pearson, R. G. (1963). Hard and soft acids and bases. *J. Am. Chem. Soc.* 85, 3533.
- Schwerdtfeger, P. and Nagle, J. K. (2019). 2018 Table of static dipole polarizabilities of the neutral elements in the periodic table. *Mol. Phys.* 117, 1200.
- Shannon, R. D. (1976). Revised effective ionic radii. *Acta Cryst.* A32, 751.
- Slater, J. C. (1930). Atomic shielding constants. *Phys. Rev.* 36, 57.
