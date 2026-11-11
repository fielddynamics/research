"""Treat the share as a field and ask which equation fixes it.
(a) uniform split e_A = mu e, e_B = (1-mu) e with the locked potential;  (b) the gradient-leg split, u = ln(V/V0)."""
import sympy as sp
mu,y,u,lam,w=sp.symbols('mu y u lambda w',positive=True); b=[1,0,16,0,1]
ok=lambda m,c: print(("PASS " if c else "FAIL ")+m)
F=y-2*sp.sqrt(y)+2*sp.log(1+sp.sqrt(y))
# (a) uniform split: S = e_A^-1 e_B = c I, c = (1-mu)/mu, measure det e_A = mu^4 det e
c=(1-mu)/mu
U=sp.expand(sp.simplify(mu**4*sum(b[n]*sp.binomial(4,n)*c**n for n in range(5))))
bern=sum(b[n]*sp.binomial(4,n)*mu**(4-n)*(1-mu)**n for n in range(5))
ok("det(e_A) V(S) = sum_n b_n C(4,n) mu^(4-n) (1-mu)^n: the locked potential is the expected b_N when each leg is TetB with prob 1-mu",
   sp.expand(U-bern)==0)
ok("palindromic: U(mu) = U(1-mu); U = 98mu^4 - 196mu^3 + 102mu^2 - 4mu + 1", sp.expand(U-U.subs(mu,1-mu))==0 and sp.expand(U-(98*mu**4-196*mu**3+102*mu**2-4*mu+1))==0)
Up=sp.diff(U,mu)
ok("with Poisson-in-f_A energy mu*y plus k*U(mu), stationarity y = -k U'(mu) has its root at mu = 1/2 when y = 0 and |U'| <= 4: it cannot give mu(0) = 0 or mu -> 1",
   Up.subs(mu,sp.Rational(1,2))==0 and Up.subs(mu,0)==-4 and Up.subs(mu,1)==4)
W=mu+mu/(1-mu)+2*sp.log(1-mu)
ok("what the uniform split needs instead: W'(mu) = (mu/(1-mu))^2 = x^2, with W containing (1/2) ln det(e_B/e) = 2 ln(1-mu)",
   sp.simplify(sp.diff(W,mu)-(mu/(1-mu))**2)==0)
# (b) gradient leg: V = 49(1+lambda), w = V/V0 = 1+lambda, u = ln w
A=1-sp.exp(-u)                      # share of the deformed face = 1 - V0/V
Bu=-(sp.exp(u)-sp.exp(-u))+2*u      # auxiliary potential = -2(sinh u - u)
E=A*y+Bu
ok("B(w) = 1/w - w + 2 ln w = -2(sinh u - u), u = ln(V/V0): odd under V/V0 -> V0/V", sp.simplify((1/w-w+2*sp.log(w)).subs(w,sp.exp(u))-Bu)==0)
ustar=sp.log(1+sp.sqrt(y))
ok("dE/du = e^-u y - 2(cosh u - 1) = 0 at u* = ln(1 + sqrt y): the locked-potential ratio V/V0 = 1 + |grad Phi|/a0", sp.simplify(sp.diff(E,u).subs(u,ustar))==0)
ok("value E(u*) = F(y) = y - 2 sqrt y + 2 ln(1 + sqrt y): the SST kinetic function", sp.simplify(E.subs(u,ustar)-F)==0)
ok("coupling at the solution is the share: 1 - V0/V = sqrt(y)/(1+sqrt(y)) = mu(x)", sp.simplify(A.subs(u,ustar)-sp.sqrt(y)/(1+sp.sqrt(y)))==0)
d2=sp.simplify(sp.diff(E,u,2).subs(u,ustar))
ok("d2E/du2 = -2 sqrt(y) < 0 at u*: the share field sits at a maximum (as a Lagrange-type auxiliary field, like the Legendre form)", sp.simplify(d2+2*sp.sqrt(y))==0)
print("   (any mu admits some Legendre pair; the content here is that the auxiliary variable is ln of the locked potential on the")
print("    gradient leg, its coupling is the face share 1 - V0/V, and its potential is -2(sinh u - u))")
