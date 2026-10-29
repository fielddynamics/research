# Electron Configurations from Tetrahedral Topology

*Sub-shell structure, filling order and the transition-metal exceptions from the K = 4 channel hierarchy · Gravity Field Dynamics (GFD) · Field Dynamics Research*

`atomic-physics` `electron-configuration` `periodic-table` `madelung-rule` `angular-momentum` `so3`

---

## Summary

The ground-state electron configurations of the elements follow three layers of structure. Sub-shells hold 2, 6, 10 and 14 electrons. They fill in the Madelung order, by increasing $n + l$ and then increasing $n$. And a minority of elements, mostly transition metals, depart from that order: chromium is $3d^5 4s^1$ rather than $3d^4 4s^2$, copper $3d^{10} 4s^1$ rather than $3d^9 4s^2$.

This folder derives all three layers from the $(3+1) \times (3+1) = 16$ coupling channels of the stellated octahedron, with no fitted parameter. The analysis below separates what the derivation establishes, what it leaves open, and why the open part fails where it does.

| Layer | Status |
|---|---|
| Sub-shell capacities $2(2l+1)$ and shell capacity $2n^2$ | Derived; exact |
| Madelung filling order | Derived; correct for 70 of 83 elements |
| Exceptions from coupling-polynomial landmarks | The landmarks $f = 13, 17, 21$ correspond to empty, half-filled and full sub-shells; applied as a rule, they give **76 of 83**, against a ceiling of **77** for any rule of this kind; random landmarks of the same number never do as well |
| Exceptions from the mod-$K$ landmark (tier 2) | Resolves Nb and Rh but wrongly changes seven elements; net loss |
| Remaining seven elements | Require a row-dependent energy term the framework does not yet contain |

---

## 1. The derivation

### 1.1 Capacities

Each face of the tetrahedron carries $K = D + 1 = 4$ channels: three spatial and one gate. At Sierpiński depth $d$ the gate is excluded, and the $3^d$ spatial channels form the $d$-fold tensor product of the vector representation of SO(3). Each depth contributes one new irreducible representation, of angular momentum $l = d$ and dimension $2l + 1$:

$$3 \otimes 3 = 1 \oplus 3 \oplus \mathbf{5}, \qquad 3 \otimes 3 \otimes 3 \supset \mathbf{7}.$$

With the factor 2 from the two time-face orientations, the capacities are $2(2l+1) = 2, 6, 10, 14$, and the shell sum $\sum_{l=0}^{n-1} 2(2l+1) = 2n^2$.

### 1.2 Filling order

A sub-shell $(n, l)$ is reached through $n$ radial face-crossings and $l$ angular depth iterations, so its coupling cost is $n + l$. Filling by increasing cost, with lower $n$ first at equal cost, is Madelung's rule. It is correct for 70 of the 83 stable elements.

### 1.3 Landmarks for the exceptions

The coupling polynomial $f(K, s) = 1 + Ks + K^2$ takes the values 13, 17 and 21 at the TetB cavity, the Field Origin and the TetA exterior. Evaluated at the fractional filling $p = n_e / C$ of a sub-shell of capacity $C$,

$$f_1 = 13 + 8p,$$

the three landmarks fall at $p = 0$, $\tfrac12$ and $1$: the empty, half-filled and full sub-shell (**tier 1**). Two further landmark sets are defined: occupancies that are multiples of $K = 4$, one complete tetrahedral face (**tier 2**), and the same polynomial on the 16-channel grid (**tier 3**). An s sub-shell, with capacity 2, sits on a tier-1 landmark at every occupancy, so it is neutral, and the d or f sub-shell decides.

**The promotion rule.** An electron moves from the s sub-shell into the d or f sub-shell when that moves the d or f occupancy onto a higher tier.

