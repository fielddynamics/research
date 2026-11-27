"""Reproduce the seven SVG figures (repository dark style) and machine-readable numerical tables."""
from pathlib import Path
import csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
from model import *
ROOT=Path(__file__).resolve().parent
FIG=ROOT/'figures';RES=ROOT/'results'; FIG.mkdir(exist_ok=True);RES.mkdir(exist_ok=True)
# Repository dark diagram palette (see ../make_figures.py and ../../diagrams/closure-hinge.svg)
NAVY='#eef5fb';TEAL='#59d4b5';BLUE='#78bdf0';GOLD='#d6a15e';GRAY='#b7c9d7';BG='none';SURF='#13283d';EDGE='#496075'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.labelcolor':NAVY,'axes.titlecolor':NAVY,'text.color':NAVY,'xtick.color':NAVY,'ytick.color':NAVY,'figure.facecolor':SURF,'savefig.facecolor':SURF,'axes.facecolor':BG,'svg.fonttype':'path','grid.color':'#26435a','legend.facecolor':'#1b3a52','legend.edgecolor':EDGE,'legend.labelcolor':NAVY,'axes.edgecolor':GRAY,'axes.spines.top':False,'axes.spines.right':False})
def dress(path):
    """Swap matplotlib's flat background for the repository frame: navy gradient, rounded border."""
    import re
    svg=path.read_text();w=float(re.search(r'width="([\d.]+)pt"',svg).group(1));h=float(re.search(r'height="([\d.]+)pt"',svg).group(1))
    frame=('<defs><linearGradient id="gpbg" x2="1" y2="1"><stop stop-color="#102237"/><stop offset="1" stop-color="#162f43"/></linearGradient></defs>'
           f'<rect x="0.75" y="0.75" width="{w-1.5:.2f}" height="{h-1.5:.2f}" rx="12" fill="url(#gpbg)" stroke="{EDGE}" stroke-width="1.2"/>')
    svg,n=re.subn(r'<g id="patch_1">\s*<path d="[^"]*"\s*style="fill: %s"\s*/>\s*</g>'%SURF,frame,svg,count=1)
    assert n==1,path
    path.write_text(svg)
def save(fig,name,subtitle):
    fig.text(.05,.025,subtitle,fontsize=9,color=GRAY,ha='left',va='bottom',wrap=True)
    fig.subplots_adjust(left=.09,right=.97,top=.79,bottom=.17,wspace=.35,hspace=.42)
    fig.savefig(FIG/f'{name}.svg');plt.close(fig);dress(FIG/f'{name}.svg')
def title(fig,head,sub):
    fig.text(.05,.965,head,fontsize=17,fontweight='bold',va='top');fig.text(.05,.915,sub,fontsize=10,color=GRAY,va='top')
def profile(ax,shape):
    if shape=='stepped':
        y=np.repeat(np.r_[0,1,4,4+np.arange(1,8)*11/7],2)[1:-1]; w=np.repeat(half_width((y[::2]+y[1::2])/2,shape),2)
    else:
        y=np.linspace(0,15,1201);w=half_width(y,shape)
    ax.fill_betweenx(y,-w,w,color=BLUE,alpha=.19);ax.plot(w,y,color=NAVY,lw=1.8);ax.plot(-w,y,color=NAVY,lw=1.8);ax.plot([-w[0],w[0]],[0,0],color=NAVY);ax.plot([-w[-1],w[-1]],[15,15],color=NAVY);ax.axvline(0,color=GRAY,ls=':',lw=1);ax.set(xlim=(-2.6,2.6),ylim=(-.4,15.5),aspect='equal',xlabel='Width (cubits)');ax.set_xticks([-2,0,2]);ax.set_yticks([0,1,4,15])
fig,axs=plt.subplots(1,4,figsize=(11,6));title(fig,'01  |  Geometry before interpretation','Normal-to-floor section; the corbels extend along the inclined gallery.')
for a,s,t in zip(axs,['stepped','smooth','equal_area','envelope'],['Seven-step model','Smooth equal-area','Equal-area rectangle','Bounding rectangle']):
    profile(a,s);a.set_title(t+f'\nA = {area(s)*CUBIT**2:.2f} m²',fontsize=10)
axs[0].set_ylabel('Normal height (cubits)');save(fig,'01_geometry','Survey-derived ideal proportions; equal course heights are a modelling choice. Controls are not actual monuments.')
# Gather outputs
rows=[]
for s in ['stepped','smooth','equal_area','envelope']:
    for r in ([1,2,3,4] if s=='stepped' else [2,3,4]):
        for p in ['even','odd']:
            ev,_=modes(s,r,p)
            for j,f in enumerate(cutoff(ev)): rows.append((s,r,p,j,float(ev[j]),float(f)))
