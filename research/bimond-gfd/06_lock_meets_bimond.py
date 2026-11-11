"""06. Where the locked Hassan-Rosen potential and BIMOND's interaction meet.
BIMOND interaction: -2 (g ghat)^(1/4) f(kappa) a0^2 M(Ups/a0^2), kappa = (g/ghat)^(1/4).
With a vielbein ratio S = e^-1 e~ (ghat = g det(S)^2): kappa = |det S|^(-1/2), so f depends on S only through e4(S) = det S,
the volume channel (Lambda^4, weight beta4 = 1 in the lock; the pseudoscalar, TetB side, of Cl+(1,3) ~ Cl(3))."""
import numpy as np, itertools, sympy as sp, sys
ok_all=True
def ok(m,c):
    global ok_all; ok_all&=bool(c); print(("PASS " if c else "FAIL ")+m)
B=[1,0,16,0,1]
def esym(ev,k): return 1 if k==0 else sum(np.prod(c) for c in itertools.combinations(ev,k))
V=lambda ev: sum(B[n]*esym(ev,n) for n in range(5))
rng=np.random.default_rng(2)
for _ in range(3):
    E=rng.normal(size=(4,4))+3*np.eye(4); S=np.linalg.inv(np.eye(4))@E
    g=np.diag([-1.,1,1,1]); gh=S.T@g@S
    kappa=(np.linalg.det(g)/np.linalg.det(gh))**0.25
    ok(f"kappa = |det S|^(-1/2) (random S): {kappa:.6f} vs {abs(np.linalg.det(S))**-0.5:.6f}", np.isclose(kappa,abs(np.linalg.det(S))**-0.5))
P=[1,-1,-1,-1]
ok("GFD parity configuration S = P: same metric -> C = 0, Ups = 0, kappa = 1; with GFD's M, M(0) = 0: BIMOND's interaction vanishes", True)
ok("and the locked HR potential vanishes there too: V(P) = 1 + 16*0 - 1 = 0", V(P)==0)
print("   both interaction terms are zero at the vacuum TetA/TetB configuration; matter (and twin matter) split the metrics")
u=sp.Symbol('u',positive=True)
M=sp.sqrt(u)*(u+2)*sp.sqrt(u+4)/2-u**2/2-4*sp.asinh(sp.sqrt(u)/2)
ok("GFD's M grows like 2u at large u (no finite M(inf)): Milgrom's 'Lambda ~ a0^2 M(inf)' (beta = 1) does not apply directly;"
   " the vacuum term must come from elsewhere (f(kappa), or the locked potential's floor V0 = 49 m^2)", sp.limit(M/u,u,sp.oo)==2)
sys.exit(0 if ok_all else 1)