The validator [`gfd_electron_config.py`](gfd_electron_config.py) shows that among the 13 Madelung exceptions the measured configuration sits on a higher tier than the Madelung one in 10 cases (Cr, Cu, Mo, Ag, Au, Pd, La, Gd by tier 1; Nb, Rh by tier 2). Ru, Ce and Pt are not resolved.

---

## 2. What is notable

**The capacities are a derivation, not an input.** The numbers 2, 6, 10, 14 normally come from solving the Schrödinger equation in a central potential. Here they follow from counting channels on a tetrahedral face and reducing the tensor products by SO(3), with the gate exclusion supplying the step from $3^d$ to $2l+1$.

**The polynomial's landmarks coincide with the physical ones.** In standard atomic physics, half-filled and full sub-shells are favoured because exchange energy peaks there (Hund's rules). In GFD the same three occupancies are the three values the coupling polynomial is built from: the cavity (13), the Field Origin (17) and the exterior (21). The half-filled shell sits at the Field Origin. Nothing was adjusted to make these occupancies special.

**The landmarks carry most of the explanatory power available.** Applied as a rule to all 83 elements, tier 1 alone gives 76 correct configurations: it fixes seven exceptions (Cr, Cu, Mo, Ag, Au, La, Gd) and wrongly changes one element (W). As section 4 shows, no rule that sees only the sub-shell occupancy can exceed 77. In 5,000 trials with three randomly chosen landmarks per sub-shell, none reached 76 ($p < 0.0002$).

---

## 3. Testing the rule on every element

A rule that resolves exceptions must also leave the other elements alone. The validator scores the rule on a fixed list of the 13 exceptions; it does not apply the rule to the 70 elements that Madelung's rule already gets right. [`promotion_rule_check.py`](promotion_rule_check.py) applies the rule to all 83: start from the Madelung configuration and move one electron from $ns$ to $(n-1)d$, or from $(n-2)f$ to $(n-1)d$, whenever that raises the d or f sub-shell's tier.

| Rule applied to all 83 elements | Correct | Exceptions fixed | Correct Madelung configurations changed |
|---|---|---|---|
| Madelung's rule alone | 70 | — | — |
| All three tiers | 71 | Cr, Cu, Nb, Mo, Rh, Ag, La, Gd, Au | V, Co, Ta, W, Ir, Pm, Tb, Tm |
| **Tier 1 only** | **76** | Cr, Cu, Mo, Ag, La, Gd, Au | W |
| Ceiling for any occupancy-only rule (section 4) | 77 | | |

The 80 of 83 in the synthesis is 70 (Madelung) plus 10 (resolved exceptions). It counts the 70 without asking whether the rule would change them. Applied to every element, tier 2 changes seven of them.

---

## 4. Why the rule fails where it does

### 4.1 A ceiling for every occupancy-only rule

The tiers depend only on how many electrons occupy the sub-shell. Any such rule must therefore treat alike all elements that start from the same Madelung occupancy. The measured configurations do not:

| Madelung start | Keeps the Madelung configuration | Promotes |
|---|---|---|
| $d^3 s^2$ | V, Ta | Nb |
| $d^4 s^2$ | W | Cr, Mo |
| $d^6 s^2$ | Fe, Os | Ru |
| $d^7 s^2$ | Co, Ir | Rh |
| $d^8 s^2$ | Ni | Pd ($d^{10}$), Pt ($d^9 s^1$) |

Whatever a rule decides for $d^3 s^2$, it gets vanadium or niobium wrong. Across the five rows at least six elements must be wrong, so **no rule that sees only the occupancy can score above 77 of 83**. The limit holds for any choice of landmarks, tiers or tie-breaks. Tier 1 reaches 76, one short of it.

### 4.2 What the ceiling points to: the row

The elements that defeat an occupancy-only rule share a pattern. They are separated by row, not by occupancy:

