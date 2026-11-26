"""Checks of the octal walk, BBP clock and rotational averaging. Not physical validation."""
import mpmath as mp
import numpy as np
from scipy.special import eval_legendre
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
root=Path(__file__).resolve().parent
mp.mp.dps=400
checks=[]
def ck(name,test):
    assert bool(test),name
    checks.append(name);print('PASS',name)
C=np.roll(np.eye(8),1,axis=0)
ck('clock order eight',np.array_equal(np.linalg.matrix_power(C,8),np.eye(8)))
q=1/np.sqrt(2)
ck('eight equal amplitude steps give 1/16',np.isclose(q**8,1/16))
# Slots j=1,...,8 are represented by basis indices j-1. Read compensation is essential.
w=np.array([4,0,0,-2,-1,-1,0,0]);ell=w/q**np.arange(8);e0=np.eye(8)[:,0]
for y in np.linspace(0,1,21):
    R=np.linalg.inv(np.eye(8)-q*y*C)
    ck('BBP clock read at y='+str(round(y,2)),np.isclose(ell@R@e0,(4-2*y**3-y**4-y**5)/(1-y**8/16)))
ck('BBP integral equals pi',abs(mp.quad(lambda y:(4-2*y**3-y**4-y**5)/(1-y**8/16),[0,1])-mp.pi)<mp.mpf('1e-390'))
H=np.array([[(-1)**((a&b).bit_count()) for b in range(8)] for a in range(8)])/np.sqrt(8)
CW=H@C@H.T
ck('clock is not Walsh diagonal',np.isclose(np.linalg.norm(CW-np.diag(np.diag(CW))),np.sqrt(5)))
for i in range(8):
    b0,b1,b2=(i>>0)&1,(i>>1)&1,(i>>2)&1
    u=(b0^1)+2*(b1^b0)+4*(b2^(b1&b0))
    ck('three-bit carry at '+str(i),u==(i+1)%8)
N=np.zeros((8,8),int);v=3;f=mp.pi-3
for k in range(1,500):
    f*=8;d=int(f);f-=d;u=(v+d)%8;N[v,u]+=1;v=u
    if N.min():break
ck('first complete coverage at transition 332',k==332 and N.min()==1 and N.max()==10)
ck('balanced pair registration',np.allclose(N/(64*N),np.ones((8,8))/64))
F=np.zeros((4,4),int)
for a in range(8):
    for b in range(8):F[min(a,7-a),min(b,7-b)]+=N[a,b]
ck('complement pair diagonal count is 80',F.trace()==80)
raw=1-16*F.trace()/(17*k)
ck('raw face-pair stiffness differs from balanced',not np.isclose(raw,13/17))
S=np.array([[2*((i>>b)&1)-1 for b in (2,1,0)] for i in range(8)])/np.sqrt(3)
ck('uniform cube second moment isotropic',np.allclose(S.T@S/8,np.eye(3)/3))
for vec in [np.array([1,0,0]),np.ones(3)/np.sqrt(3),np.array([1,2,3])/np.sqrt(14)]:
    s4=np.sum(vec**4)
    ck('cube fourth moment formula',np.isclose(np.mean((S@vec)**4),(3-2*s4)/9))
    ck('cube degree-four multipole',np.isclose(np.mean(eval_legendre(4,S@vec)),7*(3-5*s4)/36))
# Axisymmetric harmonic overlap from addition theorem; numerical spherical quadrature.
z,wz=np.polynomial.legendre.leggauss(32);phi=np.arange(128)*2*np.pi/128
X=np.sqrt(1-z[:,None]**2)*np.cos(phi[None,:]);Y=np.sqrt(1-z[:,None]**2)*np.sin(phi[None,:]);Z=np.broadcast_to(z[:,None],X.shape)
for l in range(1,13):
    vals=[np.sqrt(2*l+1)*eval_legendre(l,a) for a in [X,Y,Z]]
    G=np.array([[np.sum(wz[:,None]*a*b)/256 for b in vals] for a in vals]);p=eval_legendre(l,0)
    ck('axis harmonic Gram l='+str(l),np.allclose(G,np.eye(3)+p*(np.ones((3,3))-np.eye(3)),atol=1e-12))
    # Projectors on weighted-sampled functions, using the analytic rank-one product norm and trace.
    A=G[2,1]*G[1,0]
    ck('three-sweep norm and repeated eigenvalue l='+str(l),np.isclose(abs(A),p*p) and np.isclose(A*G[0,2],p**3))
