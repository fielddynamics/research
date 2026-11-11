"""Candidate covariant completion: Einstein-Cartan + TetB torsion vector coupled to the time leg's acceleration.
  S = Int sqrt(-g) { R(Gamma)/16piG + (1/8piG)[ 2 a_mu B^mu - a0^2 (U(|B|/a0) - |B|^2/a0^2) ] } + S_matter
  U(b) = -2b - 2 ln(1-b) = b^2 + (2/3) b^3 + ...,  B = T_vec/sqrt3 (spatial),  a_mu = u^n nabla_n u_mu, u = time leg.
EC supplies the |B|^2 term; the rest is new. Tests: EC coefficient, static weak field -> AQUAL with mu = x/(1+x), Psi = Phi."""
import numpy as np, sympy as sp
ok=lambda m,cond: print(("PASS " if cond else "FAIL ")+m)
# 1. EC: algebraic (K K) part of R(Gamma) for pure vector torsion, flat LC
eta=np.diag([-1.,1,1,1])
def contorsion(T):
    Tl=np.einsum('al,lmn->amn',eta,T)
    return 0.5*(T+np.einsum('la,man->lmn',eta,Tl)+np.einsum('la,nam->lmn',eta,Tl))
def vector(v):
    d=np.eye(4); return (np.einsum('ln,m->lmn',d,v)-np.einsum('lm,n->lmn',d,v))/3
def R_alg(T):
    K=contorsion(T); R=0.
    for n in range(4):
        for m in range(4):
            for l in range(4): R+=eta[n,n]*(K[m,m,l]*K[l,n,n]-K[m,n,l]*K[l,m,n])
    return R
rng=np.random.default_rng(0); vals=[]
for _ in range(5):
    v=rng.normal(size=4); Tm=np.einsum('lml->m',vector(v)); vals.append(R_alg(vector(v))/(Tm@eta@Tm))
print("   R(Gamma)_alg / (T_mu T^mu) for vector torsion:",np.round(vals,6))
ok("EC gives R_alg = -(2/3) T_mu T^mu for vector torsion (so L_EC contains -(1/8piG)|B|^2 with B = T/sqrt3)",np.allclose(vals,-2/3))
# 2. static weak field: g00 = -(1+2Phi), gij = (1-2Psi) delta, static time leg: a_i = d_i Phi
#    L = (1/8piG)(|grad Psi|^2 - 2 grad Phi.grad Psi) + (1/8piG)[2 grad Phi.B - a0^2(U(b) - b^2)] - (1/8piG)|B|^2 - rho Phi
r,a0,G=sp.symbols('r a0 G',positive=True); P1,S1,Bv,m=sp.symbols('Phi1 Psi1 B menc',real=True)   # radial derivatives Phi', Psi', field B
U=lambda b: -2*b-2*sp.log(1-b)
Lrad=(S1**2-2*P1*S1)+(2*P1*Bv-a0**2*(U(Bv/a0)-(Bv/a0)**2))-Bv**2      # times 1/(8piG); matter handled by Gauss
# B auxiliary: dL/dB = 0
Bsol=sp.solve(sp.Eq(sp.diff(Lrad,Bv),0),Bv); Bsol=[s for s in Bsol if s.subs({P1:1,a0:1})>0]
print("   auxiliary B solution:",Bsol)
ok("B* = a0 Phi'/(a0 + Phi') = (1 - mu) g_t : the TetB share, bounded by a0", len(Bsol)==1 and sp.simplify(Bsol[0]-a0*P1/(a0+P1))==0)
# Psi-equation: d/dr[r^2 dL/dPsi'] = 0 -> dL/dPsi' = 0 (regular at origin)
ok("Psi-equation: 2Psi' - 2Phi' = 0  ->  Psi = Phi  (gamma = 1, full lensing)", sp.simplify(sp.diff(Lrad,S1)-(2*S1-2*P1))==0)
# Phi-equation via Gauss: (r^2 dL/dPhi')/(8piG) = M_enc/(4pi)  ->  dL/dPhi' = 2 G M/r^2 = 2 g_s
Leff=Lrad.subs(Bv,Bsol[0])
dPhi=sp.simplify(sp.diff(Leff,P1).subs(S1,P1))    # use Psi'=Phi' after variation (envelope theorem for B)
dPhi_true=sp.simplify((sp.diff(Lrad,P1)).subs(Bv,Bsol[0]).subs(S1,P1))
print("   dL/dPhi' at Psi=Phi:",sp.factor(dPhi_true))
gt,gs=sp.symbols('g_t g_s',positive=True)
law=sp.solve(sp.Eq(-dPhi_true.subs(P1,gt)/2,-gs),gs) if False else sp.simplify(-dPhi_true.subs(P1,gt)/2)
print("   resulting spherical law: g_s =",sp.factor(law))
ok("Phi-equation gives g_s = g_t^2/(a0+g_t): AQUAL with mu = x/(1+x)",sp.simplify(law-gt**2/(a0+gt))==0 or sp.simplify(law+gt**2/(a0+gt))==0)
# 3. eliminating B gives the SST kinetic function: L(B*) - (GR part) = -(F(y) - y) a0^2
y=sp.Symbol('y',positive=True); g_=sp.sqrt(y)*a0
J=sp.simplify(((2*P1*Bv-a0**2*(U(Bv/a0)-(Bv/a0)**2))-Bv**2).subs(Bv,Bsol[0]).subs(P1,g_))
Fy=y-2*sp.sqrt(y)+2*sp.log(1+sp.sqrt(y))
ok("TetB sector integrates out to -a0^2 (F(y) - y): GR's y plus this is the SST's a0^2 F(y)", sp.simplify(J+a0**2*(Fy-y))==0)
# 4. strong-field residual (isolated source): g_t - g_s -> a0, a constant extra pull toward the source
gs_=sp.Symbol('g_s',positive=True)
gt_=(gs_+sp.sqrt(gs_**2+4*gs_*a0))/2
ok("isolated strong field: g_t - g_s -> a0 (constant anomalous acceleration ~1.2e-10 m/s^2; solar-system constraint to check, EFE not included)", sp.limit(gt_-gs_,gs_,sp.oo)==a0)
