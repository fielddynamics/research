# The Constitutive Law from Exchange Symmetry

*Why the interpolating function of modified gravity has to be $\mu(x) = x/(x+1)$ · Gravity Field Dynamics (GFD) · Field Dynamics Research*

`constitutive-law` `interpolating-function` `MOND` `AQUAL` `exchange-symmetry` `algebra` `proof`

---

This folder holds a two-page proof, written as supplementary material to the letter [*The Gravitational Constitutive Law from the Tetrad Frame Geometry*](../../papers/letter-constitutive-law-tetrad-geometry/), together with a script that checks every algebraic step. This page explains what the proof says and why it matters. It assumes first-year calculus and a little algebra, nothing more.

## The problem

Newton's law of gravity works very well in the Solar System. It fails at the edges of galaxies. Stars far from a galaxy's centre orbit faster than the visible matter can explain, and their orbital speed stops falling with distance: the rotation curve goes flat.

In 1983 Mordehai Milgrom noticed that the failure is set by acceleration, not by distance. Above a characteristic acceleration $a_0 \approx 1.2 \times 10^{-10}\ \mathrm{m\,s^{-2}}$, gravity behaves as Newton said. Below it, gravity is stronger than Newton's law predicts. In 1984 Bekenstein and Milgrom wrote this as a field equation, AQUAL:

$$\nabla \cdot \left[\mu\!\left(\frac{|\nabla\Phi|}{a_0}\right)\nabla\Phi\right] = 4\pi G\rho .$$

The function $\mu$ takes the acceleration ratio $x = g/a_0$ and returns a number between 0 and 1. At high accelerations it must approach 1, so that Newton is recovered. At low accelerations it must behave like $x$, so that rotation curves go flat. These two limits are all the physics demands, and infinitely many functions satisfy them. The two best known are

$$\mu_{\text{simple}}(x) = \frac{x}{x+1}, \qquad \mu_{\text{standard}}(x) = \frac{x}{\sqrt{1+x^2}} ,$$

and there are many others, including exponential forms. Milgrom's framework gives no reason to prefer one. In 2005 Famaey and Binney found that the simple form fits the Milky Way better, but a fit is not a reason. For four decades the function has been chosen by hand. A theory that chooses a whole function by hand has, in effect, a free function in it.

## The answer

In Gravity Field Dynamics the choice disappears. The proof shows that, given the geometry of the framework, **the simple form is the only function possible**. Every other candidate breaks a specific, named premise.

## The setting

GFD reads gravity through the geometry of the stellated octahedron: two interlocking tetrahedra, TetA and TetB, which the tetrad equation produces as two bounded regions exchanged by spatial parity (mirror reflection). TetA is the region we observe as ordinary space and time. The field's capacity is shared between the two regions, and $\mu$ is the share carried by TetA. When $\mu = 1$ the field is entirely in TetA and gravity is Newtonian. When $\mu$ is small, most of the field sits in TetB.

It helps to describe the share as odds rather than as a fraction. If TetA carries $\mu$ and TetB carries $1-\mu$, the odds between them are

$$\Omega = \frac{\mu}{1-\mu} .$$

Odds run from 0 (all TetB) to infinity (all TetA), and even odds, $\Omega = 1$, mean an equal split. Odds make the exchange of the two regions simple: swapping TetA and TetB turns odds of $\Omega$ into odds of $1/\Omega$.

## The three premises

**(E) Endpoint.** At zero acceleration the field sits entirely in TetB: $\mu(0) = 0$.

**(X) Exchange closure.** Parity exchanges TetA and TetB, and parity is a symmetry of the tetrad equation. So if some acceleration produces a state in which TetA carries a share $\mu$, some acceleration must produce the mirror state, in which TetB carries that share. The proof assumes nothing more about the exchange than this. It does not assume where the mirror state sits, or what the exchange does to accelerations. Those come out of the proof.

**(A) Degree one.** The tetrad equation is polynomial, so the acceleration and the share are taken to satisfy a polynomial equation. The premise is that this equation has degree one in each variable.

Degree one has a concrete meaning. A relation of degree one in $\mu$ gives exactly one share for each acceleration, the way a straight line gives one $y$ for each $x$. A relation of degree two can give two, the way a parabola can. The proof's lemma makes this exact: the degree of the relation in a variable is the number of values that variable can take, in general, for a given value of the other.

