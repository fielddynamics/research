"""Where in the 24 + 16 + 24 connection grid does a slow particle get pushed?
Christoffel (Newton): Gamma^i_00 -> slice i, lower pair (0,0): a diagonal (shared, root-blind) slot of the 16.
Torsion: find every T^l_[mn] whose contorsion gives K^i_(00) != 0."""
import numpy as np
eta=np.diag([-1.,1,1,1])
def contorsion(T):
    Tl=np.einsum('al,lmn->amn',eta,T)
    return 0.5*(T+np.einsum('la,man->lmn',eta,Tl)+np.einsum('la,nam->lmn',eta,Tl))
hits=[]
for l in range(4):
    for m in range(4):
        for n in range(m+1,4):
            T=np.zeros((4,4,4)); T[l,m,n]=1; T[l,n,m]=-1
            if any(abs(contorsion(T)[i,0,0])>1e-12 for i in (1,2,3)): hits.append((l,m,n))
print("torsion components that push a slow particle:",hits)
ok=hits==[(0,0,1),(0,0,2),(0,0,3)]
print(("PASS " if ok else "FAIL ")+"only the three time-slice, time-space components T^0_[0i] (3 of the 24) carry a TetB force;")
print("     Newton's static pull Gamma^i_00 sits in the shared diagonal 16, identical for TetA and TetB (why GR works locally).")
