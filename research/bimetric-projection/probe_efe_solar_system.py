"""External-field effect in the solar system for the SST's mu = x/(1+x) (QUMOND form, which shares the spherical law).
Units G M_sun = a0 = 1 (r_M = sqrt(GM/a0) = 1). External (galactic) field g_e = eta * z^.
Phantom field P = (nu(|g_N|) - 1) g_N, nu(y) = 1/2 + sqrt(1/4 + 1/y)  (inverse of the simple mu).
Tidal tensor of the phantom potential at the Sun: T_zz = 3 Int dr/r^2 Int [P_r P2(cos) + P_th cos sin] sin dth.
Anomalous potential dPhi = -(Q2/2) x_i x_j (e_i e_j - delta_ij/3)  ->  T_zz = -(2/3) Q2  (|Q2| reported)."""
import numpy as np, warnings
from scipy import integrate, optimize
warnings.filterwarnings('ignore')
nu=lambda y: 0.5+np.sqrt(0.25+1/y)
def Tzz(eta):
    def inner(r):
        th=np.linspace(0,np.pi,2001); ct,st=np.cos(th),np.sin(th)
        gx=-st/r**2; gz=-ct/r**2+eta                       # g_N = -r^/r^2 + eta z^   (x = radial-in-plane)
        gn=np.hypot(gx,gz); f=nu(gn)-1
        Px,Pz=f*gx,f*gz
        Pr=Px*st+Pz*ct; Pt=Px*ct-Pz*st
        P2=0.5*(3*ct**2-1)
        return np.trapezoid((Pr*P2+Pt*ct*st)*st,th)/r**2
    lo=integrate.quad(inner,1e-4,1,limit=400)[0]; hi=integrate.quad(lambda t: inner(1/t)/t**2,1e-4,1,limit=400)[0]  # r>1 via t=1/r
    return 3*(lo+hi)
GM=1.32712440018e20; a0=1.2e-10; rM=np.sqrt(GM/a0); unit=a0/rM
print(f"r_M = {rM/1.496e11:.0f} AU ; a0/r_M = {unit:.3e} s^-2")
for ge in (1.9e-10,2.4e-10):
    eta=ge/a0; T=Tzz(eta); Q2=1.5*abs(T)*unit
    print(f"g_e = {ge:.1e} (eta = {eta:.2f}):  T_zz = {T:+.4f} a0/r_M   ->  |Q2| = {Q2:.2e} s^-2")
print("Cassini (Hees et al. 2014): Q2 = (3 +- 3) x 10^-27 s^-2; theory range quoted there 2.1e-27 .. 4.1e-26 s^-2 across mu families")

# robustness to a0 and g_e
for a0v,gev in ((0.9e-10,2.4e-10),(1.0e-10,2.2e-10)):
    u2=a0v/np.sqrt(GM/a0v); print(f"a0 = {a0v:.1e}, g_e = {gev:.1e}: |Q2| = {1.5*abs(Tzz(gev/a0v))*u2:.2e} s^-2")
# every exchange-symmetric mu with the deep-MOND limit: mu = (1 + tanh h(ln x))/2, h odd, h ~ t/2 at both ends
# => 1 - mu ~ C/x at large x.  Family h(t) = t/2 + alpha tanh(t)  (alpha = 0 is GFD's mu)
def make(alpha):
    h=lambda t: 0.5*t+alpha*np.tanh(t); mu=lambda X: 0.5*(1+np.tanh(h(np.log(X))))
    ys=np.logspace(-8,8,4001); Xs=np.array([optimize.brentq(lambda X: X*mu(X)-yv,1e-12,1e12,xtol=1e-14) for yv in ys])
    lnu=np.log(Xs/ys); return mu,(lambda y: np.exp(np.interp(np.log(y),np.log(ys),lnu)))
def Tzz_nu(nuf,eta):
    def inner(r):
        th=np.linspace(0,np.pi,2001); ct,st=np.cos(th),np.sin(th)
        gx=-st/r**2; gz=-ct/r**2+eta; gn=np.hypot(gx,gz); f=nuf(gn)-1
        return np.trapezoid((f*(gx*st+gz*ct)*0.5*(3*ct**2-1)+f*(gx*ct-gz*st)*ct*st)*st,th)/r**2
    rs=np.logspace(-3,3,3001); return 3*np.trapezoid(np.array([inner(r) for r in rs])*rs,np.log(rs))
print("exchange-symmetric family (eta = 1.58):")
for al in (0.0,0.6,2.0,4.0):
    mu_,nu_=make(al); print(f"   alpha = {al:3.1f}: mu(10) = {float(mu_(np.array([10.0]))[0]):.4f}   |Q2| = {1.5*abs(Tzz_nu(nu_,1.58))*unit:.2e} s^-2")
print("   -> even an implausibly sharp transition (alpha = 4) stays above the Cassini 2-sigma bound ~9e-27 s^-2")
