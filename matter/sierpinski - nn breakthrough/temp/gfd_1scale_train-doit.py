#!/usr/bin/env python3
"""
GFD Single-Scale Test: B/A = NN(256) × 64
=============================================
One neural network, one output: energy per position.

  NN: 256-dim input → 4 hidden → 1 output  (energy per position)
  B/A_predicted = output

If gate depth doesn't matter (a ≈ b ≈ c ≈ d), this single network
should achieve the same R² = 0.999986 as the three-network model.

The output × 64 gives the total sector energy budget.
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
            sub256 = [float(b) for b in vec256]

            # Concatenate all three views: 16 + 64 + 256 = 336
            combined = face16 + chan64 + sub256

            elements.append({
                'sym': sym, 'A': A, 'ba': ba, 'shell': shell,
                'combined': combined,
            })
    return elements


# ═══════════════════════════════════════════════════
# NETWORK
# ═══════════════════════════════════════════════════

class SingleScaleModel(nn.Module):
    """
    One network: 336-dim combined vector → 12 hidden → 1 output.
    Input = face(16) + chan(64) + sub(256) concatenated.
    Same total hidden units as the 3-scale model (3 × 4 = 12).
    Output = B/A predicted.
    """
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(336, 12),
            nn.ReLU(),
            nn.Linear(12, 1),
        )

    def forward(self, x):
        return self.net(x)


# ═══════════════════════════════════════════════════
# TRAINING
# ═══════════════════════════════════════════════════

def train(elements, epochs=80000, lr=0.01, n_restarts=10, print_every=20000):
    X = torch.tensor([el['combined'] for el in elements], dtype=torch.float32)
    Y = torch.tensor([el['ba'] for el in elements], dtype=torch.float32).unsqueeze(1)

    best_r2 = -999
    best_model = None

    for restart in range(n_restarts):
        torch.manual_seed(restart * 97 + int(torch.randint(0, 1000000, (1,)).item()))
        model = SingleScaleModel()
        optimizer = optim.Adam(model.parameters(), lr=lr)
        scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=20000, gamma=0.5)

        for epoch in range(epochs + 1):
            pred = model(X)
            loss = nn.MSELoss()(pred, Y)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            scheduler.step()

            if epoch % print_every == 0 and restart == 0:
                with torch.no_grad():
                    bp = model(X)
                    err = (bp - Y).abs()
                    mae = err.mean().item()
                    mx = err.max().item()
                    pcts = (err / Y).abs() * 100
                    w05 = (pcts <= 0.5).sum().item()
                    w1 = (pcts <= 1.0).sum().item()
                    print(f"  ep={epoch:>6d}  MSE={loss.item():.6f}  MAE={mae*1000:.0f}keV  "
                          f"Max={mx:.3f}  ≤0.5%:{w05}/{len(elements)}  ≤1%:{w1}/{len(elements)}")

        with torch.no_grad():
            bp = model(X)
            ss_res = ((bp - Y)**2).sum().item()
            ss_tot = ((Y - Y.mean())**2).sum().item()
            r2 = 1 - ss_res / ss_tot
            err = (bp - Y).abs()
            mae = err.mean().item()

        metrics = f"  restart={restart} R²={r2:.6f}  MAE={mae*1000:.0f}keV"

        if r2 > best_r2:
            best_r2 = r2
            best_model = SingleScaleModel()
            best_model.load_state_dict(model.state_dict())
            print(f"{metrics} ◄ best")
        else:
            print(metrics)

    return best_model, X, Y


# ═══════════════════════════════════════════════════
# REPORT
# ═══════════════════════════════════════════════════

def report(model, elements, X, Y, outdir='.'):
    model.eval()

    print(f"\n{'='*90}")
    print(f"  SINGLE-SCALE RESULT: B/A = NN(336→12→1)")
    print(f"  Input = face(16) + chan(64) + sub(256) concatenated")
    print(f"{'='*90}")

    print(f"\n  {'Sym':>3} {'A':>3} {'sh':>2} {'Known':>7} {'Pred':>7} {'ΔkeV':>6} "
          f"{'Out×64':>8} {'ε/pos':>8}")
    print(f"  {'─'*3} {'─'*3} {'─'*2} {'─'*7} {'─'*7} {'─'*6} "
          f"{'─'*8} {'─'*8}")

    export = {}
    with torch.no_grad():
        for i, el in enumerate(elements):
            pred_ba = model(X[i].unsqueeze(0)).item()
            known = el['ba']
            delta = pred_ba - known
            sector_energy = pred_ba * 64
            eps_per_pos = pred_ba  # B/A IS the energy per position in a full sector

            pct = abs(delta / known) * 100 if known > 0 else 0.0
            flag = " ★" if pct < 0.1 else (" ●" if pct < 0.5 else ("" if pct < 1 else " ✗"))

            print(f"  {el['sym']:>3} {el['A']:>3} {el['shell']:>2} {known:>7.3f} {pred_ba:>7.3f} "
                  f"{delta*1000:>+6.0f} {sector_energy:>8.2f} {eps_per_pos:>8.4f}{flag}")

            export[el['sym']] = {
                'A': el['A'], 'shell': el['shell'],
                'known_ba': round(known, 3),
                'pred_ba': round(pred_ba, 4),
                'sector_energy_x64': round(sector_energy, 3),
                'energy_per_position': round(eps_per_pos, 6),
            }

    # Global stats
    with torch.no_grad():
        bp = model(X)
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

    print(f"\n  COMPARISON TO 3-SCALE MODEL:")
    print(f"  3-scale: R² = 0.999986, MAE = 0.8 keV/n")
    print(f"  1-scale: R² = {r2:.6f}, MAE = {errs.mean().item()*1000:.1f} keV/n")
    if r2 > 0.99998:
        print(f"  ✓ Single network MATCHES 3-network → gate depth carries no energy information")
    elif r2 > 0.9999:
        print(f"  ~ Single network is CLOSE but not identical → small gate depth signal may exist")
    else:
        print(f"  ✗ Single network WORSE → gate depth DOES carry energy information")

    # Export JSON
    path = os.path.join(outdir, 'gfd_1scale.json')
    with open(path, 'w') as f:
        json.dump(export, f, indent=2)
    print(f"\n  Exported {path}")

    # Export CSV
    csv_path = os.path.join(outdir, 'gfd_1scale_results.csv')
    with open(csv_path, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['Sym', 'A', 'Shell', 'BA_Known', 'BA_Pred',
                     'Sector_Energy_x64', 'Energy_Per_Position'])
        for el in elements:
            d = export[el['sym']]
            w.writerow([el['sym'], d['A'], d['shell'],
                        d['known_ba'], d['pred_ba'],
                        d['sector_energy_x64'], d['energy_per_position']])
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
    print("  TRAINING: B/A = NN_single(336→12→1)  [one output, all inputs combined]")
    print("  Same input data, same total hidden units as 3-scale model")
    print("=" * 90)

    model, X, Y = train(
        elements, epochs=80000, lr=0.01, n_restarts=10, print_every=20000
    )

    export = report(model, elements, X, Y, basedir)

    # Save model
    torch.save(model.state_dict(), os.path.join(basedir, 'gfd_1scale_model.pt'))
    print(f"  Model saved to gfd_1scale_model.pt")
