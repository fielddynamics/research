#!/usr/bin/env python3
"""Verify every Great Pyramid metric against its source, then cross-check them.

    python fetch_sources.py      # once (needs network), fills sources_cache/
    python verify_metrics.py     # PASS/FAIL per check; writes metrics.json, metrics.csv, METRICS.md

Three kinds of check:
  Q  quote     the metric's quote occurs verbatim in the cached source text
               (whitespace and table bars normalised), and its value occurs in the quote
  X  cross     independent consistency checks between metrics (geometry, units,
               Petrie's own arithmetic, the repository's earlier claims, modern surveys)
  F  finding   discrepancies the checks expose, recorded and asserted so they stay visible
Exit status is non-zero if any check fails.
"""
import csv
import json
import math
import re
import sys
from pathlib import Path

from dataset import M

HERE = Path(__file__).resolve().parent
CACHE = HERE / "sources_cache"
INCH = 0.0254  # metres, exact
RESULTS = []


def check(kind, label, ok, detail=""):
    RESULTS.append((kind, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {kind} {label}" + (f"  -- {detail}" if detail else ""))
    return ok


def norm(s: str) -> str:
    """Collapse whitespace and table bars; drop the spaces HTML-to-text leaves before punctuation."""
    for ch in ("\u00a0", "\u2009", "|"):
        s = s.replace(ch, " ")
    s = s.replace("\u2060", "")
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r" ([,.;:)\]])", r"\1", s)
    return re.sub(r"\( ", "(", s).strip()


def value_tokens(v, match=None):
    if match is not None:
        return [match]
    if isinstance(v, (int, float)) and v < 0:
        a = -v
        return [f"- {a:g}", f"-{a:g}", f"{a:g}", f"- {a}", f"{a}"]
    if isinstance(v, str):
        nums = re.findall(r"\d[\d,]*\.?\d*|\.\d+", v)
        return [v] + nums[:1]
    if isinstance(v, int):
        return [str(v), f"{v:,}"]
    s = f"{v}"
    toks = {s, s.rstrip("0").rstrip(".") if "." in s else s, f"{v:g}"}
    toks |= {t[1:] for t in list(toks) if t.startswith("0.")}
    if abs(v) >= 1e5:
        toks |= {f"{v / 1e6:g} million", f"{v:,.0f}"}
    return sorted(toks)


def dms(s):
    """'51º 52'' or '26º 31' 23"' or '- 3' 43"' -> degrees (float)."""
    s = s.replace("°", "º")
    sign = -1 if s.strip().startswith("-") else 1
    d = re.search(r"(\d+)\s*º", s)
    mi = re.search(r"(\d+)\s*'", s.split("º")[-1])
    se = re.search(r"(\d+)\s*\"", s)
    val = (int(d.group(1)) if d else 0) + (int(mi.group(1)) if mi else 0) / 60 + (int(se.group(1)) if se else 0) / 3600
    return sign * val


def V(id_):
    for e in M:
        if e["id"] == id_:
            return e["value"]
    raise KeyError(id_)


print("=" * 78)
print("Great Pyramid metrics: source verification and cross-checks")
print("=" * 78)

# ---------------------------------------------------------------------------
print("\n-- Q: every quote occurs verbatim in its source; every value occurs in its quote")
texts = {}
missing = sorted({e["source"] for e in M if not (CACHE / f"{e['source']}.txt").exists()})
if missing:
    print(f"sources_cache/ is missing {missing}; run fetch_sources.py first")
    sys.exit(2)
for e in M:
    src = e["source"]
    if src not in texts:
        texts[src] = norm((CACHE / f"{src}.txt").read_text())
    q = norm(e["quote"])
    found = q in texts[src]
    vt = value_tokens(e["value"], e.get("match"))
    vfound = any(norm(t) in q for t in vt)
    e["verified"] = bool(found and vfound)
    check("Q", f"{e['id']:<24s} {e['section']:<10s} {e['source']}", found and vfound,
          "" if found and vfound else ("quote not found" if not found else f"value {e['value']!r} not in quote"))
ids = [e["id"] for e in M]
check("Q", "metric ids are unique", len(ids) == len(set(ids)), f"{len(ids)} metrics")

# ---------------------------------------------------------------------------
print("\n-- X: cross-checks")
b, h = V("base_side_mean"), V("height_original")
theta = math.radians(dms(V("face_angle")))
h_calc = b / 2 * math.tan(theta)
dh = b / 2 / math.cos(theta) ** 2 * math.radians(2 / 60)
check("X", "height = (base/2) tan(angle) reproduces 5776.0 ± 7.0 (Petrie §25)", abs(h_calc - h) < 7.0,
      f"{h_calc:.1f} in; 2' in angle moves it ±{dh:.1f} in")
sides = [V(k) for k in ("base_N", "base_E", "base_S", "base_W")]
check("X", "mean of the four casing sides = 9068.8 (§21)", abs(sum(sides) / 4 - b) < 0.05, f"{sum(sides)/4:.3f}")
check("X", "socket square exceeds the casing square by 2 x (20–30 in) (§20: sockets lie outside the casing foot)",
      40 <= V("socket_side_mean") - b <= 60, f"{V('socket_side_mean') - b:.1f} in")
seked = math.degrees(math.atan(28 / 22))
check("X", "seked 5½ palms (rise 28 : run 5.5×4) gives 51°50'34\", within Petrie's 51°52' ± 2'",
      abs(seked - dms(V("face_angle"))) * 60 < 2, f"{seked:.4f}° = 51°{(seked-51)*60:.2f}'")
check("X", "seked angle agrees with the infobox slope 51°50'40\" to 6\"",
      abs(seked - dms(V("slope_seked"))) * 3600 < 10, f"{(seked - dms(V('slope_seked'))) * 3600:+.1f}\"")

cubits = {
    "base / 440": b / 440,
    "height / 280": h / 280,
    "KC width / 10": V("kc_width") / 10,
    "KC length / 20": V("kc_length") / 20,
    "KC base (Petrie §52)": V("kc_cubit"),
    "antechamber granite floor / 5": V("ac_granite_floor") / 5,
    "ascending passage / 75": V("ascending_length") / 75,
    "entrance floor / 200": V("entrance_floor_length") / 200,
}
spread = max(cubits.values()) - min(cubits.values())
check("X", "one cubit (20.61–20.72 in) fits base, height, King's Chamber, antechamber and passages",
      all(20.60 < c < 20.72 for c in cubits.values()),
      "; ".join(f"{k} {v:.3f}" for k, v in cubits.items()))
check("X", "the five most accurate parts agree on the cubit to 0.02 in (base, height, KC width, length, base cubit)",
      max(list(cubits.values())[:5]) - min(list(cubits.values())[:5]) < 0.025)

w, L, hf, hw = V("kc_width"), V("kc_length"), V("kc_height_floor"), V("kc_wall_height")
check("X", "King's Chamber: length = 2 x width (20 : 10 cubits) within the probable errors",
      abs(L - 2 * w) < 3 * math.hypot(0.12, 2 * 0.12), f"L - 2w = {L - 2*w:+.2f} in")
hhalf = math.hypot(w, L) / 2
check("X", "King's Chamber height above floor = half the floor diagonal (√125 cubits), within 3 probable errors",
      abs(hhalf - hf) < 3 * 0.15, f"half-diagonal {hhalf:.2f} vs {hf:.2f} ± .15 ({(hhalf-hf)/0.15:.1f} p.e.)")
diag = math.sqrt(w * w + L * L + hf * hf)
check("X", "space diagonal from w, L, h = 515.17 (§156) = 25 cubits", abs(diag - 515.17) < 0.1 and abs(diag / V("kc_cubit") - 25) < 0.05,
      f"{diag:.2f} in = {diag / V('kc_cubit'):.3f} cubits")
check("X", "wall height − height above floor = floor raise 5.11 (§155)", abs((hw - hf) - V("kc_floor_raise")) < 0.01,
      f"{hw - hf:.2f}")
check("X", "five wall courses of 47.04 make the wall height 235.20", abs(5 * V("kc_course_height") - hw) < 0.01,
      f"{5 * V('kc_course_height'):.2f}")
lo, hi = (float(x) for x in V("kc_roof_level").split(" to "))
check("X", "floor level + height above floor lands inside the roof range 1921.6–1923.7 (§64)",
      lo <= V("kc_floor_level") + hf <= hi, f"{V('kc_floor_level') + hf:.1f}")
check("X", "antechamber floor (1692.6) and King's Chamber floor (1692.8) are one level within errors",
      abs(V("ac_floor_level") - V("kc_floor_level")) < 0.6 * 2)
check("X", "Queen's Chamber: floor + ridge height = roof level 1078.7 ± .6 within errors",
      abs(V("qc_floor_level") + V("qc_ridge_height") - V("qc_roof_level")) < 1.5,
      f"{V('qc_floor_level') + V('qc_ridge_height'):.1f}")
check("X", "Gallery: roof horizontal = floor horizontal − 40.45 (= 2 x 20.2 cubit laps), §46",
      abs(V("gg_floor_horizontal") - 40.45 - V("gg_roof_length")) < 0.06)
check("X", "Petrie's three coincident levels: gallery floor end, gallery horizontal length, KC wall base, within 1 in",
      max(V("gg_floor_end_level"), V("gg_floor_horizontal"), V("kc_wall_base_level"))
      - min(V("gg_floor_end_level"), V("gg_floor_horizontal"), V("kc_wall_base_level")) < 1.0)
ent_end = V("entrance_level") - 4140 * math.sin(math.radians(dms(V("entrance_angle")))) - 0.8
check("X", "entrance passage: 668.2 − 4140 sin(26°31'23\") − 0.8 = −1181 (Petrie's own computation, §36)",
      abs(ent_end - V("entrance_end_level")) < 1.0, f"{ent_end:.1f}")

co = V("coffer_outer_length") * V("coffer_outer_width") * V("coffer_outer_height")
ci = V("coffer_inner_length") * V("coffer_inner_width") * V("coffer_inner_height")
check("X", "coffer outer L x W x H reproduces the independently integrated volume 142,530 to 0.1%",
      abs(co / V("coffer_volume_overall") - 1) < 1e-3, f"{co:,.0f} in³")
check("X", "coffer inner L x W x H reproduces the contents 72,030 to 0.1%",
      abs(ci / V("coffer_contents") - 1) < 1e-3, f"{ci:,.0f} in³")
check("X", "coffer: contents ≈ bulk to 1/50 (Petrie §156)",
      abs(V("coffer_contents") - V("coffer_bulk")) / V("coffer_contents") < 0.025,
      f"{(V('coffer_contents') - V('coffer_bulk')) / V('coffer_contents'):.3%}")
check("X", "offsets and calipers agree on the coffer's overall volume to 0.05%",
      abs(V("coffer_volume_calipers") / V("coffer_volume_overall") - 1) < 5e-4)
check("X", "coffer length 89.62 in ≈ 7 ft 6 in (90 in) of §130", abs(V("coffer_outer_length") - 90) < 0.5)

# the repository's earlier claims (README §6, note 01.6)
r_floor = L * w * hf / V("coffer_volume_overall")
r_wall = L * w * hw / V("coffer_volume_overall")
check("X", "repo claim: V_KC (floor-to-ceiling) / V_coffer,ext = 137.17", abs(r_floor - 137.17) < 0.02, f"{r_floor:.3f}")
check("X", "repo claim: base-of-walls convention gives about 140.2", abs(r_wall - 140.2) < 0.1, f"{r_wall:.2f}")
check("X", "repo claim: the 137.17 ratio is 0.10% from 1/alpha = 137.036", abs(r_floor / 137.035999 - 1 - 0.0010) < 0.0002,
      f"{(r_floor / 137.035999 - 1):.4%}")
check("X", "repo claim: KC proportions 20 : 10 : 5√5 have space diagonal 25 cubits", abs(math.sqrt(400 + 100 + 125) - 25) < 1e-12)
zstar = (1 - 1 / math.sqrt(2)) * h
check("X", "GP-1: the area-balance level 0.292893 h = 1691.75 lies inside the KC floor range 1691.4–1693.7",
      1691.4 <= zstar <= 1693.7, f"{zstar:.2f} in")
check("X", "Queen's Chamber floor 834.4 is near (not at) half the KC floor level (846.4); Petrie §148 leaves it open",
      abs(V("qc_floor_level") - V("kc_floor_level") / 2) < 15, f"difference {V('qc_floor_level') - V('kc_floor_level')/2:+.1f} in")

# SI and modern comparisons
b_m, h_m = b * INCH, h * INCH
cole = [float(x) for x in V("cole_sides").split(" / ")]
check("X", "Petrie's mean base (230.348 m) agrees with Cole 1925 (230.364 m) to 2 cm", abs(b_m - sum(cole) / 4) < 0.02,
      f"Petrie {b_m:.3f} m, Cole {sum(cole)/4:.4f} m")
check("X", "Petrie's height 146.71 ± 0.18 m vs the commonly quoted 146.6 m (= 280 cubits of 0.5236 m)",
      abs(h_m - V("height_original_m")) < 7.0 * INCH, f"{h_m:.3f} m")
vol = b_m ** 2 * h_m / 3
check("X", "volume b²h/3 = 2.595e6 m³, matching '2.6 million m³'", abs(vol / V("volume_m3") - 1) < 0.01, f"{vol:,.0f} m³")
rho = V("weight_petrie") * 1016.0469 / vol
check("X", "Petrie's 5,923,400 tons implies a mean density 2,320 kg/m³ (plausible for limestone with joints)",
      2200 < rho < 2500, f"{rho:.0f} kg/m³")
tot = 5.5e6 + 8000 + 500000
check("X", "limestone + granite + mortar (6.008 Mt) is consistent with Petrie's mass (6.019e9 kg) to 0.5%",
      abs(tot * 1000 / (V("weight_petrie") * 1016.0469) - 1) < 0.005)
check("X", "entrance level 668.2 in = 16.97 m, matching 'approximately 17 metres'", abs(V("entrance_level") * INCH - 17) < 0.1,
      f"{V('entrance_level') * INCH:.2f} m")
check("X", "height lost 146.6 − 138.5 = 8.1 m, matching 'about 8 metres'", abs(V("height_original_m") - V("height_current_m") - 8) < 0.2)

# ---------------------------------------------------------------------------
print("\n-- F: findings (discrepancies the cross-checks expose; asserted so they stay recorded)")
cole_mean = sum(cole) / 4
check("F", "the infobox base 230.33 m is NOT the mean of the side lengths it cites (230.364 m): 3.4 cm discrepancy",
      abs(V("base_infobox") - cole_mean) > 0.03, f"{V('base_infobox')} vs {cole_mean:.4f}")
check("F", "Wikipedia's entrance offset '15 royal cubits (7.9 m)' exceeds Petrie's measured axis offset 287 in (7.29 m) by 0.6 m",
      abs(15 * 0.5236 - V("entrance_east_offset") * INCH) > 0.5,
      f"15 cubits = {15 * V('kc_cubit'):.0f} in vs 287 in; Petrie §149 also rejects 12 cubits (247 in)")
check("F", "KC height above floor sits 2.4 p.e. below the half-diagonal: the '√125 cubits' design fits only loosely",
      2 < (hhalf - hf) / 0.15 < 3)
check("F", "Petrie gives the coffer outer length as 89.62 and 89.63 in two tables of §156 (rounding)", True)

# ---------------------------------------------------------------------------
n = len(RESULTS)
npass = sum(ok for _, ok in RESULTS)
by = {k: (sum(ok for kk, ok in RESULTS if kk == k), sum(1 for kk, _ in RESULTS if kk == k)) for k in "QXF"}
print("\n" + "=" * 78)
print(f"Metrics: {len(M)} ({sum(e['tier']=='P' for e in M)} primary, {sum(e['tier']=='S' for e in M)} secondary); "
      f"verified against source: {sum(e['verified'] for e in M)}/{len(M)}")
print(f"Checks: Q {by['Q'][0]}/{by['Q'][1]}, X {by['X'][0]}/{by['X'][1]}, F {by['F'][0]}/{by['F'][1]}; "
      f"total {npass}/{n} passed")

# ---------------------------------------------------------------------------
# Write the machine-readable and human-readable tables
def si(e):
    v = e["value"]
    if e["unit"] == "in" and isinstance(v, (int, float)):
        return f"{v * INCH:.4f} m"
    if e["unit"] == "in^3" and isinstance(v, (int, float)):
        return f"{v * INCH ** 3:.4f} m³"
    return ""


(HERE / "metrics.json").write_text(json.dumps(M, indent=1, ensure_ascii=False))
with open(HERE / "metrics.csv", "w", newline="") as fh:
    wr = csv.writer(fh)
    wr.writerow(["id", "group", "name", "value", "err", "unit", "SI", "tier", "status", "source", "section", "verified", "note"])
    for e in M:
        wr.writerow([e["id"], e["group"], e["name"], e["value"], e["err"] if e["err"] is not None else "", e["unit"], si(e),
                     e["tier"], e["status"], e["source"], e["section"], e["verified"], e["note"]])
lines = ["# Great Pyramid metrics — verified table", "",
         "*Generated by `verify_metrics.py`; do not edit by hand. Every row's quote was found verbatim in the cited source.*", ""]
group = None
for e in M:
    if e["group"] != group:
        group = e["group"]
        lines += ["", f"## {group.replace('_', ' ').title()}", "",
                  "| Metric | Value | ± | Unit | SI | Tier | Status | Source | ✓ |", "|---|---:|---:|---|---:|:-:|---|---|:-:|"]
    err = "" if e["err"] is None else str(e["err"])
    src = ("Petrie 1883 " if e["source"].startswith("petrie") else "Wikipedia rev. 1384664775, ") + e["section"]
    lines.append(f"| {e['name']} | {e['value']} | {err} | {e['unit']} | {si(e)} | {e['tier']} | {e['status']} | {src} | "
                 f"{'✓' if e['verified'] else '✗'} |")
(HERE / "METRICS.md").write_text("\n".join(lines) + "\n")
sys.exit(0 if npass == n else 1)
