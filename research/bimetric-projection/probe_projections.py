import numpy as np, sympy as sp
x,t,Q,s=sp.symbols('x t Q s',positive=True)
print("=== T1: locked V along the TetA->TetB interpolation S = mu*I + (1-mu)*P = diag(1,sig,sig,sig)")
sig=sp.Symbol('sigma')
e2=3*sig+3*sig**2; e4=sig**3
V=sp.factor(1+16*e2+e4); print(" V(sigma) =",V)
Vx=sp.factor(sp.simplify(V.subs(sig,(x-1)/(x+1)))); print(" V(sigma(x)) =",Vx)
print(" V/98 at x=1:",Vx.subs(x,1)/98, "  zero of V at x =",sp.solve(sp.Eq(Vx,0),x))
for name,expr in [('V/98',Vx/98),('(V-0)/(V(inf))',Vx/sp.limit(Vx,x,sp.oo))]:
    print(" ",name,"vs mu:",[ (xx, float(expr.subs(x,xx)), xx/(1+xx)) for xx in (0.1,1,10)])
print("=== T2: locked screening, mu_eff(Q) = 1/(1+s), Q ~ M/r^3")
def sQ(Qn):
    rr=np.roots([Qn**2,6*Qn,6,-2]); re=[z.real for z in rr if abs(z.imag)<1e-10 and z.real>0]
    return min(re,key=lambda w:abs(w-1/3))
Qs=np.logspace(-3,4,15)
for Qn in Qs:
    sv=sQ(Qn); me=1/(1+sv); m=(me-0.75)/0.25
    print(f"  Q={Qn:9.3g}  s={sv:.4f}  mu_eff={me:.4f}  normalised m={m:.4f}   Q/(1+Q)={Qn/(1+Qn):.4f}   Q^(2/3)/(1+Q^(2/3))={Qn**(2/3)/(1+Qn**(2/3)):.4f}")
print("=== T3: locked decoupling integers")
d=(49,32,16,0); print("  d =",d,"  d2/d1^2 =",sp.Rational(16,32**2),"  d0=(K+D)^2?",d[0]==7**2," d1=2K^2?",d[1]==2*16," d2=K^2?",d[2]==16)
print("=== T4: can a polynomial (Galileon) static energy contain ln(1+sqrt y)? series check")
y=sp.Symbol('y',positive=True); F=y-2*sp.sqrt(y)+2*sp.log(1+sp.sqrt(y))
print("  F series in u=sqrt(y):",sp.series(F.subs(y,sp.Symbol('u')**2),sp.Symbol('u'),0,8))
