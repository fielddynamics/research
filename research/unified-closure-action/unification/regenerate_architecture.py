from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle,FancyBboxPatch
p=Path(__file__).resolve().parent
plt.rcParams.update({'font.size':11,'font.family':'DejaVu Sans'})
def save(fig,name):
    for ext in ['svg','png']:fig.savefig(p/f'{name}.{ext}',dpi=180,bbox_inches='tight',facecolor='white')
    plt.close(fig)
fig,ax=plt.subplots(figsize=(8,5));ax.set_aspect('equal');ax.axis('off');ax.set_xlim(-1.2,3.7);ax.set_ylim(-1.25,1.25)
for r,c,lab,y in [(1.07,'#d97706','16 invariant subchannel contrasts',.91),(.77,'#0d9488','4 invariant subface contrasts',.40),(.45,'#3182ce','1 invariant face contrast',-.12),(.14,'#334155','1 conserved scalar',-.75)]:
    ax.add_patch(Circle((0,0),r,facecolor=c,alpha=.13,edgecolor=c,lw=2));ax.annotate(lab,xy=(r*.66,r*.68 if r>.2 else 0),xytext=(1.35,y),arrowprops=dict(arrowstyle='-',color=c),color=c,va='center')
ax.set_title('Weighted three-grade closure',fontweight='bold');save(fig,'12_three_grade_closure')
def box(ax,x,y,w,h,txt,c='#334155'):
    ax.add_patch(FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle='round,pad=.05',facecolor='white',edgecolor=c,lw=1.6));ax.text(x,y,txt,ha='center',va='center',color=c,fontsize=10)
def arrow(ax,x1,y1,x2,y2):ax.annotate('',(x2,y2),(x1,y1),arrowprops={'arrowstyle':'->','color':'#64748b','lw':1.5})
fig,ax=plt.subplots(figsize=(8,5));ax.set_xlim(0,10);ax.set_ylim(0,8);ax.axis('off');box(ax,5,7,5,1,'Common odds coordinate: r = μ/(1−μ)');box(ax,2.5,4.8,4.3,1.2,'Drained: x = r\nμ = x/(1+x)','#3182ce');box(ax,7.5,4.8,4.3,1.2,'Internal bound: x = r(1+r)\nx(1−μ)² = μ','#d97706');arrow(ax,4.5,6.45,2.5,5.45);arrow(ax,5.5,6.45,7.5,5.45);box(ax,5,2.5,7.4,1.2,'Common generating prescription\nF(y) = sup [μy − V(μ)]');arrow(ax,2.5,4.15,4.1,3.15);arrow(ax,7.5,4.15,5.9,3.15);box(ax,5,.6,7.4,.8,'Distinct physical regime selection remains to be derived','#64748b');arrow(ax,5,1.85,5,1.05);save(fig,'13_common_generator')
fig,ax=plt.subplots(figsize=(9,7));ax.set_xlim(0,10);ax.set_ylim(0,11);ax.axis('off');box(ax,5,10,8,1,'Dual-tetrad cell and H36 vortex dynamics');box(ax,5,8.4,8,1,'64-address ledger and weighted three-cycle read');arrow(ax,5,9.45,5,8.95);box(ax,2.6,6.5,4.4,1.2,'Conserved boundary scalar\nRecursive source registration','#3182ce');box(ax,7.4,6.5,4.4,1.2,'21 invariant contrasts\nConditional collective attenuation','#d97706');arrow(ax,4.5,7.85,2.6,7.15);arrow(ax,5.5,7.85,7.4,7.15);box(ax,5,4.5,8,1.1,'Response and stiffness\nOdds potential + conditional G normalization');arrow(ax,2.6,5.85,4,5.1);arrow(ax,7.4,5.85,6,5.1);box(ax,5,2.8,8,1,'Static gravity: recursive boundary action\nInternal bound response: separate regime');arrow(ax,5,3.9,5,3.35);box(ax,5,.8,8,1.3,'OPEN: native attenuation and charge,\ncausal covariant tensor dynamics, independent scales','#64748b');arrow(ax,5,2.25,5,1.5);save(fig,'14_unified_architecture')