In GFD the degree in $\mu$ has a physical reading: it counts the directions in which the coupling runs. In a galaxy's exterior field, matter sources the field and the field does not source itself, so the coupling runs one way. (The galaxy itself is a bound vortex whose TetB is fed through its drain; the one-way coupling describes its exterior.) A self-sourcing field, the regime of atomic nuclei in [Paper XIII](../../papers/13-nuclear-binding-bidirectional-sst/), sources itself and couples in both directions. It obeys $x(1-\mu)^2 = \mu$, which has degree two in $\mu$ and needs a square root to solve. The degree in $x$ is the power with which the acceleration drives the share, the exponent of the driving term in the [equilibrium route](../../papers/letter-constitutive-law-tetrad-geometry/Supplementary/supplementary_equilibrium_route.tex).

## How the proof works

The argument has three steps.

**Step 1.** A polynomial of degree one in each of two variables has only four terms: $P = a\,x\mu + b\,x + c\,\mu + d$. The endpoint premise says the relation holds at $x = 0, \mu = 0$, which forces $d = 0$. Rewritten in odds, the relation becomes

$$\Omega(x) = \frac{\alpha x}{\gamma x + \delta}$$

for some constants $\alpha, \gamma, \delta$.

**Step 2.** At zero acceleration TetA is empty. By exchange closure, the mirror state, with TetB empty and the odds infinite, must occur at some acceleration. Odds of this form become infinite at exactly one place, where the denominator vanishes. There are three possibilities:

- If that place is a positive acceleration, the denominator changes sign there, so the odds turn negative on one side. Negative odds are impossible.
- If that place is a negative acceleration, the odds never become infinite for any acceleration between zero and infinity, so the mirror state never occurs. That breaks closure.
- The only remaining possibility is that the odds become infinite at infinite acceleration. That means $\gamma = 0$, and the odds are simply proportional to the acceleration, $\Omega = k\,x$.

**Step 3.** The constant $k$ only sets the unit of acceleration. Measuring acceleration in the unit where $k = 1$, which defines $a_0$, gives

$$\Omega = x, \qquad x\,(1-\mu) = \mu, \qquad \mu(x) = \frac{x}{x+1} .$$

The odds between the two regions equal the acceleration ratio itself.

## What comes out for free

Several properties that are usually assumed now follow from the proof:

- **Newton is recovered.** As $x \to \infty$, $\mu \to 1$. This was not put in.
- **The exchange is an inversion.** Swapping TetA and TetB is the map $x \to 1/x$. Equivalently, $\mu(x) + \mu(1/x) = 1$: a field at twice $a_0$ and a field at half $a_0$ split their capacity in mirror proportions.
- **$a_0$ has a meaning.** It is the fixed point of the inversion, the acceleration at which TetA and TetB carry equal shares, $\mu(1) = \tfrac12$. The proof says what $a_0$ is. It does not give its numerical value, which the framework derives elsewhere.
- **The exchange is parity itself.** Writing $s = 2\mu - 1$, so that TetA is $s = +1$ and TetB is $s = -1$, the law becomes $s(x) = (x-1)/(x+1)$, and the exchange becomes $s \to -s$, the sign flip that parity applies to the rank-one term of the coupling polynomial $f(K,s) = 1 + sK + K^2$.

## Each premise is necessary

A proof is only as strong as its weakest premise. To show that none of the premises is padding, the proof gives, for each one, functions that satisfy the other two but not the law:

| Premise removed | What becomes possible |
|---|---|
| Endpoint (E) | $\Omega = (x+b)/(bx+1)$ with $0 < b < 1$: TetA is never empty, even at zero acceleration |
| Exchange closure (X) | $\Omega = \alpha x/(\gamma x+\delta)$ with $\gamma > 0$: TetA never carries the whole field |
| Degree one (A) | $x^n(1-\mu)^m = \mu$ for any other $n, m \ge 1$. This includes the bound-state law ($n = 1, m = 2$) and the steeper laws $\mu = x^n/(1+x^n)$ ($m = 1$) |

