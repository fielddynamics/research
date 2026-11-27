from pathlib import Path
import json
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap,BoundaryNorm
import numpy as np
p=Path(__file__).parent
V=np.array(json.loads((p/'pencil_incidence.json').read_text())['punctured_intersections'])
fig,ax=plt.subplots(figsize=(10,6.4));fig.subplots_adjust(left=.12,right=.96,top=.79,bottom=.16)
cmap=ListedColormap(['#e8eef4','#9ec5da','#dfa34c','#b55b27']);norm=BoundaryNorm([-.5,.5,2.5,4.5,5.5],4)
ax.imshow(V,aspect='auto',cmap=cmap,norm=norm)
for i in range(17):
 for j in range(13):ax.text(j,i,str(V[i,j]),ha='center',va='center',fontsize=9,color='#ffffff' if V[i,j]==5 else '#17334a')
ax.set_xticks(range(13),['P sector']+[str(i) for i in range(1,13)],rotation=0,fontsize=8);ax.set_yticks(range(17),[str(i+1) for i in range(17)],fontsize=8);ax.set_xlabel('13 Baer sectors (one has 20 points; twelve have 21)',labelpad=10);ax.set_ylabel('17 punctured lines (16 points each)');ax.set_xticks(np.arange(-.5,13,1),minor=True);ax.set_yticks(np.arange(-.5,17,1),minor=True);ax.grid(which='minor',color='white',linewidth=.7);ax.tick_params(which='minor',bottom=False,left=False);ax.axhline(4.5,color='#17334a',linewidth=2);ax.axvline(.5,color='#17334a',linewidth=2)
fig.text(.12,.94,'Origin-centred projective incidence',fontsize=20,weight='bold',color='#17334a');fig.text(.12,.89,'Actual GF(16) enumeration: 272 points, two distinct partitions',fontsize=11,color='#45627a');fig.text(.12,.055,'Each row totals 16. Each external sector has one five-point secant. Rank ratio = 17/13.',fontsize=10,color='#17334a')
for ext in ('png','svg'):fig.savefig(p/'figures'/f'projective_pencil.{ext}',dpi=180)
