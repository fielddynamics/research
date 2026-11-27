from itertools import permutations
from pathlib import Path
import sympy as s
import mpmath as mp
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
root=Path(__file__).parent
checks=[]
def ck(label,condition):
    assert condition,label
    checks.append(label);print(f'PASS {len(checks):02d} {label}')
t,k=s.symbols('t k',positive=True)
C=s.Matrix([[-t,1,0,0],[0,-t**4,1,0],[0,0,-t**16,1]])
v=s.Matrix([1,t,t**5,t**21]);e=s.eye(4)[:,3]
ck('constraint rank three',C.rank()==3)
ck('one exact null direction',C*v==s.zeros(3,1))
Z=(v.T*v)[0];P=v*v.T/Z
ck('massless projector',s.simplify(P*P-P)==s.zeros(4))
w=s.factor((e.T*P*e)[0]);ck('massless residue',w==t**42/(1+t**2+t**10+t**42))
ck('sum massive residues is one minus massless',s.simplify((e.T*(s.eye(4)-P)*e)[0]-(1-w))==0)
# One gradient per coordinate, equal stiffness and penalties; no fit.
M=C*C.T
ck('massive eigenvalues equal those of CC^T',s.expand((C.T*C).charpoly().as_expr()-s.Symbol('lambda')*M.charpoly().as_expr())==0)
# Symmetry-constrained capacity: actual invariant field vectors vs isotropic ensemble.
I=s.eye(16);swap=s.zeros(16)
for i in range(4):
 for j in range(4):swap[4*j+i,4*i+j]=1
B=s.eye(1).row_join(s.zeros(1,16)).col_join(s.zeros(16,1).row_join(I-swap))
ck('unrestricted signed capacity 13',s.trace(B)==13)
ck('unrestricted neutral capacity 17',B.rows==17)
def rep(p):
 U=s.zeros(4)
 for i,j in enumerate(p):U[j,i]=1
 return s.diag(s.eye(1),s.kronecker_product(U,U))
for name,grp,d,cap in [('C3',[(0,1,2,3),(0,2,3,1),(0,3,1,2)],7,5),('S3',[ (0,)+p for p in permutations([1,2,3])],6,3),('S4',list(permutations(range(4))),3,1)]:
 Q=sum(map(rep,grp),s.zeros(17))/len(grp)
 ck(name+' invariant projector',Q*Q==Q and Q*B==B*Q)
 ck(name+' invariant neutral dimension',s.trace(Q)==d)
 ck(name+' invariant signed capacity',s.trace(Q*B)==cap)
# ADM lapse Schur determinant with general numerical rational shift and spatial metric
h=s.Matrix([[3,1,0],[1,4,1],[0,1,2]]);beta=s.Matrix([1,2,-1]);N=s.symbols('N',positive=True);G=s.BlockMatrix([[s.Matrix([[-N**2+(beta.T*h*beta)[0]]]),beta.T*h],[h*beta,h]]).as_explicit()
ck('ADM determinant lapse ratio exact',s.factor(G.det())==-N**2*h.det())
ck('ADM inverse time component',s.simplify(G.inv()[0,0]+1/N**2)==0)
# 21-dimensional determinant normalized derivative independent of common attenuation
z=s.symbols('z',positive=True);D=s.diag(*([t*(1+z)]+[t]*20));D0=t*s.eye(21)
ck('constant determinant attenuation cancels',s.simplify(D.det()/D0.det())==1+z)
# Weak isotropic tetrad: determinant and optical geometry.
u,vv,gamma=s.symbols('u v gamma',real=True)
e4=s.diag(s.exp(u),s.exp(-vv),s.exp(-vv),s.exp(-vv))
ck('tetrad volume is exp(u-3v)',s.simplify(e4.det()-s.exp(u-3*vv))==0)
ck('fixed volume imposes v=u/3',s.solve(u-3*vv,vv)==[u/3])
ck('GR weak spatial lock is not fixed volume',s.simplify(e4.det().subs(vv,u))==s.exp(-2*u))
nopt=s.exp(-u-vv)
ck('pure conformal scaling leaves optical index one',nopt.subs(vv,-u)==1)
ck('lapse-only optical index first-order coefficient',s.diff(nopt.subs(vv,0),u).subs(u,0)==-1)
ck('GR weak optical index first-order coefficient',s.diff(nopt.subs(vv,u),u).subs(u,0)==-2)
# Under a linear coordinate change the scalar susceptibility is invariant.
A=s.Matrix([[5,1],[1,3]]);a=s.Matrix([2,1]);F=s.Matrix([[2,1],[1,1]])
ck('clock susceptibility coordinate invariant',(a.T*A.inv()*a)[0]==((F.T*a).T*(F.T*A*F).inv()*(F.T*a))[0])
# Spectral decomposition at actual alpha (reference illustrative value).
mp.mp.dps=100; alpha=1/mp.mpf('137.035999177');T=mp.sqrt(alpha)
Cm=mp.matrix([[-T,1,0,0],[0,-T**4,1,0],[0,0,-T**16,1]])
vals,U=mp.eigsy(Cm.T*Cm);weights=[U[3,j]**2 for j in range(4)];w0=weights[0]
ck('high precision gapless eigenvalue',abs(vals[0])<mp.mpf('1e-90'))
ck('high precision residue formula',abs(w0/(T**42/(1+T**2+T**10+T**42))-1)<mp.mpf('1e-60'))
ck('spectral weights sum to one',abs(sum(weights)-1)<mp.mpf('1e-90'))
ck('massive branches positive',all(vals[j]>0 for j in range(1,4)))
# relative correction to potential and force for point sources; r measured in sqrt(kappa/L)
def rel(x,force=False):
 return sum(weights[j]/w0*mp.exp(-mp.sqrt(vals[j])*x)*(1+mp.sqrt(vals[j])*x if force else 1) for j in range(1,4))
lo,hi=mp.mpf(0),mp.mpf(200)
for _ in range(400):
 m=(lo+hi)/2
 if rel(m,True)>mp.mpf('.01'):lo=m
 else:hi=m
x=(lo+hi)/2
ck('force crossover verified',abs(rel(x,True)-mp.mpf('.01'))<mp.mpf('1e-85'))
print('alpha^21',mp.nstr(alpha**21,15));print('w0',mp.nstr(w0,15));print('eigenvalues',*[mp.nstr(vals[j],20) for j in range(1,4)]);print('weights',*[mp.nstr(a,15) for a in weights]);print('1 percent force crossover r/ell',mp.nstr(x,15));print('equality force at r/ell=100',mp.nstr(rel(100,True),15))
xs=np.linspace(0,140,281);ys=[float(mp.log10(rel(float(a),True))) for a in xs]
fig,ax=plt.subplots(figsize=(8,4.5),layout='constrained');ax.plot(xs,ys,label='massive / massless force');ax.axhline(-2,ls='--',color='gray',label='1% correction');ax.axvline(float(x),ls=':',color='gray');ax.set(xlabel=r'Distance $r/\ell$, $\ell=\sqrt{\kappa/L}$',ylabel='log10 relative force',title='Clock constraint: finite-range modes cannot be ignored');ax.legend();ax.grid(alpha=.2);fig.savefig(root/'clock_force_crossover.svg');plt.close(fig)
print(f'{len(checks)} checks passed')
