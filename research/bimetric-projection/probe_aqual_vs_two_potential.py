"""SST (AQUAL form) vs the two-potential torsion reading (TetA = Newtonian/Christoffel field g_N,
TetB = torsion force b = (nu-1) g_N, curl-free part): same spherical law, different off-sphere?
Units G = M = 1. Periodic FFT box (artifacts are common to both solvers)."""
import numpy as np, sys
N=int(sys.argv[1]) if len(sys.argv)>1 else 128; L=48.0; dx=L/N
a0=1/9.                                   # r_M = sqrt(GM/a0) = 3
x=(np.arange(N)-N//2)*dx; X,Y,Z=np.meshgrid(x,x,x,indexing='ij')
k=2*np.pi*np.fft.fftfreq(N,dx); KX,KY,KZ=np.meshgrid(k,k,k,indexing='ij'); K2=KX**2+KY**2+KZ**2; K2[0,0,0]=1
def mu(s): return s/(1+s)
def nu(y): return 0.5+np.sqrt(0.25+1/np.maximum(y,1e-30))
def grad_from_rho(rho):          # g = -grad Phi, lap Phi = 4 pi rho
    rk=np.fft.fftn(rho-rho.mean()); Pk=-4*np.pi*rk/K2; Pk[0,0,0]=0
    return [np.real(np.fft.ifftn(-1j*kk*Pk)) for kk in (KX,KY,KZ)]
def curlfree(v):
    vk=[np.fft.fftn(c) for c in v]; dv=(KX*vk[0]+KY*vk[1]+KZ*vk[2])/K2
    return [np.real(np.fft.ifftn(kk*dv)) for kk in (KX,KY,KZ)]
norm=lambda v: np.sqrt(v[0]**2+v[1]**2+v[2]**2)
def solve(rho,iters=60):
    gN=grad_from_rho(rho)
    nN=norm(gN); q=[nu(nN/a0)*c for c in gN]; gQ=curlfree(q)             # two-potential (QUMOND form)
    g=[c.copy() for c in gQ]
    for it in range(iters):                                                # AQUAL: mu(|g|) g = gN + curl
        m=mu(norm(g)/a0); h=[m*c for c in g]; hcf=curlfree(h); gNcf=curlfree(gN)
        h=[hc - hcfc + gNc for hc,hcfc,gNc in zip(h,hcf,gNcf)]          # keep h's curl part, set div(h)=div(gN)
        nh=norm(h); gnew=curlfree([nu(nh/a0)*c for c in h])
        diff=max(np.abs(gn-go).max() for gn,go in zip(gnew,g)); g=gnew
        if diff<1e-7*norm(g).max(): break
    return gN,gQ,g,it
def report(name,rho,radii,axis):
    gN,gQ,gA,it=solve(rho)
    i0=N//2; print(f"{name}: AQUAL iterations {it}")
    print("   R    g_N        g_twoPot   g_AQUAL    analytic-sph   (AQUAL-twoPot)/AQUAL")
    for R in radii:
        j=i0+int(round(R/dx)); Rr=(j-i0)*dx
        gn=-gN[0][j,i0,i0]; gq=-gQ[0][j,i0,i0]; ga=-gA[0][j,i0,i0]
        gs=gn; gt_sph=0.5*(gs+np.sqrt(gs**2+4*gs*a0))
        print(f" {Rr:5.2f} {gn:.5e} {gq:.5e} {ga:.5e} {gt_sph:.5e}   {100*(ga-gq)/ga:+.2f}%")
r=np.sqrt(X**2+Y**2+Z**2)
plummer=(3/(4*np.pi*1.0**3))*(1+r**2/1.0**2)**-2.5
report("Spherical Plummer (control: both should match the spherical law)",plummer,[1,2,3,5,8],0)
A,B=2.0,0.6; R2=X**2+Y**2; zb=np.sqrt(Z**2+B**2)
mn=(B**2/(4*np.pi))*(A*R2+(A+3*zb)*(A+zb)**2)/((R2+(A+zb)**2)**2.5*zb**3)
report("Miyamoto-Nagai disk (a=2, b=0.6), in-plane",mn,[1,2,3,5,8],0)
