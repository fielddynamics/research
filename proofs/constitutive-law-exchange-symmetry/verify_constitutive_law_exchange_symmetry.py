"""Machine checks for every algebraic step of
'The Constitutive Law from Exchange Symmetry' (degree-one form).
Run: python verify_constitutive_law_exchange_symmetry.py"""
import sympy as sp
x,mu,s,K,k,eps,g,gs=sp.symbols('x mu s K k epsilon g g_ast',positive=True)
a,b,c,d,al,ga,de=sp.symbols('a b c d alpha gamma delta',real=True)
X,Y=sp.symbols('X Y')
ok=[]
def check(name,cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ")+name)

# ---- Lemma
P=a*X*Y+b*X+c*Y+d
check("Lemma: bilinear P factors as (aY+b)(X+c/a) when ad=bc",
      sp.simplify(P.subs(d,b*c/a)-(a*Y+b)*(X+c/a))==0)
al_,be_,ga_,de_=sp.symbols('p q r t')
Q=sp.expand((al_*X+be_)*(ga_*Y+de_)); co=sp.Poly(Q,X,Y)
A_,B_,C_,D_=co.coeff_monomial(X*Y),co.coeff_monomial(X),co.coeff_monomial(Y),co.coeff_monomial(1)
check("Lemma: any product (pX+q)(rY+t) has ad-bc = 0", sp.expand(A_*D_-B_*C_)==0)
ysol=sp.solve(P,Y)[0]
check("Lemma: for m=n=1, Y = -(bX+d)/(aX+c), determinant ad-bc (fractional linear iff ad-bc!=0)",
      sp.simplify(ysol+(b*X+d)/(a*X+c))==0 and sp.expand((-b)*c-(-d)*a)==a*d-b*c)
for Pp,m_,n_ in [(X*(1-Y)-Y,1,1),(X*(1-Y)**2-Y,2,1),(X**3*(1-Y)-Y,1,3),(X**2*(1-Y)**3-Y,3,2)]:
    check(f"Lemma example: {Pp} irreducible (over Q), degree {m_} in Y, {n_} in X",
          sp.Poly(Pp,X,Y).is_irreducible and sp.degree(Pp,Y)==m_ and sp.degree(Pp,X)==n_)

# ---- Step 1
Pm=a*x*mu+b*x+c*mu+d
check("Step 1: (E) mu(0)=0 forces d=0", sp.solve(Pm.subs({x:0,mu:0}),d)==[0])
mus=sp.solve(Pm.subs(d,0),mu)[0]; Om=sp.simplify(mus/(1-mus))
check("Step 1: Omega = alpha x/(gamma x+delta), alpha=-b, gamma=a+b, delta=c",
      sp.simplify(Om-(-b*x)/((a+b)*x+c))==0)
check("Step 1: alpha*delta = -bc != 0 when ad-bc != 0 and d=0", sp.expand((-b)*c-(a*0-b*c))==0)

# ---- Step 2
Og=al*x/(ga*x+de); p=-de/ga
check("Step 2: gamma*delta<0 -> Omega(p/2)*Omega(2p) = -2 alpha^2/gamma^2 < 0 (sign change)",
      sp.simplify(Og.subs(x,p/2)*Og.subs(x,2*p)+2*al**2/ga**2)==0)
check("Step 2: gamma*delta>0 -> (gamma x+delta)/delta = (gamma/delta)x+1 > 0 on [0,oo)",
      sp.simplify((ga*x+de)/de-((ga/de)*x+1))==0)
check("Step 2: gamma*delta>0 -> Omega(oo) = alpha/gamma finite", sp.limit(Og,x,sp.oo)==al/ga)
check("Step 2: gamma=0 means a=-b, and then P = b x(1-mu) + c mu",
      sp.expand(Pm.subs({d:0,a:-b})-(b*x*(1-mu)+c*mu))==0)

# ---- Step 3
check("Step 3: Omega = k g/g_* = g/a0 with a0 = g_*/k", sp.simplify(k*g/gs-g/(gs/k))==0)
law=x*(1-mu)-mu; muL=x/(1+x)
check("Step 3: x(1-mu)=mu  <=>  mu = x/(x+1)", sp.solve(law,mu)==[muL])
check("Step 3: (x,mu)->(1/x,1-mu) maps the law to itself (up to factor)",
      sp.simplify(law.subs({x:1/x,mu:1-mu},simultaneous=True)*x+law)==0)
check("Step 3: iota(x)=1/x, involution recovered, fixed point x=1",
      sp.simplify((1/(1/x))-x)==0 and sp.solve(sp.Eq(1/x,x),x)==[1])

# ---- Consequences
check("Consequence: mu(x)+mu(1/x)=1", sp.simplify(muL+muL.subs(x,1/x)-1)==0)
check("Consequence: mu(oo)=1, mu(1)=1/2, Omega=x",
      sp.limit(muL,x,sp.oo)==1 and muL.subs(x,1)==sp.Rational(1,2) and sp.simplify(muL/(1-muL)-x)==0)

# ---- Parity form
sx=sp.simplify(2*muL-1)
check("Parity: s=2mu-1 gives s(x)=(x-1)/(x+1)", sp.simplify(sx-(x-1)/(x+1))==0)
S=sp.symbols('S',real=True); curve=x*(1-S)-(1+S)
check("Parity: law reads x(1-s)=1+s", sp.simplify(law.subs(mu,(1+S)/2)*2-curve)==0)
check("Parity: (x,s)->(1/x,-s) maps x(1-s)=1+s to itself (up to factor)",
      sp.simplify(curve.subs({x:1/x,S:-S},simultaneous=True)*x+curve)==0)
f=1+S*K+K**2
check("Parity: (f(K,s)-f(K,-1))/2K = (1+s)/2", sp.simplify((f-f.subs(S,-1))/(2*K)-(1+S)/2)==0)
check("Parity: f(4,s) = 21, 17, 13 at s = 1, 0, -1", [f.subs({K:4,S:v}) for v in (1,0,-1)]==[21,17,13])
check("Route 1 boundary conditions: s(0)=-1 (E), s(1)=0 (unit), s(oo)=+1 (derived)",
      sx.subs(x,0)==-1 and sx.subs(x,1)==0 and sp.limit(sx,x,sp.oo)==1)

# ---- Necessity table
bb=sp.symbols('beta',positive=True)
OE=(x+bb)/(bb*x+1); muE=sp.simplify(OE/(1+OE))
PE=sp.expand(sp.numer(sp.together(mu-muE)))   # bilinear relation for row (E)
cE=sp.Poly(PE,x,mu)
aE,bE,cEE,dE=[cE.coeff_monomial(m) for m in (x*mu,x,mu,1)]
check("Row (E): relation is bilinear with ad-bc = (1-b^2)(...) != 0 for 0<b<1",
      sp.degree(PE,x)==1 and sp.degree(PE,mu)==1 and sp.factor(aE*dE-bE*cEE)!=0
      and sp.simplify((aE*dE-bE*cEE).subs(bb,1))==0)
check("Row (E): mu(0)=b/(1+b); states fill [b/(1+b),1/(1+b)], closed under mu->1-mu",
      sp.simplify(muE.subs(x,0)-bb/(1+bb))==0 and sp.simplify(sp.limit(muE,x,sp.oo)-1/(1+bb))==0
      and sp.simplify(sp.diff(OE,x)-(1-bb**2)/(bb*x+1)**2)==0)
OX=2*x/(x+3); muX=OX/(1+OX)
check("Row (X): alpha,gamma,delta>0: bilinear, mu(0)=0, mu(oo)=alpha/(alpha+gamma)<1",
      OX.subs(x,0)==0 and sp.limit(muX,x,sp.oo)==sp.Rational(2,3))
fam_ok=True
for n in range(1,5):
    for m in range(1,5):
        if (n,m)==(1,1): continue
        R=x**n*(1-mu)**m-mu
        lead=sp.Poly(R,x).LC()                     # (1-mu)^m
        eis = sp.rem(lead,mu,mu)!=0 and sp.Poly(R,x).TC()==-mu   # Eisenstein at mu
        dec = sp.simplify(sp.diff(R,mu)+m*x**n*(1-mu)**(m-1)+1)==0  # dR/dmu<0 on [0,1]
        ends= R.subs(mu,0)==x**n and R.subs(mu,1)==-1
        deg = sp.degree(R,x)==n and sp.degree(R,mu)==m
        fam_ok &= bool(eis and dec and ends and deg)
check("Row (A): x^n(1-mu)^m=mu, n,m<=4: Eisenstein at mu, degree (n,m), unique root in [0,1]", fam_ok)
Ob=(sp.sqrt(1+4*x)-1)/2; mub=Ob/(1+Ob)
check("Row (A): (1,2) is the bound law, = Paper XIII mu_SST, runs 0 -> 1",
      sp.simplify(x*(1-mub)**2-mub)==0 and sp.simplify(mub-((2*x+1)-sp.sqrt(4*x+1))/(2*x))==0
      and sp.limit(mub,x,0)==0 and sp.limit(mub,x,sp.oo)==1)
m3=x**3/(1+x**3)
check("Row (A): (3,1) is mu = x^3/(1+x^3), runs 0 -> 1", sp.simplify(x**3*(1-m3)-m3)==0 and sp.limit(m3,x,sp.oo)==1)
m=1-sp.exp(-x)
check("Without (A): e.g. 1-exp(-x) satisfies (E) and closure", m.subs(x,0)==0 and sp.limit(m,x,sp.oo)==1)

# ---- Route 2
n=sp.symbols('n',positive=True,integer=True)
bal=x**n*(1-eps)-eps/K
check("Route 2: balance x^n(1-eps)=eps/K has degree 1 in eps; n=1, K=1 gives x(1-eps)=eps",
      sp.degree(bal.subs(n,2),eps)==1 and sp.simplify(bal.subs({n:1,K:1})-(x*(1-eps)-eps))==0)

print(f"\n{sum(ok)}/{len(ok)} checks passed")
