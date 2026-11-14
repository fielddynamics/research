# The Hourglass Lemma

*Field Dynamics Research, 2026-11-13 (revised 2026-11-14). Status: research. Verification: `python verify_hourglass_lemma.py` (21 exact sympy checks). Overview: [`README.md`](README.md).*

---

## Question

In GFD, TetA and TetB together form a vortex: spiral → throat → spiral, like water through a drain. The throat is the Field Origin, the neck of the hourglass (Coles Notes §2–3). TetB is the chamber beyond it, reached only through the Field Origin. The exchange of TetA and TetB is spatial parity, −I, the element that doubles the symmetry of one tetrahedron to that of the stellated octahedron ([Gram-matrix proof](../../proofs/gram-matrix-tetrad-equation/), Theorem 2).

So: what does parity do to an hourglass vortex? Which parts of the flow does it keep, which does it reverse, and where does the vortex's handedness sit?

The constitutive law is not in question here. μ(x) = x/(x+1) is proved ([exchange symmetry](../../proofs/constitutive-law-exchange-symmetry/)), and the [two-connection note](../two-connection-dual-chamber/) shows two fields on the two roots composing as TetA μg plus TetB (1 − μ)g, with odds x. That note also finds the chirality: the axial torsion is zero for any static tetrad, appears only with rotation, and is opposite on the two roots. *If chirality has a role, it is in the rotating (vortex) sector.* This note starts on that sector.

## Set-up

Put the throat at the origin and the axis along z. Split the velocity of an axisymmetric vortex into two parts:
- **the swirl,** the azimuthal component $v_\varphi$, which turns about the axis;
- **the through-flow,** the meridional components $(v_r, v_z)$, which carry the flow in through one spiral, through the throat, and out through the other.

Parity sends every point to its opposite and carries the flow along with it: $(\Pi v)(\mathbf x) = -v(-\mathbf x)$.

## Lemma (the hourglass under parity)

For any axisymmetric velocity field:

**(a)** Π is an involution, and in cylindrical components

$$\Pi:\ (v_r,\ v_\varphi,\ v_z)(r, z) \;\mapsto\; (v_r,\ v_\varphi,\ -v_z)(r, -z).$$

**(b) The rotation is preserved.** The vorticity of the image is $\boldsymbol\omega(-\mathbf x)$: the vortex turns the same way after the exchange. On the axis the vorticity points the same way above and below the throat.

**(c) The through-flow is reversed.** A drain becomes a fountain with the same swirl. The spiral that fed the throat now leaves it, and the one that left it now feeds it. Parity exchanges *which spiral feeds which*; it does not change the turning.

**(d) The handedness is the swirl times the through-flow.** The helicity density $h = \mathbf v \cdot \boldsymbol\omega$ is exactly the cross term

$$h = \mathbf v_{\rm swirl}\cdot\nabla\times\mathbf v_{\rm through} + \mathbf v_{\rm through}\cdot\nabla\times\mathbf v_{\rm swirl},$$

so pure swirl is achiral and pure through-flow is achiral. Under parity, $h[\Pi v](\mathbf x) = -h[v](-\mathbf x)$: the helicity is a pseudoscalar, and the mirror vortex has the opposite handedness. Reversing the swirl alone also reverses it.

**(e)** The throat is the only fixed point of parity.

**(f) The rate difference across the throat.** Let the swirl turn at the mean rate $\bar\Omega$ plus a half-difference $\delta$ that takes opposite signs on the two sides of the throat. Far from it, TetA then turns at $\bar\Omega + \delta$ and TetB at $\bar\Omega - \delta$. Parity keeps $\bar\Omega$ and flips $\delta$, so $\delta = 0$, one rate on both sides, is the only case parity leaves unchanged. With $0 < |\delta| < \bar\Omega$ both chambers turn the same way at different rates, and the difference is a shear across the throat: the radial vorticity there is nonzero exactly when $\delta \neq 0$.

The checks verify (a), (b) and (d) for a general axisymmetric field (arbitrary component functions), and (c), (d) on an explicit smooth, incompressible hourglass: $v_r = -arz$, $v_z = az^2 - w$, $v_\varphi = \Omega r/(1 + r^2)$. For (f) the swirl is $v_\varphi = \frac{r}{1+r^2}\bigl(\bar\Omega + \delta\, z/\sqrt{1+z^2}\bigr)$.

## Reading in GFD

Read with the upper spiral as TetA, the throat as the Field Origin, and the lower spiral as TetB (the framework's reading, not derived here):

- **TetA and TetB share the turning** (b). The rotation is the part of the vortex that parity leaves alone.
- **They exchange roles in the through-flow** (c). Which chamber feeds which is the part parity reverses, so the direction of flow through the Field Origin is what tells the two chambers apart.
- **The vortex's handedness is parity-odd and needs both parts** (d). A vortex that only turns, or only flows through, has no handedness. This is the flow-level counterpart of two results already in the repo:
  - the [Gram-matrix proof](../../proofs/gram-matrix-tetrad-equation/)'s Proposition 1: the two roots differ only in orientation, which flips under parity;
  - the [two-connection note](../two-connection-dual-chamber/)'s chirality: axial torsion is zero when static, switched on by rotation, and opposite on the two roots.

  The helicity adds one thing to these. Rotation alone is not enough; the chirality needs rotation *and* through-flow.
- **The interior turns at its own rate** (f). TetB turns the same way as TetA, faster or slower; counter-rotation is only an extreme. The rate difference is the part of the swirl parity does not produce, and it shows up as a shear at the Field Origin.
- **Drive and brake** always refer to the interior TetB (the framework's definition, Stephen Nelson, 2026-11-14). They are seen as measured observations above or below what the photometric mass predicts: a **drive** is $M_{\rm dec} > M_{\rm phot}$, a **brake** is $M_{\rm dec} < M_{\rm phot}$, and a **quiet** interior is $M_{\rm dec} = M_{\rm phot}$. In the rate picture, drive and brake are TetB turning faster or slower than the rate the no-slip partition gives it ([`ROLL_RATIO.md`](ROLL_RATIO.md)), not faster or slower than TetA: the no-slip partition already has the chambers turning at different rates everywhere except the ring, and is quiet. (Revised 2026-11-14. An earlier version read drive as TetB faster than TetA.)

## What it does not do

- It is about a velocity field in an observer's space. It does not yet connect the flow to the tetrad's connection, so it does not show that the helicity *is* the axial torsion. That identification is the next step (below), and it has to be derived, not matched.
- The assignment of the upper spiral to TetA and the lower to TetB is the framework's reading.
- It makes no dynamical claim. Nothing here says how fast the vortex turns or what sets its rate.

## Next

1. **Transport theorem.** Carry a tetrad along a streamline from the TetA spiral through the throat into the TetB spiral. Show that it arrives as Proposition 2(b) of the Gram-matrix proof (connections that differ, by a torsion), not 2(a) (the covariant mirror, identical). Then compute its axial torsion and compare it with the helicity of (d).
2. **Drive and brake from the interior.** A galaxy-level measure of TetB's effect, read from decoded against photometric mass at the drain rather than across the disk.

