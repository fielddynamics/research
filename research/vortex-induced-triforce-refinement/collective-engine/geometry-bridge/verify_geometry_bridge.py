"""Coordinate-free flywheel-to-Gram bridge, then checks in the tetrad realization.
Requires sympy, numpy, scipy, matplotlib. No new Hamiltonian or fitted constants.
"""
from itertools import combinations, permutations
from pathlib import Path
import sympy as S
import numpy as np
from scipy.linalg import expm
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
root=Path(__file__).resolve().parent
n=0
def ck(label,cond):
 global n
 assert bool(cond),label
 n+=1;print(f'PASS {n:03d} {label}')
I=S.eye(4); J=S.ones(4); P=I-J/4; G=4*I-J
pairs=[(i,j) for i in range(4) for j in range(4) if i!=j]; edges=list(combinations(range(4),2))
R=S.zeros(4,12);Q=S.zeros(4,12)
for k,(i,j) in enumerate(pairs):R[i,k]=1;Q[j,k]=1
Pr=S.eye(12)-R.T*R/3; C=Q*Pr; K=C*C.T
ck('row closed orthogonal projection rank eight',Pr*Pr==Pr and Pr.rank()==8)
ck('column read Gram 2I minus off diagonal 2/3',K==S.Rational(2,3)*G)
F=S.sqrt(S.Rational(3,2))*C.T
ck('normalized physical read covectors reproduce tetrad Gram',F.T*F==G)
ck('four read directions sum zero',F*S.ones(4,1)==S.zeros(12,1))
ck('three-dimensional canonical column-active space',F.rank()==3 and (F*F.T/4)**2==F*F.T/4)
ck('five row-closed directions invisible to column read',Pr.rank()-F.rank()==5)
# Independent construction: no coordinates in the graph boundary operators.
B=S.zeros(4,6); D=S.zeros(6,4)
for h,(i,j) in enumerate(edges):B[i,h]=-1;B[j,h]=1
for i in range(4):
 tri=[j for j in range(4) if j!=i]
 for a,b in [(tri[0],tri[1]),(tri[1],tri[2]),(tri[2],tri[0])]:
  D[edges.index(tuple(sorted((a,b)))),i]=(-1)**i*(1 if a<b else -1)
ck('boundary of boundary zero',B*D==S.zeros(4,4))
ck('four oriented triangular cycles reproduce tetrad Gram exactly',D.T*D==G)
ck('cycle space is exactly three dimensional',D.rank()==3 and B.rank()==3)
ck('cycle projector is exact',D*D.T/4==S.eye(6)-B.T*B/4)
ck('canonical map from read frame to cycles is partial isometry', (D*F.T/4).T*(D*F.T/4)==F*F.T/4 and (D*F.T/4)*(D*F.T/4).T==D*D.T/4)
ck('maps four read vectors to four oriented cycles',D*F.T*F/4==D)
# Actual tetrahedral coordinates enter only here for comparison.
A=S.Matrix([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]])
ck('standard tetrad factorization',A*A.T==G and A.T*A==4*S.eye(3))
U=F*A/4;V=D*A/4
ck('read isometry from intrinsic spatial triplet',U.T*U==S.eye(3) and U*A.T==F)
ck('cycle isometry from intrinsic spatial triplet',V.T*V==S.eye(3) and V*A.T==D)
# All S4 symmetries, ordinary polar read versus oriented axial cycles.
for p in permutations(range(4)):
 T=S.zeros(4);L=S.zeros(12);E=S.zeros(6)
 for i,j in enumerate(p):T[j,i]=1
 for h,(i,j) in enumerate(pairs):L[pairs.index((p[i],p[j])),h]=1
 for h,(i,j) in enumerate(edges):a,b=p[i],p[j];E[edges.index(tuple(sorted((a,b)))),h]=1 if a<b else -1
 sign=T.det()
 ck('read covariance under '+str(p),L*F==F*T)
 ck('oriented cycle covariance under '+str(p),E*D==sign*D*T)
