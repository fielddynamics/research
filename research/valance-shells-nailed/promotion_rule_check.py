#!/usr/bin/env python3
"""
Generative check of the three-tier promotion rule
=================================================

gfd_electron_config.py scores the rule on the 13 known Madelung exceptions:
it compares the tier of the Madelung d/f occupancy with the tier of the
observed one. That establishes that the observed configuration sits on a
higher tier in 10 of 13 cases. It does not ask the converse question: if the
rule is applied to every element, does it also promote electrons in elements
whose Madelung configuration is already correct?

This script applies the rule, as stated in gfd_electron_config_synthesis.md,
generatively to all 83 elements (Z = 1-83):

  Start from the Madelung configuration. Consider transferring one or two
  electrons from the outer ns sub-shell into the open (n-1)d sub-shell, and
  one electron from an open (n-2)f sub-shell into (n-1)d. A transfer occurs
  when it moves the d/f sub-shell concerned to a strictly higher resonance
  tier (T1 > T2 > T3 > off-resonance). Otherwise the Madelung configuration
  stands.

Variant B also allows ns -> (n-2)f transfers, since the synthesis phrases the
rule as "from s to d/f".

A look-elsewhere test then asks how often a random landmark set, with as many
resonant occupancies as the tiers mark, would do as well.

    python promotion_rule_check.py
"""
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gfd_electron_config as g

L = {0: "s", 1: "p", 2: "d", 3: "f"}


def tier(ne, cap, tier_fn):
    return tier_fn(ne, cap)


def default_tier(ne, cap):
    return g.tier_score(ne, cap)[0]


def candidates(cfg, allow_s_to_f, max_k=2):
    """Yield (new_config, (n,l) of the d/f sub-shell whose tier decides)."""
    if not cfg:
        return
    n_s = max(n for (n, l) in cfg if l == 0)          # outermost s
    s_key, d_key, f_key = (n_s, 0), (n_s - 1, 2), (n_s - 2, 3)
    s_cnt = cfg.get(s_key, 0)
    if n_s - 1 >= 3:                                  # a d sub-shell exists below
        d_cnt = cfg.get(d_key, 0)
        for k in range(1, max_k + 1):
            if s_cnt >= k and d_cnt + k <= 10:
                new = dict(cfg); new[s_key] = s_cnt - k; new[d_key] = d_cnt + k
                yield new, d_key, d_cnt, d_cnt + k, 10
    if n_s - 2 >= 4 and cfg.get(f_key, 0) > 0:      # f -> d
        f_cnt, d_cnt = cfg[f_key], cfg.get(d_key, 0)
        if d_cnt < 10:
            new = dict(cfg); new[f_key] = f_cnt - 1; new[d_key] = d_cnt + 1
            yield new, f_key, f_cnt, f_cnt - 1, 14
    if allow_s_to_f and n_s - 2 >= 4 and 0 < cfg.get(f_key, 0) < 14 and s_cnt >= 1:
        f_cnt = cfg[f_key]
        new = dict(cfg); new[s_key] = s_cnt - 1; new[f_key] = f_cnt + 1
        yield new, f_key, f_cnt, f_cnt + 1, 14


def predict(Z, allow_s_to_f=False, tier_fn=default_tier, max_k=2):
    mad = g.fill_madelung(Z)
    best, best_gain = mad, 0
    for new, key, before, after, cap in candidates(mad, allow_s_to_f, max_k):
        gain = tier_fn(before, cap) - tier_fn(after, cap)    # positive = higher tier
        if gain > best_gain:
            best, best_gain = new, gain
    return {k: v for k, v in best.items() if v > 0}


def clean(cfg):
    return {k: v for k, v in cfg.items() if v > 0}


def score(allow_s_to_f=False, tier_fn=default_tier, max_k=2):
    right, false_pos, fixed, missed = 0, [], [], []
    for Z in range(1, 84):
        obs = clean(g.parse_config_string(g.KNOWN_CONFIGS_RAW[Z]))
        mad = clean(g.fill_madelung(Z))
        pred = predict(Z, allow_s_to_f, tier_fn, max_k)
        ok = pred == obs
        right += ok
        if mad == obs and not ok:
            false_pos.append(Z)
        if mad != obs and ok:
            fixed.append(Z)
        if mad != obs and not ok:
            missed.append(Z)
    return right, false_pos, fixed, missed


SYM = ["", "H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne", "Na", "Mg", "Al", "Si", "P", "S",
       "Cl", "Ar", "K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge",
       "As", "Se", "Br", "Kr", "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd",
       "In", "Sn", "Sb", "Te", "I", "Xe", "Cs", "Ba", "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd",
       "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg",
       "Tl", "Pb", "Bi"]


def names(zs):
    return ", ".join(SYM[z] for z in zs) or "none"


def main():
    mad_right = sum(clean(g.fill_madelung(Z)) == clean(g.parse_config_string(g.KNOWN_CONFIGS_RAW[Z]))
                    for Z in range(1, 84))
    print("=" * 74)
    print("  GENERATIVE CHECK OF THE PROMOTION RULE (Z = 1-83)")
    print("=" * 74)
    print(f"  Madelung alone: {mad_right}/83 correct")
    variants = (("S: one electron, s->d and f->d (literal reading)", False, 1),
                ("A: one or two electrons, s->d and f->d", False, 2),
                ("B: as A, plus s->f", True, 2))
    for label, sf, mk in variants:
        right, fp, fx, ms = score(sf, max_k=mk)
        print(f"\n  Rule applied generatively, variant {label}")
        print(f"    correct:                         {right}/83")
        print(f"    exceptions fixed ({len(fx):2d}):            {names(fx)}")
        print(f"    exceptions still wrong ({len(ms):2d}):      {names(ms)}")
        print(f"    false promotions ({len(fp):2d}):            {names(fp)}")
        if fp:
            for Z in fp:
                print(f"      {SYM[Z]:2} predicted {g.config_to_string(predict(Z, sf, max_k=mk))[-22:]:>22}"
                      f"   observed {g.KNOWN_CONFIGS_RAW[Z][-22:]:>22}")

    # Look-elsewhere: random resonant sets of the same size per shell
    def resonant_set(cap):
        return {ne for ne in range(cap + 1) if default_tier(ne, cap) < 99}
    d_res, f_res = resonant_set(10), resonant_set(14)
    print(f"\n  Resonant occupancies: d {sorted(d_res)} ({len(d_res)}/11), "
          f"f {sorted(f_res)} ({len(f_res)}/15)")
    base_right = score(False, max_k=1)[0]
    random.seed(7)
    trials, as_good = 5000, 0
    for _ in range(trials):
        rd = set(random.sample(range(11), len(d_res)))
        rf = set(random.sample(range(15), len(f_res)))
        def tf(ne, cap, rd=rd, rf=rf):
            return 1 if ne in (rd if cap == 10 else rf) else 99
        as_good += score(False, tf, max_k=1)[0] >= base_right
    print(f"  Random resonant sets of the same size ({trials} trials), variant S:")
    print(f"    fraction scoring >= {base_right}/83: {as_good / trials:.3f}")
    return dict(madelung=mad_right, variant_s=score(False, max_k=1), variant_a=score(False),
                variant_b=score(True),
                p_random=as_good / trials)


if __name__ == "__main__":
    main()
