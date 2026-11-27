import sympy as S
x,y,s,q,ke,ko,b=S.symbols('x y s q ke ko b',real=True)
d=ko-2*b*s
E=ke*(x-b*y*y)**2/2+ko*y*y/2-s*x-q*y
xs=s/ke+b*q*q/d**2;ys=q/d;Es=-s*s/(2*ke)-q*q/(2*d)
count=0
def check(v):
 global count
 assert S.simplify(v)==0,v
 count+=1
check(E-(ke*(x-b*y*y-s/ke)**2/2+d*(y-q/d)**2/2+Es))
for v in (x,y):check(S.diff(E,v).subs({x:xs,y:ys}))
check(E.subs({x:xs,y:ys})-Es)
check(xs.subs(q,-q)-xs);check(ys.subs(q,-q)+ys)
check(xs.subs(q,0)-s/ke);check(ys.subs(q,0))
check(S.diff(xs,q,2)-2*b/d**2);check(S.diff(xs,q).subs(q,0));check(S.diff(ys,s).subs(q,0))
H=S.hessian(E,(x,y)).subs({x:xs,y:ys});check(H.det()-ke*d);check(H[0,0]-ke)
J=S.Matrix([xs,ys]).jacobian([s,q]);
for v in H*J-S.eye(2):check(v)
check(S.diff(Es,s)+xs);check(S.diff(Es,q)+ys)
for v in S.hessian(Es,(s,q))+J:check(v)
for k in [1,2,4]:
 for Q in [-2,-1,0,1,2]:
  sub={ke:k,ko:5,b:S.Rational(1,4),s:2,q:Q}
  check((H.det()-ke*d).subs(sub));check((E.subs({x:xs,y:ys})-Es).subs(sub))
print(f'{count} exact assertions passed; conditional witness only.')
