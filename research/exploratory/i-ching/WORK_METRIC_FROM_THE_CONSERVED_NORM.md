# The Work Metric from the Conserved Norm

*Exploratory programme, Gravity Field Dynamics (GFD) · Field Dynamics Research · November 2026*

**Status:** exact finite algebra [T], with one stated physical premise. It closes the open condition of [work-metric rigidity](WORK_METRIC_RIGIDITY.md) without the factorised-chamber assumption. It does not derive α, the determinant read, or the long-wave source action. Proof 26 is unchanged.

---

## What this settles, and why it matters

[Work-metric rigidity](WORK_METRIC_RIGIDITY.md) showed that the hexagram read algebra allows exactly two work weights on the 21 contrast directions: a on the exchange-even sector and b on the exchange-odd one. The ratio of the [orientation character](ORIENTATION_CHARACTER_AND_SEED_DUAL.md) is 17/13 exactly when a = b. That note left one question open: what forces a = b?

The answer here needs two things:

1. **Each address is an independent record.** The work metric has no cross terms between different addresses, so it is diagonal in the address basis.
2. **The complete Walsh read preserves work.**

Together they force the metric to be a scalar, hence a = b. The native flywheel dynamics already measures work this way: its conserved quantity is the plain Euclidean norm of its coordinates. So under GFD's own dynamics, the 17/13 ratio does not need an extra assumption about how the chambers factorise.

## 1. The flat-read theorem

**Theorem.** Let U be an orthogonal (or unitary) read on N records that is *flat*: |U_xz|² = 1/N for every x and z, so every coefficient sees every record with the same weight. If a work metric H is diagonal in the records and preserved by the read, UHUᵀ = H, then H is a multiple of the identity.

*Proof.* Write H = diag(h). The x-th diagonal entry of UHUᵀ is

$$\sum_z |U_{xz}|^2\, h_z = \frac1N \sum_z h_z = \bar h,$$

the same for every x. Invariance makes that entry equal to h_x, so every h_x = h̄. ∎

The hexagram Walsh read is flat with N = 64, both in its symplectic form and in its ordinary binary form. So any diagonal, read-preserved work metric on the 64 addresses is c·I. Restricted to the 21 contrast directions it stays c·I, so a = b = c. The weighted counts of the rigidity note then give

$$\frac{\operatorname{tr}(H P_0)}{\operatorname{tr}(H S_u)} = \frac{14c + 3c}{14c - c} = \frac{17}{13},$$

and the same ratio against the shared zone, for every one of the seven marked axes.

**What each hypothesis does:**
- **Flatness is essential.** The XOR read R is a permutation, so it preserves any diagonal metric that is constant on its orbits, including unequal ones. R alone cannot force a = b. The complete, unbiased Walsh read is what equalises the weights.
- **Diagonality is essential.** The rigidity note's metrics with a ≠ b are preserved by the Walsh read too. But each couples every hexagram (a, b) to its exchange (b, a), so it is not diagonal in the records.

## 2. The native dynamics measures work in that metric

The Field Origin vertex law in [the constitutive vertex](../../hadamard-null-cone-vortex-flywheel/vertex-research/CONSTITUTIVE_VERTEX.md) is

$$i\dot\psi = \bigl(H_0 + g(u)\,V\bigr)\psi,\qquad u = \tfrac12\,\psi^\dagger V\psi,$$

with Hermitian H₀ and V and a real, state-dependent gain g(u). Any Hermitian generator, even a nonlinear one through a real scalar gain, conserves exactly ψ†ψ. That is the Euclidean norm: diagonal in the coordinates, with every coordinate weighted equally. The chamber exchange is measured in the same norm, Ṅ_A = −Ṅ_B, and the note records that "the total norm of all coordinates is conserved".

So if registration counts the conserved, exchanged quantity, the occupation, the work metric is the identity on independent coordinates. Both hypotheses of the theorem hold, and a = b.

This also matches the framework's interpretation rules. Rule 13 says ownership is single-valued, so each record is owned once with no cross-record terms; that is diagonality. Proof 26's Theorem 3 shows the complete read is reversible; that is invariance.

## 3. The one premise, and where it could fail

The premise is that **what is registered is occupation, not energy.** The energy ψ†H₀ψ also defines a quadratic form, but it couples different coordinates through the cross kernel. It is not diagonal in the records, so the theorem does not apply to it, and an energy-weighted register could give a ≠ b. Registration recording inventory (how much each record holds) rather than stiffness (how hard it is to move) is the natural reading of Rules 12 and 13. It is still a premise, and it is the only one this note needs.

**Also open:**
- **The address count.** The native Stage VII model resolves 16 amplitudes per chamber. The 64-address register is Proof 23's depth-two refinement. The theorem needs only that the registered records are orthonormal coordinates in the conserved norm, but the explicit embedding of the 64 records into the native coordinates is not yet written.
- **The rest of G.** The determinant read, the gain |t|² = α and the long-wave source action are untouched.

## 4. Where this leaves the 17/13 chain

| Step | Status |
|---|---|
| 21, 17, 13 as dimension, positive rank and trace of one orientation operator | [T], [orientation character](ORIENTATION_CHARACTER_AND_SEED_DUAL.md) |
| The 17 register forced by the Walsh dual of the dependent seed | [T], same note |
| The weighted ratio is 17/13 exactly when a = b | [T], [work-metric rigidity](WORK_METRIC_RIGIDITY.md) |
| a = b from independent records and a work-preserving complete read | [T], this note |
| The native dynamics registers in exactly that metric, if registration counts occupation | [D], one stated premise |

## Verify

`python -m pytest -q scripts/finite_field_reciprocity/test_conserved_norm_metric.py` — 19 tests. They cover:
- both Walsh reads are orthogonal and flat;
- the diagonal of a conjugated diagonal metric is its mean, so only scalar diagonal metrics are preserved;
- the XOR read alone fails to force a scalar;
- the a ≠ b metrics are read-invariant but couple each hexagram to its exchange;
- the weighted counts 14a + 3b, 14a − b and 10a + 3b on all seven axes;
- 17/13 for a scalar metric on every axis;
- a nonlinear Hermitian flow with a real state-dependent gain conserves the Euclidean norm while exchanging occupation between the chambers.
