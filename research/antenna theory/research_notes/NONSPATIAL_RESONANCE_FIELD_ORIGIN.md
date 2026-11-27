# TetA and TetB communicate through the nonlinear Field Origin — by resonance, not through space

**Status key:** [T] identity or theorem under the stated definitions · [N] reproduced finite computation · [D] consequence of the stated model · [H] physical hypothesis.

## What is being laid out, and why it matters

GFD's position is that TetA is our observable 3+1 chamber and TetB is a subspace reachable only through the Field Origin. There is no spatial transport between them. If that is right, any account of how the chambers influence each other has to work **without a spatial path**: no shared coordinate, no adjacency, no lateral leak. The only connection is the Field Origin, which GFD holds to be nonlinear.

This note sets out a mechanism with exactly that structure and checks what it implies. It does three things:

1. It writes down the smallest model in which TetA and TetB have **no direct term at all** and still exchange completely.
2. It shows that what decides whether they exchange is **resonance**, meaning matched modes on the two sides, and not distance.
3. It roots the Field Origin's nonlinearity in vortex physics, so the nonlinearity isn't an arbitrary choice.

Without this, "they communicate through the Field Origin" is a sentence. With it, the sentence has a model whose consequences can be tested.

## 1. The picture, in vortex terms [H]

Take a water vortex shaped like an hourglass: one spiral funnel above, one below, joined at a narrow throat. Each funnel carries its own standing waves, the wave families of its spiral. The two funnels never touch side by side. The only thing they share is the **core at the throat**. A disturbance in the upper spiral reaches the lower spiral only by exciting the core, and the core passes it on. How much gets through depends on whether the lower spiral has a wave at the same frequency.

In GFD terms:

| Vortex hourglass | GFD |
|---|---|
| upper spiral and its standing waves | TetA and its band modes |
| lower spiral and its standing waves | TetB and its band modes |
| shared core at the throat | the Field Origin |
| no side-by-side contact between funnels | no spatial transport between chambers |
| lower spiral turning the same way but more slowly | TetB modes detuned from TetA |

Only behaviour expected of a water vortex is used: standing waves on each spiral, a shared core, and a core whose wave response depends on amplitude (Section 4).

## 2. The model [D]

For one band, write the TetA mode amplitude as a, the Field Origin (core) mode as o, and the TetB mode as b:

```
i da/dt = ω_A a + g o
i do/dt = ω_O o + χ|o|²o + g(a + b)
i db/dt = ω_B b + g o
```

**There is no a–b term.** In the coupling graph, A and B are joined only through O (figure 01). Remove the origin and the two chambers are disconnected [T]. That is the formal meaning of "non-spatial" here: the chambers share no coordinate and no edge, and the only coupling term in the equations is the one at the vertex.

The model is lossless and time-reversible: |a|² + |o|² + |b|² is conserved, and conjugating the state then evolving it again runs the motion backwards (tested). Nothing is dissipated, which fits the framework's informational reading. No circuit, power or loss machinery is imported.

## 3. Results

### 3.1 Complete exchange with no direct path [T]

With all three frequencies equal and the system starting entirely in TetA:

$$a=\tfrac{1}{2}\big(1+\cos\sqrt2\,gt\big),\qquad o=-\tfrac{i}{\sqrt2}\sin\sqrt2\,gt,\qquad b=\tfrac12\big(\cos\sqrt2\,gt-1\big).$$

At gt = π/√2 the whole inventory sits in TetB and the origin is empty again (figure 02). The chambers exchange everything, yet no term ever connects them directly.

### 3.2 The origin need not hold the inventory: a virtual vertex [D, N]

Detune the origin by Δ ≫ g. Eliminating o gives an effective TetA–TetB coupling

$$J=\frac{g^2}{\Delta}.$$

With g = 0.1 and Δ = 2, the model exchanges 99.99% of the inventory, while the origin's peak occupation stays at about 1% (figure 03). The first transfer comes at t ≈ 317, against π/(2|J|) ≈ 314 predicted. The Field Origin **carries** the exchange without ever **holding** it. This is the sense in which the chambers communicate *through* the origin rather than *via a stop at* the origin.

### 3.3 Resonance decides who talks to whom [D, N]

Detune TetB by δ. The peak TetB occupation follows the two-mode resonance law

$$P_{\max}=\frac{J^2}{J^2+(\delta/2)^2},$$

to within 0.01 at every tested δ (figure 04). A detuning of δ = 2J already halves the exchange (here J = 0.005, so δ = 0.01). **Matched frequencies, not proximity, select which modes exchange.**

Applied to the self-similar band ladder (bands at 2ⁿω₀, the ladder measured on Sierpiński antennas), two matched ladders exchange in every band (> 0.999 each). A partner ladder scaled by 0.9, 1.1 or 1.5 exchanges less than 5% in every band. Self-similarity on both sides is what lets the whole ladder resonate at once.

### 3.4 The nonlinear origin [D, N]

Hasimoto (1972) showed that a thin vortex filament under local induction obeys the cubic nonlinear Schrödinger equation. The χ|o|²o term is that cubic form. This is the nonlinearity a vortex core naturally has, so it is used here rather than one chosen for convenience.

Finding (figure 05, `outputs/nonlinear_vertex.csv`, χ = 1, g = 1):

| Inventory N | Peak Field Origin share | Time to 50% in TetB |
|---:|---:|---:|
| 0.01 | 0.500 | 1.41 |
| 4 | 0.453 | 1.60 |
| 16 | 0.295 | 3.86 |
| 64 | 0.141 | 6.32 |

- Small inventory: the linear result returns exactly (tested).
- Large inventory: **exchange still completes** (> 0.99 in TetB), but the origin's own share falls steadily. The core's amplitude-dependent frequency shift detunes it, which pushes it into the virtual regime of 3.2.

So the nonlinear vertex **self-regulates toward pure resonance**: the more the chambers have to exchange, the less the Field Origin keeps and the more purely it acts as a resonant channel. Exchange slows but doesn't stop.

What did **not** appear: a nonlinearity at the vertex alone does not trap the inventory on one side while TetA and TetB stay matched. The A↔B symmetry survives. Blocking or one-way behaviour would need a detuning or an asymmetry. That fits the vortex reading, where the lower spiral turning more slowly is a detuning.

## 4. Two regimes of one vertex [H]

The framework calls for one nonlinear vertex law with two regimes:

- **Drainless / resonant:** no net throughflow. The chambers exchange by resonance, as modelled above. A local solar system's field has no open drain, so its TetA–TetB relation lives here. This is consistent with the position that only TetA applies within it.
- **Draining / transfer:** an open drain (a galaxy) adds net throughflow at the core. This package does **not** model that regime. Extending the vertex to it is the next step (see `NEXT_STEPS.md`).

## 5. What this does and does not establish

- **Establishes [T/D]:** a lossless, reversible mechanism in which two chambers with no shared coordinate exchange fully through one nonlinear vertex. The exchange is selected by resonance, and a vortex-native nonlinearity makes the vertex increasingly virtual at high inventory.
- **Does not establish:** that GFD's chambers obey these equations. It also doesn't establish the band-diagonal coupling assumption, the values of g, Δ or χ, any link to 2/17 or the coupling polynomial's 21/17/13, or matter transfer. Those are open [H].
