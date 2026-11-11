"""04. Prediction from 03: an isolated galaxy can only be braked, M_dec <= M_phot (twin/TetB mass >= 0).
Per galaxy: ratio = M_dec/M_bar = g_s,inferred / g_bar with g_s,inferred = g_obs^2/(a0 + g_obs) (GFD inversion), outer half of points.
Data: SPARC RAR (cached CSV, flat Upsilon = 0.5/0.7, minimal pipeline: 0.18 dex point scatter, so only the distribution's skew is testable)."""
import numpy as np, csv
a0=1.2e-10
T={}
for line in open('../../papers/07-dual-tetrad-topology-field-origin/v7/python/sparc_tully_fisher_table.dat'):
    p=line.split()
    if len(p)>17: T[p[0]]=dict(Q=int(p[17]),inc=float(p[5]))
pts={}
for r in csv.DictReader(open('../../papers/letter-radial-acceleration-relation-sparc/supplementary/sparc_rar.csv')):
    gb=float(r['g_bar_ms2']); go=float(r['g_obs_ms2']); pts.setdefault(r['galaxy'],[]).append((gb,go))
def run(sel,lab):
    L=[]
    for g,ps in pts.items():
        if g not in T or not sel(T[g]) or len(ps)<4: continue
        ps=sorted(ps,key=lambda t:-t[0])[len(ps)//2:]          # outer half (lowest g_bar)
        L.append(np.median([np.log10((go**2/(a0+go))/gb) for gb,go in ps]))
    L=np.array(L)
    print(f"{lab:26s} N={len(L):3d}  median log10(M_dec/M_bar) = {np.median(L):+.3f}  mean {L.mean():+.3f}"
          f"  frac > +0.1 dex: {np.mean(L>0.1):.2f}   frac < -0.1 dex: {np.mean(L<-0.1):.2f}")
    return L
run(lambda d: True,"all")
run(lambda d: d['Q']==1 and d['inc']>=45,"Q=1, inc>=45")
print("brake-only (rhohat >= 0) predicts the distribution sits at or below 0 with a tail toward negative values;")
print("an excess of drives (> +0.1 dex) in isolated galaxies would need rhohat < 0, an environmental drive, or a higher Upsilon.")
