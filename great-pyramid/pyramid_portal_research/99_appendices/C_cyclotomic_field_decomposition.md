# Appendix C — Cyclotomic Field Decomposition

**Status:** Reference / structural
**Reading time:** 5 minutes
**Depends on:** 01.1

---

## Statement

The 21st cyclotomic field factors as

$$
\boxed{\mathbb Q(\zeta_{21}) \cong \mathbb Q(\zeta_3) \otimes_{\mathbb Q} \mathbb Q(\zeta_7)}
$$

reflecting the apparatus's $\mathbb Z_3 \times \mathbb Z_7$ symmetry. This is a load-bearing identity for the framework: it explains why the 21-fold structure factors into a $3$-part (cyclotomic, antechamber) and a $7$-part (Grand Gallery corbels).

## Statement at the level of groups

The cyclic group $\mathbb Z_{21}$ factors:

$$
\mathbb Z_{21} \cong \mathbb Z_3 \times \mathbb Z_7
$$

because $\gcd(3, 7) = 1$. This is the Chinese Remainder Theorem at the level of cyclic groups.

The Galois group of $\mathbb Q(\zeta_{21}) / \mathbb Q$ is $(\mathbb Z/21\mathbb Z)^\times \cong \mathbb Z_2 \times \mathbb Z_6$, of order $\varphi(21) = 12$.

## Statement at the level of polynomials

The cyclotomic polynomial $\Phi_{21}(x)$ factors as

$$
\Phi_{21}(x) = \prod_{\substack{1 \le k \le 20 \\ \gcd(k, 21) = 1}} (x - \zeta_{21}^k)
$$

There are $\varphi(21) = 12$ such $k$ values: $\{1, 2, 4, 5, 8, 10, 11, 13, 16, 17, 19, 20\}$. So $\Phi_{21}$ has degree 12.

Explicitly:

$$
\Phi_{21}(x) = x^{12} - x^{11} + x^9 - x^8 + x^6 - x^4 + x^3 - x + 1
$$

## Connection to the apparatus

Each $\mathbb Z_{21}$ representation can be uniquely written as the **tensor product** of a $\mathbb Z_3$ rep and a $\mathbb Z_7$ rep:

$$
\rho_{(a, b)} = \rho_a^{\mathbb Z_3} \otimes \rho_b^{\mathbb Z_7}
$$

with $a \in \{0, 1, 2\}$ and $b \in \{0, 1, \ldots, 6\}$.

In the apparatus:

- $a \in \mathbb Z_3$ corresponds to the **antechamber filter** with three portcullis grooves ([04.6](../04_apparatus_engineering/04.6_antechamber_Z3_filter.md))
- $b \in \mathbb Z_7$ corresponds to the **Grand Gallery corbel index** ([04.5](../04_apparatus_engineering/04.5_grand_gallery_kernel.md))

The portal protocol's address $(a, b)$ thus has a direct geometric interpretation in the pyramid.

## Subfield lattice

The lattice of subfields of $\mathbb Q(\zeta_{21})$ corresponds (Galois) to the lattice of subgroups of $(\mathbb Z/21\mathbb Z)^\times \cong \mathbb Z_2 \times \mathbb Z_6$:

```
                       Q(ζ_21)
                      /        \
                  Q(ζ_3, √-7)  Q(√-3, ζ_7)
                  /              \
              Q(ζ_3)            Q(ζ_7)
                  \              /
                   Q(√-3)    Q(√-7)
                      \      /
                       Q(√21)
                         |
                         Q
```

(Schematic; not all intermediate fields shown.)

This rich subfield structure can be exploited for selection rules in the portal protocol: applying a projector onto, say, $\mathbb Q(\zeta_3) \subset \mathbb Q(\zeta_{21})$ restricts the active states to those invariant under the $\mathbb Z_7$ part.

## Idempotent decomposition

The group algebra $\mathbb C[\mathbb Z_{21}]$ decomposes as a direct sum of 21 one-dimensional representations:

$$
\mathbb C[\mathbb Z_{21}] = \bigoplus_{j = 0}^{20} \mathbb C \cdot e_j
$$

where the idempotents $e_j$ project onto the $j$-th character:

$$
e_j = \frac{1}{21} \sum_{k = 0}^{20} \zeta_{21}^{-jk} g^k
$$

with $g$ a generator of $\mathbb Z_{21}$.

Each $e_j$ corresponds to one of the 21 sectors and **commutes** with all the others. The apparatus's 21-mode comb (when present) corresponds to the 21 idempotents $\{e_j\}_{j=0}^{20}$.

In the $(a, b)$ labeling, $j = 7a + 3b \pmod{21}$ (after applying the CRT isomorphism).

## The Z_3 "even" sector

In the WRT computation (per [03.6](../03_portal_topology/03.6_WRT_invariant_decomposition.md)), sectors with $a = 0$ **vanish**. These correspond to the trivial $\mathbb Z_3$ rep tensored with each of the 7 $\mathbb Z_7$ reps:

$$
(a, b) = (0, 0), (0, 1), \ldots, (0, 6)
$$

These 7 sectors do not contribute to the WRT invariant. Their cancellation reflects an algebraic symmetry of the Lawrence-Rozansky-Hikami formula (specifically, the Z_3 "even" sector lies in the kernel of the quadratic form mod the Gauss-sum factor).

The remaining 14 sectors arrange in **7 conjugate pairs** (under complex conjugation of $\zeta_{21}^j$). This 7-pair structure matches the 7 Grand Gallery corbels.

## Connection to the gravity equation

The gravity coupling $\alpha_G \propto (17/13) \alpha^{21}$ involves both:

- The factor $17/13 = \Phi_4(4)/\Phi_6(4)$ comparing the $s = 0$ and $s = -1$ graded identity traces
- The exponent $21 = \Phi_3(4) = \text{Tr}(I_{+1})$

Each cyclotomic value is a trace of one of the three idempotents $P_0, P_1, P_2$ acting on the closure space $C_4$. The product $(17/13) \alpha^{21}$ is therefore *not* arbitrary — it is the natural ratio of complementary cyclotomic projections.

This is the **deepest reason** the gravity equation comes out the way it does. See [02.1](../02_gravity_derivation/02.1_gravity_equation.md) for the full derivation.

## A useful identity

For computations in the apparatus:

$$
\sum_{j=0}^{20} \zeta_{21}^j = 0 \quad \text{(since } \zeta_{21} \neq 1\text{)}
$$

This implies that **arbitrary** sums over the 21 sectors with constant coefficients vanish. Nontrivial sums require sector-dependent weights (selection rules), which is exactly what the apparatus's $\mathbb Z_3$ filter provides.

This is why the antechamber's portcullis grooves are functionally essential: without them, the chamber's 21-mode comb would sum to zero and produce no output.

---

**Cross-references:**
- [01.1 Cyclotomic algebra](../01_framework_foundations/01.1_cyclotomic_algebra.md)
- [03.6 WRT invariant decomposition](../03_portal_topology/03.6_WRT_invariant_decomposition.md)
- [04.5 Grand Gallery kernel](../04_apparatus_engineering/04.5_grand_gallery_kernel.md)
- [04.6 Antechamber Z_3 filter](../04_apparatus_engineering/04.6_antechamber_Z3_filter.md)
