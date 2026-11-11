"""01. The tetrad Einstein-Hilbert 4-form is odd under the parity that maps TetA to TetB.
S_EH[e] = Int eps_abcd e^a ^ e^b ^ R^cd(omega).  Under e -> P e (P = diag(1,-1,-1,-1), det P = -1):
omega -> P omega P, R -> P R P, so eps_abcd picks up det P.  Hence S_EH[Pe] = -S_EH[e]:
TetA and TetB with equal Planck mass enter with opposite signs -> BIMOND's alpha + beta = 0."""
import numpy as np, itertools, sys
eps=np.zeros((4,4,4,4))
for p in itertools.permutations(range(4)): eps[p]=np.linalg.det(np.eye(4)[list(p)])
P=np.diag([1.,-1,-1,-1]); ok=True
epsP=np.einsum('abcd,ai,bj,ck,dl->ijkl',eps,P,P,P,P); ok&=np.allclose(epsP,-eps)
# explicit check: the 4-form eps_abcd e^a e^b R^cd evaluated on random e and antisymmetric R
rng=np.random.default_rng(0); e=rng.normal(size=(4,4)); R=rng.normal(size=(4,4,4,4)); R=R-R.transpose(1,0,2,3); R=R-R.transpose(0,1,3,2)
def form(e,R):   # eps_abcd e^a_m e^b_n R^cd_rs eps^{mnrs}
    return np.einsum('abcd,am,bn,cdrs,mnrs->',eps,e,e,R,eps)
eP=P@e; RP=np.einsum('ca,db,abrs->cdrs',P,P,R)
ok&=np.isclose(form(eP,RP),-form(e,R))
# proper Lorentz transformations (det +1) leave it invariant
th=0.7; L=np.eye(4); L[0,0]=L[1,1]=np.cosh(th); L[0,1]=L[1,0]=np.sinh(th)
RL=np.einsum('ca,db,abrs->cdrs',L,L,R)
ok&=np.isclose(form(L@e,RL),form(e,R))
print(("PASS" if ok else "FAIL"),"- S_EH[Pe] = -S_EH[e]; S_EH[Le] = S_EH[e] for a proper boost L")
print("     => opposite-orientation roots with equal Planck mass: alpha = -beta (BIMOND's special case)")
sys.exit(0 if ok else 1)
