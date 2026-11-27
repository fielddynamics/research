"""Regenerate all diagrams and ledger data. No external downloads."""
from pathlib import Path
import csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from sweep_engine import *
ROOT=Path(__file__).resolve().parent; FIG=ROOT/'figures'; OUT=ROOT/'outputs'
FIG.mkdir(exist_ok=True);OUT.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False,'axes.titleweight':'bold','figure.facecolor':'white','axes.facecolor':'white','svg.fonttype':'none','savefig.bbox':'tight','savefig.pad_inches':.2})
INK='#172d40'; BLUE='#28688a'; TEAL='#158477'; GOLD='#cf8b30'; GREY='#637887'; PALE='#e9f2f4'; RED='#ac4b43'
def save(fig,name):
    for ext in ('svg','png'):fig.savefig(FIG/f'{name}.{ext}',dpi=180)
    plt.close(fig)
def box(ax,xy,wh,head,body,fill=PALE):
    x,y=xy;w,h=wh;ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=.02,rounding_size=.04',facecolor=fill,edgecolor=BLUE,linewidth=1.2));ax.text(x+w/2,y+h*.71,head,ha='center',va='center',color=INK,weight='bold',fontsize=11);ax.text(x+w/2,y+h*.33,body,ha='center',va='center',color=INK,fontsize=9)
def arrow(ax,p,q):ax.add_patch(FancyArrowPatch(p,q,arrowstyle='-|>',color=GREY,mutation_scale=13,linewidth=1.5))
fig,ax=plt.subplots(figsize=(12,6.1));ax.set(xlim=(0,12),ylim=(0,6));ax.axis('off');ax.text(.15,5.7,'ONE CLOSURE ENGINE  /  FOUR DISTINCT MAPS',fontsize=18,weight='bold',color=INK);ax.text(.15,5.3,'Finite algebra is verified; the physical transduction arrows remain research targets.',color=GREY)
for x,head,body in [(0.2,'Inventory','TetA / TetB\nstanding-wave state'),(3.2,'Coherent ledger','64 address records\nπ first-visit scheduler'),(6.2,'Walsh read','Tree: 21 readers\nFWHT: 48 radix-4 reads'),(9.2,'Invariant register','22 common + contrasts\n42 rotating coordinates')]:box(ax,(x,3.7),(2.55,1.1),head,body)
for x in (2.75,5.75,8.75):arrow(ax,(x,4.25),(x+.43,4.25))
box(ax,(2.1,1.65),(3.3,1.12),'Logical read / reset','13 → 17 → 21\nthree ascending sweeps (hypothesis)');box(ax,(6.35,1.65),(3.3,1.12),'Settlement / registration','Common record + 21 innovations\nconditional determinant gain')
arrow(ax,(10.45,3.67),(8.0,2.8));arrow(ax,(5.4,2.21),(6.32,2.21));ax.plot([8.0,8.0,1.45,1.45],[1.63,.7,.7,3.65],ls='--',color=RED);ax.text(4.7,.35,'Next closure: retain or export previous information; physical coupling not established',ha='center',color=RED,fontsize=10);save(fig,'01_engine_map')
fig,ax=plt.subplots(figsize=(11,4.5));ax.set(xlim=(0,24),ylim=(0,5));ax.axis('off');ax.text(.2,4.7,'THREE SUB-READS OF THE 4 × 4 × 4 TREE',fontsize=16,weight='bold',color=INK)
for j,(title,count,detail) in enumerate([('Fine subchannels',16,48),('Intermediate subfaces',4,12),('Coarse faces',1,3)]):
    x=.35+j*7.7;box(ax,(x,1.75),(6.6,1.6),title,f'{count} four-port Walsh readers\n{detail} retained differences');
    if j<2:arrow(ax,(x+6.6,2.55),(x+7.55,2.55))
ax.text(.4,.9,'64 = 48 + 12 + 3 + 1 common scalar',weight='bold',fontsize=14,color=INK);ax.text(.4,.35,'Tree transform B is reversible. Full FWHT = D B, where D mixes only retained detail strata.',color=GREY);save(fig,'02_recursive_tree')
fig,ax=plt.subplots(figsize=(10.8,4.5)); common=set.intersection(*(support(u) for u in (3,5,6)));groups=[sorted(common)]+[sorted(support(u)-common) for u in (3,5,6)];ax.set(xlim=(0,22),ylim=(-.2,4.2));ax.axis('off');ax.text(.2,3.85,'DAUGHTER MASKS: EXACT CUMULATIVE REGISTER RANK',fontsize=16,weight='bold',color=INK);ax.text(.2,3.45,'Common seed removed: 9 shared contrasts + 4 unique per daughter normal',color=GREY)
colors=[GREY,BLUE,TEAL,GOLD];widths=[9,4,4,4]
for i in range(3):
    start=.2
    for j,w in enumerate(widths):
        if j<=i+1:ax.barh(2.75-i*.8,w-.08,left=start,height=.52,color=colors[j]);ax.text(start+w/2,2.75-i*.8,str(w),ha='center',va='center',color='white',weight='bold')
        start+=w
    ax.text(21.6,2.75-i*.8,str([13,17,21][i]),va='center',weight='bold',color=INK)
