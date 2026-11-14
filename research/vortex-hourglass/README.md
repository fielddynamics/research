# The Hourglass Vortex Under Parity

*Working note, Field Dynamics Research, 2026-11-13. Status: research, not a paper. Verification: `python verify_hourglass_lemma.py` (16 checks, exact sympy).*

`vortex` `hourglass` `throat` `Field-Origin` `spatial-parity` `helicity` `chirality` `TetA` `TetB` `research`

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

The checks verify (a), (b) and (d) for a general axisymmetric field (arbitrary component functions), and (c), (d) on an explicit smooth, incompressible hourglass: $v_r = -arz$, $v_z = az^2 - w$, $v_\varphi = \Omega r/(1 + r^2)$.

## Reading in GFD

Read with the upper spiral as TetA, the throat as the Field Origin, and the lower spiral as TetB (the framework's reading, not derived here):

- **TetA and TetB share the turning** (b). The rotation is the part of the vortex that parity leaves alone.
- **They exchange roles in the through-flow** (c). Which chamber feeds which is the part parity reverses, so the direction of flow through the Field Origin is what tells the two chambers apart.
- **The vortex's handedness is parity-odd and needs both parts** (d). A vortex that only turns, or only flows through, has no handedness. This is the flow-level counterpart of two results already in the repo:
  - the [Gram-matrix proof](../../proofs/gram-matrix-tetrad-equation/)'s Proposition 1: the two roots differ only in orientation, which flips under parity;
  - the [two-connection note](../two-connection-dual-chamber/)'s chirality: axial torsion is zero when static, switched on by rotation, and opposite on the two roots.

  The helicity adds one thing to these. Rotation alone is not enough; the chirality needs rotation *and* through-flow.

## What it does not do

- It is about a velocity field in an observer's space. It does not yet connect the flow to the tetrad's connection, so it does not show that the helicity *is* the axial torsion. That identification is the next step (below), and it has to be derived, not matched.
- The assignment of the upper spiral to TetA and the lower to TetB is the framework's reading.
- It makes no dynamical claim. Nothing here says how fast the vortex turns or what drives it.

## Next

1. **Transport theorem.** Carry a tetrad along a streamline from the TetA spiral through the throat into the TetB spiral. Show that it arrives as Proposition 2(b) of the Gram-matrix proof (connections that differ, by a torsion), not 2(a) (the covariant mirror, identical). Then compute its axial torsion and compare it with the helicity of (d).
2. **Drive and brake.** In the archive TetB can spin *with* the galaxy (drive) or *against* it (brake) (Coles Notes, vortex picture). By (b), the pure parity image always co-rotates. So a counter-rotating interior is a part of the flow that parity does *not* produce, an odd-swirl component. Whether drive and brake are exactly the even and odd swirl components is a question to settle, not a claim.

## Files

| File | Contents |
|---|---|
| [`verify_hourglass_lemma.py`](verify_hourglass_lemma.py) | Exact checks of (a)–(e): general axisymmetric field, and an explicit incompressible hourglass |
