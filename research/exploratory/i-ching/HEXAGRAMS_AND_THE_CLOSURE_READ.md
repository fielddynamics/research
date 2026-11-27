# The Hexagrams and the Closure Read

*Exploratory programme, Gravity Field Dynamics (GFD) · Field Dynamics Research · November 2026*

`i-ching` `hexagrams` `finite-fields` `projective-plane` `walsh-hadamard` `closure`

---

## What this shows, and why it matters

[Proof 26](../../../proofs/recursive-field-closure-response/) reads a field object's 64 closure addresses with a three-sweep Walsh–Hadamard transform. An order-three rotation of its labels then leaves exactly 21 invariant directions, in grades of 1, 4 and 16. That 21 is the exponent in Newton's constant.

This note shows that **the 64 hexagrams of the *I Ching* carry that same read and that same 21**, through an operation the book's own line structure supplies:

- The rotation is multiplication by ω in the field F₄. On a hexagram, it acts on the three pairs of corresponding lines (1 & 4, 2 & 5, 3 & 6), the lines the classical commentaries relate to each other (應, *ying*).
- It moves every hexagram except one. The other 63 fall into 21 orbits, in grades of 1, 4 and 16: the points of the projective plane PG(2,4).
- The trigram families, the six individual lines and the one-line changes between trigrams are, exactly, the tetrahedra, octahedral core and core bonds of [Proofs 24](../../../proofs/flywheel-tetrad-geometry/) and [25](../../../proofs/tetrad-flywheel-convergence/).

It also separates what the hexagrams do *not* give. The book's other natural rotation, about the Heaven–Earth axis, gives 23 directions, not 21. And the π walk that settles the 64 hexagrams does not perform the read.

Status: the results below are exact finite algebra [T], checked by script. They connect this exploratory folder to Proofs 23–26. They are not evidence about gravity on their own: the *I Ching* gives another exact representation of the same address space, not an independent measurement.

## Conventions

As in [`scripts/closure_walk_proof_iching.py`](scripts/closure_walk_proof_iching.py), yang = 1 and a trigram's value is 4·bottom + 2·middle + top. So Earth ☷ = 0, Mountain ☶ = 1, Water ☵ = 2, Wind ☴ = 3, Thunder ☳ = 4, Fire ☲ = 5, Lake ☱ = 6, Heaven ☰ = 7. A hexagram is the pair (lower, upper), so there are 8 × 8 = 64. Adding trigrams means combining them line by line (XOR: two equal lines give yin, two different lines give yang).

## 1. A threefold map on the hexagrams

Define

$$R(a, b) = (b,\ a \oplus b).$$

The upper trigram moves down, and the new upper trigram is the line-by-line combination of the two. Applying R three times gives (a, b) → (b, a⊕b) → (a⊕b, a) → (a, b), so **R³ = I**.

R fixes only Earth over Earth: (a, b) = (b, a⊕b) forces a = b and a = 0. Its square fixes nothing else either. So the other 63 hexagrams fall into orbits of exactly three:

$$64 = 1 + 3 \times 21.$$

## 2. R is ω on the corresponding lines

Pair line *i* of the lower trigram with line *i* of the upper: bottom with fourth, second with fifth, third with sixth. Each pair has four states, which we write as x + yω in F₄ = {0, 1, ω, ω²}, where ω² = ω + 1.

On every pair, R acts as multiplication by ω:

$$\omega\,(x + y\omega) = y + (x + y)\,\omega.$$

So a hexagram is a vector in F₄³, one digit per corresponding pair, and R is the scalar ω. That is exactly the setting of Proof 26, whose label cycle is ω on each of its three digits. Proof 26's [Lean formalisation](../../../proofs/recursive-field-closure-response/LEAN_AUDIT.md) checks that cycle as `cycle_is_omega` and its 21 orbits as `invariant_directions`.

## 3. The three grades: 21 = 1 + 4 + 16

