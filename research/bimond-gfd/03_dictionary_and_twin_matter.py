"""03. Dictionary BIMOND (alpha = -beta = -1) <-> GFD, and what twin matter does to the decoded mass.
phi*  = phi - phihat : Newtonian potential of (rho - rhohat)            <-> TetA, the source field
phihat               : grad phihat = -M' grad phi* (+ twin Newtonian)   <-> TetB field (phantom), |.| <= a0
phi   = phi* + ...   : what matter follows (and light, gamma = 1)       <-> TetA + TetB total
rhohat (twin matter) : negative active mass for phi*                    <-> occupied TetB (the drain / throat)"""
import sympy as sp, sys
ok_all=True
def ok(m,c):
    global ok_all; ok_all&=bool(c); print(("PASS " if c else "FAIL ")+m)
a0,G,r=sp.symbols('a0 G r',positive=True); M,Mh=sp.symbols('M Mhat',positive=True)
Mp=lambda s: sp.Rational(-1,2)+sp.sqrt(sp.Rational(1,4)+a0/s)          # M'(z) written in s = |g*| (s > 0)
gst=G*(M-Mh)/r**2                                                       # g* = g_s - ghat_s
gt=(1+Mp(gst))*gst                                                      # physical acceleration (for M > Mhat)
B=gt-gst
ok("TetB field B = g - g* = a0 g_t/(a0+g_t) = (1-mu) g_t, bounded by a0", sp.simplify(B-a0*gt/(a0+gt))==0)
ok("cross term: (grad phi)^2 - (grad phihat)^2 = |grad phi*|^2 + 2 grad phi*.grad phihat (the TetA-TetB coupling from alpha = -beta)",
   sp.expand((sp.Symbol('a')+sp.Symbol('b'))**2-sp.Symbol('b')**2-sp.Symbol('a')**2-2*sp.Symbol('a')*sp.Symbol('b'))==0)
# the decoding-mass letter's M_dec = r^2 g_s/G with g_s from the GFD spherical law applied to the observed g_t
Mdec=r**2*(gt**2/(a0+gt))/G
ok("decoding theorem: M_dec = M - Mhat exactly, at every radius, so Delta M_eff = M_phot - M_dec = Mhat (enclosed twin/TetB mass)",
   sp.simplify(Mdec-(M-Mh))==0)
print("   -> with rhohat >= 0 an isolated galaxy can only be braked (M_dec <= M_phot); a 'drive' must come from the environment")
print("      (the host's net field) or from rhohat < 0.  CamB (M_dec < M_phot) is a brake: an occupied TetB of mass Delta M_eff.")
# twin-dominated interior: g* < 0 -> repulsion (Milgrom 2010: TM's phantom mass repels both kinds)
ok("if Mhat > M inside r, g* < 0: matter is repelled (Milgrom's 'TM phantom mass is repulsive')", sp.simplify(gst.subs(Mh,2*M))<0)
# deep Newtonian regime: twin and ordinary matter decouple apart from Newtonian -G Mhat/r^2 in phi*
ok("strong-field regime (g* >> a0): M' g* -> a0, a constant TetB tail (not zero) around every source in BIMOND as written",
   sp.limit(Mp(sp.Symbol('s',positive=True))*sp.Symbol('s',positive=True)/a0,sp.Symbol('s',positive=True),sp.oo)==1)
print("   (that tail is what the solar system excludes; removed only by the net-field rule, see 05)")
sys.exit(0 if ok_all else 1)
