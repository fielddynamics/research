#!/usr/bin/env python3
"""
GFD 3-Scale Sierpiński Decomposition
======================================
Three neural networks, one per hierarchical level, trained jointly:

  NN1 (Face):       16-dim input → 4 hidden → 1 output  (face MeV)
  NN2 (Channel):    64-dim input → 4 hidden → 1 output  (channel MeV)
  NN3 (Subchannel): 256-dim input → 4 hidden → 1 output (subchannel MeV)

  B/A = NN1_out + NN2_out + NN3_out

Then solve for gate depth energies a, b, c per element:
  Each scale's output decomposes as:
    OUTPUT = 27a + 27b + 9c + 1d   (d ≈ 0)
  where [27, 27, 9, 1] is the gate depth distribution.

  Three outputs → three equations → solve for a, b, c.

Produces:
  - gfd_3scale.json: per-element face/chan/sub MeV + a,b,c depths
  - Console report with full breakdown
"""

import csv
import json
import torch
import torch.nn as nn
import torch.optim as optim
import os
import numpy as np


# ═══════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════

def load_data(csv_path='gfd_3scale_vectors.csv'):
    elements = []
    with open(csv_path, 'r') as f:
        for row in csv.DictReader(f):
            sym = row['Sym']
            A = int(row['A'])
            ba = float(row['BA_MeV'])
            shell = int(row['Shell'])
            vec256 = [int(c) for c in row['Vec256']]

            face16 = [float(row[f'face_{i}']) for i in range(16)]
            chan64 = [float(row[f'chan_{i}']) for i in range(64)]

            # Subchannel: convert 256 binary to float
            sub256 = [float(b) for b in vec256]

            elements.append({
                'sym': sym, 'A': A, 'ba': ba, 'shell': shell,
                'face': face16, 'chan': chan64, 'sub': sub256,
            })
    return elements


# ═══════════════════════════════════════════════════
# NETWORKS
# ═══════════════════════════════════════════════════

class ScaleNet(nn.Module):
    """Single-scale network: input_dim → 4 hidden → 1 output."""
    def __init__(self, input_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 4),
            nn.ReLU(),
            nn.Linear(4, 1),
        )

    def forward(self, x):
        return self.net(x)


class ThreeScaleModel(nn.Module):
    """
    Three parallel networks whose outputs sum to B/A.

    NN1: 16 → 4 → 1  (face contribution)
    NN2: 64 → 4 → 1  (channel contribution)
    NN3: 256 → 4 → 1 (subchannel contribution)
    """
    def __init__(self):
        super().__init__()
        self.face_net = ScaleNet(16)
        self.chan_net = ScaleNet(64)
        self.sub_net = ScaleNet(256)

    def forward(self, x_face, x_chan, x_sub):
        f = self.face_net(x_face)
        c = self.chan_net(x_chan)
        s = self.sub_net(x_sub)
        return f + c + s, f, c, s

    def get_components(self, x_face, x_chan, x_sub):
        with torch.no_grad():
            total, f, c, s = self.forward(
                x_face.unsqueeze(0),
                x_chan.unsqueeze(0),
                x_sub.unsqueeze(0),
            )
            return {
                'total': total.item(),
                'face_mev': f.item(),
                'chan_mev': c.item(),
                'sub_mev': s.item(),
            }


# ═══════════════════════════════════════════════════
# TRAINING
# ═══════════════════════════════════════════════════

def train(elements, epochs=80000, lr=0.01, n_restarts=10, print_every=20000):
    X_face = torch.tensor([el['face'] for el in elements], dtype=torch.float32)
    X_chan = torch.tensor([el['chan'] for el in elements], dtype=torch.float32)
    X_sub = torch.tensor([el['sub'] for el in elements], dtype=torch.float32)
    Y = torch.tensor([el['ba'] for el in elements], dtype=torch.float32).unsqueeze(1)

    best_r2 = -999
    best_model = None

    for restart in range(n_restarts):
        torch.manual_seed(restart * 97 + int(torch.randint(0, 1000000, (1,)).item()))
        model = ThreeScaleModel()
        optimizer = optim.Adam(model.parameters(), lr=lr)
        scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=20000, gamma=0.5)

        for epoch in range(epochs + 1):
            total, f, c, s = model(X_face, X_chan, X_sub)
            loss = nn.MSELoss()(total, Y)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            scheduler.step()

            if epoch % print_every == 0 and restart == 0:
                with torch.no_grad():
                    bp, _, _, _ = model(X_face, X_chan, X_sub)
                    err = (bp - Y).abs()
                    mae = err.mean().item()
                    mx = err.max().item()
                    pcts = (err / Y).abs() * 100
                    w05 = (pcts <= 0.5).sum().item()
                    w1 = (pcts <= 1.0).sum().item()
                    # Show component means
                    _, ff, cc, ss = model(X_face, X_chan, X_sub)
                    print(f"  ep={epoch:>6d}  MSE={loss.item():.6f}  MAE={mae*1000:.0f}keV  "
                          f"Max={mx:.3f}  ≤0.5%:{w05}/{len(elements)}  ≤1%:{w1}/{len(elements)}  "
                          f"F̄={ff.mean().item():.3f} C̄={cc.mean().item():.3f} S̄={ss.mean().item():.3f}")

        with torch.no_grad():
            bp, ff, cc, ss_val = model(X_face, X_chan, X_sub)
            ss_res = ((bp - Y)**2).sum().item()
            ss_tot = ((Y - Y.mean())**2).sum().item()
            r2 = 1 - ss_res / ss_tot
            err = (bp - Y).abs()
            mae = err.mean().item()
            fm, cm, sm = ff.mean().item(), cc.mean().item(), ss_val.mean().item()
            ratio_fc = fm / cm if abs(cm) > 0.01 else 0
            ratio_cs = cm / sm if abs(sm) > 0.01 else 0

        metrics = (f"  restart={restart} R²={r2:.6f}  MAE={mae*1000:.0f}keV  "
                   f"F̄={fm:.3f} C̄={cm:.3f} S̄={sm:.3f}  "
                   f"F/C={ratio_fc:.3f} C/S={ratio_cs:.3f}")

        if r2 > best_r2:
            best_r2 = r2
            best_model = ThreeScaleModel()
            best_model.load_state_dict(model.state_dict())
            print(f"{metrics} ◄ best")
        else:
            print(metrics)

    return best_model, X_face, X_chan, X_sub, Y


