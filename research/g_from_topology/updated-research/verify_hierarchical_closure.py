#!/usr/bin/env python3
"""Conditional fixed-domain hierarchical closure. No new physical fit."""
import numpy as np
import sympy as s
from scipy.optimize import brentq
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
out=Path(__file__).resolve().parent
counts={'exact':0,'numerical':0}
def check(name, condition, kind='numerical'):
    assert bool(condition),name
    counts[kind]+=1
    print('PASS',kind,name)
def eq(name,a,b):
    d=a-b
    check(name, all(s.simplify(x)==0 for x in d) if isinstance(d,s.MatrixBase) else s.simplify(d)==0,'exact')
def near(name,a,b,tol=2e-9):
    check(name,np.allclose(a,b,rtol=tol,atol=tol))
# Exact grounded path: unknowns 1..5, endpoints fixed.
K=s.diag(*([2]*5))
for i in range(4): K[i,i+1]=K[i+1,i]=-1
I=s.eye(5)
def proj(K,indices):
    E=s.eye(K.rows)[:,indices]
    return E*(E.T*K*E).inv()*E.T*K
P=proj(K,[2]); Q=proj(K,[1,2,3]); H=I-Q
for label,A in [('child',P),('parent',Q)]:
    eq(label+' idempotence',A*A,A);eq(label+' energy adjoint',A.T*K,K*A)
eq('nested forward',P*Q,P);eq('nested reverse',Q*P,P)
bands=[P,Q-P,H]
for i,A in enumerate(bands):
    eq(f'band {i} idempotence',A*A,A)
    for j,B in enumerate(bands):
        if i!=j: eq(f'orthogonal {i} {j}',A.T*K*B,s.zeros(5))
eq('partition',sum(bands,s.zeros(5)),I)
eq('dual sweep nesting',(I-Q).T*(I-P).T,(I-Q).T)
f=s.Matrix([0,0,7,0,0]); g=(I-P).T*f
eq('sweep distributes half to either boundary',g,s.Matrix([0,s.Rational(7,2),0,s.Rational(7,2),0]))
eq('two sweeps vs direct',(I-Q).T*g,(I-Q).T*f)
eq('mass on outer boundary',(I-Q).T*f,s.Matrix([s.Rational(7,2),0,0,0,s.Rational(7,2)]))
A=proj(K,[1]); B=proj(K,[2]);check('adjacent nonnested projections need not commute',A*B!=B*A,'exact')
# Scalar settlement is not an idempotent closure.
x=s.symbols('x',positive=True); mu=lambda x:x/(1+x)
eq('mu composed with mu',mu(mu(x)),x/(1+2*x))
eq('pointwise flux double partition',mu(mu(x)*x)*mu(x)*x,x**4/((1+x)*(1+x+x*x)))
# Schur reduction exact: arbitrary boundary variables, internal load.
Iix=[1,2,3]; Bix=[0,4]; L=K.extract(Iix,Iix); M=K.extract(Iix,Bix); D=K.extract(Bix,Bix); fi=f[Iix,:]; fb=f[Bix,:]
b=s.Matrix(s.symbols('b0 b1')); u=L.inv()*(fi-M*b); S=D-M.T*L.inv()*M; fs=fb-M.T*L.inv()*fi
z=s.Matrix([b[0],*u,b[1]]); E=(z.T*K*z)[0]/2-(f.T*z)[0]; Ered=(b.T*S*b)[0]/2-(fs.T*b)[0]-(fi.T*L.inv()*fi)[0]/2
eq('Schur value',E,Ered);eq('boundary gradient',s.Matrix([s.diff(E,t) for t in b]),S*b-fs)
eq('boundary record source',fs,s.Matrix([s.Rational(7,2),s.Rational(7,2)]))
eq('internal residual independent of boundary',u+L.inv()*M*b,L.inv()*fi)
# Pointwise nonlinear leakage into unresolved child contrasts.
j=lambda v:v*abs(v)/(1+abs(v))
eq('unprojected nonlinear residual at host zero',j(s.Rational(1,2))-j(-s.Rational(1,2)),s.Rational(1,3))
eq('unprojected nonlinear residual at host one',j(s.Rational(3,2))-j(s.Rational(1,2)),s.Rational(11,15))
# 2-D grounded Laplacian (all outside boundary values zero).
def grid(n):
    A=np.eye(n*n)*4
    for i in range(n):
        for j in range(n):
            for di,dj in ((1,0),(-1,0),(0,1),(0,-1)):
                ii,jj=i+di,j+dj
                if 0<=ii<n and 0<=jj<n:A[i*n+j,ii*n+jj]=-1
    return A
def pnum(K,ind):
    E=np.eye(len(K))[:,ind];return E@np.linalg.solve(E.T@K@E,E.T@K)
