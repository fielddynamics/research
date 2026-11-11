"""Localise the locked-HR mixing share: can F(y) come from an auxiliary share field?
L_aux(y, s) = y*s - W(s); stationarity in s should return the SST kinetic function F(y)."""
import sympy as sp
y,s,x,c,th=sp.symbols('y s x c theta',positive=True)
ok=lambda m,cond: print(("PASS " if cond else "FAIL ")+m)
F=y-2*sp.sqrt(y)+2*sp.log(1+sp.sqrt(y))
W=s+s/(1-s)+2*sp.log(1-s)
ok("W'(s) = (s/(1-s))^2 : the derivative of W is the squared odds", sp.simplify(sp.diff(W,s)-(s/(1-s))**2)==0)
sstar=sp.sqrt(y)/(1+sp.sqrt(y))
ok("stationary point of y*s - W(s) is s* = sqrt(y)/(1+sqrt(y)) = mu(sqrt y)", sp.simplify(sp.diff(y*s-W,s).subs(s,sstar))==0)
ok("value at s*: y*s* - W(s*) = F(y) = y - 2 sqrt y + 2 ln(1+sqrt y)", sp.simplify((y*s-W).subs(s,sstar)-F)==0)
ok("W''(s) = 2s/(1-s)^3 > 0: s* is a maximum of y*s - W, a Legendre pair (F convex <-> W convex)", sp.simplify(sp.diff(W,s,2)-2*s/(1-s)**3)==0)
# mixing-angle form with s = sin^2(theta), odds x = tan^2(theta)
Fth=sp.tan(th)**4-2*sp.tan(th)**2-2*sp.log(sp.cos(th)**2)
ok("with tan^2(theta) = sqrt(y):  F = tan^4 th - 2 tan^2 th - 2 ln cos^2 th (numeric, 0<th<pi/2)", all(abs(float((F.subs(y,sp.tan(t)**4)-Fth.subs(th,t)).evalf()))<1e-12 for t in (0.1,0.5,1.0,1.4)))
# express the share through the locked capacities
Cg=1+48*c**2; Cf=c**2*(c**2+48); V=1+96*c**2+c**4
Wc=sp.simplify(W.subs(s,Cf/V))
ok("W in locked capacities: W = C_f/V + C_f/C_g + 2 ln(C_g/V)", sp.simplify(Wc-(Cf/V+Cf/Cg+2*sp.log(Cg/V)))==0)
print("   (non-polynomial: the needed potential is not of the HR form sum beta_n e_n)")
# can the HR conformal mode c(x) be that auxiliary field? compare its gradient energy with the SST scalar energy
G=6.674e-11; cl=2.998e8; a0=1.2e-10; kpc=3.0857e19
for L in (1,10,100):
    for al in (1.0,6.888):
        ratio=3*al**2*cl**4*(1/(L*kpc))**2/a0**2     # [6 M_f^2 (dc)^2] / [a0^2/(8 pi G)] with dc ~ 1/L (O(1) change of x)
        print(f"   L = {L:3d} kpc, alpha = {al:5.3f}: HR conformal-mode gradient energy / SST scalar energy ~ {ratio:.1e}")
ok("the conformal mode cannot be auxiliary on galactic scales (ratio >> 1)", 3*cl**4*(1/(100*kpc))**2/a0**2>1e10)
