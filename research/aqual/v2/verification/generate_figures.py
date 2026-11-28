from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch
import numpy as np
from aqual import *
OUT=Path(__file__).resolve().parents[1]/'figures';OUT.mkdir(exist_ok=True)
plt.rcParams.update({'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'white','axes.titleweight':'bold','savefig.bbox':'tight'})
blue='#216a91';teal='#168579';gold='#c17b32';purple='#7559a3';ink='#233746'
def save(fig,name):
    fig.savefig(OUT/(name+'.svg'));fig.savefig(OUT/(name+'.png'),dpi=160);plt.close(fig)
def plot(title,xlabel,ylabel):
    fig,ax=plt.subplots(figsize=(8,4.5),layout='constrained');ax.set(title=title,xlabel=xlabel,ylabel=ylabel);ax.grid(alpha=.18);return fig,ax
def flow(title,items,name):
    fig,ax=plt.subplots(figsize=(10,2.9));ax.set(xlim=(0,len(items)),ylim=(0,1));ax.axis('off');ax.set_title(title,pad=15)
    for i,(head,body) in enumerate(items):
        col=[blue,teal,purple,gold][i%4];ax.add_patch(FancyBboxPatch((i+.08,.24),.82,.52,boxstyle='round,pad=.025',facecolor=col+'18',edgecolor=col,lw=1.5));ax.text(i+.49,.61,head,ha='center',va='center',weight='bold',color=col,fontsize=11);ax.text(i+.49,.41,body,ha='center',va='center',fontsize=10,color=ink)
        if i<len(items)-1:ax.annotate('',(i+1.07,.5),(i+.92,.5),arrowprops=dict(arrowstyle='->',color=ink,lw=1.3))
    save(fig,name)
flow('From structural partition to registered gravity',[('Geometry','1 + sK + K²\n13 / 17 / 21'),('Constitutive law','μ = x/(1+x)\nexchange'),('Energy','F′(y) = μ(√y)\nvariation'),('NET field','ownership split\nAQUAL + Poisson'),('Registration','boundary data\nnext closure')],'01_architecture')
x=np.logspace(-3,3,500)
fig,ax=plot('Complementary shares and continuous capacity','Total acceleration x = g/a₀','Share');ax.semilogx(x,mu(x),color=blue,label='TetA share μ');ax.semilogx(x,1-mu(x),color=teal,label='TetB share 1−μ');ax.axvline(1,ls=':',color=ink);ax.legend(loc='center left');t=ax.twinx();t.semilogx(x,capacity(x),color=gold,ls='--',label='C = 13 + 8μ');t.set(ylabel='Capacity C',yticks=[13,17,21],ylim=(13,21));t.legend(loc='center right');save(fig,'02_partition')
fig,ax=plot('Deep-field energy: cancellation, not logarithmic dominance','x = √y','Magnitude');x=np.logspace(-4,1,450);ax.loglog(x,x*x,label='y',color=blue);ax.loglog(x,2*x,label='|−2√y|',color=teal);ax.loglog(x,2*np.log1p(x),label='2 ln(1+√y)',color=gold,ls='--');ax.loglog(x,energy(x*x),label='Full F(y)',color=purple,lw=3);ax.loglog(x,2*x**3/3,label='Deep asymptote ⅔x³',color=ink,ls=':');ax.legend(ncol=2);save(fig,'03_energy')
x=np.logspace(-3,3,500);fig,ax=plot('The AQUAL current response','x','Dimensionless eigenvalue');ax.semilogx(x,mu(x),label='Transverse μ',color=blue);ax.semilogx(x,x*(x+2)/(1+x)**2,label='Longitudinal μ+xμ′',color=teal);ax.semilogx(x,2-mu(x),label='Anisotropy ratio 2−μ',color=purple,ls='--');ax.legend();save(fig,'04_response')
z=np.logspace(-6,3,500);fig,ax=plot('Spherical-static radial acceleration relation','Source acceleration gₛ/a₀','Total acceleration gₜ/a₀');ax.loglog(z,total(z),label='Simple-law prediction',color=blue,lw=2.5);ax.loglog(z,z,label='Newtonian',color=ink,ls='--');ax.loglog(z,np.sqrt(z),label='Deep-field limit',color=teal,ls=':');ax.legend();save(fig,'05_radial_relation')
fig,ax=plot('Ownership split: the child residual is Newtonian','Position (schematic)','Potential (arbitrary units)');r=np.linspace(-3,3,600);host=.22*r+.055*r*r;res=-.9*np.maximum(1-r*r,0)**2;ax.plot(r,host,color=teal,label='Parent mountain Φ̄');ax.plot(r,host+res,color=blue,lw=2.5,label='Total Φ = Φ̄ + δ');ax.plot(r,res,color=purple,ls='--',label='Owned residual δ');ax.axvspan(-1,1,color=blue,alpha=.07);ax.axvline(-1,color=ink,ls=':');ax.axvline(1,color=ink,ls=':');ax.legend();ax.text(0,-.58,'closure envelope',ha='center');save(fig,'06_mountain')
flow('Closure of closures: preserve the registered child contribution',[('Local body','internal settlement\nboundary data'),('Star system','owned residual\n+ parent field'),('Galaxy','drained net field\nregister locally'),('Cluster','compose children\nnonlinear case open')],'07_hierarchy')
r=np.logspace(-2,3,450);fig,ax=plot('Point mass: two limits and the equal-share ring','r / rM','v² / √(GMa₀)');ax.loglog(r,r*point_mass(r),color=blue,label='AQUAL spherical');ax.loglog(r,1/r,color=ink,ls='--',label='Newtonian');ax.axhline(1,color=teal,ls=':',label='Flat-curve limit');ax.axvline(1,color=gold,ls=':');ax.axvline(np.sqrt(2),color=purple,ls=':');ax.legend();ax.text(.97,8,'rM',rotation=90,ha='right',color=gold);ax.text(1.49,8,'√2 rM',rotation=90,color=purple);save(fig,'08_point_mass')
fig,ax=plot('Legendre dual: the conjugate read','Dimensionless input','Energy');x=np.linspace(0,3,400);z=source(x);ax.plot(x,energy(x*x),label='F(x²)',color=blue);ax.plot(z,dual(z),label='Q(z²)',color=teal);ax.plot(z,dual(z)-z*z,label='Interaction M(z²)',color=purple);ax.legend();save(fig,'09_duality')
flow('Conditional READ → SETTLE → REGISTER bridge',[('READ','Walsh gradient\np = ∇Φ'),('SETTLE','vacancy cost W\nq* = p/(1+x)'),('ELIMINATE','|p|²/2 − L*\n= a₀² F/2'),('REGISTER','torsion response\ncurrent J = p−q')],'10_settlement')