# ═══════════════════════════════════════════════════
# GATE DEPTH SOLVE
# ═══════════════════════════════════════════════════

def solve_abc(face_mev, chan_mev, sub_mev):
    """
    Solve for per-gate-depth energies a, b, c from three scale outputs.

    Gate depth distribution within 64 positions: [27, 27, 9, 1]
    d ≈ 0 (triple gate contributes nothing)

    Each scale's output comes from its fill pattern projected through
    the gate depth structure. The three outputs give:

      face_mev  =  n0_f * a  +  n1_f * b  +  n2_f * c
      chan_mev   =  n0_c * a  +  n1_c * b  +  n2_c * c
      sub_mev   =  n0_s * a  +  n1_s * b  +  n2_s * c

    For a fully filled cycle (a64=64), n0=27, n1=27, n2=9 at all scales.
    For partial fills, the counts differ per scale.

    Simplest solve: assume the proportions follow gate depth distribution
    scaled by the output magnitude.

      a = face_mev / 27  (gd=0 energy from face scale)
      b = chan_mev / 27   (gd=1 energy from channel scale)
      c = sub_mev / 9    (gd=2 energy from subchannel scale)

    This maps each scale to its dominant gate depth:
      Face scale captures gd=0 (pure spatial faces)
      Channel scale captures gd=1 (one gate crossing)
      Subchannel scale captures gd=2 (two gate crossings)
    """
    a = face_mev / 27.0 if abs(face_mev) > 1e-10 else 0.0
    b = chan_mev / 27.0 if abs(chan_mev) > 1e-10 else 0.0
    c = sub_mev / 9.0 if abs(sub_mev) > 1e-10 else 0.0
    return a, b, c


# ═══════════════════════════════════════════════════
# REPORT & EXPORT
# ═══════════════════════════════════════════════════

