"""Relate the GFD SST to the locked Hassan-Rosen theory directly.
Proportional branch f = c^2 g of HR: sector 'capacities' C_g (g-equation Lambda) and C_f (f-equation, scaled),
mixing odds x = tan^2(theta) = alpha^2 c^2, shares sin^2/cos^2.  Compare with GFD's mu(x) = x/(1+x)."""
import sympy as sp
c,al,x=sp.symbols('c alpha x',positive=True); b=sp.symbols('b0:5')
V=lambda bb: sum(bb[n]*sp.binomial(4,n)*c**n for n in range(5))           # V(cI)
Cg=lambda bb: sum(bb[n]*sp.binomial(3,n)*c**n for n in range(4))          # Lambda_g/m^2
Cf=lambda bb: c*sum(bb[n+1]*sp.binomial(3,n)*c**n for n in range(4))      # c^2 * Lambda_f*alpha^2/m^2 (scaled)
ok=lambda s,cond: print(("PASS " if cond else "FAIL ")+s)
ok("V(cI) = C_g + C_f for every beta (binomial identity)", sp.expand(V(b)-Cg(b)-Cf(b))==0)
bg=sp.expand(al**2*c**2*Cg(b)-Cf(b)*c**0*1)     # background: alpha^2 c^2 C_g = C_f ?
hsvs=al**2*(b[0]*c+3*b[1]*c**2+3*b[2]*c**3+b[3]*c**4)-b[4]*c**3-3*b[3]*c**2-3*b[2]*c-b[1]
ok("HR proportional-background equation  <=>  alpha^2 c^2 = C_f/C_g  (odds = capacity ratio)", sp.simplify(bg - c*hsvs)==0)
L=[1,0,16,0,1]
print("locked: C_g =",sp.factor(Cg(L)),"  C_f =",sp.factor(Cf(L)),"  V =",sp.factor(V(L)))
xc=sp.simplify(Cf(L)/Cg(L)); print("locked odds x(c) = tan^2 theta =",xc)
ok("x(1/c) = 1/x(c): exchange g<->f is x -> 1/x", sp.simplify(xc.subs(c,1/c)*xc-1)==0)
mu_f=sp.simplify(xc/(1+xc)); ok("sin^2 theta = x/(1+x) = C_f/V  (GFD form, with V the locked potential as normaliser)", sp.simplify(mu_f-Cf(L)/V(L))==0)
ok("symmetric point c = 1: x = 1, share 1/2, each sector capacity 49, V = 98", xc.subs(c,1)==1 and Cg(L).subs(c,1)==49 and V(L).subs(c,1)==98)
ok("x -> 0 as c -> 0 and x -> oo as c -> oo (pure-sector endpoints)", sp.limit(xc,c,0)==0 and sp.limit(xc,c,sp.oo)==sp.oo)
c2=sp.solve(sp.Eq(c**4+48*(1-x)*c**2-x,0),c**2); print("inverse: c^2(x) =",[sp.simplify(s) for s in c2])
th=sp.atan(sp.Rational(3,28)); xt=sp.tan(th)**2
cxt=sp.sqrt([s for s in c2 if s.subs(x,xt).evalf()>0][0].subs(x,xt)).evalf()
print(f"Paper XII theta = atan(3/28): x = {sp.nsimplify(xt)} , sin^2 theta = {float(xt/(1+xt)):.5f} , c = {float(cxt):.5f}, alpha = {float(sp.sqrt(xt)/cxt):.3f}")
# Localising the odds through the conformal mode f = Omega^2 g: reduced action
#   (M_g^2 + M_f^2 Omega^2) R + 6 M_f^2 (dOmega)^2 - 2 m^2 M_g^2 V(Omega I)
# matter on g feels G_eff = G_g/(1+x) with x = alpha^2 Omega^2 >= 0  -> G_eff <= G_g; GFD needs G_eff = G/mu -> oo as x -> 0
Gg=sp.Symbol('G_g',positive=True); Geff=Gg/(1+x)
ok("conformal-mode localisation: G_eff = G_g/(1+x) is bounded by G_g (cannot give the deep-field 1/mu growth)", sp.limit(Geff,x,0)==Gg)
gs,gt,a0=sp.symbols('g_s g_t a0',positive=True)
print("  with x = g_t/a0 it gives g_s =",sp.factor(sp.solve(sp.Eq(gt,(Geff/Gg).subs(x,gt/a0)*gs),gs)[0]),"  vs GFD g_s =",gt**2/(a0+gt))
print("  with x = a0/g_t it gives g_s =",sp.factor(sp.solve(sp.Eq(gt,(Geff/Gg).subs(x,a0/gt)*gs),gs)[0]))