The last row matters most. It shows that "the relation is algebraic" is not enough on its own, because all of those alternatives are algebraic. What does the work is the degree, and the framework's own bound-state law is exactly the case that degree one excludes. The standard form fails in the same way: $\mu = x/\sqrt{1+x^2}$ satisfies $\mu^2(1+x^2) = x^2$, which has degree two in $\mu$.

## Why it matters

**It turns a choice into a consequence.** The function that MOND chooses by hand, GFD derives, and the function it derives is the one the data prefer. This removes a free function from the theory and supports the framework's claim to have no free parameters.

**It moves the debate to the right place.** The proof is conditional: if the premises hold, the law follows. Because every step is checked and every premise is shown to be necessary, a referee cannot attack the step from premises to law. The only open question is whether the premises are true, and those are physical claims, set out in the main letter and in Paper XIII, where they can be tested.

**It ties the framework together.** The letter derives the same law by three routes: from the rank structure of the metric through the coupling polynomial, from equilibrium of the field, and from exchange symmetry. The proof shows that all three rest on the same fact, a relation of degree one in each variable:

- In the coupling-polynomial route it is the map $s(x) = (x-1)/(x+1)$. Of that route's three boundary conditions, one is the endpoint premise, one is the choice of unit, and one is derived here.
- In the equilibrium route it is the balance $x(1-\epsilon) = \epsilon$, which is linear in both variables.

The same algebra also places the galactic law and the nuclear law side by side: the same relation, run in one direction or in two.

## What it does not do

The proof does not establish its premises. The geometry of TetA and TetB, the parity exchange and the one-directional coupling of unbound fields are claims of the framework, argued in the papers listed below. Nor does the proof compute $a_0$. Its job is narrower and exact: if GFD's geometry is right, the constitutive law cannot be anything else.

## A note on earlier versions

Earlier forms of this argument, in the [letter's supplement](../../papers/letter-constitutive-law-tetrad-geometry/Supplementary/supplementary_exchange_symmetry.tex) and in the [RAR letter's supplement](<../../papers/letter-radial-acceleration-relation-sparc/supplementary/supplementary_constitutive_law_exchange_symmetry (1).tex>), reached the fractional-linear form in one step. The first does it by asserting that a rational bijection of the line is fractional linear. That is true only when the inverse is also rational: $x^3$ is a rational bijection of the real line that is not fractional linear. The second does it by requiring the map to be an automorphism of the projective line. This version proves that step from an explicit degree lemma, states the requirement openly as premise (A), gives it a physical reading, and shows it to be necessary. It also assumes less about the exchange and derives more: the inversion, the involution and the complement symmetry are all results here.

## Contents

| File | Contents |
|---|---|
| [`constitutive_law_exchange_symmetry.pdf`](constitutive_law_exchange_symmetry.pdf) | The proof, two pages |
| [`constitutive_law_exchange_symmetry.tex`](constitutive_law_exchange_symmetry.tex) | LaTeX source (IOP journal class, included) |
| [`verify_constitutive_law_exchange_symmetry.py`](verify_constitutive_law_exchange_symmetry.py) | Symbolic checks of the lemma, every step, the parity form, every row of the necessity table and the links to the other routes |
| [`iopjournal.cls`](iopjournal.cls) | Document class, copied from the letter so the source builds here |

```bash
pip install sympy
python verify_constitutive_law_exchange_symmetry.py      # 34/34
pdflatex -interaction=nonstopmode constitutive_law_exchange_symmetry.tex
```

## Related papers

- [*The Gravitational Constitutive Law from the Tetrad Frame Geometry*](../../papers/letter-constitutive-law-tetrad-geometry/): the main letter, with the three routes to $\mu(x)$.
- [Equilibrium route](../../papers/letter-constitutive-law-tetrad-geometry/Supplementary/supplementary_equilibrium_route.tex): the same law from single-channel detailed balance.
- **Paper XIII**, [*Nuclear Binding Energy from the Bidirectional Scalar-Tensor Transition*](../../papers/13-nuclear-binding-bidirectional-sst/): one-directional and bidirectional coupling, and the bound-state law.
- [Bound and Unbound Gravity](../../research/bound-gravity-and-packing/): the two states of a gravity field.

---

*The algebra is complete and machine-checked. The physical premises are GFD's, stated so that they can be tested.*
