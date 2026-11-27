# Great Pyramid · Core Framework Proofs

*Five proofs that fix what is exact in the Great Pyramid programme, what it rests on, and what it cannot claim · Gravity Field Dynamics (GFD), exploratory*

Each folder holds a README (statement, proof, premises, necessity, scope) and a verification script that prints PASS or FAIL for every step, with its output. The framework these proofs belong to is described in [`../CORE_FRAMEWORK.md`](../CORE_FRAMEWORK.md).

| Proof | Result | Checks |
|---|---|---|
| [GP-1](gp1-half-section-balance-plane/) | **The half-section theorem.** In any cone, of any base shape, slope or tilt, a uniform current with $J_z \ne 0$ has structural share $\mu_B = (1-u)^{D-1}$ and a unique balance level $u^* = 1 - 2^{-1/(D-1)}$. In $D = 3$ that is $1 - 1/\sqrt2$, and only in $D = 3$ does it coincide with the halving of the meridional ("vertical") area. The volume and height halvings are distinct levels (0.2063, 0.5). Petrie's King's Chamber floor lies 0.30 σ from the area level and > 180 σ from the others [O]. | 53 |
| [GP-2](gp2-balance-plane-robustness/) | **Robustness, and the constitutive share at Giza.** For affine $\mathbf J$, $\mu_B = (1-u)^2(1+bu)$, with $b$ the fractional change of $J_z$ from base centroid to apex. The level is unique for all $b > -1$, and shifts by $\frac{\sqrt2-1}{4}b\,h$ (598.1 in per unit $b$, reproducing note 01.7 in closed form). Any non-uniformity $\varepsilon$ confines it to $\pm\varepsilon h/(2\sqrt2)$, a sharp bound. The Earth's gravity moves it 0.70 mm; with self-gravity, < 0.36 in. By the net-field rule the constitutive share at Giza is $\mu = 1$ exactly, so $\mu_B$ is **not** the TetA/TetB partition. | 42 |
| [GP-3](gp3-coupling-signatures-and-hinge/) | **The signatures are forced; the hinge is unique.** $f(K,s) = \lvert K+e^{i\theta}\rvert^2$ is an irreducible integer quadratic iff $s \in \{-1,0,1\}$ ($\varphi(n) = 2 \iff n \in \{3,4,6\}$). The only coincidences $f(K,s) = f(K',s')$ between levels are the hinges $f(k,+1) = f(k+1,-1)$, and 17 occurs nowhere else. The three values are pairwise coprime at every $K$. Fusion tower $21 \to 273 \to 65793$. Exact counts: $\lvert PG(2,3)\rvert = 13$, $\lvert PG(2,4)\rvert = 21$, ovoid of $PG(3,4)$ = 17. | 39 |
| [GP-4](gp4-registration-and-coherence/) | **Registration and coherence.** $C_N = 1$ iff support lies on one $N$-gon coset. Full registration allows any coherence. Coherence forces registration: $1 - \operatorname{Re}(e^{-iN\varphi}m_N) \le N^2(1 - C_1)$, sharp. Registration at coprime orders 3 and 7 *is* coherence, so $\mathbb Z_3\times\mathbb Z_7 \cong \mathbb Z_{21}$ does not factor the registration condition. Only the full character sum is an exact selector; the 14-character filter has sidelobes of exactly ½. | 35 |
| [GP-5](gp5-two-site-transfer-bound/) | **Resonance selects, it does not create.** For any two-site drive, $\lvert c_y(t)\rvert \le \sin\min(\int_0^t\lvert\kappa\rvert, \pi/2)$, attained at resonance. With $\kappa = 0$ there is no transfer under any frequency programme, and complete transfer needs $t \ge \pi/(2\sup\lvert\kappa\rvert)$. Detuning tolerance $\lvert\Delta\rvert \le 2\lvert\kappa\rvert\sqrt{(1-\eta)/\eta}$. The Gram mismatch $d_G$ is a pseudometric, and the selector $M_{xy} \in [0,1]$ can only slow a transfer. | 22 |
| | **Total** | **191** |

```bash
python run_all.py        # all five, ~45 s; requires sympy, mpmath, numpy, scipy
```

**Status tags** follow the repository (llms.txt, Rule 11): **[T]** theorem, **[D]** derived, **[E]** exploratory, **[O]** observational.

**Lean.** Each proof also has a `lean/` folder with a Lean 4 / Mathlib (v4.36.0) formalisation of its algebraic and finite statements: 61 theorems in all (GP-1 9, GP-2 11, GP-3 20, GP-4 9, GP-5 12), no `sorry`, standard axioms only. GitHub Actions builds each one and audits its axioms on every change (`.github/workflows/lean-great-pyramid-gp*.yml`). Each folder's `LEAN_AUDIT.md` lists what is formalised and what is still checked only by script (measure-theoretic flux, numerics, finite-field enumeration, the time-dependent transfer bound).
