"""R3. The horizon reading of the coupling law. Reported, not judged.
Tiling picture: amplitudes proportional to temperatures, tA ~ T_U(g) = hbar g/(2 pi c kB),
tB ~ T_GH(H) = hbar H/(2 pi kB). Isolated picture: squares. Also: what T_U = T_GH gives,
and what the repo's written form T_GH = hbar H/(2 pi kB c) gives."""
import sympy as sp
hbar, kB, c, g, H, a = sp.symbols("hbar k_B c g H a", positive=True)
TU = lambda acc: hbar * acc / (2 * sp.pi * c * kB)
TGH = hbar * H / (2 * sp.pi * kB)
TGH_repo = hbar * H / (2 * sp.pi * kB * c)
x_tiling = sp.simplify(TU(g) / TGH)
x_iso = sp.simplify((TU(g) / TGH) ** 2)
print("tiling, amplitudes ~ temperatures:  x = tA/tB =", x_tiling, " -> mu(x) = x/(1+x) with a0 =", sp.solve(sp.Eq(x_tiling, 1), g)[0])
print("isolated pixel, squares ~ temperatures: share variable (tA/tB)^2 =", x_iso, " -> mu would need g/a0 itself, not its square: no Tully-Fisher (Q4)")
print("T_U(a) = T_GH  gives a =", sp.solve(sp.Eq(TU(a), TGH), a)[0])
print("dimension check of the repo's T_GH = hbar H/(2 pi kB c): T_GH_repo / T_GH =", sp.simplify(TGH_repo / TGH),
      "(a temperature divided by a speed: not a temperature)")
print("T_U(a) = T_GH_repo gives a =", sp.solve(sp.Eq(TU(a), TGH_repo), a)[0], "(not an acceleration either)")
H0 = 70e3 / 3.0857e22; cc = 2.99792458e8
print(f"\nnumbers, H0 = 70 km/s/Mpc = {H0:.4e} /s:")
print(f"  cH0       = {cc*H0:.3e} m/s^2  (what the temperature ratio gives)")
print(f"  cH0/2pi   = {cc*H0/(2*sp.pi.evalf()):.3e} m/s^2  (the repo's a0)")
print(f"  empirical a0 = 1.2e-10 m/s^2: ratio cH0/a0 = {cc*H0/1.2e-10:.2f}, (cH0/2pi)/a0 = {cc*H0/(2*float(sp.pi))/1.2e-10:.3f}")
print("\nR3 PASS (reported) - in the tiling picture the temperature ratio has the right form, x = g/(cH), so the fixed "
      "TetB coupling would be the horizon temperature; but the scale it gives is a0 = cH (5.7 x too large), not cH/2pi. "
      "The repo's cH/2pi needs a further 1/(2 pi) that the standard temperatures do not supply.")
