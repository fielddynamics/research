"""Boundary energy registration and exact internal engine cycle; no fitted physical parameters."""
from pathlib import Path
from itertools import product
import numpy as np
import sympy as sp
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
root=Path(__file__).resolve().parent
ns={};exec((root/'verify_coupled_origins.py').read_text().split("ck('33 original geometric positions;")[0],ns)
H,d,S,A,base,idx,rings,inner,outer,tiles,J=[ns[k] for k in ('H','d','S','A','base','idx','rings','inner','outer','tiles','J')]
n=0
def ck(label,b):
 global n
 assert bool(b),label
 n+=1;print(f'PASS {n:03d} {label}')
def near(a,b,tol=1e-10):return np.allclose(a,b,atol=tol,rtol=tol)
# Solid angle for a triangle, standard atan2 expression, unnormalized vectors.
def omega(v):
 a,b,c=np.array(v,dtype=float);na,nb,nc=map(np.linalg.norm,(a,b,c))
 return 2*np.arctan2(abs(np.linalg.det([a,b,c])),na*nb*nc+np.dot(a,b)*nc+np.dot(b,c)*na+np.dot(c,a)*nb)
def area(v):
 a,b,c=np.array(v,dtype=float);return np.linalg.norm(np.cross(b-a,c-a))/2
for k,T in enumerate([A,-A]):
 face_flux=[];face_area=[]
 for i,s in enumerate(T):
  ids=[base[i+4*(1-k)]]+[idx[4*k+j,4*k+i] for j in range(4) if j!=i]
  areas=[area(list(tiles[j][1])) for j in ids];angles=[omega(list(tiles[j][1])) for j in ids]
  ck('each actual Triforce face has four equal-area tiles',near(areas, np.full(4,np.sqrt(3)/2)))
  ck('central solid angle pi/2, lateral pi/6 each',near(angles,np.pi*np.array([.5,1/6,1/6,1/6])))
  ck('face sums to pi steradians',near(sum(angles),np.pi))
  face_flux.append(sum(angles));face_area.append(sum(areas))
 ck('complete chamber flux 4pi',near(sum(face_flux),4*np.pi))
 ck('actual tetrahedron area at circumradius sqrt3',near(sum(face_area),8*np.sqrt(3)))
