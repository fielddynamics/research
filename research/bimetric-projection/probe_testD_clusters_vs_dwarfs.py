"""Test D: outer-halo globular clusters vs Milky Way dwarfs at low acceleration.
Option 1: bound star clusters (no Field Origin) are pure TetA -> Newtonian; dwarf galaxies -> GFD with the MW net field.
Option 2: everything -> GFD with the MW net field (MOND-like with external field).
Estimators (Wolf et al. 2010 mass within r_1/2 = 4Re/3, M(<r_1/2) = M/2):
  Newtonian      sigma^2 = G M / (8 Re)
  GFD, EFE-dom.  sigma^2 = G M / (8 Re mu(x)),  mu = x/(1+x),  x = (g_e + g_in)/a0   (quasi-Newtonian, G_eff = G/mu; anisotropy ignored)
  check: McGaugh 2016 deep-EFE form sigma^2 = a0 G M/(3 g_e r_1/2) for Crater II.
Data: Pal 14 (Jordi+2009), Pal 4 (Frank+2012), Crater II (Caldwell+2017; Ji+2021 S5), Antlia 2 (Ji+2021)."""
import numpy as np
G=4.30091e-3   # pc (km/s)^2 / Msun
a0=3700/1000.0 # km^2 s^-2 pc^-1  (a0 = 3700 km^2 s^-2 kpc^-1)
VMW=184.0
objs=[ # name, type, M (Msun) [low, best, high], Re (pc), D_GC (kpc), sigma_obs, err
 ("Pal 14","GC",(5.9e3,1.2e4,1.25e4),26.0,71,(0.38,0.12)),
 ("Pal 4","GC",(2.0e4,2.98e4,2.98e4),18.4,103,(0.87,0.18)),
 ("Crater II","dwarf",(1.6e5,3.3e5,6.6e5),1066.,120,(2.34,0.36)),
 ("Antlia 2","dwarf",(0.8e6,1.66e6,3.3e6),2541.,130,(5.98,0.37)),
]
mu=lambda x: x/(1+x)
print(f"{'object':10s} {'type':5s} {'x_e':>6s} {'x_in':>7s} {'sig_N':>12s} {'sig_GFD':>12s} {'observed':>11s}   verdict")
for name,typ,(Ml,M,Mh),Re,D,(so,se) in objs:
    ge=VMW**2/(D*1000)/a0                         # x_e
    rh=4*Re/3
    sN=lambda m: np.sqrt(G*m/(8*Re))
    gin=lambda m: G*(m/2)/rh**2/a0
    sG=lambda m: np.sqrt(G*m/(8*Re)/mu(ge+gin(m)))
    rng=lambda f: f"{f(M):.2f}[{f(Ml):.2f}-{f(Mh):.2f}]"
    zN=(so-sN(M))/se; zG=(so-sG(M))/se
    print(f"{name:10s} {typ:5s} {ge:6.3f} {gin(M):7.4f} {rng(sN):>14s} {rng(sG):>14s} {so:5.2f}+-{se:.2f}   z_N={zN:+.1f}  z_GFD={zG:+.1f}")
# cross-check with McGaugh's deep-EFE formula for Crater II
M=3.3e5; rh=4*1066/3; ge=VMW**2/120e3
print(f"\ncheck: McGaugh deep-EFE Crater II sigma = {np.sqrt(3700/1000*G*M/(3*ge*rh)):.2f} km/s (paper: 2.1)")
print("\nrobustness: McGaugh-style estimator sigma^2 = G M /(4 Re mu(x)) (full M; ~sqrt2 larger):")
for name,typ,(Ml,M,Mh),Re,D,(so,se) in objs:
    ge=VMW**2/(D*1000)/a0; rh=4*Re/3; gin=G*(M/2)/rh**2/a0
    s=np.sqrt(G*M/(4*Re)/mu(ge+gin)); print(f"   {name:10s} sigma_GFD = {s:.2f}  observed {so:.2f}+-{se:.2f}  z = {(so-s)/se:+.1f}")