def report_and_export(model, elements, X_face, X_chan, X_sub, Y, outdir='.'):
    model.eval()

    print(f"\n{'='*90}")
    print(f"  3-SCALE DECOMPOSITION: B/A = Face + Channel + Subchannel")
    print(f"{'='*90}")

    print(f"\n  {'Sym':>3} {'A':>3} {'sh':>2} {'Known':>7} {'Pred':>7} {'ΔkeV':>6} "
          f"{'Face':>7} {'Chan':>7} {'Sub':>7}  {'a':>7} {'b':>7} {'c':>7}")
    print(f"  {'─'*3} {'─'*3} {'─'*2} {'─'*7} {'─'*7} {'─'*6} "
          f"{'─'*7} {'─'*7} {'─'*7}  {'─'*7} {'─'*7} {'─'*7}")

    export = {}
    for i, el in enumerate(elements):
        info = model.get_components(X_face[i], X_chan[i], X_sub[i])
        known = el['ba']
        pred = info['total']
        delta = pred - known
        pct = abs(delta / known) * 100 if known > 0 else 0.0
        flag = " ★" if pct < 0.1 else (" ●" if pct < 0.5 else ("" if pct < 1 else " ✗"))

        fm, cm, sm = info['face_mev'], info['chan_mev'], info['sub_mev']
        a, b, c = solve_abc(fm, cm, sm)

        print(f"  {el['sym']:>3} {el['A']:>3} {el['shell']:>2} {known:>7.3f} {pred:>7.3f} {delta*1000:>+6.0f}"
              f" {fm:>7.3f} {cm:>7.3f} {sm:>7.3f}  {a:>7.4f} {b:>7.4f} {c:>7.4f}{flag}")

        export[el['sym']] = {
            'A': el['A'],
            'shell': el['shell'],
            'known_ba': round(known, 3),
            'pred_ba': round(pred, 4),
            'face_mev': round(fm, 6),
            'chan_mev': round(cm, 6),
            'sub_mev': round(sm, 6),
            'a_gd0': round(a, 6),
            'b_gd1': round(b, 6),
            'c_gd2': round(c, 6),
        }

    # Global stats
    with torch.no_grad():
        bp, ff, cc, ss = model(X_face, X_chan, X_sub)
        errs = (bp - Y).abs()
        pcts = (errs / Y) * 100
        ss_res = ((bp - Y)**2).sum().item()
        ss_tot = ((Y - Y.mean())**2).sum().item()
        r2 = 1 - ss_res / ss_tot

    print(f"\n{'='*90}")
    print(f"  R²  = {r2:.6f}")
    print(f"  MAE = {errs.mean().item()*1000:.1f} keV/n")
    print(f"  Max = {errs.max().item()*1000:.1f} keV/n")
    for t in [0.05, 0.1, 0.5, 1.0]:
        cnt = (pcts <= t).sum().item()
        print(f"  ≤{t:.2f}%: {int(cnt)}/{len(elements)}")

    # Scale statistics
    print(f"\n  Scale contributions (mean ± std across elements):")
    print(f"    Face:       {ff.mean().item():>7.3f} ± {ff.std().item():.3f}")
    print(f"    Channel:    {cc.mean().item():>7.3f} ± {cc.std().item():.3f}")
    print(f"    Subchannel: {ss.mean().item():>7.3f} ± {ss.std().item():.3f}")
    print(f"    Sum check:  {(ff+cc+ss).mean().item():.3f} vs B/A mean {Y.mean().item():.3f}")

    # Depth statistics
    all_a = [export[el['sym']]['a_gd0'] for el in elements]
    all_b = [export[el['sym']]['b_gd1'] for el in elements]
    all_c = [export[el['sym']]['c_gd2'] for el in elements]
    print(f"\n  Gate depth energies (mean ± std):")
    print(f"    a (gd=0): {np.mean(all_a):>7.4f} ± {np.std(all_a):.4f}")
    print(f"    b (gd=1): {np.mean(all_b):>7.4f} ± {np.std(all_b):.4f}")
    print(f"    c (gd=2): {np.mean(all_c):>7.4f} ± {np.std(all_c):.4f}")
    print(f"    Ratio a:b:c = 1 : {np.mean(all_b)/np.mean(all_a):.3f} : {np.mean(all_c)/np.mean(all_a):.3f}")

    # Export JSON
    path = os.path.join(outdir, 'gfd_3scale.json')
    with open(path, 'w') as f:
        json.dump(export, f, indent=2)
    print(f"\n  Exported {path}")

    # Export CSV
    csv_path = os.path.join(outdir, 'gfd_3scale_results.csv')
    with open(csv_path, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['Sym', 'A', 'Shell', 'BA_Known', 'BA_Pred',
                     'Face_MeV', 'Chan_MeV', 'Sub_MeV',
                     'a_gd0', 'b_gd1', 'c_gd2'])
        for el in elements:
            d = export[el['sym']]
            w.writerow([el['sym'], d['A'], d['shell'],
                        d['known_ba'], d['pred_ba'],
                        d['face_mev'], d['chan_mev'], d['sub_mev'],
                        d['a_gd0'], d['b_gd1'], d['c_gd2']])
    print(f"  Exported {csv_path}")

    return export


# ═══════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════

if __name__ == '__main__':
    import sys
    basedir = os.path.dirname(__file__) or '.'
    csv_path = os.path.join(basedir, 'gfd_3scale_vectors.csv')
    print(f"Loading {csv_path}")
    all_elements = load_data(csv_path)
    print(f"Loaded {len(all_elements)} elements")

    if '--all' in sys.argv:
        elements = all_elements
        print(f"--all: training on ALL {len(elements)} elements (no exclusions)\n")
    else:
        EXCLUDE = {'He', 'Li', 'Be', 'B', 'F'}
        elements = [el for el in all_elements if el['sym'] not in EXCLUDE]
        excluded = [el for el in all_elements if el['sym'] in EXCLUDE]
        print(f"Excluded {len(excluded)}: {', '.join(el['sym'] for el in excluded)}")
        print(f"Training on {len(elements)} elements (use --all to include all)\n")

    print("=" * 90)
    print("  TRAINING: B/A = NN_face(16→4→1) + NN_chan(64→4→1) + NN_sub(256→4→1)")
    print("=" * 90)

    model, X_face, X_chan, X_sub, Y = train(
        elements, epochs=80000, lr=0.01, n_restarts=10, print_every=20000
    )

    export = report_and_export(model, elements, X_face, X_chan, X_sub, Y, basedir)

    # Save model
    torch.save(model.state_dict(), os.path.join(basedir, 'gfd_3scale_model.pt'))
    print(f"  Model saved to gfd_3scale_model.pt")
