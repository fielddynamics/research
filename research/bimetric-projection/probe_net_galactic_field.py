"""SST with the coarse-grained matter coupling: only the galaxy's net (smoothed) field enters x = |grad Phi_bar|/a0.
Bound subsystems (a star with its planets) gravitate internally through the metric (GR).
(1) Milky Way rotation curve from smooth baryons (unchanged galactic predictions).
(2) What a local solar system feels: the net galactic field (uniform -> removed by free fall) plus its tide."""
import numpy as np
from scipy.special import i0,i1,k0,k1
G=6.674e-11; Ms=1.989e30; kpc=3.0857e19; a0=1.2e-10; AU=1.496e11
def v2_disk(R,M,Rd):
    S0=M/(2*np.pi*Rd**2); y=R/(2*Rd)
    return 4*np.pi*G*S0*Rd*y**2*(i0(y)*k0(y)-i1(y)*k1(y))
def v2_hern(R,M,a): return G*M*R/(R+a)**2
def gN(R):   # McMillan-type baryons as in the decoding-mass letter
    return (v2_hern(R,1.5e10*Ms,0.6*kpc)+v2_disk(R,4.57e10*Ms,2.2*kpc)+v2_disk(R,1.5e10*Ms,7.0*kpc))/R
gt=lambda gs: 0.5*(gs+np.sqrt(gs**2+4*gs*a0))
print("(1) Milky Way, smooth baryons, SST spherical law in the plane:")
for Rk in (5,8.2,15,25,50):
    R=Rk*kpc; print(f"    R = {Rk:5.1f} kpc   v_N = {np.sqrt(gN(R)*R)/1e3:6.1f}   v_SST = {np.sqrt(gt(gN(R))*R)/1e3:6.1f} km/s")
R0=8.2*kpc; h=1e-4*R0
ge=gt(gN(R0)); dgdR=(gt(gN(R0+h))-gt(gN(R0-h)))/(2*h)
print(f"(2) at the Sun: net galactic field g_e = {ge:.3e} m/s^2 (x = {ge/a0:.2f})")
print("    free fall removes the uniform part; what remains is the galactic tide:")
Trr=-dgdR; Tpp=-ge/R0   # radial and azimuthal tidal components of the smooth field (sign: stretching)
print(f"    tidal components: d g/dR = {dgdR:+.2e} s^-2 ,  g/R = {ge/R0:.2e} s^-2")
for name,d in (('Earth',1.0),('Saturn',9.58),('Neptune',30.1)):
    r=d*AU; print(f"    {name:8s} r = {d:5.2f} AU: galactic tidal acceleration ~ {max(abs(dgdR),ge/R0)*r:.1e} m/s^2")
print(f"    Cassini bound Q2 ~ 9e-27 s^-2 (2 sigma): galactic tide is {9e-27/max(abs(dgdR),ge/R0):.0f}x below it")
print("    no Sun-centred a0 monopole and no EFE quadrupole: inside the solar system the theory is GR + galactic tide")
print("    (in the local-source reading those were: constant 1.2e-10 m/s^2 at every planet, and Q2 = 4e-26 s^-2)")
