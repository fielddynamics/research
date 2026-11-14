"""Checks for the section 'Three routes tested' of the research note 'Two connections and the dual chamber'.
Route 1: the two chambers as a two-state system. Route 2: TetB's clock rate (equivalently the share) as an auxiliary field.
Route 4: TetB as a channel through a throat of capacity a0. Exact sympy. Run: python verify_three_routes.py"""
import sympy as sp
ok=[]
def check(n,c): ok.append(bool(c)); print(("PASS " if c else "FAIL ")+n)
x,y,w,g,a0,gN,T=sp.symbols('x y w g a_0 g_N T',positive=True)
F=lambda Y: Y-2*sp.sqrt(Y)+2*sp.log(1+sp.sqrt(Y))
mu=lambda X: X/(1+X)

print("--- Route 1: the two chambers as a two-state system")
Z=1+x
check("1a with Z = V/V0 = 1 + x (two states, statistical weights 1 and x), the TetB occupation d ln Z/d ln x is mu(x)",
      sp.simplify(x*sp.diff(sp.log(Z),x)-mu(x))==0)
check("1b the SST energy is F = y - 2(Z - 1) + 2 ln Z: the logarithm is ln Z, the log-partition function of the two chambers",
      sp.simplify(F(x**2)-(x**2-2*(Z-1)+2*sp.log(Z)))==0)
s_=sp.symbols('s',positive=True)
check("1c F is the work integral of the TetB occupation against y: F(y) = int_0^y mu(sqrt t) dt; partial fractions of 2x^2/(1+x) "
      "produce the ln Z", sp.simplify(sp.integrate(2*s_*mu(s_),(s_,0,x))-F(x**2))==0)
check("1d if each chamber's weight is proportional to a horizon temperature, TetA ~ T(a0) and TetB ~ T_Unruh(g) = hbar g/(2 pi c k), "
      "the odds are T_U(g)/T(a0) = g/a0 and the TetB share is g/(g + a0) = mu", sp.simplify((g/(g+a0))-mu(g/a0))==0)
muM=(sp.sqrt(x**2+1)-1)/x
check("1e Milgrom's 1999 vacuum construction, inertia ~ T_U(sqrt(g^2 + a0^2)) - T_U(a0), gives a different law, (sqrt(1+x^2) - 1)/x, "
      "which goes as x/2 in the deep field: the additive two-state weighting reproduces mu, the subtractive one does not",
      sp.simplify(muM-mu(x))!=0 and sp.limit(muM/x,x,0)==sp.Rational(1,2))
dE=sp.symbols('dE',positive=True)
Tsol=lambda X: sp.solve(sp.Eq(sp.exp(-dE/T),X),T)
check("1f a Boltzmann factor at one positive temperature with a fixed gap dE > 0 gives odds exp(-dE/T) < 1 only: it cannot reach x > 1, "
      "so the weights are not Boltzmann factors; they are linear in x, a ratio of temperatures (1d)",
      Tsol(sp.Rational(1,2))!=[] and Tsol(2)==[])
lam_,m_=sp.symbols('lambda m',real=True)
sp_=sp.log(1+sp.exp(lam_))                                # ln Z as a function of the log-odds lambda = ln x
check("1g in the log-odds lambda = ln x, ln Z = ln(1 + e^lambda) (the softplus) and its slope is the logistic share 1/(1 + e^-lambda) = mu",
      sp.simplify(sp.diff(sp_,lam_)-1/(1+sp.exp(-lam_)))==0)
