#!/usr/bin/env python3
"""
Baseline comparison for the vortex-radius programme
====================================================

Every GFD result in this folder starts from r = n^2 a0 / Z_eff with Clementi's
Z_eff. This script asks what that formulation adds over standard baselines:

  A. Atomic radii      GFD vortex formula vs Slater's rules (1930), scored against
                       Clementi's calculated radii and against independent
                       empirical (covalent) radii.
  B. Polarisability    GFD fitted power law vs zero-parameter and one-parameter
                       r^3 baselines, with a hold-out test (fit on Z = 1-10,
                       predict Z = 11-20).
  C. H-H bond length   look-elsewhere test: how many simple expressions in a0
                       land as close to 74.14 pm as a0*sqrt(2) does?

All reference values are read from data/atomic_reference.csv (sources in
data/SOURCES.md). Python 3.8+, standard library only.

    python baseline_comparison.py
"""
import csv
import math
import os
from fractions import Fraction

A0_PM = 52.9177210903
HERE = os.path.dirname(os.path.abspath(__file__))


def load():
    with open(os.path.join(HERE, "data", "atomic_reference.csv")) as fh:
        rows = list(csv.DictReader(fh))
    for r in rows:
        for k in ("Z", "n"):
            r[k] = int(r[k])
        for k in ("zeff_clementi", "r_clementi_pm", "r_covalent_cordero_pm", "alpha_A3"):
            r[k] = float(r[k])
    return rows


# ---------------------------------------------------------------- helpers

def mean(xs):
    return sum(xs) / len(xs)


def pearson(x, y):
    mx, my = mean(x), mean(y)
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    sx = math.sqrt(sum((a - mx) ** 2 for a in x))
    sy = math.sqrt(sum((b - my) ** 2 for b in y))
    return sxy / (sx * sy)


