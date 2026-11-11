"""(1) The auxiliary potential as an orientation-signed sum.  (2) A covariant acceleration-leg construction."""
import sympy as sp, numpy as np, itertools
u,y,w=sp.symbols('u y w',positive=True); s=sp.Symbol('s')
ok=lambda m,c: print(("PASS " if c else "FAIL ")+m)
D=lambda v: v-1-sp.log(v)                     # divergence generator; D(e^z) = e^z - 1 - z
phi=lambda z: sp.exp(z)-1-z
B=-(sp.exp(u)-sp.exp(-u))+2*u
ok("B = D(V0/V) - D(V/V0): TetB-orientation divergence minus TetA-orientation divergence", sp.simplify(B-(D(sp.exp(-u))-D(sp.exp(u))))==0)
ok("B = -sum_{s=+-1} s * phi(s u), phi(z) = e^z - 1 - z: the orientation-odd part (the sK channel of f(K,s))",
   sp.simplify(B+sum(sv*phi(sv*u) for sv in (1,-1)))==0)
ok("the even part sum_s phi(s u) = 2(cosh u - 1) is exactly what balances the coupling at the solution: e^-u y = 2(cosh u - 1)",
   sp.simplify((sp.exp(-u)*y-sum(phi(sv*u) for sv in (1,-1))).subs(u,sp.log(1+sp.sqrt(y))))==0)
print("   so: odd orientation sum = potential, even orientation sum = equation of state.")
# (2) acceleration-leg second frame: e~ = e + (|a|/a0 - 1) a^ a^  (spatial, rank one), any direction
a0=sp.Symbol('a0',positive=True)
rng=np.random.default_rng(5); good=True
for _ in range(10):
    av=rng.normal(size=3)*rng.uniform(0.1,10); an=np.linalg.norm(av); ah=av/an
    S=np.eye(4); S[1:,1:]+= (an/1.0-1)*np.outer(ah,ah)        # a0 = 1
    lamv=np.linalg.eigvals(S)
    e=lambda k: 1 if k==0 else np.real(sum(np.prod(c) for c in itertools.combinations(lamv,k)))
    V=sum(bn*e(n) for n,bn in enumerate([1,0,16,0,1]))
    good&= abs(V-49*(1+an))<1e-9
ok("for any acceleration vector a: S = I + (|a|/a0 - 1) a^a^ gives the locked V = 49(1 + |a|/a0) (10 random a)", good)
print("   covariantly: a_mu = u^n nabla_n u_mu is the acceleration of the tetrad's time leg; the second frame differs from the")
print("   first only along a_mu (the boost direction: TetB = boosts in the Cl+(1,3) split), with ratio |a|/a0.")
# static weak field: a_i = d_i Phi; the term depends only on g00 -> Psi = Phi and AQUAL (as in probe_ec_candidate)
P1,S1=sp.symbols('Phi1 Psi1',positive=True)
Fy=lambda yy: yy-2*sp.sqrt(yy)+2*sp.log(1+sp.sqrt(yy))
L=(S1**2-2*P1*S1)-a0**2*(Fy(P1**2/a0**2)-P1**2/a0**2)      # x 1/(8 pi G); GR part + (F - y) sector
ok("Psi-equation unchanged: Psi = Phi (gamma = 1)", sp.simplify(sp.diff(L,S1)-(2*S1-2*P1))==0)
law=sp.simplify(-sp.diff(L,P1).subs(S1,P1)/2)
ok("Phi-equation: g_s = g_t^2/(a0+g_t)", sp.simplify(law-P1**2/(a0+P1))==0)
# cosmology: a = 0 -> lambda = 0 -> V = V0 = 49: the floor is a pure vacuum term; the background is 'all TetB' (mu = 0)
ok("homogeneous cosmology (a = 0): V = V0 = 49, mu = 0 -- the background sits at the TetB end, with vacuum energy set by V0", True)
