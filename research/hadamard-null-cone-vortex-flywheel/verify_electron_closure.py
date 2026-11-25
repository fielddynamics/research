"""Verify conditional electron closure algebra; no physical parameter fitted."""
import csv, math
from pathlib import Path
import numpy as np
import sympy as s
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
root=Path(__file__).resolve().parent
checks=0

def check(label, test):
    global checks
    assert bool(test), label
    checks+=1
    print(f'PASS {checks:03d} {label}')

def eq(label, a,b):
    check(label,s.simplify(a-b)==0)

A,B,R,E,M,K,gamma,alpha,h,c,a0,G = s.symbols('A B R E M K gamma alpha h c a0 G',positive=True)
# A=alpha*hbar*c, B=a0*c^2/(K^2 G), fixed G on radial variation.
mp=a0*alpha**2*h/(K**2*gamma*c**3)
rp=K**2*gamma*c**2/(alpha*a0)
gp=K**4*gamma**3*c**7/(alpha**4*h*a0**2)
eq('joint EM closure',mp*c**2,alpha*h*c/rp)
eq('joint saturation',K**2*gp*mp/rp**2,a0)
eq('joint topology',gp,gamma*h*c/mp**2)
eq('joint radius product',mp*rp,alpha*h/c)
eq('joint constant product',gp*mp**2,gamma*h*c)
check('log residual Jacobian determinant, fixed G',s.Matrix([[1,1],[-1,2]]).det()==3)
check('log residual Jacobian determinant, inherited G(M)',s.Matrix([[1,1],[1,2]]).det()==1)
check('log three-variable closure system nonsingular',s.Matrix([[1,1,0],[-1,2,-1],[2,0,1]]).det()==1)
for label, expr, exponent in [('m',mp,1),('r',rp,-1),('G',gp,-2)]:
    eq('a0 log sensitivity '+label,a0*s.diff(expr,a0)/expr,exponent)
for label, expr, exponent in [('m',mp,-1),('r',rp,1),('G',gp,3)]:
    eq('gamma log sensitivity '+label,gamma*s.diff(expr,gamma)/expr,exponent)

# Exact four-channel raw pair read vs normalized read.
d=s.Matrix(s.symbols('d1:5',real=True)); ones=s.ones(4,1)
P=(d*ones.T+ones*d.T)/2
x=s.symbols('x',real=True)
eq('raw pair read',sum(P),4*sum(d))
eq('equal central raw pair read',sum(P).subs(dict.fromkeys(d,x)),16*x)
eq('normalized pair read',sum(P).subs(dict.fromkeys(d,x))/16,x)
U=s.Matrix([[1,1,1,1],[1,1,-1,-1],[1,-1,1,-1],[1,-1,-1,1]])/2
check('Hadamard orthonormal',U.T*U==s.eye(4))
check('equal four central channels are pure scalar',U*ones==s.Matrix([2,0,0,0]))
for perm in __import__('itertools').permutations(range(4)):
    check('pair read permutation invariant '+str(perm),s.simplify(sum(P.extract(perm,perm))-sum(P))==0)