with (RES/'cutoffs.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['geometry','refinement','parity','mode_index','lambda_per_cubit2','cutoff_hz']);w.writerows(rows)
fig,axs=plt.subplots(1,2,figsize=(11,5.2));title(fig,'02  |  Mode cutoffs and mesh refinement','The tall section supports low-frequency even modes; odd modes require substantially higher frequencies.')
for i,(s,label) in enumerate(zip(['stepped','smooth','equal_area','envelope'],['Seven steps','Smooth','Equal area','Envelope'])):
    e=cutoff(modes(s,4,'even')[0]);o=cutoff(modes(s,4,'odd')[0]);axs[0].scatter(e[:5],np.full(5,i)+.12,marker='o',color=TEAL,label='Even' if i==0 else None);axs[0].scatter(o[:4],np.full(4,i)-.12,marker='^',color=GOLD,label='Odd' if i==0 else None)
axs[0].set(yticks=range(4),yticklabels=['Seven steps','Smooth','Equal area','Envelope'],xlabel='Cutoff (Hz)',xlim=(-4,150));axs[0].invert_yaxis();axs[0].axvline(odd_bound(),ls='--',color=GRAY,lw=1);axs[0].legend(loc='lower right');axs[0].grid(axis='x',alpha=.25)
for p,col,idx in [('even',TEAL,1),('odd',GOLD,0)]:
    f=np.array([cutoff(modes('stepped',r,p)[0])[idx] for r in range(1,5)]);axs[1].plot(range(1,5),f-f[-1],marker='o',color=col,label=p.capitalize());
axs[1].set(xlabel='Mesh refinement multiplier',ylabel='Cutoff minus finest value (Hz)',xticks=[1,2,3,4]);axs[1].grid(alpha=.25);axs[1].legend();save(fig,'02_cutoffs','Mesh spacing = 1/(7r) cubit. Numerical convergence indicators, not certified continuum error bars.')
fig,axs=plt.subplots(1,4,figsize=(11,6));title(fig,'03  |  Transverse pressure modes','Computed on the seven-step section, reconstructed across the symmetry axis.')
x,y,mask,K,D,d=grid('stepped',4)
for ax,(p,j) in zip(axs,[('even',0),('even',1),('even',2),('odd',0)]):
    ev,v=modes('stepped',4,p);z=np.full(mask.shape,np.nan);z[mask]=v[:,j];full=np.c_[z[:,::-1]*(1 if p=='even' else -1),z];full/=np.nanmax(abs(full));ax.imshow(full,origin='lower',extent=(-2,2,0,15),vmin=-1,vmax=1,cmap='RdBu_r',interpolation='nearest');ax.set(xlabel='x (cubits)',xticks=[-2,0,2],yticks=[0,4,15]);ax.set_title(f'{p.capitalize()} {j}\n{cutoff(ev[j]):.2f} Hz',fontsize=11)
axs[0].set_ylabel('y (cubits)');save(fig,'03_modes','Red and blue denote opposite pressure phase, not field chambers. Eigenvector sign is arbitrary; constant mode has zero cutoff.')
fig,axs=plt.subplots(1,2,figsize=(11,5.1));title(fig,'04  |  Longitudinal array coherence','27 illustrative pair centres, alternating measured mean recess lengths.')
p,V=slots();freq=np.linspace(1,150,4000);k=2*np.pi*freq/C
for w,lab,col in [(np.ones(27),'Equal weights',BLUE),(V,'Alternating volume weights',TEAL)]:
    F=np.abs(array_factor(k,p,w)/sum(w))**2;axs[0].plot(freq,F,label=lab,color=col,lw=1.3);axs[1].plot(freq,F,label=lab,color=col,lw=1.3)
for a in axs:
    a.axvline(C/(2*1.67),color=GOLD,ls='--',lw=1);a.axvline(C/(4*1.67),color=GRAY,ls=':',lw=1);a.grid(alpha=.2);a.set(xlabel='Plane-mode frequency (Hz)',ylabel='Normalized array factor');
axs[0].set(xlim=(1,150),ylim=(0,1.04));axs[0].legend(fontsize=9);axs[1].set(xlim=(45,57),ylim=(0,.009));axs[1].set_title('Half-order detail');save(fig,'04_array','Array coherence is not measured reflectance. At the illustrated Bragg frequency the gallery already supports higher transverse modes.')
fig,axs=plt.subplots(1,2,figsize=(11,5.2));title(fig,'05  |  Passive impedance response','Plane-wave models, illustrative equal 1 m² external leads; no gain or frequency conversion.')
A=area()*CUBIT**2;ff=np.linspace(.01,20,2500);base=expansion_power(ff,L,A);T=[];R=[]
for f in ff:
    M=slot_chain(f,A,L,p,V);T.append(abs(scatter(M,1,1)[1,0])**2);R.append(abs(scatter(M,A,A)[0,0])**2)
axs[0].plot(ff,base,color=GRAY,label='No slots',lw=1.3);axs[0].plot(ff,T,color=TEAL,label='With lumped slots',lw=1.2);axs[0].set(xlabel='Frequency (Hz)',ylabel='Transmitted power',ylim=(0,1.05));axs[0].legend(fontsize=9)
axs[1].plot(ff,np.array(R)*100,color=TEAL,label='Illustrative array');axs[1].plot(ff,[100*shunt_reflection_bound(f,A,V) for f in ff],color=GOLD,ls='--',label='Any slot positions: upper bound');axs[1].set(xlabel='Frequency (Hz)',ylabel='Reflected power (%)');axs[1].legend(fontsize=9)
for a in axs:a.grid(alpha=.25)
save(fig,'05_transfer','Left: mismatch dominates an ideal expansion. Right: slot-only bound with matched gallery-area leads. Near cutoff, use multimode analysis.')
fig,ax=plt.subplots(figsize=(10,4.8));title(fig,'06  |  Keep the survey endpoints distinct','Petrie virtual horizontal run compared with the GP-1 predicted level and King’s Chamber floor.')
vals=[1688.9,ZSTAR/.0254,1692.55];labs=['Virtual horizontal floor run','GP-1 geometric height','King’s Chamber floor'];colors=[BLUE,TEAL,GOLD]
for i,(v,lab,col) in enumerate(zip(vals,labs,colors)):
    ax.scatter(v,i,s=110,c=col,zorder=5);ax.text(v+.3,i-.22,f'{v:.2f} in',va='center',fontsize=12,fontweight='bold',color=col)
ax.errorbar(vals[1],1,xerr=7*(1-1/np.sqrt(2)),color=TEAL,capsize=5,alpha=.7);ax.set(yticks=range(3),yticklabels=labs,xlim=(1686.5,1695.5),ylim=(-.6,2.6),xlabel='Inches');ax.invert_yaxis();ax.grid(axis='x',alpha=.25);fig.subplots_adjust(left=.32,right=.97,bottom=.19,top=.8);fig.text(.05,.03,'Height allowance propagated from ±7 in reconstruction; no uncertainty asserted for virtual run.\nThe physical model length is a separate 88-cubit ideal.',fontsize=9,color=GRAY);fig.savefig(FIG/'06_balance.svg');plt.close(fig);dress(FIG/'06_balance.svg')
fig,ax=plt.subplots(figsize=(11,5));title(fig,'07  |  A testable processing chain','Use the architecture to determine the input/output operators, not integer labels to prescribe them.')
ax.set_xlim(0,10);ax.set_ylim(0,5);ax.axis('off')
blocks=[(0.2,1.9,2.1,1.7,'Ascending passage','Input / load',GRAY),(2.8,1.9,2.1,1.7,'Grand Gallery','Mode selection\nphase delay',BLUE),(5.4,1.9,2.1,1.7,'Antechamber','Aperture scattering\nimpedance',GOLD),(8,1.9,1.8,1.7,'King’s Chamber','Resonant\nterminal',TEAL)]
for x0,y0,w,h,t,s,col in blocks:
    ax.add_patch(Rectangle((x0,y0),w,h,fc=col,alpha=.12,ec=col,lw=2));ax.text(x0+w/2,y0+h-.42,t,ha='center',fontweight='bold',color=col);ax.text(x0+w/2,y0+.49,s,ha='center',va='center',fontsize=10)
for x0 in [2.3,4.9,7.5]:ax.add_patch(FancyArrowPatch((x0,2.74),(x0+.5,2.74),arrowstyle='<->',mutation_scale=13,color=NAVY,lw=1.6))
ax.text(5,1.15,'Measure complex transfer functions • compare symmetric and antisymmetric drives',ha='center',fontsize=12);ax.text(5,.65,'GP-6 boundary response   →   GP-7 eigenmodes   →   GP-8 reciprocity   →   GP-9 selection',ha='center',fontsize=11,color=TEAL)
save(fig,'07_chain','Schematic acoustic hypothesis. The historical blocked passage, shafts, granite elasticity and losses require separate boundary conditions.')
# Numerical synopsis
M=moments();e=cutoff(modes('stepped',4,'even')[0]);o=cutoff(modes('stepped',4,'odd')[0]);freqs=C/(2*1.67)
with (RES/'summary.txt').open('w') as f:
    f.write(f'cubit_m={CUBIT:.9f}\narea_m2={A:.9f}\nlength_m={L:.9f}\nvolume_m3={A*L:.9f}\nslot_volume_proxy_m3={V.sum():.9f}\nfirst_even_hz={e[1]:.9f}\nfirst_odd_hz={o[0]:.9f}\nodd_lower_hz={odd_bound():.9f}\neven_upper_hz={cutoff(M[0]/(M[2]-M[1]**2/M[0])):.9f}\nodd_upper_hz={cutoff(M[0]/M[3]):.9f}\nFSR_hz={C/(2*L):.9f}\nBragg_hz={freqs:.9f}\nslots_only_R_upper_20Hz={shunt_reflection_bound(20,A,V):.12f}\nvirtual_run_minus_GP1_inches={(VIRTUAL_RUN-ZSTAR)/.0254:.9f}\n')
print('Generated 7 SVG figures and results tables')