mm=sp.symbols('mm',positive=True)
obj=mm*lam_-sp_                                            # mu lambda - ln Z
lam_star=sp.log(mm/(1-mm))
val=mm*lam_star-sp.log(1+mm/(1-mm))
ent=mm*sp.log(mm)+(1-mm)*sp.log(1-mm)
check("1h its Legendre dual is the mixing entropy of the two chambers: mu lambda - ln Z is concave in lambda, stationary at "
      "lambda = ln(mu/(1 - mu)), where it equals mu ln mu + (1 - mu) ln(1 - mu): the shares are the maximum-entropy split for given log-odds",
      sp.simplify(sp.diff(obj,lam_).subs(lam_,lam_star))==0 and sp.simplify(sp.diff(obj,lam_,2)+sp.exp(lam_)/(1+sp.exp(lam_))**2)==0
      and all(abs(float((val-ent).subs(mm,q)))<1e-14 for q in (0.1,0.37,0.5,0.81)))
check("1i the time-leg energy is a Gaussian relative entropy: F - y = -2 D(Z) with D(Z) = Z - 1 - ln Z = 2 KL(N(0, Z) || N(0, 1)), so "
      "F - y = -4 KL between a Gaussian of variance Z = 1 + x and the unit Gaussian",
      sp.simplify((F(x**2)-x**2)+4*sp.Rational(1,2)*(Z-1-sp.log(Z)))==0)

print("--- Route 2: TetB's clock rate as an auxiliary field")
G_=lambda W,Y: -Y/W - W + 1/W + 2*sp.log(W)      # candidate for the time-leg term F - y, with W = V/V0 = TetB clock factor 1 + x
sol=sp.solve(sp.diff(G_(w,y),w),y)
check("2a the term (F - y) = max over w of [-y/w - w + 1/w + 2 ln w]: its w-equation is algebraic and gives y = (w - 1)^2, i.e. w = 1 + x",
      len(sol)==1 and sp.expand(sol[0]-(w-1)**2)==0)
check("2b at that point its value is exactly F(y) - y", sp.simplify(G_(1+x,x**2)-(F(x**2)-x**2))==0)
d2=sp.simplify(sp.diff(G_(w,y),w,2).subs(y,(w-1)**2).subs(w,1+x))
check("2c and it is a maximum in w: d^2/dw^2 = -2x(1+x)/(1+x)^3 < 0", sp.simplify(d2+2*x*(1+x)/(1+x)**3)==0)
check("2d for fixed w the term is linear in y, with slope -1/w; adding the curvature term's y gives the conductivity 1 - 1/w = 1 - V0/V, "
      "the TetB volume share. At w = 1 + x it is mu(x): for fixed w the field equation is linear, as in QUMOND",
      sp.simplify(sp.diff(y+G_(w,y),y)-(1-1/w))==0 and sp.simplify((1-1/(1+x))-mu(x))==0)
check("2e envelope: d/dy of the stationary value equals the partial derivative at fixed w, so treating w as an independent field gives "
      "the same Phi-equation as the SST", sp.simplify(sp.diff(F(y)-y,y)-sp.diff(G_(w,y),y).subs(w,1+sp.sqrt(y)))==0)
mu_=sp.symbols('mu_',positive=True)
Zm=1/(1-mu_)                                              # the clock factor in terms of the share: w = Z = 1/(1 - mu)
K=Zm-1/Zm-2*sp.log(Zm)
check("2f change variables from the clock factor w to the share mu = 1 - 1/w (w = Z = 1/(1 - mu)): the auxiliary form becomes "
      "F(y) = max over mu of [mu y - K(mu)] with K = Z - 1/Z - 2 ln Z = 2(sinh u - u), u = ln Z",
      sp.simplify((mu_*y-K) - (y+G_(Zm,y)))==0 and sp.simplify(K.subs(mu_,1-sp.exp(-lam_))-2*(sp.sinh(lam_)-lam_)).rewrite(sp.exp).simplify()==0)
check("2g K'(mu) = (mu/(1 - mu))^2 = Omega^2: maximizing over the share sets y = Omega^2, i.e. the odds equal x. The constitutive law is "
      "the stationarity condition of the share", sp.simplify(sp.diff(K,mu_)-(mu_/(1-mu_))**2)==0)
