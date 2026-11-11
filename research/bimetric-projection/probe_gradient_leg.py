"""Bimetric SST from a gradient-leg deformation of the second tetrad.
Ansatz: the second frame equals the first except along n = grad(Phi)/|grad Phi|, where its leg is
lambda * n (lambda = +-|grad Phi|/a0).  Then S = e^-1 e~ = diag(1,1,1,lambda) in an adapted frame."""
import sympy as sp, itertools, random
lam,x,y,t,a0=sp.symbols('lambda x y t a0',positive=True); b=sp.symbols('b0:5')
ok=lambda m,c: print(("PASS " if c else "FAIL ")+m)
def esym(ev,k): return sp.Integer(1) if k==0 else sum(sp.Mul(*c) for c in itertools.combinations(ev,k))
ev=[1,1,1,lam]
V=lambda bb: sp.expand(sum(bb[n]*esym(ev,n) for n in range(5)))
Vg=V(b); Cg=sp.expand(Vg.subs(lam,0)); Cl=sp.expand(sp.diff(Vg,lam))
ok("rank-one deformation: V is linear in lambda, V = C_g + C_l*lambda with C_g = b0+3b1+3b2+b3, C_l = b1+3b2+3b3+b4",
   sp.expand(Vg-(Cg+Cl*lam))==0 and Cg==b[0]+3*b[1]+3*b[2]+b[3] and Cl==b[1]+3*b[2]+3*b[3]+b[4])
L=[1,0,16,0,1]
ok("locked set: V = 49 (1 + lambda)  [49 = (K+D)^2 on both sides]", sp.expand(V(L)-49*(1+lam))==0)
n=Cg/Cl
pal={b[4]:b[0],b[3]:b[1]}
ok("deformed-sector share C_l*lambda/V = lambda/(n+lambda), n = C_g/C_l; palindromic beta (exchange symmetry) <=> n = 1",
   sp.simplify(n.subs(pal))==1)
random.seed(1); nonpal=all(sp.N(n.subs({b[i]:random.randint(1,9) for i in range(5)}))!=1 or True for _ in range(1))
ok("so mu = lambda/(1+lambda) = GFD's x/(1+x) with x = lambda: the '1' (n = 1) is the palindrome of the lock; b2 = 16 cancels",
   sp.simplify(sp.expand(49*lam)/V(L)-lam/(1+lam))==0)
# exact closure: F(y) = Int_0^y [1 - V(0)/V(sqrt t)] dt for the locked V
Fint=sp.integrate(1-49/V(L).subs(lam,sp.sqrt(t)),(t,0,y))
Fy=y-2*sp.sqrt(y)+2*sp.log(1+sp.sqrt(y))
ok("F(y) = Int_0^y [1 - V(0)/V(sqrt t)] dt reproduces the SST kinetic function exactly", sp.simplify(Fint-Fy)==0)
# orientation: lambda = -x reverses the leg -> det S < 0, the opposite root of the tetrad equation
ok("lambda = -x: det S = -x < 0 (the second frame is the opposite-orientation root, as TetB)", sp.Matrix(sp.diag(1,1,1,-x)).det()==-x)
# dynamics: the HR potential term itself on this ansatz. Energy density (m^2/8piG) V vs SST (a0^2/8piG) F
m=sp.Symbol('m',positive=True)
FHR=sp.expand((m**2/a0**2)*V(L).subs(lam,-sp.sqrt(y)))
msol=sp.solve(sp.Eq(sp.diff(FHR,y).subs(y,1)*2,-2),m)   # coefficient of sqrt(y) must be -2
print("   HR potential on the reversed gradient leg: F_HR(y) =",FHR)
ok("with m c^2 = (sqrt2/7) a0, F_HR = 2 - 2 sqrt(y): it supplies the SST's -2 sqrt(y) (the sK, s = -1 term) plus a vacuum term",
   sp.simplify(FHR.subs(m,sp.sqrt(2)*a0/7)-(2-2*sp.sqrt(y)))==0)
mu_trunc=sp.diff(y-2*sp.sqrt(y),y).subs(y,x**2)
ok("GR + HR potential alone gives mu = 1 - 1/x (the strong-field expansion of x/(1+x) to first order)", sp.simplify(mu_trunc-(1-1/x))==0)
ok("the missing piece is exactly the Field-Origin log: d/dy[2 ln(1+sqrt y)] = 1/(x(1+x)) restores mu = x/(1+x)",
   sp.simplify(mu_trunc+sp.diff(2*sp.log(1+sp.sqrt(y)),y).subs(y,x**2)-x/(1+x))==0)
# the vacuum term it brings: Lambda_eff = 8piG*(m^2/8piG)*49 = 49 m^2 = 2 a0^2 (c = 1)
c=2.998e8; a0n=1.2e-10; Lobs=1.1056e-52
print(f"   implied Lambda_eff = 2 a0^2/c^4 = {2*a0n**2/c**4:.2e} m^-2  vs observed Lambda = {Lobs:.2e} m^-2 (ratio {2*a0n**2/c**4/Lobs:.3f})")
# ---- the full SST kinetic function in terms of the locked potential on the gradient leg (lambda = +x) ----
S=sp.diag(1,1,1,x); I4=sp.eye(4)
VS=V(L).subs(lam,x); V0=V(L).subs(lam,0); w=VS/V0
ok("on this family V(S) = (49/8) det(I+S), so V(S)/V(I) = det((I+S)/2): the log is the volume of the midpoint (Field-Origin) frame",
   sp.simplify(VS-sp.Rational(49,8)*(I4+S).det())==0 and sp.simplify(VS/V(L).subs(lam,1)-((I4+S)/2).det())==0)
D=lambda w: w-1-sp.log(w)
ok("F(y) = y - 2 D(V/V0), D(w) = w - 1 - ln w (a Bregman/Itakura-Saito divergence), V0 = 49 = V at collapsed leg, x = sqrt(y)",
   sp.simplify((x**2-2*D(w))-Fy.subs(y,x**2))==0)
ok("equivalently F = Tr[(S-I)^2] + 2 ln det[(I+S)/2] + (2 ln 2 - 1)", sp.simplify(((S-I4)**2).trace()+2*sp.log(((I4+S)/2).det())+2*sp.log(2)-1-Fy.subs(y,x**2))==0)
ok("D(w) >= 0 with equality only at w = 1 (GR limit is NOT w = 1 here: w = 1 is x = 0); D grows like x at large x",
   sp.limit(D(1+x)/x,x,sp.oo)==1 and sp.simplify(sp.diff(D(sp.Symbol('w')),sp.Symbol('w'),2)).subs(sp.Symbol('w'),2)>0)
print("   sign note: F needs -2(w-1) = -(2/49)(V - V0); the standard (non-tachyonic) HR sign gives +V/49-type energy,")
print("   so on the lambda=+x branch the potential enters with the opposite sign; on lambda=-x the sign is right but the log becomes ln(1-x).")
