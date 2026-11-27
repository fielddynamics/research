import sympy as s
R=s.Rational
G=s.Matrix([[3,-1,0],[-1,3,0],[0,0,1]])
x=s.Matrix([R(1,3),1,-R(4,15)])
M=s.Matrix([[-2,R(1,2),-2],[-R(1,2),1,-1],[-5,-1,-R(89,10)]])
C=s.Matrix([[0,-R(1,2),0],[-R(1,2),0,-1],[1,-3,1]])
f=R(225,1232); lam=R(11,10); I=s.eye(3); L=M-lam*I
Q=x*x.T*G/(x.T*G*x)[0]; P=I-Q; b=P*C*x; A=-L+Q; v=A.inv()*b; k=(f*b.T*G*v)[0]
checks=0
def ck(c):
 global checks
 assert c
 checks+=1
ck(G*C==C.T*G); ck(G*M==M.T*G); ck(M*x==lam*x); ck(Q*Q==Q); ck(P*P==P); ck(P.T*G==G*P); ck(P*b==b); ck((x.T*G*b)[0]==0); ck((x.T*G*v)[0]==0); ck((f*x.T*G*C*x)[0]==R(59,308)); ck(v==s.Matrix([-430,-296,-2960])/11319); ck(k==R(42815,290521)); ck(1/k==R(290521,42815)); ck(A*v==b)
h=s.symbols('h'); B=L+h*f*b*b.T*G; dx=v/(1-h*k)
for e in B*dx+b: ck(s.cancel(e)==0)
ck(s.cancel((2*f*x.T*G*C*dx)[0]-2*k/(1-h*k))==0)
ck(s.cancel((x.T*G*dx)[0])==0)
ck(2*k/(1-R(308,59)*k)==R(5052170,3953719)); ck(2*k==R(85630,290521))
ck((B.subs(h,1/k)*v).applyfunc(s.simplify)==s.zeros(3,1))
for z in [0,1,2,3,4,5,6,R(308,59)]:
 ck((B.subs(h,z)*dx.subs(h,z)+b).applyfunc(s.simplify)==s.zeros(3,1)); ck((x.T*G*dx.subs(h,z))[0]==0)
print(f'{checks} exact assertions passed'); print('k =', k, 'h_c =', 1/k); print('u_prime at t=1:',R(5052170,3953719),float(R(5052170,3953719)))
