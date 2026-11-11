"""05. Local systems in BIMOND-GFD.
BIMOND as written applies M' to every source: around the Sun in the Milky Way's field it is QUMOND with GFD's nu,
which leaves (i) a constant a0 pull toward the Sun and (ii) an external-field quadrupole Q2.
Net-field rule (GFD, EINSTEIN_TETA_PARTITION.md): the TetB potential phihat is sourced by the coarse-grained galactic phi*:
   Lap phihat = div[ M'(|grad phibar*|) grad phibar* ]  (linear in phihat; QUMOND makes the rule a one-line change)
Inside a bound system grad phibar* is the galaxy's smooth field, so phihat contributes a uniform pull (cancels in free fall) + tide."""
import numpy as np, warnings
warnings.filterwarnings('ignore')
nu=lambda y: 0.5+np.sqrt(0.25+1/y)
def Tzz(eta):   # tidal tensor of the per-source phantom potential at the Sun, units a0/r_M (G M_sun = a0 = 1)
    def inner(r):
        th=np.linspace(0,np.pi,2001); ct,st=np.cos(th),np.sin(th)
        gx=-st/r**2; gz=-ct/r**2+eta; gn=np.hypot(gx,gz); f=nu(gn)-1
        return np.trapezoid((f*(gx*st+gz*ct)*0.5*(3*ct**2-1)+f*(gx*ct-gz*st)*ct*st)*st,th)/r**2
    rs=np.logspace(-3,3,3001); return 3*np.trapezoid(np.array([inner(r) for r in rs])*rs,np.log(rs))
GM=1.32712440018e20; a0=1.2e-10; AU=1.496e11; rM=np.sqrt(GM/a0); ge=2.28e-10
Q2=1.5*abs(Tzz(ge/a0))*a0/rM
print(f"per-source BIMOND (as written): constant extra pull at every planet = a0 = {a0:.1e} m/s^2; Q2 = {Q2:.2e} s^-2")
print(f"   Cassini: Q2 = (3 +- 3)e-27 s^-2 -> excluded by {Q2/3e-27:.0f}x the central value")
R0=8.2*3.0857e19; tide=ge/R0
print(f"net-field rule: phihat from the galaxy's smooth phi*: uniform part {ge*(1-1.9/2.9):.2e} m/s^2 (cancels in free fall), tide ~ {tide:.1e} s^-2")
print(f"   at Saturn (9.58 AU): {tide*9.58*AU:.1e} m/s^2 ; Cassini margin ~ {9e-27/tide:.0f}x")
print("   between the bodies: phi* alone, i.e. Newton/GR (TetA), exactly; twin and ordinary matter do not interact there")
