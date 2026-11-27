import itertools as it
import sympy as s
import numpy as np
n=0
def check(label,x):
 global n
 assert x,label
 n+=1; print('PASS',label)
K,t,a,b,z=s.symbols('K t a b z', real=True)
I=lambda m:s.eye(m)
L=s.Matrix([[1,0],[z,1]])
Ss=[I(1),s.kronecker_product(L,L),s.kronecker_product(L,L,L,L)]
for j,S in enumerate(Ss):
 check(f'level {j} trace',s.trace(S)==4**j)
 check(f'level {j} determinant',S.det()==1)
 check(f'level {j} support',sum(x!=0 for x in S)==9**j)
 check(f'level {j} scalar gain determinant',(t*S).det()==t**(4**j))
 check(f'level {j} inverse sign',S.inv()==S.subs(z,-z))
check('capacity',sum(S.rows**2 for S in Ss)==273)
check('support',sum(sum(x!=0 for x in S) for S in Ss)==91)
check('trace',sum(s.trace(S) for S in Ss)==21)
check('root parity trace',sum((-1)**j*s.trace(S) for j,S in enumerate(Ss))==13)
check('root even trace',sum(s.trace(S) for j,S in enumerate(Ss) if j%2==0)==17)
check('capacity relation',s.expand((1+K+K**2)*(1-K+K**2)-(1+K**2+K**4))==0)
check('center average not zero-branch',(1+K**2)!=1)
# construct exact detail basis per node using Hadamard signs and integer entries;
# uniform block over suffixes. Distinct columns orthogonal; rotation permutes them.
h=s.Matrix([[1,1,1,1],[1,1,-1,-1],[1,-1,1,-1],[1,-1,-1,1]])
words=list(it.product(range(4),repeat=3)); ix={w:i for i,w in enumerate(words)}
rot=lambda x: (0,2,3,1)[x]
P=s.zeros(64)
for i,w in enumerate(words):P[ix[tuple(map(rot,w))],i]=1
Q=(I(64)+P+P**2)/3
check('C3 projector',Q*Q==Q)
check('invariant total',s.trace(Q)==22)
D=[]
for depth in range(3):
 cols=[]
 for p in it.product(range(4),repeat=depth):
  for j in range(1,4):
   cols.append(s.Matrix([h[w[depth],j] if w[:depth]==p else 0 for w in words]))
 C=s.Matrix.hstack(*cols); Dk=C*C.T/(4**(3-depth)); D.append(Dk)
 check(f'detail {depth} projection',Dk*Dk==Dk)
 check(f'detail {depth} equivariance',P*Dk==Dk*P)
 check(f'detail {depth} rank',s.trace(Dk)==3*4**depth)
 check(f'detail {depth} invariant rank',s.trace(Q*Dk)==4**depth)
 for d in D[:-1]:check(f'detail {depth} orthogonal previous',d*Dk==s.zeros(64))
E=s.ones(64)/64
check('complete tree decomposition',sum(D,E)==I(64))
# local contrast map preserving common and all S4 labels
P0=s.ones(4)/4; Pc=I(4)-P0; A=P0+t*Pc
check('common preserved',A*s.ones(4,1)==s.ones(4,1))
for p in it.permutations(range(4)):
 U=s.zeros(4)
 for j,k in enumerate(p):U[k,j]=1
 check('S4 commute '+str(p),U*A==A*U)
check('local determinant',s.factor(A.det())==t**3)
check('physical amplitude free',A.subs(t,s.Rational(1,2))!=A.subs(t,s.Rational(1,3)))
check('composition',s.simplify(A*A.subs(t,a)-A.subs(t,a*t))==s.zeros(4))
# a full tensor of the elementary four-way map has different exponents
check('tensor replicate determinant exponent',3*1*4**0+3*2*4**1==27)
check('scalar four-way tensor replication exponent',4+2*16==36)
# explicit two-chamber orthogonal coupling with arbitrary rational cosine/sine
for u,v in [(s.Rational(3,5),s.Rational(4,5)),(s.Rational(5,13),s.Rational(12,13))]:
 W=s.BlockMatrix([[P0+u*Pc,-v*Pc],[v*Pc,P0+u*Pc]]).as_explicit()
 check('paired chamber lossless '+str(u),W.T*W==I(8))
 check('paired chamber retained '+str(u),W[:4,:4]==A.subs(t,u))
 check('paired chamber complement '+str(u),W[4:,:4].T*W[4:,:4]==(1-u*u)*Pc)
# determinant on invariant contrast by exact trace ranks and numerical actual operators
Qn=np.array(Q,float); e,V=np.linalg.eigh(Qn-np.array(E,float)); V=V[:,e>.5]
check('invariant contrast frame',V.shape==(64,21))
for ts in [(0.3,0.3,0.3),(0.7,0.5,0.9),(0.12,0.33,0.88)]:
 J=np.eye(64)
 for g,d in zip(ts,D):J=(np.eye(64)+(g-1)*np.array(d,float))@J
 logdet=np.linalg.slogdet(V.T@J@V)[1]
 expected=sum(4**i*np.log(g) for i,g in enumerate(ts))
 check('actual invariant determinant '+str(ts),abs(logdet-expected)<1e-10)
 check('scalar unchanged '+str(ts),np.allclose(J@np.ones(64),np.ones(64)))
print(f'{n} assertions passed')
