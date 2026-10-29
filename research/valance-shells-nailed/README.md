# Electron Configurations from Tetrahedral Topology

*Sub-shell structure and filling order from the K = 4 channel hierarchy · Gravity Field Dynamics (GFD) · Field Dynamics Research*

`atomic-physics` `electron-configuration` `periodic-table` `madelung-rule` `angular-momentum` `so3`

---

## Summary

This folder derives the structure of the periodic table's electron shells from the $(3+1) \times (3+1) = 16$ coupling channels of the stellated octahedron. It does three things:

1. **Sub-shell capacities.** At each Sierpiński depth $d$, the gate-excluded spatial channels form the $d$-fold tensor product of the 3-dimensional vector representation of SO(3). The new highest irreducible representation at depth $d$ has dimension $2l+1$ with $l = d$, and the factor 2 from the two time-face orientations gives the capacities 2, 6, 10, 14 (s, p, d, f) and the shell capacity $2n^2$.
2. **Filling order.** The energy cost of sub-shell $(n, l)$ is counted as $n$ radial face-crossings plus $l$ angular depth iterations, which gives the Madelung $(n+l, n)$ order. Madelung's rule is correct for 70 of the 83 stable elements.
3. **Exceptions.** A three-tier resonance rule built on the coupling polynomial, $f_1 = 13 + 8\,(n_e/C)$, marks favoured sub-shell occupancies: empty, half-filled and full ($f_1 \in \{13, 17, 21\}$, tier 1), and multiples of $K = 4$ electrons (tier 2). The observed configuration sits on a higher tier than the Madelung one in 10 of the 13 Madelung exceptions (Cr, Cu, Mo, Pd, Ag, La, Gd, Au, Nb, Rh). Ru, Ce and Pt are not resolved.

Steps 1 and 2 reproduce standard structure: the capacities are those of quantum-mechanical angular momentum, and the order is Madelung's. Step 3 is the new content, and the section below tests it.

## Testing the resonance rule generatively

[`gfd_electron_config.py`](gfd_electron_config.py) scores the rule on the 13 exceptions alone, comparing the tier of the Madelung occupancy with the tier of the observed one. A predictive rule must also leave the other 70 elements alone. [`promotion_rule_check.py`](promotion_rule_check.py) therefore applies the rule, as stated in the synthesis, to all 83 elements: start from the Madelung configuration and move an electron from $ns$ to $(n-1)d$, or from $(n-2)f$ to $(n-1)d$, whenever that moves the d/f sub-shell to a higher tier.

| Version of the rule | Correct (of 83) | Exceptions fixed | Exceptions missed | Correct Madelung configurations changed |
|---|---|---|---|---|
| Madelung alone | 70 | — | 13 | — |
| One electron (literal reading) | **71** | 9 | Ru, Pd, Ce, Pt | 8: V, Co, Ta, W, Ir, Pm, Tb, Tm |
| Up to two electrons | 65 | 9 | Nb, Ru, Ce, Pt | 14 |
| Up to two, plus $s \to f$ | 62 | 9 | Nb, Ru, Ce, Pt | 17 |

Applied generatively, the rule gains one element over Madelung's rule, not ten. The same tier landmarks that favour Cr ($3d^5$) and Nb ($4d^4$) also favour $3d^4$ for vanadium, $3d^8$ for cobalt, $5d^4$ for tantalum and $5d^5$ for tungsten, and in each of those elements nature keeps the Madelung configuration.

The tiers still carry real information. They mark 5 of the 11 possible d occupancies and 6 of the 15 f occupancies as resonant. Random landmark sets of the same sizes, run through the same one-electron rule, reach 71 or more correct in 2.5% of 5,000 trials. The half-filled and filled landmarks are in the right places; what the rule lacks is the energy scale that decides when a promotion is worth its cost. Real configurations depend on small differences between the $ns$ and $(n-1)d$ orbital energies, and those differences change with $Z$.

## Running

```bash
python gfd_electron_config.py      # capacities, Madelung order, the 13 exceptions
python promotion_rule_check.py     # the rule applied to all 83 elements, with a chance test
```

Both use the Python standard library only.

## Contents

| File | Contents |
|---|---|
| [`gfd_electron_config_synthesis.md`](gfd_electron_config_synthesis.md) | The full derivation: channel structure, capacities, Madelung order, the three tiers and each exception |
| [`gfd_electron_config.py`](gfd_electron_config.py) | Validator for the derivation, scored on the 13 exceptions |
| [`promotion_rule_check.py`](promotion_rule_check.py) | Generative test of the resonance rule over all 83 elements, with a look-elsewhere test |

## Related work

- [`atomic-properties/`](../atomic-properties/): the vortex-radius programme, and pre-registered tests of screening derived from the constitutive law. Configurations from this folder supply the shell occupancies those tests need.
- [Paper 11](../../papers/11-nuclear-shells-tetrahedral-packing/): the nuclear counterpart, magic numbers from tetrahedral packing with gate exclusion.