# Cross products in the actual geometry; D has a single global orientation choice.
X=S.Matrix.vstack(*[A[i,:].T.cross(A[j,:].T).T for i,j in edges])
sign=1 if X==D*A else -1
ck('complementary cycle difference is actual cross product',X==sign*D*A)
# Real skew q products give a cycle. Use exact integer complex q in W.
from random import Random
rng=Random(20261126)
for t in range(24):
 x=S.Matrix([rng.randint(-5,5) for _ in range(4)]);y=S.Matrix([rng.randint(-5,5) for _ in range(4)]);x=P*x;y=P*y
 a=S.Matrix([x[i]*y[j]-y[i]*x[j] for i,j in edges]); j=D.T*a
 ck('phase wedge conserved around four labels '+str(t),B*a==S.zeros(4,1) and D*j==4*a)
 ck('exact phase-wedge norm '+str(t),a.dot(a)==x.dot(x)*y.dot(y)-x.dot(y)**2)
 zre=A.T*x/4;zim=A.T*y/4;chi=2*zre.cross(zim)
 ck('cycle currents equal axial read '+str(t),a==X*chi/2 and j==2*sign*A*chi)
# Geometry of actual intrinsic frame +/- and core vertices.
verts=[tuple(A[i,:]) for i in range(4)]; opp=[tuple(-A[i,:]) for i in range(4)]
mid=[tuple((A[i,:]+A[j,:])/2) for i,j in edges];basis=[tuple(1 if i==j else 0 for i in range(3)) for j in range(3)];
ck('eight inversion-related read vertices equal cube corners',len(set(verts+opp))==8 and all(abs(x)==1 for v in verts+opp for x in v))
ck('six sums are octahedron vertices',set(mid)==set(basis+[tuple(-x for x in v) for v in basis]))
for a in verts+opp:
 vs=[S.Matrix([a[i] if i==j else 0 for i in range(3)]) for j in range(3)]
 apex=S.Matrix(a); det=S.Matrix.hstack(*[v-apex for v in vs]).det()
 ck('one nondegenerate stellation per direction '+str(a),abs(det)==2)
# Counterexample: distort the physical embedding without changing any graph relation.
L=S.diag(2,1,1);A_bad=A*L
ck('same four independent phase records allow nonisometric coordinate chart',A_bad.rank()==3 and A_bad.T*S.ones(4,1)==S.zeros(3,1) and A_bad*A_bad.T!=G)
# Fixed Stage VII couplings, abstract 33 sites using only leg indices.
outer=[(sg,i,j) for sg in (1,-1) for i,j in pairs]; central=[(sg,i) for sg in (1,-1) for i in range(4)]; labels=['O']+outer+central;H=S.zeros(33)
def bond(a,b,v):i,j=labels.index(a),labels.index(b);assert H[i,j]==0;H[i,j]=H[j,i]=v
for sg in (1,-1):
 for i in range(4):
  for j,l in combinations([j for j in range(4) if j!=i],2):bond((sg,i,j),(sg,i,l),-1)
for sg,i,j in outer:
 if sg==1:bond((sg,i,j),(-sg,j,i),-S.Rational(1,2))
 bond((sg,i,j),(sg,i),-2);bond((sg,i,j),(-sg,j),-1)
for i,j in pairs:bond((1,i),(-1,j),-1)
for sg,i in central:bond('O',(sg,i),-1);H[labels.index((sg,i)),labels.index((sg,i))]=-S.Rational(99,10)
ck('all original 104 bonds from labels alone',sum(H[i,j]!=0 for i,j in combinations(range(33),2))==104)
# Use an orthonormal coordinate chart in W; exact intertwiner on W, no A required.
E=S.zeros(33,12)
for sg,i,j in outer:
 h=labels.index((sg,i,j));E[h,:4]=P[i,:];E[h,4:8]=P[j,:]
