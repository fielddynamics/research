# Referee Review and Response

*Internal review of "The SST Covariant Completion in Its Quasi-Static Limit" (Theorems 1–6, commit 232dda6), written as a journal referee would, with the change made for each point.*

---

## Summary of the submission

The proof takes GFD's four-term covariant action (the SST) and derives its quasi-static weak-field content:
- the AQUAL field equation with μ = x/(x+1);
- the exact spherical field equation, with its solver and decoder;
- the Newtonian and deep limits and the baryonic Tully–Fisher relation;
- well-posedness;
- with a single potential, γ = 1 and lensing mass equal to dynamical mass.

The algebra is correct and machine-checked. The main concern is that one step rests on a "reading" of the action, which a referee will not accept as stated.

## Major points

**M1. "Reading (ii)" is not a property of an action.** The equations of motion of an action follow from varying it, and the draft's Remark shows that varying the curvature term together with F does not give Eq. (1). Saying that the curvature term "carries the tensor sector" while "Φ's response is carried by F" is a statement about which terms are varied with respect to what. As written, a referee would call it an unstated modification.

*Response.* The reading is now stated precisely, as Lemma 1, an exact identity. Under it, the static weak-field Lagrangian of the SST is

  (1/8πG)[(∇Ψ)² − 2∇Φ·∇Ψ] − (a₀²/8πG)[F(y) − y] − ρΦ,

that is, the curvature term in full plus the scalar term with its Newtonian part y supplied by the curvature term. On Ψ = Φ this equals −(a₀²/8πG)F(y) − ρΦ, the energy the archive uses (checked). The action is presented as written; Lemma 1 is the precise statement of how the framework varies it. The Remark is kept: counting y twice would give ∇·[(1 + μ)∇Φ] = 4πGρ.

**M2. γ = 1 was posited, not derived.** Theorem 6 assumed the single-potential metric (Letter 3's reading), and the Coles Notes record this as open.

*Response.* With Lemma 1, γ = 1 is now derived at leading order:
- the Ψ-equation of the curvature term is ∇²(Φ − Ψ) = 0, so Ψ = Φ for fields that vanish at infinity;
- the Φ-equation on Ψ = Φ is then Eq. (1).

Theorem 1 now delivers both. The stated scope is leading order in the static weak field: the stress–energy of the F sector enters at higher order, and the full metric equations are still open.

**M3. The matter coupling.** The draft said −ρΦ is "the weak-field form of minimal coupling" without showing it. *Response.* Shown: a point mass's action −mc²∫dτ, with √(−g₀₀) = √(1 + 2Φ/c²), gives −mc² − mΦ + O(Φ²/c²) per unit time (checked). So minimal coupling to a metric whose g₀₀ carries Φ is the −ρΦ source. That is consistent with the documentation's "minimally coupled to the metric".

**M4. Novelty and prior work.** The field equation, the spherical reduction, the limits, Tully–Fisher, well-posedness and the deep-field deflection are standard AQUAL results for the simple μ (Bekenstein–Milgrom 1984; Milgrom 1983; Famaey–McGaugh 2012). *Response.* A "Contributions and prior work" paragraph now says so. What the proof adds:
- the derivation from the SST's own terms, with the reading made exact (Lemma 1) and γ = 1 derived;
- the capacity form;
- the exact solver/decoder pair;
- the TetB-share bound and the ring;
- machine checks of every step.

## Minor points

**m1. The covariance of y.** If Φ is the metric potential, |∇Φ|² is defined in the static frame, not as a spacetime scalar. *Response.* The Scope section now says this explicitly: the limit uses the static frame, and the covariant form of y is open.

**m2. The deflection is in the Born approximation.** It is integrated along the unperturbed ray. *Response.* Stated. The spherical lensing-mass identity is now separated from the general statement that the lensing potential is ∫(Φ + Ψ)dz = 2∫Φ dz.

**m3. Tully–Fisher for an isolated mass.** v⁴ → GMa₀ holds for an isolated system. With an external field the AQUAL equation has the external field effect. *Response.* Stated.

**m4. Uniqueness needs boundary conditions.** *Response.* Uniqueness is stated for fields with given boundary data or decaying at infinity. The equation is elliptic away from ∇Φ = 0, and existence for AQUAL is cited to Bekenstein–Milgrom.

**m5. Paper I's processing boundary.** *Response.* Rephrased neutrally: at r = √(GM/a₀) the Newtonian acceleration equals a₀; there x = φ and μ = 1/φ. The ring μ = ½ is at √(2GM/a₀).

## Assessment after revision

With Lemma 1, the proof is a derivation rather than a reading. The SST, varied as the framework varies it, gives Ψ = Φ (γ = 1) and the field equation in the quasi-static weak field, and everything SPARC, Tully–Fisher and the decoder test follows exactly. What remains open is stated: the full metric equations, the covariant form of y, the fourth term and α, ℒ_matter beyond weak field, and the bimetric match.

## Checks

The script grows from 22 to 26 checks, adding:
- the Lemma 1 identity;
- the Ψ-equation ∇²(Φ − Ψ) = 0;
- the Φ-equation on Ψ = Φ;
- the expansion of −mc²√(−g₀₀).
