# 05 · The SST action, time leg and stability

[Back](../README.md) · [Next](06_net_field.md)

## 1. The four-term action and the counting issue

The archive's SST writes the curvature term, the scalar response $F$, an electromagnetic coupling factor $e^{-2\Phi/c^2}$, and matter. In units with $c=1$ its schematic form is

$$S=\int\sqrt{-g}\,d^4x\left[\frac R{16\pi G}-\frac{a_0^2}{8\pi G}F(y)-\frac14 e^{-2\Phi/c^2}\mathcal F_{\mu\nu}\mathcal F^{\mu\nu}+\mathcal L_m\right].$$

Use $\mathcal F_{\mu\nu}$ for the electromagnetic tensor, to avoid confusion with the AQUAL energy. Normalizations in physical SI units require corresponding $c$ and electromagnetic factors. The important correction in P-sst is that the curvature already supplies the Newtonian $y$ term. If the written expression is interpreted as a literal second, independent full $F$ addition to the lapse response, its static field equation would involve $1+\mu$, not $\mu$. The proof adopts the GFD reading in which **the additional lapse energy is $F-y$**, making the total on shell equal to $F$. A self-contained covariant action should state that subtraction explicitly, rather than relying on double-counting being removed by interpretation.

In weak-field Newtonian gauge with lapse potential $\Phi$ and spatial potential $\Psi$, the static curvature contribution is $(|\nabla\Psi|^2-2\nabla\Phi\cdot\nabla\Psi)/(8\pi G)$. Add $-a_0^2(F-y)/(8\pi G)-\rho\Phi$. Varying $\Psi$ gives $\Delta(\Phi-\Psi)=0$, so matching boundary data imply $\Phi=\Psi$. Varying $\Phi$ then yields AQUAL. The matter source follows from $-mc^2\sqrt{-g_{00}}\simeq-mc^2-m\Phi$ when the potential is the metric lapse. It is not the variation of a decoupled extra scalar. In the stipulated weak-field truncation, the leading PPN slip is zero; this is not a complete PPN analysis or nonlinear lensing theorem.

## 2. Covariant, nonnegative argument of the energy

P-timeleg uses a unit timelike field $u$ normal to the chosen foliation, $u\cdot u=-1$, $a^\mu=u^\nu\nabla_\nu u^\mu$. Since $a\cdot u=0$, it is spacelike or zero. The correct scalar argument in this construction is

$$y=\frac{c^4}{a_0^2}a_\mu a^\mu\ge0.$$

For a static metric $ds^2=-N^2c^2dt^2+h_{ij}dx^idx^j$, $a_i=\partial_i\ln N$. Define $\Phi=c^2\ln N$; then $c^2a_i=\partial_i\Phi$ exactly in the static frame. The squared norm reduces to the spatial metric norm of the gradient. The time leg is part of a preferred-foliation description, not a second physical chamber and not reverse time.

Define the physical acceleration magnitude $A=c^2\sqrt{a_\mu a^\mu}$ and the correction $f_{\rm fol}(A)=a_0^2[F(A^2/a_0^2)-A^2/a_0^2]$. In the adopted Blanchet–Marsat type foliation action (in geometric units, with the appropriate $c$ factors restored), $\mu=1+f'_{\rm fol}/(2A)$. Thus the correction is $-2a_0A+2a_0^2\ln(1+A/a_0)$; the asymptotic derivative does not vanish. The original notes' open question about $F(y<0)$ is avoided by this definition of $y$. In FLRW the comoving time leg is geodesic, so $a=0$, $y=0$ and this correction vanishes on the homogeneous background. Perturbation cosmology remains distinct.

## 3. Stability, signal speeds and the net-field necessity

The preferred-foliation proof uses the static stability inequality $f'_{\rm fol}\le A f''_{\rm fol}\le0$ for the branch considered. Direct differentiation gives

$$f'_{\rm fol}=-2a_0\mu,\qquad f''_{\rm fol}=-2/(1+x)^2.$$

More generally the inequality is equivalent to $\mu'\ge0$ and $d[x(1-\mu)]/dx\ge0$. For the simple law, both follow from screening. This explains why removing the strong-field tail simply by choosing a steep interpolation would conflict with that branch's stability criterion. It does not prove stability of every covariant perturbation, strong coupling or all backgrounds.

If one instead used a separate Lorentzian kinetic scalar $y=g^{\mu\nu}\partial_\mu\Phi\partial_\nu\Phi/a_0^2$, the RAQUAL static-background characteristics would be $c_\perp=c$ and $c_\parallel=c\sqrt{2-\mu}$ where $x>0$. They follow from the principal symbol, not from $\mu\le1$. That is a different theory from the acceleration-of-time-leg construction. Do not transfer those speeds to the SST khronon. The archive's khronon analysis at $\beta=\lambda=0$ reports a degenerate nonpropagating mode with a tidal frequency $\omega^2=2\Omega^2/(2-\mu)=-dg/dr$ about a point mass; ordinary PPN expansions can be singular in that limit. It reports vanishing anomalous local preferred-frame response **under the prescribed net-field rule**, not an unconditional result from the original pointwise action. Non-stationary systems, cosmological perturbations, strong coupling, full PPN, and the EM exponential coupling to lapse normalization remain open.

## 4. What the upgrade settles and what it does not

The time-leg and quasi-static proofs give a coherent conditional static sector with minimal matter coupling and a nonnegative covariant $y$. They show precisely why the pointwise action cannot be the final model: it retains the $a_0$ self-tail and external-field quadrupole. The mountain-scale action is a further ownership prescription, developed next. A full relativistic local action selecting the ownership surfaces, including all moving-boundary variations, and a consistent treatment of the electromagnetic term and all modes are still required. Static convexity and the archive's selected khronon inequality do not replace these obligations.
