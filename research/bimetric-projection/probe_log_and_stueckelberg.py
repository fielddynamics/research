"""(1) Why standard bimetric projections give density scaling and the GFD one gives acceleration scaling.
(2) The SST's departure from GR as a relative entropy of the locked capacity ratio.
(3) Scale needed if the log comes from integrating out an ultralocal Gaussian field on the midpoint frame."""
import sympy as sp, numpy as np
r,x,w,a0=sp.symbols('r x w a0',positive=True); h=sp.Function('h'); Phi=sp.Function('Phi')
ok=lambda m,c: print(("PASS " if c else "FAIL ")+m)
# (1) Stueckelberg reference frame e~^i = d phi^i with phi^i = x^i h(r): eigenvalues of S
X=sp.symbols('X Y Z',real=True); R=sp.sqrt(sum(q**2 for q in X))
J=sp.Matrix(3,3,lambda i,j: sp.diff(X[i]*h(R),X[j]))
Jr=sp.simplify(J.subs({X[0]:r,X[1]:0,X[2]:0}).doit())
print("   spatial S for phi^i = x^i h(r), on the x-axis:",Jr)
ok("Stueckelberg frame: radial eigenvalue (r h)', transverse eigenvalues h (twice)",
   sp.simplify(Jr[0,0]-sp.diff(r*h(r),r))==0 and sp.simplify(Jr[1,1]-h(r))==0 and sp.simplify(Jr[2,2]-h(r))==0)
ok("GFD gradient leg diag(1,1,1,lambda) needs h = 1 and (r h)' = lambda: possible only for lambda = 1 -> not a pullback of a flat reference frame",
   sp.simplify(sp.diff(r*1,r))==1)
print("   decoupling limit (h = 1 - pi'/(r L^3)): eigenvalues 1 - pi''/L^3, 1 - pi'/(r L^3): second derivatives -> density M/r^3")
print("   GFD gradient leg: lambda = Phi'/a0: first derivative -> acceleration M/r^2")
# a pullback that does carry the acceleration: h = Phi/(a0 r)  ->  radial Phi'/a0, transverse Phi/(a0 r)
G,M=sp.symbols('G M',positive=True)
hK=-(G*M/r)/(a0*r)    # Phi = -GM/r
ok("with h = Phi/(a0 r) and Kepler Phi = -GM/r: S = diag(1, -x, -x, x), x = GM/(a0 r^2)  (radial +x, transverse -x)",
   sp.simplify(sp.diff(r*hK,r)-G*M/(a0*r**2))==0 and sp.simplify(hK+G*M/(a0*r**2))==0)
lam1=sp.Symbol('l')
ev=[1,-x,-x,x]
import itertools
e=lambda k: sp.Integer(1) if k==0 else sum(sp.Mul(*c) for c in itertools.combinations(ev,k))
Vk=sp.expand(1+16*e(2)+e(4)); print("   locked V on that frame:",sp.factor(Vk),"  (not the partition form; the rank-one leg is the one that gives 49(1+x))")
# (2) relative entropy
D=w-1-sp.log(w)
KL=sp.Rational(1,2)*(w-1-sp.log(w))   # KL( N(0,w) || N(0,1) )
y=sp.Symbol('y',positive=True); F=y-2*sp.sqrt(y)+2*sp.log(1+sp.sqrt(y))
ok("F(y) - y = -2 D(w) = -4 KL( N(0,w) || N(0,1) ),  w = V(S)/V0 = 1 + sqrt(y)", sp.simplify((F-y)-(-4*KL).subs(w,1+sp.sqrt(y)))==0)
ok("D is the Bregman divergence of -ln: D(w) = (-ln w) - (-ln 1) - (-1)(w-1)", sp.simplify(D-((-sp.log(w))-0-(-1)*(w-1)))==0)
# (3) ultralocal Gaussian: Int d^N psi exp(-psi^T A psi /2) ~ det(A)^(-1/2) per point; energy density + (N/2) Lc^4 ln det A
#     need energy (a0^2/8piG) * 2 ln det((I+S)/2)
hbar=1.054571817e-34; c=2.99792458e8; Gn=6.674e-11; a0n=1.2e-10; eV=1.602176634e-19
k=2*a0n**2/(8*np.pi*Gn)                       # J/m^3
for N in (2,4,8):
    Lc=(2*k/N*(hbar*c)**3)**0.25/eV
    print(f"   N = {N} real components: cutoff L_c = {Lc*1e3:.2f} meV")
rhoL=0.685*3*(70e3/3.0857e22)**2/(8*np.pi*Gn)*c**2
print(f"   dark-energy scale (rho_Lambda (hbar c)^3)^(1/4) = {(rhoL*(hbar*c)**3)**0.25/eV*1e3:.2f} meV ; required coefficient / rho_Lambda = {k/rhoL:.3f}")
