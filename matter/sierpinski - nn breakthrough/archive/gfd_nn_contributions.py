#!/usr/bin/env python3
"""
GFD Sierpiński Contribution Network
=====================================
Architecture:
  64 inputs (walk fill vector, values 0-4)
      ↓ fully connected
  H hidden nodes (small, learns global context)
      ↓ fully connected  
  64 raw contributions (one per walk position)
      × input (mask: unfilled positions zeroed)
  64 masked contributions
      ↓ sum
  1 scalar = predicted B/A MeV

Training: MSE(Σ masked_contributions, known_B/A)

Result: for each element, 64 numbers that sum to B/A.
Each number = that walk position's MeV contribution in context.
"""

import csv
import json
import torch
import torch.nn as nn
import torch.optim as optim
import os


# ═══════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════

class Element:
    __slots__ = ['sym', 'ba_mev', 'shell', 'vec256', 'vec64']
    def __init__(self, sym, ba_mev, shell, vec256_str):
        self.sym = sym
        self.ba_mev = float(ba_mev)
        self.shell = int(shell)
        self.vec256 = [int(c) for c in vec256_str]
        self.vec64 = [
            self.vec256[i] + self.vec256[i+64] + self.vec256[i+128] + self.vec256[i+192]
            for i in range(64)
        ]

def load_data(csv_path='gfd_sierpinski_256.csv'):
    elements = []
    with open(csv_path, 'r') as f:
        for row in csv.DictReader(f):
            elements.append(Element(row['Sym'], row['BA_MeV'], row['Shell'], row['Vec256']))
    return elements


# ═══════════════════════════════════════════════════
# NETWORK
# ═══════════════════════════════════════════════════

class ContributionNet(nn.Module):
    """
    64 → H hidden → 64 contributions → mask × input → sum → B/A

    The hidden layer sees the full fill pattern (global context).
    The output layer produces 64 per-position energy contributions.
    Masking ensures only filled positions count.
    The sum of masked contributions = predicted B/A.
    """
    def __init__(self, n_hidden=16):
        super().__init__()
        self.hidden = nn.Linear(64, n_hidden)
        self.act = nn.ReLU()
        self.contributions = nn.Linear(n_hidden, 64)

    def forward(self, x):
        h = self.act(self.hidden(x))       # 64 → H → ReLU
        raw = self.contributions(h)          # H → 64 raw contributions
        masked = torch.relu(raw) * (x > 0).float()  # non-negative + zero unfilled
        ba = masked.sum(dim=1, keepdim=True)  # sum → scalar B/A
        return ba, masked, raw

    def get_contributions(self, x):
        """Get per-position contributions for a single element."""
        with torch.no_grad():
            ba, masked, raw = self.forward(x.unsqueeze(0))
            return {
                'ba': ba.item(),
                'contributions': masked.squeeze().numpy(),
                'raw': raw.squeeze().numpy(),
            }


# ═══════════════════════════════════════════════════
# TRAINING
# ═══════════════════════════════════════════════════