for sg,i in central:E[labels.index((sg,i)),8:12]=P[i,:]
M=S.Matrix([[-2,S.Rational(1,2),-2],[-S.Rational(1,2),1,-1],[-5,-1,-S.Rational(89,10)]])
ck('published collective reduction follows from label graph before embedding',H*E==E*S.kronecker_product(M,I))
ck('intrinsic collective sector has nine dimensions',E.rank()==9)
ck('intrinsic norm factors into multiplicity metric times W',E.T*E==2*S.kronecker_product(S.Matrix([[3,-1,0],[-1,3,0],[0,0,1]]),P))
# Read the actual bond currents from full Hamiltonian evolution with no coordinate geometry.
Hn=np.array(H,float);En=np.array(E,float);Dn=np.array(D,float);Xn=np.array(X,float);An=np.array(A,float)
z=np.array([1,1j,0])/np.sqrt(2); q=An@z;rho=np.sqrt(3)/8
init=rho*En@np.kron([1/3,1,0],q)
for t in [0,.01,.1,.5,1,2,4,8]:
 uvw=expm(-1j*np.array(M,float)*t)@np.array([1/3,1,0]);psi=expm(-1j*Hn*t)@init
 ck('abstract full graph equals reduced evolution t='+str(t),np.allclose(psi,rho*En@np.kron(uvw,q)))
 curr=2*np.imag(psi[:,None]*Hn.T*psi.conj()[None,:]); jj=[];ii=[]
 for i in range(4):
  tr=[j for j in range(4) if j!=i]
  if i%2:tr[1],tr[2]=tr[2],tr[1]
  ids=[labels.index((1,i,j)) for j in tr];jj.append(sum(curr[a,b] for a,b in zip(ids,ids[1:]+ids[:1]))/3)
 for i,j in edges:ii.append(curr[labels.index((1,i)),labels.index((-1,j))])
 av=abs(uvw[1])**2;aw=abs(uvw[2])**2
 ck('actual ring-edge current telescoping t='+str(t),np.allclose(av*np.array(ii),3*aw/4*Dn@jj))
# Diagrams: actual geometry and exact Gram, and cycles of the four-leg graph.
fig=plt.figure(figsize=(11,4.8),layout='constrained');ax=fig.add_subplot(121,projection='3d');ax.set_box_aspect([1,1,1]);ax.view_init(20,30)
for apex in np.vstack([An,-An]):
 v=np.diag(apex);col='#2864b4' if np.prod(apex)>0 else '#c66a18';faces=[[apex,v[i],v[j]] for i,j in combinations(range(3),2)]
 ax.add_collection3d(Poly3DCollection(faces,facecolors=col,edgecolors=col,alpha=.13,linewidths=1));ax.scatter(*apex,color=col,s=24)
 ax.add_collection3d(Poly3DCollection([v],facecolors='#148779',edgecolors='#148779',alpha=.32))
ax.set(xlim=(-1.1,1.1),ylim=(-1.1,1.1),zlim=(-1.1,1.1),title='Eight intrinsic directions and the octahedral core');ax.set_axis_off()
a=fig.add_subplot(122);a.imshow(np.array(G,float),cmap='RdBu',vmin=-3,vmax=3);a.set_xticks(range(4),range(1,5));a.set_yticks(range(4),range(1,5));a.set_title('One Gram matrix from two constructions')
for i in range(4):
 for j in range(4):a.text(j,i,str(G[i,j]),ha='center',va='center',fontsize=16,color='white' if i==j else 'black')
a.set_xlabel('Leg / oriented face cycle');a.set_ylabel('Leg / oriented face cycle')
for ext in ['png','svg']:fig.savefig(root/f'geometry_gram.{ext}',dpi=170)
plt.close(fig)
fig,axs=plt.subplots(1,4,figsize=(11,3),layout='constrained');p=np.array([[0,1],[-.86,-.5],[.86,-.5],[0,0]])
for i,a in enumerate(axs):
 for h,(j,k) in enumerate(edges):
  a.plot(*p[[j,k]].T,color='#cbd5e1',lw=1.2)
  if D[h,i]:
   x,y=p[j],p[k];x,y=(x,y) if D[h,i]==1 else (y,x);a.annotate('',xy=.12*x+.88*y,xytext=.88*x+.12*y,arrowprops=dict(arrowstyle='->',color='#148779',lw=2.1))
 a.scatter(*p.T,s=270,color='#eff6ff',edgecolor='#2864b4',zorder=4)
 for j,(x,y) in enumerate(p):a.text(x,y,str(j+1),ha='center',va='center',zorder=5)
 a.set_title(f'Oriented cycle {i+1}');a.set_aspect('equal');a.set_xlim(-1.1,1.1);a.set_ylim(-.75,1.2);a.axis('off')
fig.suptitle('Four oriented cycles; each has norm² 3, each pair shares one edge with opposite sign')
for ext in ['png','svg']:fig.savefig(root/f'four_cycles.{ext}',dpi=170)
plt.close(fig)
print(f'{n}/{n} checks passed')