ax.text(.2,.05,'Q₃ → Q₃ ∪ Q₅ → Q₃ ∪ Q₅ ∪ Q₆   |   3 ⊕ 5 ⊕ 6 = 0',color=INK,fontsize=12);save(fig,'03_mask_rank')
digits=certified_octal();rows=pi_ledger(digits);inv=read_innovations(rows);steps=[x['step'] for x in rows]
fig,ax=plt.subplots(figsize=(11,5));
for i,color in zip((1,2,3),(BLUE,TEAL,GOLD)):ax.step(steps,[x[f'bank{i}'] for x in rows],where='post',label=f'Orbit-member bank {i}',color=color,lw=2)
ax.step(steps,[np.trace(L) for _,d,L in inv],where='post',color=GREY,ls='--',label='Known-mean contrast rank',lw=1.5)
for n,label in zip([104,156,192,332],['rank 21 inferred','bank 1 complete','bank 2 complete','bank 3 complete']):ax.axvline(n,color='#b0b8bf',lw=1,ls=':');ax.text(n-3,2,label,rotation=90,ha='right',va='bottom',fontsize=9,color=INK)
ax.set(xlim=(0,338),ylim=(0,23),xlabel='Fractional octal transitions (integer digit = step 0)',ylabel='Filled nonzero-orbit slots / rank',title='π ledger: three interleaved banks, not three disjoint time intervals');ax.legend(loc='lower right',frameon=False);ax.grid(alpha=.15);save(fig,'04_pi_banks')
fig,ax=plt.subplots(figsize=(10.5,4.2));
for i in range(3):
    t=np.linspace(i,i+1,200,endpoint=False);ax.plot(t,17-4*np.cos(np.pi*(t-i)),color=BLUE,lw=2.6);ax.plot([i+1,i+1],[13,21],color=RED,ls='--',lw=1.5);ax.text(i+.5,21.65,f'Sweep {i+1}',ha='center',color=INK,weight='bold')
ax.scatter([0,1,2,3],[13]*4,color=TEAL,zorder=4);ax.set(yticks=[13,17,21],xticks=[0,1,2,3],xticklabels=['Start','Reset 1','Reset 2','Reset 3'],ylim=(11.7,22.6),xlabel='Illustrative normalized phase — not calibrated to π steps',ylabel='Signed trace',title='Current working hypothesis: ascend, commit, immediately reset');ax.grid(axis='y',alpha=.2);save(fig,'05_immediate_reset')
fig,ax=plt.subplots(figsize=(10.8,4.5));ax.set(xlim=(0,64),ylim=(-.3,4.2));ax.axis('off');ax.text(.1,3.85,'64 RECORDS: INFORMATION-PRESERVING ORBIT READ',fontsize=16,weight='bold',color=INK);ax.text(.1,3.4,'One fixed record + 21 triples, each resolved into mean and two quadratures',color=GREY)
ax.barh(2.65,1,height=.55,color=GREY);ax.barh(2.65,63,left=1,height=.55,color=BLUE);ax.text(32,2.65,'21 × 3 orbit members',ha='center',va='center',color='white',weight='bold');ax.text(.6,3.02,'fixed',fontsize=8,ha='left');
ax.barh(1.6,22,height=.65,color=TEAL);ax.barh(1.6,42,left=22,height=.65,color=GOLD);ax.text(11,1.6,'22 invariant',ha='center',va='center',color='white',weight='bold');ax.text(43,1.6,'42 rotating contrasts',ha='center',va='center',color='white',weight='bold');
ax.barh(.58,1,height=.5,color=GREY);ax.barh(.58,21,left=1,height=.5,color=TEAL);ax.text(11.5,.58,'21 contrasts',ha='center',va='center',color='white',weight='bold');ax.text(23,.58,'+ retain 42 if full reconstruction is required',va='center',color=INK);save(fig,'06_orbit_fourier')
fig,ax=plt.subplots(figsize=(10.4,4.6));n=np.arange(7);labels=['1','4','16','13','17','21','273'];values=[1,4,16,13,17,21,273];ax.bar(n[:3],values[:3],color=TEAL);ax.bar(n[3:6],values[3:6],color=BLUE);ax.set(xticks=n[:6],xticklabels=['grade 1','grade 2','grade 3','TetB trace','Origin trace','TetA trace'],ylim=(0,25),ylabel='Dimension / trace',title='Proof 26: 1 + 4 + 16 is the grade flag; 13 / 17 / 21 are signed traces');
for i,v in enumerate(values[:6]):ax.text(i,v+.5,str(v),ha='center',weight='bold',color=INK)
ax.text(.01,-.23,'The 9 + 4 + 4 + 4 mask partition is a different decomposition. Equal counts do not identify operators.',transform=ax.transAxes,color=GREY);save(fig,'07_signed_flag')
fig,ax=plt.subplots(figsize=(10.4,4.6));first=np.full((8,8),-1);counts=np.zeros((8,8),int)
for z in rows:
 a,b=z['a'],z['b'];counts[a,b]+=1
 if z['new']:first[a,b]=z['step']