# Smooth, idempotent read of two closure energies; NOT a microscopic energy derivation.
Ee=A/R; Ec=B*R**2; Rstar=(A/B)**s.Rational(1,3)
V=(2*Ee+Ec)/3
w=s.symbols('w',real=True)
eq('weighted read stationarity coefficient',s.diff(w*Ee+(1-w)*Ec,R).subs(A,B*R**3),B*R*(2-3*w))
eq('registered energy stationarity',s.diff(V,R).subs(A,B*R**3),0)
eq('registered energy curvature',s.diff(V,R,2).subs(A,B*R**3),2*B)
eq('registered energy equality',V.subs(A,B*R**3),B*R**2)
eq('old unnormalized energy double count',(Ee+Ec/2).subs(A,B*R**3),s.Rational(3,2)*B*R**2)
x=s.symbols('x',positive=True)
Vn=(2/x+x**2)/3
eq('normalized registered read minimum',Vn.subs(x,1),1)
eq('global minimum factorization',Vn-1,(x-1)**2*(x+2)/(3*x))
eq('dimensionless curvature',s.diff(Vn,x,2).subs(x,1),2)
# Family of equally idempotent power means: physical dynamics not unique.
p,t=s.symbols('p t',real=True,nonzero=True)
logV=s.log((2*s.exp(-p*t)+s.exp(2*p*t))/3)/p
eq('power mean first log derivative',s.diff(logV,t).subs(t,0),0)
eq('power mean second log derivative',s.diff(logV,t,2).subs(t,0),2*p)
eq('geometric mean is flat',(1/R)**s.Rational(2,3)*(R**2)**s.Rational(1,3),1)
# Reciprocal lossless interface example, positive energy proxies treated as impedances.
rr=(1-x**3)/(1+x**3); tt=2*x**s.Rational(3,2)/(1+x**3)
S=s.Matrix([[rr,tt],[tt,-rr]])
check('optical interface orthogonal',s.simplify(S.T*S-s.eye(2))==s.zeros(2))
eq('optical closure perfect transmission',tt.subs(x,1),1)
eq('optical closure zero reflection',rr.subs(x,1),0)
eq('optical reflection local curvature',s.diff(rr**2,x,2).subs(x,1),s.Rational(9,2))
eq('four ports all matched', (tt**8).subs(x,1),1)
# Bare scale-homogeneous vortex mode is insufficient to select radius.
eq('scale-homogeneous eigenenergy derivative',s.diff(A/R,R),-A/R**2)
# Positive exterior field energy read and hypothetical volume-cost balance.
P0=s.symbols('P0',positive=True)
F=G*M**2/(2*R)+4*s.pi*R**3*P0/3
eq('free boundary matching',s.diff(F,R).subs(P0,G*M**2/(8*s.pi*R**4)),0)
eq('free boundary positive curvature',s.diff(F,R,2).subs(P0,G*M**2/(8*s.pi*R**4)),2*G*M**2/R**3)
eq('on-shell source-included static action has opposite field sign',G*M**2/(2*R)-G*M**2/R,-G*M**2/(2*R))
# Numerical consistency, not new measured values. Use previous package's constants.
alpha_n=1/137.035999177; h_n=1.054571817e-34; c_n=299792458.; K_n=4
Gref=6.67430e-11; mref=9.1093837139e-31
rows=[]
for loop in (0,1):
    gamma_n=17/13*alpha_n**21*(1+alpha_n/(2*math.pi) if loop else 1)
    a_required=K_n**2*gamma_n*mref*c_n**3/(alpha_n**2*h_n)
    G_at_mref=gamma_n*h_n*c_n/mref**2
    for a in (1.2e-10,1.22e-10,1.225e-10,a_required):
        m=a*alpha_n**2*h_n/(K_n**2*gamma_n*c_n**3); r=alpha_n*h_n/(m*c_n); g=gamma_n*h_n*c_n/m**2
        check(f'numeric EM closure {loop} {a:.15g}',math.isclose(m*c_n**2,alpha_n*h_n*c_n/r,rel_tol=2e-15))
        check(f'numeric grav saturation {loop} {a:.15g}',math.isclose(K_n**2*g*m/r**2,a,rel_tol=2e-15))
        check(f'numeric topology closure {loop} {a:.15g}',math.isclose(g*m*m/(h_n*c_n),gamma_n,rel_tol=2e-15))
        rows.append([loop,a,m,r,g,100*(m/mref-1),100*(g/Gref-1),'reference mass inverted; NOT prediction' if a==a_required else 'illustrative independent a0 input'])
    print(f'order={loop}: a0 required at reference mass={a_required:.12g}, G at reference mass={G_at_mref:.12g}')
with (root/'electron_closure_values.csv').open('w',newline='') as f:
    wr=csv.writer(f);wr.writerow(['loop','a0_m_s2','mass_kg','radius_m','G_SI','mass_relative_error_percent','G_relative_error_percent','input_note']);wr.writerows(rows)
# Illustrate both the energy-accounting issue and the non-independent input sensitivity.
fig,ax=plt.subplots(1,3,figsize=(14.3,4.3),layout='constrained')
xv=np.linspace(.35,2.1,500)
ax[0].plot(xv,1/xv,label='EM read $1/x$',color='#2563a6');ax[0].plot(xv,xv*xv,label='closure read $x^2$',color='#c46b25')
ax[0].plot(xv,(2/xv+xv*xv)/3,label='registered mean',color='#09857b',lw=2.6);ax[0].plot(xv,1/xv+xv*xv/2,label='old additive cost',ls='--',color='#666')
ax[0].scatter([1],[1],c='#09857b',zorder=4);ax[0].set(xlabel='$R/R_*$ ',ylabel='Energy / matched energy',title='A. Match two reads, not two energies',ylim=(0,3.8));ax[0].legend(fontsize=8)
T=4*xv**3/(1+xv**3)**2
ax[1].plot(xv,T,label='one port',color='#2563a6',lw=2);ax[1].plot(xv,T**4,label='all four (factorized)',color='#09857b',lw=2);ax[1].plot(xv,1-T,label='one-port reflection',color='#c46b25',ls='--');ax[1].set(xlabel='$R/R_*$',ylabel='Power fraction',title='B. Conditional optical matching',ylim=(0,1.05));ax[1].legend(fontsize=8)
a=np.linspace(1.19e-10,1.25e-10,400);gamma_n=17/13*alpha_n**21*(1+alpha_n/(2*math.pi));m=a*alpha_n**2*h_n/(K_n**2*gamma_n*c_n**3);g=gamma_n*h_n*c_n/m**2
ax[2].plot(a/1e-10,100*(m/mref-1),label='mass difference',color='#2563a6',lw=2);ax[2].plot(a/1e-10,100*(g/Gref-1),label='$G$ difference',color='#c46b25',lw=2);ax[2].axhline(0,color='#777',lw=.9);ax[2].axvline(1.22,color='#777',ls=':',lw=1);ax[2].set(xlabel='$a_0$ ($10^{-10}$ m/s²)',ylabel='Difference from reference (%)',title='C. Joint prediction (proposed loop)');ax[2].legend(fontsize=8)
for aa in ax: aa.grid(alpha=.16);aa.spines[['top','right']].set_visible(False)
fig.suptitle('Electron closure: conditional algebra and the unresolved physical read',fontsize=15)
fig.savefig(root/'figures/39_electron_closure.svg');fig.savefig(root/'figures/39_electron_closure.png',dpi=150);plt.close(fig)
print(f'\n{checks}/{checks} checks passed. Prior checks not rerun. No microscopic derivation of closure premises.')
