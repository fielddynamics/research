"""Exact conditional recursive-clock constraint checks; no fit to G."""
import sympy as s
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).parent
n=0
def ck(name,test):
 global n
 assert bool(test),name
 n+=1; print(f'PASS {n:02d} {name}')
t,k,K,l1,l2,l3=s.symbols('t k K l1 l2 l3',positive=True)
# q=(root, first, second, terminal); z=(root, three residuals)
C=s.Matrix([[-t,1,0,0],[0,-t**4,1,0],[0,0,-t**16,1]])
B=s.Matrix.vstack(s.eye(4)[0,:],C); U=B.inv(); v=U[:,0]; e=s.eye(4)[:,3]
ck('three constraints independent',C.rank()==3)
ck('null branch exact',v==s.Matrix([1,t,t**5,t**21]) and C*v==s.zeros(3,1))
ck('constraint coordinates unimodular',B.det()==1)
ck('terminal coordinate response',e.T*U==s.Matrix([[t**21,t**20,t**16,1]]))
L=s.diag(l1,l2,l3); D=s.diag(K*k**2,l1,l2,l3); A=B.T*D*B
ck('positive sum of squares',A==K*k**2*s.diag(1,0,0,0)+C.T*L*C)
G=U*D.inv()*U.T
ck('exact inverse in residual coordinates',s.simplify(A*G-s.eye(4))==s.zeros(4))
g=(e.T*G*e)[0]; target=t**42/(K*k**2)+t**40/l1+t**32/l2+1/l3
ck('pole plus local contacts',s.simplify(g-target)==0)
ck('massless pole exponent 42 in amplitude t',s.limit(k**2*g,k,0)==t**42/K)
ck('root read instead gives unsuppressed pole',G[0,0]==1/(K*k**2))
for i,m in enumerate([0,1,5,21]):
 ck(f'grade {i} pole',s.limit(k**2*G[i,i],k,0)==t**(2*m)/K)
# Arbitrary gradient metric, pole found from kernel projection. Independent rational verification.
Dg=s.diag(2,3,5,7); Ktest=C.subs(t,s.Rational(1,2)).T*s.diag(11,13,17)*C.subs(t,s.Rational(1,2)); vt=v.subs(t,s.Rational(1,2)); z=s.symbols('z', positive=True)
# use determinant/adjugate first Taylor coefficient, exact rational matrices
At=Ktest+z*Dg; adj=At.adjugate(); det=At.det(); res=adj.subs(z,0)/s.diff(det,z).subs(z,0)
ck('all-gradient massless residue exact',res==vt*vt.T/(vt.T*Dg*vt)[0])
ck('massless branch normalized stiffness',s.expand((v.T*v)[0])==1+t**2+t**10+t**42)
# no bypass: generic extra root/earlier source changes leading exponent
b0,b1,b2,b3=s.symbols('b0 b1 b2 b3'); b=s.Matrix([b0,b1,b2,b3]); read=(b.T*v)[0]
ck('generic read has lower-order bypasses',read==b0+b1*t+b2*t**5+b3*t**21)
ck('equal root and terminal reads unsuppressed',s.limit(read.subs({b0:1,b1:0,b2:0,b3:1}),t,0)==1)
# positivity and rank check on specific weights; only three massive branches
ck('internal constraint Hessian rank three',Ktest.rank()==3)
ck('null branch not localized on terminal',vt[0]==1 and vt[3]==s.Rational(1,2)**21)
# static Einstein scalar energy: after integration by parts to quadratic order
# E = A/2 (2 grad u dot grad v - |grad v|²) -> constraint grad v=grad u
u,w,a=s.symbols('u w a', real=True); E=a*(2*u*w-w*w)/2
ck('spatial constraint gradient equals lapse gradient',s.solve(s.diff(E,w),w)==[u])
ck('reduced Einstein stiffness',s.simplify(E.subs(w,u)-a*u*u/2)==0)
# dimensionless G identity after matter coupling and root energy
c,hbar,m,alpha,kap=s.symbols('c hbar m alpha kap',positive=True)
Gn=c**4*t**42/(4*s.pi*kap); gam=Gn*m*m/(hbar*c)
ck('dimensionless response',s.simplify(gam.subs(t,s.sqrt(alpha))-m*m*c**3*alpha**21/(4*s.pi*hbar*kap))==0)
kapstar=m*m*c**3/(4*s.pi*hbar)
ck('required stiffness for ratio, not a prediction',s.simplify(gam.subs({t:s.sqrt(alpha),kap:13*kapstar/17})-s.Rational(17,13)*alpha**21)==0)
# diagram of amplitude and intensity exponents (symbolic, not simulated clocks)
fig,ax=plt.subplots(figsize=(10,4.2)); ax.axis('off'); xs=[.09,.36,.63,.90]
for i,(x,lab,exp) in enumerate(zip(xs,['Reference','Grade 1','Grade 4','Grade 16'],[0,1,5,21])):
 ax.text(x,.66,lab+'\n$q_'+str(i)+'$',ha='center',va='center',fontsize=12,bbox=dict(boxstyle='round,pad=.55',fc='#eaf2f8',ec='#35698c'),transform=ax.transAxes)
 ax.text(x,.35,r'$q_'+str(i)+r'/q_0=t^{'+str(exp)+'}$',ha='center',fontsize=12,transform=ax.transAxes)
 if i<3:
  ax.annotate('',xy=(xs[i+1]-.085,.66),xytext=(x+.085,.66),xycoords='axes fraction',arrowprops=dict(arrowstyle='->',lw=2,color='#35698c'))
  ax.text((x+xs[i+1])/2,.77,r'$t^{'+str([1,4,16][i])+'}$',ha='center',transform=ax.transAxes,fontsize=13)
ax.text(.5,.13,r'Terminal clock $u=q_3$; long-range residue $t^{42}/\kappa_0$ (root-only stiffness)',ha='center',transform=ax.transAxes,fontsize=12)
ax.set_title('Conditional collective constraint: three grades, one gapless branch',fontsize=15);fig.tight_layout();fig.savefig(p/'recursive_clock_constraint.svg');plt.close(fig)
print(f'{n}/{n} checks passed')