- **The 4d row promotes more readily.** Nb, Ru, Rh and Pd all move an electron out of 5s, while their 3d and 5d counterparts (V, Fe, Co, Ni; Ta, Os, Ir) do not. In the fifth row the 4d and 5s energies lie unusually close, so a promotion costs little even when no landmark is gained.
- **The 5d row resists promotion.** Tungsten keeps $5d^4 6s^2$ although $5d^5 6s^1$ would be half-filled, as chromium and molybdenum are. In the sixth row the 6s orbital is contracted and stabilised by relativistic effects, the same effect behind the colour of gold, which raises the cost of emptying it. Platinum's $5d^9 6s^1$ sits on the boundary of the same balance.
- **Near-degenerate cases.** For Ru, Ce and Pt the competing configurations lie within a few hundredths of an electronvolt. At that scale the measured ground state is set by fine energy differences that no counting rule captures.

In energy terms, a promotion occurs when the stabilisation gained at a landmark exceeds the cost of moving the electron, $\Delta E_{\mathrm{gain}} > \varepsilon_{(n-1)d} - \varepsilon_{ns}$. The landmarks supply the first term. The second varies with the row, and the framework does not yet supply it.

### 4.3 Why tier 2 makes things worse

Tier 2 marks every multiple of four electrons. That resolves Nb ($d^4$) and Rh ($d^8$), but the same marks attract V and Ta towards $d^4$, Co and Ir towards $d^8$, and the lanthanides Pm, Tb and Tm towards $f^4$, $f^8$ and $f^{12}$, none of which occurs. Tier 2 fixes two exceptions and creates seven errors. Nb and Rh are 4d-row elements, so on the evidence of section 4.2 the row explains them better than a mod-4 landmark does.

---

## 5. What remains open

1. **A row-dependent term.** Derive, from the $K = 4$ structure, a quantity that changes from the 3d to the 4d to the 5d row: the $ns$–$(n-1)d$ gap, or a structural proxy for it. Combined with tier 1, such a term could reach above 77 and is the step that would make the exceptions a prediction.
2. **The status of tier 2.** Tier 2 is better dropped unless a physical reason is found for it to act only in the 4d row.
3. **Energies, not only labels.** Promotion energies are measured for every transition metal. A version of the rule that predicts them, not only the resulting configuration, would be a much stronger test.
4. **Heavier elements.** The rule has been scored on the 83 stable elements. The actinides and superheavy elements, where relativistic effects dominate, would test any row-dependent term out of sample.

---

## Running

```bash
python gfd_electron_config.py      # capacities, Madelung order, the 13 exceptions
python promotion_rule_check.py     # every element; tier ablation; the 77 ceiling; chance test
```

Both use the Python standard library only.

## Contents

| File | Contents |
|---|---|
| [`gfd_electron_config_synthesis.md`](gfd_electron_config_synthesis.md) | The full derivation: channel structure, capacities, Madelung order, the three tiers and each exception |
| [`gfd_electron_config.py`](gfd_electron_config.py) | Validator for the derivation, scored on the 13 exceptions |
| [`promotion_rule_check.py`](promotion_rule_check.py) | The rule applied to all 83 elements, tier ablation, the occupancy-only ceiling and a look-elsewhere test |

## Related work

- [`atomic-properties/`](../atomic-properties/): the vortex-radius programme and pre-registered tests of electron screening from the constitutive law. Configurations from this folder supply the shell occupancies those tests use.
- [Paper 11](../../papers/11-nuclear-shells-tetrahedral-packing/): the nuclear counterpart, magic numbers from tetrahedral packing with gate exclusion.

## References

- Madelung, E. (1936). *Mathematische Hilfsmittel des Physikers*, 3rd ed. Springer.
- Hund, F. (1925). Zur Deutung verwickelter Spektren. *Z. Phys.* 33, 345.
- Pyykkö, P. (1988). Relativistic effects in structural chemistry. *Chem. Rev.* 88, 563.
- Kramida, A., Ralchenko, Yu., Reader, J. and NIST ASD Team. *NIST Atomic Spectra Database*. Ground-state configurations.
