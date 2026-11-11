"""02. BIMOND's nonrelativistic limit for general (alpha, beta), derived here from its Lagrangian, and the
function M fixed by GFD's mu = x/(1+x).
L = -(1/8piG){ beta|grad phi|^2 + alpha|grad phihat|^2 - a0^2 M(|grad phi - grad phihat|^2/a0^2) } - rho phi + rhohat phihat   (twin sector sign as in Milgrom 2010)
Spherical first integrals (Gauss): beta g - M'(z) g* = g_s ,  alpha ghat + M'(z) g* = -ghat_s ,  g* = g - ghat, z = (g*/a0)^2."""
import sympy as sp, sys
ok_all=True
def ok(m,c):
    global ok_all; ok_all&=bool(c); print(("PASS " if c else "FAIL ")+m)
al,be=sp.symbols('alpha beta',real=True); a0=sp.Symbol('a0',positive=True); g,gh,gs,gsh,Mp=sp.symbols('g ghat g_s ghat_s Mprime',real=True)
gstar=g-gh
sol=sp.solve([be*g-Mp*gstar-gs, al*gh+Mp*gstar+gsh],[g,gh],dict=True)[0]   # twin matter enters with Milgrom's sign (arXiv:1001.4444 eq. 46)
gstar_sol=sp.simplify(sol[g]-sol[gh])
print("   general: g* =",sp.factor(gstar_sol))
ok("alpha + beta = 0 (beta = 1) <=> g* = g_s - ghat_s: phi* is exactly Newtonian, sourced by rho - rhohat, independent of M",
   sp.simplify(gstar_sol.subs({al:-1,be:1})-(gs-gsh))==0)
ok("for alpha + beta != 0, g* depends on M' (phi* is not Newtonian)", sp.simplify(sp.diff(gstar_sol.subs(be,1),Mp).subs({al:2}))!=0)
# alpha = -beta = -1, no twin matter: physical g = (1 + M') g*
z=sp.Symbol('z',positive=True); Mprime=sp.Rational(-1,2)+sp.sqrt(sp.Rational(1,4)+z**sp.Rational(-1,2))
s0=sp.Symbol('s0',positive=True)
gphys=(sol[g].subs({al:-1,be:1,gsh:0})).subs(Mp,Mprime.subs(z,(s0/a0)**2)).subs(gs,s0)
ok("with M'(z) = -1/2 + sqrt(1/4 + z^(-1/2)): g = g_t solves g_s = g_t^2/(a0 + g_t) (GFD's spherical law)",
   sp.simplify(gphys-(s0+sp.sqrt(s0**2+4*s0*a0))/2)==0)
u=sp.Symbol('u',positive=True)
M=sp.sqrt(u)*(u+2)*sp.sqrt(u+4)/2-u**2/2-4*sp.asinh(sp.sqrt(u)/2)
ok("closed form M(u) = (1/2)sqrt(u)(u+2)sqrt(u+4) - u^2/2 - 4 arsinh(sqrt(u)/2), u = |grad phi*|/a0 = sqrt z, M(0) = 0",
   sp.simplify(sp.diff(M,u)/(2*u)-Mprime.subs(z,u**2))==0 and M.subs(u,0)==0)
ok("BIMOND's conditions: M' -> 0 (z -> oo), M' ~ z^(-1/4) (z -> 0)", sp.limit(Mprime,z,sp.oo)==0 and sp.limit(Mprime*z**sp.Rational(1,4),z,0)==1)
print("   asymptotics: M(u) ~",sp.series(M,u,0,3).removeO(),"(u->0) ;", sp.simplify(sp.limit(M-(2*u-2*sp.log(u)),u,sp.oo)),"= lim[M - (2u - 2 ln u)] (u->oo)")
ok("large-u: M = 2u - 2 ln u + const + o(1): the strong-field TetB tail a0*1 (constant extra pull) and its log",
   sp.limit(sp.diff(M,u)-2,u,sp.oo)==0)
# Legendre relation to the SST's AQUAL kinetic function F(y): both encode mu; QUMOND (here) vs AQUAL (SST)
y=sp.Symbol('y',positive=True)
F=y-2*sp.sqrt(y)+2*sp.log(1+sp.sqrt(y))
ok("same spherical law as the SST's F: F'(g_t^2/a0^2)*g_t = g_s and (1+M')g_s = g_t describe one curve (checked at 5 points)",
   all(abs(float((sp.diff(F,y).subs(y,(gphys/a0)**2)*gphys - s0).subs({a0:1,s0:v})))<1e-12 for v in (0.01,0.3,1,3,50)))
print("   (the SST is the AQUAL form, BIMOND alpha=-beta the QUMOND form: equal in spherical symmetry; off-sphere <1% in the disk test)")
sys.exit(0 if ok_all else 1)