rot=lambda a:((a<<1)&7)|(a>>2)
seen=set();orbits=[]
for a in range(8):
    for b in range(8):
        if (a,b) in seen:continue
        o={(a,b),(rot(a),rot(b)),(rot(rot(a)),rot(rot(b)))};seen|=o;orbits.append(o)
ck('literal spatial rotation has 24 orbit records',len(orbits)==24 and sum(len(o)==1 for o in orbits)==4)
ck('axial-only complement identification yields 22 records',len(orbits)-2==22)
print('Transition matrix\n',N,'\nFace pair matrix\n',F,'\nRaw stiffness',raw,'\nChecks passed:',len(checks))
# Vector and raster figures.
fig,ax=plt.subplots(figsize=(6.4,5.5));im=ax.imshow(N,cmap='viridis');
for i in range(8):
    for j in range(8):ax.text(j,i,N[i,j],ha='center',va='center',color='white' if N[i,j]<6 else 'black')
ax.set(xticks=range(8),yticks=range(8),xlabel='Destination trigram',ylabel='Source trigram',title='First octal π closure: 332 transitions');fig.colorbar(im,ax=ax,label='Visit count');fig.tight_layout()
for ext in ('svg','png'):fig.savefig(root/f'15_pi_transition_ledger.{ext}',dpi=180)
plt.close(fig)
fig,ax=plt.subplots(figsize=(7,4.3));cycles=np.arange(1,7)
for l in (2,4,6,8):
    p=abs(eval_legendre(l,0));ax.semilogy(cycles,p**(2+3*(cycles-1)),marker='o',label=f'ℓ={l}')
ax.set(xlabel='Completed three-axis averaging cycles',ylabel='Operator norm',title='Anisotropy suppression by repeated circular averaging',xticks=cycles);ax.grid(alpha=.2);ax.legend();fig.tight_layout()
for ext in ('svg','png'):fig.savefig(root/f'16_three_sweep_isotropization.{ext}',dpi=180)
plt.close(fig)
fig,ax=plt.subplots(figsize=(7,5));a=np.arange(8)*np.pi/4+np.pi/2; xx=np.cos(a);yy=np.sin(a);weights=[0,4,0,0,-2,-1,-1,0];
for j in range(8):
    u=(j+1)%8;ax.annotate('',xy=(xx[u]*.90,yy[u]*.90),xytext=(xx[j]*.90,yy[j]*.90),arrowprops=dict(arrowstyle='->',connectionstyle='arc3,rad=.22',shrinkA=12,shrinkB=12))
    ax.scatter(xx[j],yy[j],s=850,alpha=.2);ax.text(xx[j],yy[j],str(j),ha='center',va='center',fontsize=13);ax.text(1.27*xx[j],1.27*yy[j],f'{weights[j]:+d}' if weights[j] else '0',ha='center',va='center')
ax.text(0,.12,'8-sector BBP clock',ha='center',fontsize=14);ax.text(0,-.1,'q = 1/√2 per step',ha='center');ax.text(0,-.27,'q⁸ = 1/16 per orbit',ha='center');ax.set(xlim=(-1.5,1.5),ylim=(-1.5,1.5),aspect='equal');ax.axis('off');fig.tight_layout()
for ext in ('svg','png'):fig.savefig(root/f'17_bbp_circular_clock.{ext}',dpi=180)
plt.close(fig)