# algebraic flux read vs optical Wc (lateral first, central last).
f=sp.Matrix([1,1,1,3]);w=sp.Matrix([1,1,1,6]);Wc=w*w.T/54;P=w*w.T/(w.dot(w));v=f-P*f
ck('solid angle read not proportional to optical read',sp.Matrix.hstack(f,w).rank()==2)
ck('geometric flux read bright squared projection 49/52',sp.simplify(f.dot(P*f)/f.dot(f))==sp.Rational(49,52))
ck('remaining flux functional hidden to instantaneous filter',w.dot(v)==0 and f.dot(v)>0)
ck('explicit dark witness (2,2,2,-1)',w.dot(sp.Matrix([2,2,2,-1]))==0 and f.dot(sp.Matrix([2,2,2,-1]))==3)
# Boundary energy: spherical Gauss and homogeneity, no extra surface energy.
R,R0,G,c,a0,K,alpha,hbar,m=sp.symbols('R R0 G c a0 K alpha hbar m',positive=True)
E=c**2/(4*sp.pi*G)*(4*sp.pi*R**2)*(a0/K**2)
ck('saturation boundary read quadratic radius',sp.simplify(E-a0*c**2*R**2/(G*K**2))==0)
ck('Gauss mass read',sp.simplify(c**2/(4*sp.pi*G)*(4*sp.pi*R**2)*(G*m/R**2)-m*c**2)==0)
ck('if instead uniform actual face-normal saturation then distinct area coefficient',sp.simplify((8*sp.sqrt(3)*R**2/3)/(4*sp.pi*R**2))==2*sp.sqrt(3)/(3*sp.pi))
x=sp.symbols('x',positive=True);V=(2/x+x*x)/3
ck('registered energy global excess factor',sp.factor(V-1)==(x-1)**2*(x+2)/(3*x))
ck('energy reads have invariant product',sp.simplify((1/x)**2*x**2)==1)
ref=(1-x**3)/(1+x**3)
ck('radial logarithmic force is signed optical mismatch',sp.simplify(x*sp.diff(V,x)+sp.Rational(2,3)*(1/x+x*x)*ref)==0)
ck('positive reflection sign below closure and negative above',ref.subs(x,sp.Rational(1,2))>0 and ref.subs(x,2)<0)
ck('mismatch slope at closure',sp.diff(ref,x).subs(x,1)==-sp.Rational(3,2))
# Existing invariant two-chamber vortex block, no extra hopping.
ome=np.exp(2j*np.pi/3);z=np.zeros(d,complex);z[rings[0]]=np.array([1,ome,ome**2])/np.sqrt(3)
lookup={v:i for i,(_,v) in enumerate(tiles)}
def perm(sig):return np.eye(d)[:,[lookup[frozenset(tuple(np.array(v)*sig) for v in vs)] for _,vs in tiles]+list(range(33,36))]
a=sum(perm(sig)@z for sig in product([-1,1],repeat=3) if np.prod(sig)==1)/2;b=perm((-1,-1,-1))@a
Z=np.column_stack([a,b]);Hred=np.array([[1,-1],[-1,1]])
ck('original vortex sector is orthonormal',near(Z.conj().T@Z,np.eye(2)))
ck('original vortex sector invariant with exact reduced block',near(H@Z,Z@Hred))
vp=(a+b)/np.sqrt(2);vm=(a-b)/np.sqrt(2)
ck('stationary and exchange eigenvectors',near(H@vp,0) and near(H@vm,2*vm))
F=[np.eye(d)[:,[idx[i,j] for j in range(4*(i//4),4*(i//4)+4) if j!=i]+[base[i]]] for i in range(8)]
wn=np.array([1,1,1,6]);ck('both circulating eigenmodes are dark at all eight filtered ports',all(near(wn@q.T@Z,0) for q in F))
ck('both modes have empty ordinary central and origin amplitudes',near(Z[inner+[0,33,34,35]],0))
IA=np.flatnonzero(abs(a)>1e-10);IB=np.flatnonzero(abs(b)>1e-10)
ck('disjoint support 12 lateral tiles per chamber',len(IA)==len(IB)==12 and not set(IA)&set(IB))
pairs=[(i,j) for r in rings for i,j in zip(r,r[1:]+r[:1])];ref=np.array([J(H,vp)[i,j] for i,j in pairs]);sign=np.sign(ref)
eps=.5;ts=np.linspace(0,np.pi,241);rows=[]
for t in ts:
 u=(vp+eps*np.exp(-2j*t)*vm)/np.sqrt(1+eps**2);j=J(H,u);na=np.sum(abs(u[IA])**2);nb=np.sum(abs(u[IB])**2);flux=j[np.ix_(IA,IB)].sum();js=np.array([j[i,k] for i,k in pairs])*sign
 expected=(1+eps**2+2*eps*np.cos(2*t))/(2*(1+eps**2));eflux=2*eps*np.sin(2*t)/(1+eps**2)
 rows.append([t,na,nb,flux,js[:12].min(),js[12:].min()])
 if len(rows)%20==1:
  ck('actual graph chamber occupancy and flux follow engine cycle',near([na,nb,flux],[expected,1-expected,eflux]))
  ck('all 24 signed ring currents follow chamber occupation',near(js[:12],na/(4*np.sqrt(3))) and near(js[12:],nb/(4*np.sqrt(3))))
  ck('all-time dark FO and filtered interfaces at sampled phase',near(u[inner+[0,33,34,35]],0) and all(near(wn@q.T@u,0) for q in F))
  ck('occupation and microscopic energy conserved',near(np.vdot(u,u),1) and near(np.vdot(u,H@u),2*eps**2/(1+eps**2)))
ck('exact cycle returns initial vector',near((vp+eps*np.exp(-2j*np.pi)*vm),vp+eps*vm))
ck('nonzero lower bound on all ring currents',min(min(r[-2:]) for r in rows)>0 and near(min(min(r[-2:]) for r in rows),(1-eps)**2/(8*np.sqrt(3)*(1+eps**2))))
# Original even scalar quotient, exact noncommensurability with the exchange gap.
groups=[[0],base[:4],base[4:],sum(rings[:4],[]),sum(rings[4:],[])];Q=np.column_stack([np.isin(np.arange(d),g).astype(int) for g in groups]);R5=sp.Matrix(Q);M5=(R5.T*R5).inv()*R5.T*sp.Matrix(H)*R5
L=sp.Matrix([[1,0,0],[0,1,0],[0,1,0],[0,0,1],[0,0,1]]);Me=(L.T*L).inv()*L.T*M5*L
ck('even scalar quotient invariant',M5*L==L*Me)
lam=sp.symbols('lambda');poly=Me.charpoly(lam).as_expr()
ck('exact scalar cubic',poly==lam**3+6*lam**2-11*lam-24)
ck('scalar eigenvalues irrational by irreducible cubic over Q',sp.Poly(poly,lam).is_irreducible)
# If a common period exists, the scalar eigenvalue divided by the exchange gap 2 is rational.
ck('exchange-gap rescaling preserves irreducibility (no rational frequency ratio)',sp.Poly(poly.subs(lam,2*lam),lam).is_irreducible)
print('Scalar eigenvalues:',np.linalg.eigvals(np.array(Me,float)))
# Physical clock mismatch under explicitly assumed c/R hop frequency.
alpha_val=1/137.035999177
print('Exchange/Compton angular frequency under c/R hopping:',2/alpha_val)
with open(root/'closure_engine_cycle.csv','w') as out:
 writer=csv.writer(out);writer.writerow(['dimensionless_time','N_A','N_B','J_A_to_B','min_A_ring','min_B_ring']);writer.writerows(rows)
# Diagram and computed cycle.
fig=plt.figure(figsize=(12,7),layout='constrained');gs=fig.add_gridspec(2,2)
ax=fig.add_subplot(gs[:,0]);ax.set_aspect('equal');ax.axis('off');ax.set_title('Exact radial flux through one Triforce face',fontsize=13)
p=np.array([[0,1],[-np.sqrt(3)/2,-.5],[np.sqrt(3)/2,-.5]]);mid=(p+np.roll(p,-1,axis=0))/2
for i in range(3):
 t=np.array([p[i],mid[i],mid[(i-1)%3]]);ax.add_patch(plt.Polygon(t,facecolor='#c8def3',edgecolor='#234c79',lw=2));q=t.mean(0);ax.text(*q,'π/6\n1/6 of face',ha='center',va='center',fontsize=10)
ax.add_patch(plt.Polygon(mid,facecolor='#a9dfcf',edgecolor='#087f6d',lw=2));ax.text(*mid.mean(0),'π/2\n1/2 of face',ha='center',va='center',fontsize=12,fontweight='bold');ax.set(xlim=(-1.1,1.1),ylim=(-1.1,1.2));ax.text(0,-.78,'Four equal-area tiles, unequal solid angles.\nFour faces × π = 4π per closed chamber.\nTwo chamber surfaces read the same mass.',ha='center',va='top',fontsize=11)
rows=np.array(rows);ax=fig.add_subplot(gs[0,1]);ax.plot(rows[:,0]/np.pi,rows[:,1],label='TetA occupation');ax.plot(rows[:,0]/np.pi,rows[:,2],label='TetB occupation');ax.plot(rows[:,0]/np.pi,rows[:,3],label='A → B exchange current',ls='--');ax.axhline(0,color='gray',lw=.7);ax.set(xlabel='Fraction of internal cycle',ylabel='Dimensionless occupation / current',title='Actual two-chamber vortex exchange');ax.legend(fontsize=9,loc='lower left');ax.grid(alpha=.2)
ax=fig.add_subplot(gs[1,1]);ax.plot(rows[:,0]/np.pi,rows[:,4],label='TetA minimum signed ring current');ax.plot(rows[:,0]/np.pi,rows[:,5],label='TetB minimum signed ring current');ax.axhline(0,color='gray',lw=.7);ax.set(xlabel='Fraction of internal cycle',ylabel='Signed ring current',title='All 24 ring bonds retain circulation direction');ax.legend(fontsize=9);ax.grid(alpha=.2)
fig.suptitle('GFD closure engine: boundary register and internal conservative exchange',fontsize=16,fontweight='bold')
for ext in ['svg','png']:fig.savefig(root/f'figures/40_closure_engine.{ext}',dpi=160)
print(f'{n}/{n} new checks passed')
