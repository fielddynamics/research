from native_geometry import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.linalg import eigh
from pathlib import Path
out=Path(__file__).parent
checks=0
def ck(label,test):
 global checks
 assert bool(test),label
 checks+=1;print(f'PASS {checks:02d} {label}')
M=sp.Matrix(H); I=sp.eye(36); x=sp.symbols('x');
B=sp.diag(*([int(tag.endswith('B')) for tag,_ in tiles]+[0]*3)); P=sp.diag(*[int(i in O) for i in range(36)]); V=P*M+M*P
ck('native geometry 33 positions and 104 original bonds',len(tiles)==33 and len(edges)==104)
ck('H36 real symmetric and zero diagonal',M==M.T and all(M[i,i]==0 for i in range(36)))
cp=x**5*(x-3)*(x-2)**5*(x+1)*(x**3-7*x+2)**3*(x**3+6*x**2-11*x-24)*(x**4+2*x**3-19*x**2-4*x+32)**3
ck('exact native characteristic polynomial',sp.expand(M.charpoly(x).as_expr()-cp)==0)
tr=[sp.trace(M**k) for k in range(4)]
ck('exact spectral moments',tr==[36,0,256,-624])
ck('16 TetB tiles and no additional origin coordinate',sp.trace(B)==16 and B**2==B and B*P==sp.zeros(36))
ck('throat perturbation contains only existing centre bonds',P*M*P==sp.zeros(36) and V==P*M*(I-P)+(I-P)*M*P)
for name,Z,target in [('TetB onsite',B,[16,0,112]),('throat coupling',V,[0,64,-96]),('uniform clock',M,[0,256,-624])]:
 moments=[sp.trace(M**k*Z) for k in range(3)]
 ck(name+' exact moments',moments==target)
 a=moments[0]/36; b=moments[1]/256; residual=sp.simplify(moments[2]-a*256+b*624)
 print(name, 'offset',a,'scale',b,'moment residual',residual)
 ck(name+' universal clock moment test',residual=={'TetB onsite':-sp.Rational(16,9),'throat coupling':60,'uniform clock':0}[name])
# exact parity core mode, no throat participation
p=sp.zeros(36,1)
for i,s in enumerate(S):p[base[i]]=int(np.prod(s))
ck('core parity clock has exact eigenvalue 3',M*p==3*p)
ck('parity clock has half its occupation in TetB',(p.T*B*p)[0]/(p.T*p)[0]==sp.Rational(1,2))
ck('parity clock is throat dark',V*p==sp.zeros(36,1))
# Numerical degenerate perturbation theory; no finite differencing used.
e,U=eigh(H); groups=[]
for i,ei in enumerate(e):
 if not groups or abs(ei-e[groups[-1][0]])>1e-7:groups.append([])
 groups[-1].append(i)
ck('14 distinct eigenvalues',len(groups)==14)
rows=[]
for g in groups:
 u=U[:,g]; slopes=[]
 for Z in [B,V,M]:
  z=eigh(u.T@np.array(Z,float)@u,eigvals_only=True);slopes.append(z)
 ck('degenerate group uniform scaling '+str(round(e[g[0]],5)),np.max(abs(slopes[2]-e[g[0]]))<1e-9)
 rows.append([e[g[0]],len(g),*[(v.min()+v.max())/2 for v in slopes],*[v.max()-v.min() for v in slopes]])
r=np.array(rows);np.savetxt(out/'clock_spectral_slopes.csv',r,delimiter=',',header='E,multiplicity,TetB_slope,throat_slope,uniform_slope,TetB_spread,throat_spread,uniform_spread',comments='')
ck('both local loads fail affine spectral scaling',all(np.linalg.norm(r[:,j]-(np.polyval(np.polyfit(r[:,0],r[:,j],1),r[:,0])))>0.1 for j in [2,3]))
gap=r[1:,0]-r[0,0]; b1=(r[1:,2]-r[0,2])/gap; b2=(r[1:,3]-r[0,3])/gap
print('ground referenced fractional slopes TetB range',b1.min(),b1.max(),'throat range',b2.min(),b2.max())
# Phase-only clock obstruction: static density times time derivative is a boundary term.
t=sp.symbols('t'); th=sp.Function('theta')(t); rho,b=sp.symbols('rho b', real=True)
L=-rho*b*sp.diff(th,t); ck('static matter phase coupling has identically zero bulk Euler-Lagrange source',sp.diff(L,th)-sp.diff(sp.diff(L,sp.diff(th,t)),t)==0)
q,k,c,m=sp.symbols('q k c m',real=True); f=k*q*q/2+m*c*c*b*q
ck('static coordinate coupling supplies nonzero linear source',sp.diff(f,q)==k*q+m*c*c*b)
fig,axs=plt.subplots(1,2,figsize=(10,4.4),layout='constrained')
for ax,col,label in [(axs[0],2,'TetB onsite load'),(axs[1],3,'Field Origin bond load')]:
 ax.scatter(r[:,0],r[:,col],s=15+12*r[:,1],label='Native spectral derivatives'); a=0 if col==3 else 4/9; bb=1/4 if col==3 else 0
 xx=np.linspace(r[:,0].min(),r[:,0].max(),100);ax.plot(xx,a+bb*xx,'--',label='Required affine slope from trace moments');ax.set(xlabel='Native energy (dimensionless)',ylabel='First-order energy derivative',title=label);ax.grid(alpha=.2);ax.legend(fontsize=8)
fig.savefig(out/'native_clock_spectrum.svg');plt.close(fig)
print(f'{checks} checks passed')