check("2h K is convex in the share (K'' > 0 for 0 < mu < 1), so the maximum is unique and F is its Legendre transform: F and K are a "
      "conjugate pair, the share mu and y being conjugate variables", sp.simplify(sp.diff(K,mu_,2)-2*mu_/(1-mu_)**3)==0)

print("--- Route 4: TetB as a channel through the throat")
gB=1/(1/g+1/a0)
check("4a if TetB's field is the series (harmonic) combination of the local field and a throat capacity a0, 1/g_B = 1/g + 1/a0, then "
      "g_B = a0 g/(g + a0) = a0 mu = (1 - mu) g: never more than a0", sp.simplify(gB-a0*mu(g/a0))==0 and sp.simplify(gB-(1-mu(g/a0))*g)==0)
solg=sp.solve(sp.Eq(g,gN+gB),gN)
check("4b and if the observed field is the Newtonian field plus the TetB channel, g = g_N + g_B, then g_N = g^2/(g + a0): the spherical "
      "field equation, exactly", solg==[g**2/(g+a0)])
check("4c the odds of the two channels are g_N/g_B = x: TetA carries mu, TetB carries 1 - mu", sp.simplify((g**2/(g+a0))/gB-g/a0)==0)
check("4d in the two limits the throat dominates (g >> a0: g_B -> a0, the a0 tail) or the local field does (g << a0: g_B -> g, TetB "
      "carries almost all of it)", sp.limit(gB,g,sp.oo)==a0 and sp.limit(gB/g,g,0)==1)
check("4e the series law is a product rule: g g_B = a0 g_N (total field times TetB field equals a0 times the Newtonian field), "
      "equivalently g_B/g_N = a0/g = 1/x", sp.simplify(g*gB-a0*(g**2/(g+a0)))==0)
Nn=sp.symbols('N',positive=True); mq=sp.symbols('mq',positive=True)
lhs=Nn*sp.log((1-mq)*g); rhs=sp.log(a0)+sp.log(mq*g)+(Nn-2)*sp.log(g)
famlog=sp.log(g/a0)+Nn*sp.log(1-mq)-sp.log(mq)             # log of x (1 - mu)^N / mu
check("4f the archive's family x(1 - mu)^N = mu is the channel law g_B^N = a0 g_N g^(N - 2) (logs of the two differ by an identity): "
      "N = 1 is the series law above, and N = 2 (the bound law of Papers XI and XIII) is g_B = sqrt(a0 g_N), the geometric mean of the "
      "throat capacity and the Newtonian field",
      sp.simplify(sp.expand_log(lhs-rhs-famlog,force=True))==0)
check("4g the TetB field is always below the throat capacity, a0 - g_B = a0^2/(g + a0) > 0, so the enclosed TetB (phantom) mass "
      "M_B = r^2 g_B/G is bounded by an area law, M_B < a0 r^2/G; in the deep field g_B -> g = sqrt(G M a0)/r and M_B grows like r "
      "(the isothermal halo)", sp.simplify(a0-gB-a0**2/(g+a0))==0)
nu=lambda z: (1+sp.sqrt(1+4/z))/2
gNs=g**2/(g+a0)
check("4h the same law read the other way is QUMOND's: g = nu(g_N/a0) g_N with nu(z) = (1 + sqrt(1 + 4/z))/2. Vectorially, a channel along "
      "the total field is QUMOND's construction, so the throat picture generalises to QUMOND, while the SST is AQUAL; the two agree in "
      "spherical, cylindrical and planar symmetry", all(abs(float((nu(gNs/a0)*gNs-g).subs({g:gv,a0:1})))<1e-12 for gv in (0.01,0.5,1,3,250))
      and sp.simplify((1+4*a0*(g+a0)/g**2)-((g+2*a0)/g)**2)==0)
print(f"\n{sum(ok)}/{len(ok)} checks passed")