def train(elements, n_hidden=16, epochs=80000, lr=0.01, print_every=10000):
    X = torch.tensor([el.vec64 for el in elements], dtype=torch.float32)
    Y = torch.tensor([el.ba_mev for el in elements], dtype=torch.float32).unsqueeze(1)

    best_r2 = -999
    best_model = None

    for restart in range(5):
        torch.manual_seed(restart * 42 + 7)
        model = ContributionNet(n_hidden)
        optimizer = optim.Adam(model.parameters(), lr=lr)
        scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=20000, gamma=0.5)

        for epoch in range(epochs + 1):
            ba_pred, masked, raw = model(X)
            loss = nn.MSELoss()(ba_pred, Y)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            scheduler.step()

            if epoch % print_every == 0 and restart == 0:
                with torch.no_grad():
                    bp, _, _ = model(X)
                    err = (bp - Y).abs()
                    mae = err.mean().item()
                    mx = err.max().item()
                    pcts = (err / Y).abs() * 100
                    w05 = (pcts <= 0.5).sum().item()
                    w1 = (pcts <= 1.0).sum().item()
                    print(f"  ep={epoch:>6d}  MSE={loss.item():.6f}  MAE={mae*1000:.0f}keV  "
                          f"Max={mx:.3f}  ≤0.5%:{w05}/{len(elements)}  ≤1%:{w1}/{len(elements)}")

        with torch.no_grad():
            bp, _, _ = model(X)
            ss_res = ((bp - Y)**2).sum().item()
            ss_tot = ((Y - Y.mean())**2).sum().item()
            r2 = 1 - ss_res / ss_tot

        if r2 > best_r2:
            best_r2 = r2
            best_model = ContributionNet(n_hidden)
            best_model.load_state_dict(model.state_dict())
            print(f"  restart={restart} R²={r2:.6f} ◄ best")
        else:
            print(f"  restart={restart} R²={r2:.6f}")

    return best_model, X, Y


# ═══════════════════════════════════════════════════
# RESULTS
# ═══════════════════════════════════════════════════

def report(model, elements, X, Y):
    model.eval()
    WALK = []
    for fi in range(4):
        for ci in range(4):
            for si in range(4):
                gd = (1 if fi==3 else 0) + (1 if ci==3 else 0) + (1 if si==3 else 0)
                WALK.append((fi, ci, si, gd))

    print(f"\n{'='*80}")
    print(f"  ELEMENT-BY-ELEMENT: Per-position contributions summing to B/A")
    print(f"{'='*80}")

    print(f"\n  {'Sym':>3} {'sh':>2} {'Known':>7} {'Pred':>7} {'Δ keV':>7} {'%':>6}  Top contributors")
    print(f"  {'─'*3} {'─'*2} {'─'*7} {'─'*7} {'─'*7} {'─'*6}  {'─'*40}")

    for i, el in enumerate(elements):
        info = model.get_contributions(X[i])
        ba_pred = info['ba']
        contribs = info['contributions']
        known = el.ba_mev
        delta = ba_pred - known
        pct = abs(delta / known) * 100
        flag = " ★" if pct < 0.1 else (" ●" if pct < 0.5 else ("" if pct < 1 else " ✗"))

        # Top 3 contributors
        nonzero = [(j, contribs[j]) for j in range(64) if abs(contribs[j]) > 0.001]
        nonzero.sort(key=lambda x: -abs(x[1]))
        top3 = nonzero[:3]
        top_str = "  ".join(f"{j}:{'+'if c>=0 else ''}{c:.3f}" for j, c in top3)

        print(f"  {el.sym:>3} {el.shell:>2} {known:>7.3f} {ba_pred:>7.3f} {delta*1000:>+7.0f} {pct:>5.2f}%{flag}  {top_str}")

    # Global stats
    with torch.no_grad():
        bp, _, _ = model(X)
        errs = (bp - Y).abs()
        pcts = (errs / Y) * 100
        ss_res = ((bp - Y)**2).sum().item()
        ss_tot = ((Y - Y.mean())**2).sum().item()
        r2 = 1 - ss_res / ss_tot

    print(f"\n{'='*80}")
    print(f"  R²  = {r2:.6f}")
    print(f"  MAE = {errs.mean().item()*1000:.1f} keV/n")
    print(f"  Max = {errs.max().item()*1000:.1f} keV/n")
    for t in [0.05, 0.1, 0.5, 1.0]:
        c = (pcts <= t).sum().item()
        print(f"  ≤{t:.2f}%: {int(c)}/{len(elements)}")

    # Show one full element breakdown
    print(f"\n{'='*80}")
    print(f"  FULL BREAKDOWN: Iron (Fe)")
    print(f"{'='*80}")
    fe_idx = next(i for i, el in enumerate(elements) if el.sym == 'Fe')
    info = model.get_contributions(X[fe_idx])
    contribs = info['contributions']
    running = 0
    print(f"\n  {'Step':>4} {'F':>2} {'C':>2} {'S':>2} {'gd':>2} {'MeV/n':>8} {'Running':>8}")
    print(f"  {'─'*4} {'─'*2} {'─'*2} {'─'*2} {'─'*2} {'─'*8} {'─'*8}")
    for j in range(64):
        c = contribs[j]
        if abs(c) < 0.0001:
            continue
        fi, ci, si, gd = WALK[j]
        running += c
        marker = " ◄" if abs(c) > 0.2 else ""
        print(f"  {j:>4} {fi:>2} {ci:>2} {si:>2} {gd:>2} {c:>+8.4f} {running:>8.3f}{marker}")
    print(f"\n  Total: {info['ba']:.4f} MeV/n  (Known: {elements[fe_idx].ba_mev:.3f})")