def spearman(x, y):
    def ranks(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        rk = [0.0] * len(v)
        i = 0
        while i < len(v):
            j = i
            while j + 1 < len(v) and v[order[j + 1]] == v[order[i]]:
                j += 1
            for k in range(i, j + 1):
                rk[order[k]] = (i + j) / 2.0
            i = j + 1
        return rk
    return pearson(ranks(x), ranks(y))


def mape(pred, obs):
    return 100.0 * mean([abs(p - o) / o for p, o in zip(pred, obs)])


def fit_loglog(x, y):
    """Least squares log y = log c + p log x. Returns (c, p)."""
    lx, ly = [math.log(v) for v in x], [math.log(v) for v in y]
    mx, my = mean(lx), mean(ly)
    p = sum((a - mx) * (b - my) for a, b in zip(lx, ly)) / sum((a - mx) ** 2 for a in lx)
    return math.exp(my - p * mx), p


def fit_scale(x, y):
    """Best single factor s with y ~ s * x, in log space."""
    return math.exp(mean([math.log(b / a) for a, b in zip(x, y)]))


def log_rms(pred, obs):
    """RMS of ln(pred/obs): a scale-free error, ~ fractional error when small."""
    return math.sqrt(mean([math.log(p / o) ** 2 for p, o in zip(pred, obs)]))


# ---------------------------------------------------------------- Slater's rules

def slater_zeff(Z):
    """Slater (1930) effective charge for the outermost electron, Z = 1-20."""
    shells = [("1s", 2), ("2sp", 8), ("3sp", 8), ("4s", 2)]
    occ, left = [], Z
    for name, cap in shells:
        k = min(cap, left)
        occ.append(k)
        left -= k
        if left == 0:
            break
    g = len(occ) - 1                      # index of outermost group
    same = occ[g] - 1
    s = same * (0.30 if g == 0 else 0.35)
    if g >= 1:
        s += occ[g - 1] * 0.85
    if g >= 2:
        s += sum(occ[: g - 1]) * 1.00
    return Z - s


SLATER_NSTAR = {1: 1.0, 2: 2.0, 3: 3.0, 4: 3.7}


# ---------------------------------------------------------------- report

def main():
    rows = load()
    Z = [r["Z"] for r in rows]
    sym = [r["symbol"] for r in rows]
    r_clem = [r["r_clementi_pm"] for r in rows]
    r_cov = [r["r_covalent_cordero_pm"] for r in rows]
    alpha = [r["alpha_A3"] for r in rows]

    r_gfd = [r["n"] ** 2 * A0_PM / r["zeff_clementi"] for r in rows]
    r_sla = [SLATER_NSTAR[r["n"]] ** 2 * A0_PM / slater_zeff(r["Z"]) for r in rows]
    r_sla_n = [r["n"] ** 2 * A0_PM / slater_zeff(r["Z"]) for r in rows]   # Slater Z_eff, integer n

    out = []
    p = out.append

    p("=" * 78)
    p("  BASELINE COMPARISON: what does the vortex formulation add?")
    p("=" * 78)

    # ------------------------------------------------------------ A. radii
    p("\nA. ATOMIC RADII")
    p("-" * 78)
    p(f"  {'':3} {'Clementi':>9} {'GFD':>7} {'Slater n*':>10} {'Slater n':>9} {'covalent':>9}")
    for i in range(len(rows)):
        p(f"  {sym[i]:3} {r_clem[i]:9.0f} {r_gfd[i]:7.1f} {r_sla[i]:10.1f} {r_sla_n[i]:9.1f} {r_cov[i]:9.0f}")

    p("\n  A1. Against Clementi's calculated radii (the suites' reference)")
    p(f"      GFD  r = n^2 a0 / Z_eff(Clementi): mean |error| {mape(r_gfd, r_clem):5.2f}%")
    p(f"      Slater's rules, n*:                mean |error| {mape(r_sla, r_clem):5.2f}%")
    p(f"      Slater's rules, integer n:         mean |error| {mape(r_sla_n, r_clem):5.2f}%")
    p("      Note: Clementi's radii are the radius of maximum radial density of the outermost")
    p("      orbital. For a Slater-type orbital that maximum lies at r = n/zeta = n^2 a0 / Z_eff,")
    p("      so the GFD formula with Clementi's Z_eff reproduces Clementi's radii nearly by")
    p("      definition. The < 2% agreement is a consistency check, not an independent prediction.")

    p("\n  A2. Against independent empirical radii (Cordero et al. 2008 covalent radii)")
    p("      Different radius definitions differ in scale, so each model gets one fitted scale")
    p("      factor; the comparison is of shape across the 20 elements.")
    for name, r_mod in (("GFD (Clementi Z_eff)", r_gfd), ("Slater's rules, n*", r_sla), ("Slater's rules, n", r_sla_n)):
        s = fit_scale(r_mod, r_cov)
        pred = [s * v for v in r_mod]
        p(f"      {name:22} scale {s:5.3f}  log-RMS {log_rms(pred, r_cov):5.3f}  "
          f"Pearson(log) {pearson([math.log(v) for v in r_mod], [math.log(v) for v in r_cov]):5.3f}  "
          f"Spearman {spearman(r_mod, r_cov):5.3f}")
    nonnoble = [i for i in range(len(rows)) if sym[i] not in ("He", "Ne", "Ar")]
    rg = [r_gfd[i] for i in nonnoble]; rs = [r_sla[i] for i in nonnoble]; rc = [r_cov[i] for i in nonnoble]
    sg, ss = fit_scale(rg, rc), fit_scale(rs, rc)
    p(f"      Excluding noble gases (covalent radii there are not bond-derived):")
    p(f"      GFD log-RMS {log_rms([sg*v for v in rg], rc):5.3f}   Slater n* log-RMS {log_rms([ss*v for v in rs], rc):5.3f}")

    # ------------------------------------------------------------ B. polarisability
    p("\nB. POLARISABILITY")
    p("-" * 78)
    rA_gfd = [v / 100.0 for v in r_gfd]       # pm -> Angstrom
    rA_sla = [v / 100.0 for v in r_sla]
    c, pw = fit_loglog(rA_gfd, alpha)
    pred_fit = [c * v ** pw for v in rA_gfd]
    pred_r3 = [v ** 3 for v in rA_gfd]
    s3 = fit_scale(pred_r3, alpha)
    pred_r3s = [s3 * v for v in pred_r3]
    c2, pw2 = fit_loglog(rA_sla, alpha)
    pred_sla = [c2 * v ** pw2 for v in rA_sla]
    p("  Full set, Z = 1-20 (log-RMS error; 0.10 is roughly a 10% typical error):")
    p(f"    GFD radius, fitted power law     alpha = {c:.3f} r^{pw:.2f}   (2 params)  log-RMS {log_rms(pred_fit, alpha):5.3f}")
    p(f"    GFD radius, classical alpha = r^3                         (0 params)  log-RMS {log_rms(pred_r3, alpha):5.3f}")
    p(f"    GFD radius, alpha = s r^3, s = {s3:.2f}                      (1 param)   log-RMS {log_rms(pred_r3s, alpha):5.3f}")
    p(f"    Slater radius, fitted power law  alpha = {c2:.3f} r^{pw2:.2f}   (2 params)  log-RMS {log_rms(pred_sla, alpha):5.3f}")

    train = [i for i in range(len(rows)) if Z[i] <= 10]
    test = [i for i in range(len(rows)) if Z[i] > 10]
    ct, pt = fit_loglog([rA_gfd[i] for i in train], [alpha[i] for i in train])
    pred_test = [ct * rA_gfd[i] ** pt for i in test]
    obs_test = [alpha[i] for i in test]
    st = fit_scale([rA_gfd[i] ** 3 for i in train], [alpha[i] for i in train])
    pred_test3 = [st * rA_gfd[i] ** 3 for i in test]
    p("\n  Hold-out: fit on Z = 1-10, predict Z = 11-20 (never seen in the fit):")
    p(f"    GFD power law (p = {pt:.2f} from the first period)   log-RMS on Z = 11-20: {log_rms(pred_test, obs_test):5.3f}")
    p(f"    one-parameter r^3 (s = {st:.2f})                     log-RMS on Z = 11-20: {log_rms(pred_test3, obs_test):5.3f}")
    worst = max(test, key=lambda i: abs(math.log(ct * rA_gfd[i] ** pt / alpha[i])))
    p(f"    largest hold-out miss: {sym[worst]} (predicted {ct * rA_gfd[worst] ** pt:.2f}, observed {alpha[worst]:.2f} A^3)")

    # ------------------------------------------------------------ C. look-elsewhere
    p("\nC. H-H BOND LENGTH: LOOK-ELSEWHERE TEST")
    p("-" * 78)
    target = 74.14
    gfd_err = abs(A0_PM * math.sqrt(2) - target) / target
    forms = set()
    for num in range(1, 9):
        for den in range(1, 9):
            q = Fraction(num, den)
            for power in (Fraction(1), Fraction(1, 2), Fraction(1, 3)):
                forms.add((q, power))
    hits = []
    for q, power in forms:
        val = A0_PM * float(q) ** float(power)
        if abs(val - target) / target <= gfd_err + 1e-12:
            hits.append((q, power, val))
    p(f"  a0*sqrt(2) = {A0_PM*math.sqrt(2):.2f} pm, {100*gfd_err:.2f}% from {target} pm.")
    p(f"  Expressions a0 * (p/q)^k with p, q = 1..8 and k in {{1, 1/2, 1/3}}: {len(forms)} distinct.")
    p(f"  Of these, {len(hits)} land at least as close to 74.14 pm:")
    for q, power, val in sorted(hits, key=lambda h: abs(h[2] - target)):
        p(f"    a0 * ({q})^{power} = {val:.2f} pm")
    p("  A formula is evidential only if it was fixed before comparison, or if few")
    p("  comparably simple expressions match as well.")

    # ------------------------------------------------------------ verdict
    p("\nVERDICT")
    p("-" * 78)
    p("  Radii:      the GFD formula with Clementi's Z_eff is Clementi's radius definition;")
    p("              agreement with Clementi radii is by construction. Against independent")
    p("              covalent radii it tracks shape better than Slater's rules (log-RMS 0.24 vs 0.29),")
    p("              which is the advantage of SCF screening over Slater's rules, not of GFD itself.")
    p("  Polarisab.: a radius power law describes alpha well and survives a hold-out test, but")
    p("              the same holds for any accurate radius; it is not specific to GFD.")
    p(f"  Bond H-H:   of {len(forms)} comparably simple expressions in a0, {len(hits)} come as close;")
    p("              a0*sqrt(2) is distinctive but not unique (a0*7/5 is closer).")
    p("  Next step:  derive Z_eff (or the screening) from K = 4, D = 3 geometry. Without that,")
    p("              the chain's predictive content comes from Clementi's SCF screening.")
    print("\n".join(out))
    return out


if __name__ == "__main__":
    main()
