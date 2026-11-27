import numpy as np
from pathlib import Path
H=np.array([[(-1)**((a&b).bit_count()%2) for b in range(64)] for a in range(64)],dtype=np.int64)
g=[np.arange(1,4)*16,np.array([a for a in range(64) if a%16!=0 and a%4==0]),np.array([a for a in range(64) if a%4!=0])]
n=0
def check(c):
 global n
 assert c
 n+=1
check(np.array_equal(H@H,64*np.eye(64,dtype=int)))
check([len(a) for a in g]==[3,12,48])
for A in range(65):
 b=(np.arange(64)<A).astype(int); w=H@b
 check(w[0]==A)
 check(np.array_equal(H@w,64*b))
 check(sum(w[1:]**2)==64*A-A*A)
 for d in range(3):
  block=4**(2-d); a=b.reshape(-1,block).sum(axis=1)
  # projection energy = sum(block sums^2)/block; use integer scaling by 64
  ids=np.concatenate([np.array([0])]+g[:d+1]); prev=np.concatenate([np.array([0])]+g[:d])
  prevblock=4*block; ap=b.reshape(-1,prevblock).sum(axis=1)
  check(sum(w[ids]**2)==64//block*sum(a*a))
  check(sum(w[g[d]]**2)==64//block*sum(a*a)-64//prevblock*sum(ap*ap))
  if A% (4*block)==0: check(np.all(w[g[d]]==0))
 for k in [1,2]:
  wk=H@(b+k)
  check(wk[0]==A+64*k and np.array_equal(wk[1:],w[1:]))
# arbitrary aligned prefix blocks, not merely prefix fills
for d in range(4):
 size=4**(3-d)
 for i in range(4**d):
  b=np.zeros(64,dtype=int);b[i*size:(i+1)*size]=1;w=H@b
  check(all(np.all(w[a]==0) for a in g[d:]))
# rotation x -> omega*x on each digit, integer encoding 0,1,w,w^2
perm=[0,2,3,1]
r=np.array([sum(perm[(a>>k)&3]<<k for k in (0,2,4)) for a in range(64)])
for A in range(65):
 b=(np.arange(64)<A).astype(int); tw=b+b[r]+b[r[r]]
 check(np.array_equal(tw[r],tw))
 check(sum(tw)==3*A)
# 4-way local contrast counts for binary child occupancy
h=H[:4,:4]
for mask in range(16):
 b=np.array([(mask>>i)&1 for i in range(4)]);w=h@b; k=sum(b)
 check(np.count_nonzero(w[1:])==[0,3,1,3,0][k])
print(f'{n} exact integer assertions passed')
