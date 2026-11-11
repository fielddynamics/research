"""Intersect the GFD algebra (Coles notes, gfd_algebra.py) with Milgrom's BIMOND (arXiv:0912.0790).
BIMOND: I = -(16piG)^-1 Int[ beta sqrt(g) R + alpha sqrt(ghat) Rhat - 2 (g ghat)^(1/4) f(kappa) a0^2 M(Ups/a0^2) ] + I_M[g] + Ihat_M[ghat]
NR:     L = -(1/8piG){ beta (grad phi)^2 + alpha (grad phihat)^2 - a0^2 M[(grad phi*)^2/a0^2] } - rho phi ,  phi* = phi - phihat
alpha + beta = 0, beta = 1:  Lap phi* = 4piG rho ,  Lap phi = div[(1 + M') grad phi*]   (QUMOND form)."""
import sympy as sp, numpy as np, itertools
ok=lambda m,c: print(("PASS " if c else "FAIL ")+m)
# 1. the tetrad Einstein-Hilbert 4-form is odd under internal parity -> the TetB root carries alpha = -beta
eps=np.zeros((4,4,4,4))
for p in itertools.permutations(range(4)): eps[p]=np.linalg.det(np.eye(4)[list(p)])
P=np.diag([1.,-1,-1,-1])
epsP=np.einsum('abcd,ai,bj,ck,dl->ijkl',eps,P,P,P,P)
ok("eps_abcd P^a_i P^b_j P^c_k P^d_l = det(P) eps = -eps: S_EH = Int eps_abcd e^a e^b R^cd flips sign for the opposite-orientation root",
   np.allclose(epsP,-eps))
print("     -> TetA (det e > 0) and TetB (det e~ < 0) with equal Planck mass give exactly BIMOND's alpha + beta = 0")
# 2. GFD mu fixes BIMOND's M:  nu = 1 + M'(z), z = |grad phi*|^2/a0^2, nu(y) = 1/2 + sqrt(1/4 + 1/y), y = sqrt z
z=sp.Symbol('z',positive=True); y=sp.sqrt(z)
Mp=sp.Rational(-1,2)+sp.sqrt(sp.Rational(1,4)+1/y)
ok("M'(z) -> 0 for z -> oo (Newtonian limit, as BIMOND requires)", sp.limit(Mp,z,sp.oo)==0)
ok("M'(z) ~ z^(-1/4) for z << 1 (MOND regime, as BIMOND requires)", sp.limit(Mp*z**sp.Rational(1,4),z,0)==1)
gs,gt,a0=sp.symbols('g_s g_t a0',positive=True)
gtot=(1+Mp.subs(z,(gs/a0)**2))*gs
ok("spherical: g_t = (1 + M') g_s reproduces GFD's g_s = g_t^2/(a0 + g_t)", sp.simplify(gtot-(gs+sp.sqrt(gs**2+4*gs*a0))/2)==0)
# closed form of M
u=sp.Symbol('u',positive=True)       # u = y = sqrt z ; dz = 2u du
Mu=sp.integrate((sp.Rational(-1,2)+sp.sqrt(sp.Rational(1,4)+1/u))*2*u,(u,0,u))
Mu=sp.simplify(Mu); print("     M as a function of u = |grad phi*|/a0:  M(u) =",Mu)
ok("dM/dz = M'(z) for the closed form", sp.simplify(sp.diff(Mu,u)/(2*u)-Mp.subs(z,u**2))==0)
# 3. the dictionary: phi* = TetA (Newtonian source field), phihat = TetB (phantom) potential
ga=sp.Symbol('g_A',positive=True)   # |grad phi*| = g_s
B=Mp.subs(z,(ga/a0)**2)*ga
ok("grad phihat = grad phi - grad phi* = M' grad phi*: |grad phihat| = a0 g_t/(a0 + g_t) = (1 - mu) g_t, the TetB field (saturates at a0)",
   sp.simplify((B-(a0*gtot/(a0+gtot)).subs(gs,ga)))==0 and sp.limit(B,ga,sp.oo)==a0)
# 4. the cross term comes from the opposite-sign pair of EH terms
gphi,ghat=sp.symbols('gphi ghat')
ok("(grad phi)^2 - (grad phihat)^2 = |g_A|^2 + 2 g_A.B with g_A = grad phi*, B = grad phihat: BIMOND's alpha = -beta supplies the a.B coupling that the Einstein-Cartan candidate had to add by hand",
   sp.expand((gphi**2-ghat**2).subs(gphi,ga+ghat))==sp.expand(ga**2+2*ga*ghat))
# 5. where C lives in the 24+16+24 grid: C = Gamma - Gammahat is symmetric (both Levi-Civita); C^i_00 = d_i phi* (diagonal (0,0) slot)
print("     C^lambda_(mu nu) = Gamma - Gammahat is lower-symmetric: it lives in V (x) Sym^2 V* (40), not in the torsion (24);")
print("     its NR component C^i_00 = d_i phi* sits in the diagonal (0,0) slot, the shared 16, where Newton's force sits.")
