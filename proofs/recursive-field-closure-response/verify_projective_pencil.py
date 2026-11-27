"""Revision 3 exact incidence tests. Builds PG(2,16) in the archived F4 tower.
The inherited finite-field builder is executed silently, then its actual cosets
are used; all assertions below are counted separately from inherited checks.
"""
from pathlib import Path
import runpy,contextlib,io
from collections import Counter
from fractions import Fraction as F
import numpy as np
import sympy as s
with contextlib.redirect_stdout(io.StringIO()):
    src=runpy.run_path(str(Path(__file__).parent/'sources/verify_projective_bridge.py'))
m4, digs, canon, norm, project = (src[k] for k in ['m4','digs','canon','norm','project'])
Q,blocks,pairs,points= (src[k] for k in ['Q','blocks','pairs','points'])
n=0
def ck(label,val):
    global n
    assert bool(val),label
    n+=1;print('PASS',label)
# encode a+b theta in GF16, theta^2=theta+w
mul=np.zeros((16,16),dtype=np.int64)
for x in range(16):
 for y in range(16):
    a,b=x%4,x//4;c,d=y%4,y//4;bd=m4(b,d)
    mul[x,y]=(m4(a,c)^m4(2,bd))+4*(m4(a,d)^m4(b,c)^bd)
vec=np.array([[a+4*b for a,b in zip(digs(u),digs(v))] for u,v in Q])
# Same representative vectors enumerate both points and dual line coefficients.
inc=(mul[vec[:,0,None],vec[None,:,0]]^mul[vec[:,1,None],vec[None,:,1]]^mul[vec[:,2,None],vec[None,:,2]])==0
I=inc.astype(np.int64)
ck('273 points and lines',I.shape==(273,273))
ck('each line and point degree 17',np.all(I.sum(0)==17) and np.all(I.sum(1)==17))
ck('unique joining line and intersection for all distinct pairs',np.array_equal(I.T@I,16*np.eye(273,dtype=int)+np.ones((273,273),dtype=int)))
# Actual multiplicative Baer partition, not an abstract 13x21 array.
B=np.array([[int(q in block) for q in Q] for block in blocks],dtype=np.int64)
ck('13 Baer sectors partition',B.shape==(13,273) and np.all(B.sum(0)==1) and np.all(B.sum(1)==21))
J=I@B.T
ck('every line meets every actual Baer subplane in 1 or 5',set(J.flat)=={1,5})
ck('each line secant to one Baer subplane',np.all((J==5).sum(1)==1))
for p in range(273):
    L=I[I[:,p]==1]; keep=np.arange(273)!=p;A=L[:,keep]
    ck('pencil partition centre '+str(p),A.shape==(17,272) and np.all(A.sum(0)==1) and np.all(A.sum(1)==16))
    C=B[:,keep];D=C.sum(1); V=A@C.T; b=np.argmax(B[:,p]);
    ck('punctured Baer incidence signature '+str(p),Counter(V[:,b])=={0:12,4:5} and all(Counter(V[:,j])=={1:16,5:1} for j in range(13) if j!=b) and np.all((V[:,np.arange(13)!=b]==5).sum(1)==(V[:,b]==0)))
# singleton grade P0, represented by the unique diagonal grade-zero matrix unit
p=pairs.index((1,1)); keep=np.arange(273)!=p; A=I[I[:,p]==1][:,keep];C=B[:,keep];D=C.sum(1)
ck('singleton point in selected flag',canon(Q[p])==canon((1,0)))
Q16=A.T@A; QB420=C.T@np.diag(420//D)@C
ck('pencil normalized projector',np.array_equal(Q16@Q16,16*Q16) and np.trace(Q16)==16*17)
ck('Baer normalized projector',np.array_equal(QB420@QB420,420*QB420) and np.trace(QB420)==420*13)
ck('rank ratio',F(int(np.trace(Q16)),16)/F(int(np.trace(QB420)),420)==F(17,13))
ck('projectors differ',not np.array_equal(420*Q16,16*QB420))
ck('incidence overlap trace 12/7',F(int(np.sum(Q16*QB420)),16*420)==F(12,7))
M=np.zeros((21,273),dtype=np.int64)
for i,q in enumerate(Q):M[points.index(project(norm(q))),i]=1
j=np.argmax(M[:,p]); ej=M[:,p];d=np.array([int(a==b) for a,b in pairs]);
Bpt13=M@M.T-np.outer(ej,ej);Btr273=21*(M@M.T)-np.outer(M@d,M@d)
ck('point compression exact',np.array_equal(Bpt13,13*np.eye(21,dtype=int)-np.outer(ej,ej)))
ck('point and trace compression differ',not np.array_equal(21*Bpt13,Btr273))
ck('equal traces',F(int(np.trace(Bpt13)),13)==F(int(np.trace(Btr273)),273)==F(272,13))
ck('point exceptional direction',np.array_equal(Bpt13@ej,12*ej))
ck('trace exceptional direction',np.array_equal(Btr273@np.ones(21,dtype=int),252*np.ones(21,dtype=int)))
ck('no exclusion trace',F(int(np.trace(M@M.T)),13)==21)
z=s.symbols('z');old=(1+z/16)**20*(1+3*z/52);new=(1+z/13)**17
ck('first derivatives coincide',s.diff(old,z).subs(z,0)==s.diff(new,z).subs(z,0)==s.Rational(17,13))
ck('old second derivative',s.diff(old,z,2).subs(z,0)==s.Rational(1355,832))
ck('pencil second derivative',s.diff(new,z,2).subs(z,0)==s.Rational(272,169))
ck('second derivatives discriminate',s.diff(old,z,2).subs(z,0)!=s.diff(new,z,2).subs(z,0))
print(f'TOTAL {n} new exact incidence assertions passed')
# Optional exact incidence export for diagrams or independent inspection.
if __name__=='__main__':
    import json
    V=A@C.T; b=np.argmax(B[:,p]); order=[b]+[k for k in range(13) if k!=b]; roworder=sorted(range(17),key=lambda i:(V[i,b]==0, next((k for k in range(13) if k!=b and V[i,k]==5),-1)))
    Path(__file__).with_name('pencil_incidence.json').write_text(json.dumps({'centre_matrix_unit':list(pairs[p]),'punctured_intersections':V[roworder][:,order].tolist()},indent=2)+'\n')