rng=np.random.default_rng(20261126)
for n in [5,7,9,11]:
    L=grid(n); ident=np.eye(n*n); child=[i*n+j for i in range(n//2-1,n//2+2) for j in range(n//2-1,n//2+2)]; parent=[i*n+j for i in range(1,n-1) for j in range(1,n-1)]
    P=pnum(L,child);Q=pnum(L,parent); Ps=[P,Q-P,ident-Q]
    near(f'{n} nesting',P@Q,P);near(f'{n} reverse nesting',Q@P,P)
    for i,V in enumerate(Ps):
        near(f'{n} idempotence {i}',V@V,V);near(f'{n} selfadjoint {i}',V.T@L,L@V)
        for k,W in enumerate(Ps):
            if i<k:near(f'{n} orthogonal {i},{k}',V.T@L@W,np.zeros_like(L))
    for k in range(5):
        f=np.zeros(n*n); f[child]=rng.uniform(0,1,len(child)); swept=(ident-P).T@f
        near(f'{n}.{k} eliminated sources',swept[child],0);near(f'{n}.{k} source mass',swept.sum(),f.sum())
        near(f'{n}.{k} telescoping sweep',(ident-Q).T@swept,(ident-Q).T@f)
        u=np.linalg.solve(L,f);near(f'{n}.{k} parent field',np.linalg.solve(L,swept),(ident-P)@u)
        near(f'{n}.{k} energy split',u@L@u,sum((V@u)@L@(V@u) for V in Ps))
        h=(ident-P)@rng.normal(size=n*n);near(f'{n}.{k} child unaffected by host',P@(u+h),P@u)
# Exact nonlinear variational composition on 1D paths, same fully open mu on every edge.
# F(v)=integral of j(v), units a0=1; signed inverse.
def flux(v): return v*abs(v)/(1+abs(v))
def inv(q): return np.sign(q)*(abs(q)+np.sqrt(q*q+4*abs(q)))/2
def energy(v):
    x=np.abs(v);return x*x/2-x+np.log1p(x)
def path_solution(load,a,b):
    # stationarity j_left - j_right = load, so j_edges=q0-[0,cumsum(load)]
    offset=np.r_[0,np.cumsum(load)]
    q0=brentq(lambda q:inv(q-offset).sum()-(b-a),-1000,1000,xtol=1e-13)
    v=inv(q0-offset); u=np.r_[a,a+np.cumsum(v)];return u,energy(v).sum()-np.dot(load,u[1:-1]),q0,q0-offset[-1]
for k in range(20):
    load=rng.uniform(-1,1,7);a,b=rng.uniform(-2,2,2); split=4
    u,E,_,_=path_solution(load,a,b)
    def segments(c):return path_solution(load[:split-1],a,c),path_solution(load[split:],c,b)
    def match(c):
        l,r=segments(c);return l[3]-r[2]-load[split-1]
    c=brentq(match,-100,100,xtol=1e-12);l,r=segments(c)
    near(f'nonlinear {k} boundary state',c,u[split]);near(f'nonlinear {k} energy composition',l[1]+r[1]-load[split-1]*c,E)
    near(f'nonlinear {k} recovered full field',np.r_[l[0],r[0][1:]],u)
    near(f'nonlinear {k} interface flux',match(c),0)
# Figure: same child with boundary perturbation; compare naive nonlinear residual.
v=np.linspace(-2,2,401);r=.5; actual=flux(v+r)-flux(v-r)
fig,ax=plt.subplots(1,2,figsize=(11,4.1),layout='constrained')
for b0,b1 in [(0,0),(-.5,.5),(1,1)]:
    bb=np.array([b0,b1]); uu=np.linalg.solve(np.array(L0:=K.extract(Iix,Iix)).astype(float),np.array(fi).astype(float).ravel()-np.array(M).astype(float)@bb)
    h=np.linalg.solve(np.array(L0).astype(float),-np.array(M).astype(float)@bb)
    ax[0].plot(np.arange(5),np.r_[b0,uu,b1],marker='o',label=f'boundary ({b0:g}, {b1:g})')
    ax[0].plot(np.arange(5),np.r_[0,uu-h,0],'k:',alpha=.7)
ax[0].set(title='Same settled residual, different host trace',xlabel='Graph position',ylabel='Potential (normalized)');ax[0].legend(fontsize=8);ax[0].grid(alpha=.25)
ax[1].plot(v,actual,label='Pointwise μ on total field');ax[1].axhline(flux(r)-flux(-r),ls='--',label='Separate owned mode (nonlinear)');ax[1].axhline(2*r,ls=':',label='Separate owned mode (Newtonian)');ax[1].set(title='Host leakage if μ is reapplied',xlabel='Host gradient',ylabel='Child contrast flux');ax[1].legend(fontsize=8);ax[1].grid(alpha=.25)
fig.savefig(out/'figures/hierarchical_closure.png',dpi=180);plt.close(fig)
print(f"TOTAL {sum(counts.values())}: {counts['exact']} exact + {counts['numerical']} numerical passed")
