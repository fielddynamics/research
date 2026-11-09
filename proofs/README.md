# Proofs

*Formal results of Gravity Field Dynamics, each with a plain-language summary and a script that checks every step*

---

Each folder holds one proof: the LaTeX source and PDF, a README that explains in prose what the proof says and why it matters, and a verification script that prints PASS or FAIL for every algebraic step.

| Proof | Result | Checks |
|---|---|---|
| [`forced-tetrahedral-frame/`](forced-tetrahedral-frame/) | The legs of a Lorentz tetrad, realised as equivalent and distinct vectors in three-dimensional space, are forced to a regular tetrahedron, unique up to $O(3)$. Equal norms and closure are derived, three is the only dimension in which the shape is forced, and parity completion gives the stellated octahedron | 27/27 |
| [`constitutive-law-exchange-symmetry/`](constitutive-law-exchange-symmetry/) | Under exchange closure of TetA and TetB, the endpoint $\mu(0) = 0$ and coupling of degree one in each variable, the constitutive law is uniquely $\mu(x) = x/(x+1)$. The inversion $x \to 1/x$ about $a_0$ is derived, and each premise is shown to be necessary | 34/34 |