Give each hexagram a grade: the highest corresponding pair, counted from the bottom, that is not yin–yin. R preserves the grade, and the orbits per grade are

$$\frac{4-1}{3} = 1,\qquad \frac{16-4}{3} = 4,\qquad \frac{64-16}{3} = 16.$$

These are Proof 26's three invariant grades. On them, its collective determinant is

$$\det(T^{\dagger}T) = |t_1|^2\,|t_2|^8\,|t_3|^{32},$$

which gives α²¹ = α¹ · α⁴ · α¹⁶ when every gain is |t|² = α. That premise is stated in Proof 26 and is not established here.

## 4. A second reading: 21 = 7 + 14, the Fano subplane

The orbits also split by whether the two trigrams are dependent:

- **7 orbits of dependent pairs.** For each of the seven nonzero trigrams v, the orbit is {(v, Earth), (Earth, v), (v, v)}.
- **14 orbits of independent pairs.**

The seven dependent orbits are the points of PG(2,4) that are already defined over F₂. Together they form a **Fano plane**, PG(2,2), sitting inside PG(2,4) as a Baer subplane: every one of the 21 lines of PG(2,4) meets it in 1 or 3 points. This is the same relation that Proof 26's optional appendix uses one level up, with PG(2,4) as a Baer subplane of PG(2,16).

## 5. The other rotation gives 23, not 21

The *I Ching*'s geometric rotation turns the cube about the Heaven–Earth axis, which GFD calls TIME. It cycles the three line positions of both trigrams at once. Call it T.

- **It fixes Heaven and Earth and cycles the children by age.** Thunder, the eldest son, goes to Water, the middle son, and Water to Mountain, the youngest; the daughters cycle the same way.
- **It commutes with R.** The hexagram space is F₄ ⊗ F₂³: R acts on the first factor (across the two trigrams) and T on the second (within each trigram).
- **It fixes four hexagrams:** Earth and Heaven, over each other in each order. So it has 3 + 20 = 23 invariant directions, not 21. By Burnside's count its invariant dimension is 24, against 22 for R.

T is the ordered corner-pair action of the earlier π walk. [Proof 23](../../../proofs/recursive-triforce-closure/) proves that no rotation-equivariant correspondence exists between that action and its Triforce action. What this section adds is which operation on the hexagrams does give the Triforce count: R, not T. The physical question that remains is which of the two the time-face dynamics selects.

## 6. One Walsh read

Read a hexagram as six binary lines. Its Walsh–Hadamard transform is the same whether the lines are grouped as two trigrams or as three corresponding pairs:

$$H_8 \otimes H_8 = H_4 \otimes H_4 \otimes H_4 = H_2^{\otimes 6}.$$

The first grouping is the cube read twice, once per trigram. The second is Proof 26's three sweeps, one per corresponding pair. Proof 26 proves that the three sweeps commute and that the read is reversible (`three_sweeps`, `H64_sq`).

## 7. Families, lines and line changes are the flywheel's core

- **The two families are the two tetrahedra.** With Earth as zero, the mother and her daughters form a subspace, and the father and his sons are its other coset: TetB and TetA.
- **The six lines are the octahedral core.** Each core vertex of Proof 25, (sᵢ + sⱼ)/2, is the line two family members share. For example, Heaven and Thunder share a yang bottom line, and Water and Mountain share a yin bottom line. So the octahedron's six vertices are the six individual lines: three positions, each yin or yang.
- **The core bonds are the one-line changes.** Proof 24's twelve core bonds join each member of the father's family to each member of the mother's except its own opposite. Those are exactly the pairs that differ in one line, the *I Ching*'s changing lines. The excluded pairs are the traditional opposites (Heaven–Earth, Thunder–Wind, Water–Fire, Mountain–Lake).
- **The core currents are circulations of line changes.** Proof 24's five-dimensional space of conserved core currents is the 12 − 8 + 1 = 5 circulations around the cube of line changes, split 3 + 2 by exchanging the families.

