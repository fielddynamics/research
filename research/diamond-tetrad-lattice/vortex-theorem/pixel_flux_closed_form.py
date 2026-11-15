"""Closed form of the half-plane current for the 15-site pixel (THEOREM.md, Part II), symbolic in all parameters.
Run: python pixel_flux_closed_form.py"""
import contextlib, io, os
import sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__))
ns = {"__name__": "setup"}
src = open(os.path.join(HERE, "..", "pixel-vortex", "verify_pixel_vortex.py")).read().split("# --- Theorem 2")[0]
with contextlib.redirect_stdout(io.StringIO()):
    exec(src, ns)
H, B, Hp, sites, n = ns["H"], ns["B"], ns["Hp"], ns["sites"], ns["n"]
Df, eA, eB, cA, cB = ns["Df"], ns["eA"], ns["eB"], ns["cA"], ns["cB"]
ok_all = True
for u in ([2, 1, 0], [1, 3, 0], [-1, 2, 0]):
    axis = sp.Matrix([0, 0, 1]); uu = sp.Matrix(u); v = axis.cross(uu)
    pos = [sp.Matrix(s) for s in sites]
    sv = [(v.T * p)[0] for p in pos]
    K = sp.zeros(n, n)
    for i in range(n):
        for j in range(i + 1, n):
            if H[i, j] != 0 and sv[i] * sv[j] < 0:
                t = sv[i] / (sv[i] - sv[j]); x = pos[i] + t * (pos[j] - pos[i])
                if (uu.T * x)[0] > 0:
                    sg = 1 if sv[i] < 0 else -1
                    K[i, j] += -sp.I * sg * H[i, j]; K[j, i] += sp.I * sg * H[j, i]
    Kp = sp.simplify(B.H * K * B)
    E = sp.symbols("E", real=True); r = sp.symbols("r", positive=True)
    a_c, b_c = Hp[0, 1], Hp[0, 2]
    w = sp.Matrix([r, sp.conjugate(a_c) * r / (E - eA), sp.conjugate(b_c) * r / (E - eB)])
    I_flux = sp.simplify((w.H * Kp * w)[0])
    # use the secular equation E - Df = 2cA^2/(E - eA) + 2cB^2/(E - eB) to eliminate Df
    I_red = sp.simplify(I_flux.subs(Df, E - 2 * cA**2 / (E - eA) - 2 * cB**2 / (E - eB)))
    print(f"half-plane u = {u}: I = {sp.factor(I_red)}")
    ok_all &= sp.simplify(I_red - (-(E - Df) * r**2 / 4).subs(Df, E - 2 * cA**2 / (E - eA) - 2 * cB**2 / (E - eB))) == 0
print("I = -(E - Delta_f)|r|^2 / 4 for every half-plane:", ok_all)
raise SystemExit(0 if ok_all else 1)