def export_contributions(_, elements, model, X, outdir='.'):
    """Export per-element contributions as JSON and CSV for the HTML viewer."""
    model.eval()
    export = {}
    for i, el in enumerate(elements):
        info = model.get_contributions(X[i])
        export[el.sym] = [round(float(c), 6) for c in info['contributions']]

    path = os.path.join(outdir, 'gfd_contributions.json')
    with open(path, 'w') as f:
        json.dump(export, f)
    print(f"\n  Exported {path}")

    # Also CSV: rows=elements, columns=positions
    csv_path = os.path.join(outdir, 'gfd_contributions.csv')
    with open(csv_path, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['Sym', 'BA_Known', 'BA_Pred'] + [f'c{i}' for i in range(64)])
        for i, el in enumerate(elements):
            info = model.get_contributions(X[i])
            contribs = info['contributions']
            w.writerow([el.sym, f'{el.ba_mev:.3f}', f'{info["ba"]:.4f}'] +
                       [f'{c:.6f}' for c in contribs])
    print(f"  Exported {csv_path}")

    return export


# ═══════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════

if __name__ == '__main__':
    basedir = os.path.dirname(__file__) or '.'
    csv_path = os.path.join(basedir, 'gfd_sierpinski_256.csv')
    print(f"Loading {csv_path}")
    all_elements = load_data(csv_path)
    print(f"Loaded {len(all_elements)} elements")

    EXCLUDE = {'He', 'Li', 'Be', 'B', 'F'}
    elements = [el for el in all_elements if el.sym not in EXCLUDE]
    excluded = [el for el in all_elements if el.sym in EXCLUDE]
    print(f"Excluded {len(excluded)}: {', '.join(el.sym for el in excluded)}")
    print(f"Training on {len(elements)} elements\n")

    # Try multiple hidden sizes
    print("=" * 80)
    print("  TRAINING: 64 → H → 64 → mask → sum")
    print("=" * 80)

    best_r2 = -999
    best_result = None

    for nh in [4, 8, 16]:
        print(f"\n  ── Hidden = {nh} ──")
        model, X, Y = train(elements, n_hidden=nh, epochs=80000, lr=0.01, print_every=20000)

        with torch.no_grad():
            bp, _, _ = model(X)
            ss_res = ((bp - Y)**2).sum().item()
            ss_tot = ((Y - Y.mean())**2).sum().item()
            r2 = 1 - ss_res / ss_tot

        if r2 > best_r2:
            best_r2 = r2
            best_result = (model, X, Y, nh)

    model, X, Y, nh = best_result
    print(f"\n\n  BEST: hidden={nh}, R²={best_r2:.6f}")

    report(model, elements, X, Y)
    export_contributions(None, elements, model, X, basedir)

    # Save model weights
    torch.save(model.state_dict(), os.path.join(basedir, 'gfd_contribution_model.pt'))
    print(f"  Model saved to gfd_contribution_model.pt")