## 8. Does the π walk perform the read? No

The π walk moves through the hexagrams the same way R does. It slides one trigram along at each step, from (a, b) to (b, c). What differs is how it chooses the new trigram:

| | New trigram c | Behaviour |
|---|---|---|
| π walk | b + (next base-8 digit of π), mod 8 | visits all 64 hexagrams, closing at step 332 |
| R | a ⊕ b | repeats with period 3, staying inside one orbit |

Over the first 20,000 base-8 digits of π, the walk's next trigram equals a ⊕ b on 2,504 of 19,999 steps, a rate of 0.1252. Random digits would give 1/8 = 0.125. In the 332 steps to closure, 36 steps agree.

So the π walk does not perform the read step by step. Integer addition mod 8 carries between lines, and XOR does not. The two are different processes on the same 64 addresses: **the walk traverses the register, and R reads it.** If the walk is to carry the closure read, that has to come from its dynamics, not from its covering all 64 hexagrams.

## What this does not say

- **The *I Ching* is not evidence for gravity.** It is a second, exact representation of the address space and its symmetries, useful because it exposes operations, such as R on corresponding lines, that are harder to see in the tetrahedral geometry.
- **R is not shown to be physical.** Which rotation the time-face dynamics actually performs, R or T, is open.
- **The π walk and the read stay distinct.** Whether some effective operator of the π-driven dynamics reduces to R, and produces the collective determinant, is open; step by step it does not.
- **The premises for G are unchanged.** The gain |t|² = α and the determinant source remain premises of Proof 26.

## Further results

Two notes take this algebra further:
- [Finite-field reciprocity](ICHING_FINITE_FIELD_RECIPROCITY.md) writes a hexagram as a + ωb in GF(64), reads the Walsh transform as a Hermitian incidence transform, and proves a reciprocal-edge theorem for the 17 pencil directions of PG(2,16).
- [The Frobenius reciprocal tower](FROBENIUS_RECIPROCAL_TOWER.md) splits the 273-point plane by Frobenius and inversion, and decomposes the eight trigrams by the Fano plane.
- [The shared zone](SHARED_ZONE_HEXAGRAM_READ.md) saturates the equal-or-opposite hexagrams under R to 13 directions and builds a nested 17 ⊃ 13 register. [Its Walsh rotation](SHARED_ZONE_WALSH_ROTATION.md) characterises the 17 as the minimal even completion of the 13.
- [The Walsh skew channels](WALSH_SKEW_CHANNEL_ACTION.md) identify the 28 skew directions as an exact Walsh eigenspace with a symmetric weight of 1/28.

## Verify

`python scripts/verify_hexagram_closure_read.py` (needs `numpy` and `mpmath`): 26 checks, output in [`scripts/verify_hexagram_closure_read_output.txt`](scripts/verify_hexagram_closure_read_output.txt). It covers:
- R's order and its 21 orbits;
- ω on the corresponding pairs;
- the 1/4/16 grades;
- the 7 + 14 split and the Baer property against all 21 lines of PG(2,4);
- T's 4 fixed hexagrams and 23 directions, and R and T commuting;
- the equality of the two Walsh groupings;
- the families, core vertices and one-line bonds;
- the π-walk test against 20,000 digits.

**Related proofs:**
- [Proof 23, recursive Triforce closure](../../../proofs/recursive-triforce-closure/): the 64 addresses, the label cycle, and the obstruction to the ordered corner-pair action.
- [Proof 24, flywheel tetrad geometry](../../../proofs/flywheel-tetrad-geometry/): the core bonds and conserved currents.
- [Proof 25, convergence](../../../proofs/tetrad-flywheel-convergence/): the dual tetrahedra and the core vertices.
- [Proof 26, recursive field closure response](../../../proofs/recursive-field-closure-response/): the three-sweep read, the F₄ rotation, the 21 directions and the collective determinant ([Lean audit](../../../proofs/recursive-field-closure-response/LEAN_AUDIT.md)).