im=ax.imshow(first,cmap='viridis');ax.set(xlabel='Next vertex b',ylabel='Previous vertex a',xticks=range(8),yticks=range(8),title='π schedule: first appearance of every ordered address');
for a,b in product(range(8),repeat=2):ax.text(b,a,first[a,b],ha='center',va='center',color='white' if first[a,b]<180 else 'black',fontsize=8)
fig.colorbar(im,ax=ax,label='First-visit transition');save(fig,'08_pi_first_visit')
with (OUT/'pi_step_ledger.csv').open('w',newline='') as fcsv:
    w=csv.DictWriter(fcsv,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
with (OUT/'running_settlement.csv').open('w',newline='') as fcsv:
    w=csv.writer(fcsv);w.writerow(['step','innovation_rank','resolved_rank']);w.writerows((n,round(np.trace(d)),round(np.trace(L))) for n,d,L in inv)
(OUT/'certified_octal_pi.txt').write_text(digits[0]+'.'+digits[1:]+'\n')
with (OUT/'mask_membership.csv').open('w',newline='') as fcsv:
    w=csv.writer(fcsv);w.writerow(['orbit','members','Q3','Q5','Q6']);w.writerows([i,str(o),*(int(i in support(u)) for u in (3,5,6))] for i,o in enumerate(ORBITS))
print('Base figures and ledgers regenerated.')

fig,ax=plt.subplots(figsize=(12,6.8));ax.set(xlim=(0,12),ylim=(0,7));ax.axis('off')
ax.text(.25,6.68,'THREE SWEEPS  /  ONE COUPLING POLYNOMIAL',fontsize=19,weight='bold',color=INK)
ax.text(.25,6.24,'Chronological depth is the working theory; structural counts are exact in the model.',fontsize=10,color=GREY)
for i,(head,term,body,col) in enumerate([('Face','1','1 reader → 4 faces',BLUE),('Channel','sK','4 readers → 16 channels',TEAL),('Subchannel','K²','16 readers → 64 subchannels',GOLD)]):
    x=.3+4*i;box(ax,(x,4.3),(3.4,1.45),f'Sweep {i+1} · {head}',body)
    ax.text(x+1.7,3.92,term,ha='center',fontsize=19,weight='bold',color=col)
    ax.plot([x+.32,x+1.7,x+3.05],[2.55,2.95,3.35],color=col,lw=2.8)
    for xx,yy,v in [(x+.32,2.55,13),(x+1.7,2.95,17),(x+3.05,3.35,21)]:ax.text(xx,yy+.14,str(v),ha='center',fontsize=10,color=INK,weight='bold')
    ax.plot([x+3.05,x+3.05],[3.35,2.55],ls='--',color=RED,lw=1.4)
    if i<2:arrow(ax,(x+3.44,5.02),(x+3.97,5.02))
ax.text(6,2.07,'Every sweep uses the full character:  f(4,s) = 1 + 4s + 16',ha='center',fontsize=15,weight='bold',color=INK)
ax.text(6,1.65,'Only the middle term changes:  −4 → 0 → +4    |    immediate reset, retained record',ha='center',fontsize=11,color=GREY)
box(ax,(3.2,.28),(5.6,.92),'One complete closure snapshot','Register / settle → next closure')
arrow(ax,(6,1.48),(6,1.23));save(fig,'09_three_pass_polynomial')
print('9 figures, 18 image files, 4 ledgers regenerated.')
