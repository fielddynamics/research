#!/usr/bin/env python3
"""
GFD Sierpiński Neural Binding Energy
=====================================
Reads gfd_sierpinski_256.csv, collapses Vec256 into a 64-dim vector
where each dimension = number of shells that filled that walk position (0–4).

Architecture:
  64 inputs (one per walk position)
     │  1-to-1 (diagonal, NOT fully connected)
  64 hidden nodes (each sees only its own position)
     │  all-to-one
  1 output (B/A MeV)

Each walk position learns its own energy contribution independently,
then the output sums them.
"""

import csv
import torch
import torch.nn as nn
import torch.optim as optim
import os


# ═══════════════════════════════════════════════════
# DATA OBJECT
# ═══════════════════════════════════════════════════

class Element:
    __slots__ = ['sym', 'ba_mev', 'shell', 'vec256', 'vec64']

    def __init__(self, sym, ba_mev, shell, vec256_str):
        self.sym = sym
        self.ba_mev = float(ba_mev)
        self.shell = int(shell)
        self.vec256 = [int(c) for c in vec256_str]
        # Collapse 256 → 64: sum across 4 shells per walk position
        # Position i gets vec256[i] + vec256[i+64] + vec256[i+128] + vec256[i+192]
        # Value = how many times this position has been traversed (0–4)
        self.vec64 = [
            self.vec256[i] + self.vec256[i+64] + self.vec256[i+128] + self.vec256[i+192]
            for i in range(64)
        ]

    def __repr__(self):
        return f"Element({self.sym}, B/A={self.ba_mev:.3f}, shell={self.shell})"


# ═══════════════════════════════════════════════════
# LOAD DATA
# ═══════════════════════════════════════════════════

def load_data(csv_path='gfd_sierpinski_256.csv'):
    elements = []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            el = Element(
                sym=row['Sym'],
                ba_mev=row['BA_MeV'],
                shell=row['Shell'],
                vec256_str=row['Vec256'],
            )
            elements.append(el)
    return elements


# ═══════════════════════════════════════════════════
# NEURAL NETWORK: 1-to-1 → sum
# ═══════════════════════════════════════════════════

class DiagonalLayer(nn.Module):
    """Each input i connects only to hidden node i. No cross-connections."""
    def __init__(self, n):
        super().__init__()
        self.weight = nn.Parameter(torch.randn(n) * 0.1)
        self.bias = nn.Parameter(torch.zeros(n))

    def forward(self, x):
        return x * self.weight + self.bias


class SierpinskiNet(nn.Module):
    """
    64 inputs → 64 hidden (1-to-1 diagonal) → ReLU → 1 output (sum)

    Each walk position gets its own independent weight and bias,
    then a nonlinearity, then they all feed into the output.
    """
    def __init__(self):
        super().__init__()
        self.diag = DiagonalLayer(64)
        self.act = nn.ReLU()
        self.out = nn.Linear(64, 1)

    def forward(self, x):
        h = self.diag(x)        # 64 → 64 (1-to-1)
        h = self.act(h)          # ReLU per position
        return self.out(h)       # 64 → 1


# ═══════════════════════════════════════════════════
# TRAINING
# ═══════════════════════════════════════════════════

def train(elements, epochs=50000, lr=0.01, print_every=5000):
    # Build tensors
    X = torch.tensor([el.vec64 for el in elements], dtype=torch.float32)
    Y = torch.tensor([el.ba_mev for el in elements], dtype=torch.float32).unsqueeze(1)

    model = SierpinskiNet()
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=15000, gamma=0.5)

    print(f"{'epoch':>7}  {'MSE':>10}  {'MAE keV':>8}  {'MaxErr':>8}  {'≤0.5%':>6}  {'≤1%':>5}")
    print(f"{'─'*7}  {'─'*10}  {'─'*8}  {'─'*8}  {'─'*6}  {'─'*5}")

    for epoch in range(epochs + 1):
        pred = model(X)
        loss = criterion(pred, Y)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        scheduler.step()

        if epoch % print_every == 0 or epoch == epochs:
            with torch.no_grad():
                p = model(X)
                err = (p - Y).abs()
                mae = err.mean().item()
                mx = err.max().item()
                pcts = (err / Y).abs() * 100
                w05 = (pcts <= 0.5).sum().item()
                w1 = (pcts <= 1.0).sum().item()
                print(f"{epoch:>7}  {loss.item():>10.6f}  {mae*1000:>7.1f}  {mx:>8.4f}  "
                      f"{w05:>4}/{len(elements)}  {w1:>3}/{len(elements)}")

    return model, X, Y


# ═══════════════════════════════════════════════════
# RESULTS
# ═══════════════════════════════════════════════════

def report(model, elements, X, Y):
    model.eval()
    with torch.no_grad():
        pred = model(X).squeeze()

    print(f"\n{'='*70}")
    print(f"  ELEMENT-BY-ELEMENT RESULTS")
    print(f"{'='*70}")
    print(f"\n  {'Z':>3} {'Sym':>3} {'Known':>7} {'Pred':>7} {'Δ keV':>7} {'%err':>6}")
    print(f"  {'─'*3} {'─'*3} {'─'*7} {'─'*7} {'─'*7} {'─'*6}")

    for i, el in enumerate(elements):
        p = pred[i].item()
        d = p - el.ba_mev
        pct = abs(d / el.ba_mev) * 100
        flag = " ★" if pct < 0.1 else (" ●" if pct < 0.5 else ("" if pct < 1 else " ✗"))
        print(f"  {i+2:>3} {el.sym:>3} {el.ba_mev:>7.3f} {p:>7.3f} {d*1000:>+7.1f} {pct:>5.2f}%{flag}")

    # Stats
    errs = (pred - Y.squeeze()).abs()
    pcts = (errs / Y.squeeze()) * 100
    ss_res = ((pred - Y.squeeze())**2).sum().item()
    ss_tot = ((Y.squeeze() - Y.mean())**2).sum().item()
    r2 = 1 - ss_res / ss_tot

    print(f"\n  R²  = {r2:.6f}")
    print(f"  MAE = {errs.mean().item()*1000:.1f} keV/n")
    print(f"  Max = {errs.max().item()*1000:.1f} keV/n")
    print(f"\n  Distribution:")
    for t in [0.05, 0.1, 0.2, 0.5, 1.0]:
        c = (pcts <= t).sum().item()
        print(f"    ≤{t:.2f}%: {c:>2}/{len(elements)}")


def inspect_weights(model):
    """Show what each walk position learned."""
    print(f"\n{'='*70}")
    print(f"  LEARNED WEIGHTS PER WALK POSITION")
    print(f"{'='*70}")

    WALK_ORDER = []
    for fi in range(4):
        for ci in range(4):
            for si in range(4):
                gd = (1 if fi==3 else 0) + (1 if ci==3 else 0) + (1 if si==3 else 0)
                WALK_ORDER.append((fi, ci, si, gd))

    diag_w = model.diag.weight.detach().numpy()
    diag_b = model.diag.bias.detach().numpy()
    out_w = model.out.weight.detach().numpy().squeeze()
    out_b = model.out.bias.detach().item()

    print(f"\n  {'Idx':>3} {'F':>2} {'C':>2} {'S':>2} {'gd':>2}  {'diag_w':>8} {'diag_b':>8} {'out_w':>8}  {'effective':>10}")
    print(f"  {'─'*3} {'─'*2} {'─'*2} {'─'*2} {'─'*2}  {'─'*8} {'─'*8} {'─'*8}  {'─'*10}")

    for i in range(64):
        fi, ci, si, gd = WALK_ORDER[i]
        eff = diag_w[i] * out_w[i]  # approximate effective weight
        print(f"  {i:>3} {fi:>2} {ci:>2} {si:>2} {gd:>2}  {diag_w[i]:>8.4f} {diag_b[i]:>8.4f} {out_w[i]:>8.4f}  {eff:>10.4f}")

    print(f"\n  Output bias: {out_b:.4f}")

    # Summary by gate depth
    print(f"\n  By gate depth:")
    for gd in range(4):
        idx = [i for i in range(64) if WALK_ORDER[i][3] == gd]
        effs = [diag_w[i] * out_w[i] for i in idx]
        print(f"    gd={gd}: mean_eff={sum(effs)/len(effs):.4f} "
              f"min={min(effs):.4f} max={max(effs):.4f} ({len(idx)} positions)")


# ═══════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════

if __name__ == '__main__':
    csv_path = os.path.join(os.path.dirname(__file__) or '.', 'gfd_sierpinski_256.csv')
    print(f"Loading {csv_path}")
    all_elements = load_data(csv_path)
    print(f"Loaded {len(all_elements)} elements")

    # Filter out light-element outliers
    EXCLUDE = {'He', 'Li', 'Be', 'B', 'F'}
    elements = [el for el in all_elements if el.sym not in EXCLUDE]
    excluded = [el for el in all_elements if el.sym in EXCLUDE]
    print(f"Excluded {len(excluded)}: {', '.join(el.sym for el in excluded)}")
    print(f"Training on {len(elements)} elements\n")

    # Show a few
    for el in [elements[0], elements[20], elements[-1]]:
        v_str = ''.join(str(x) for x in el.vec64)
        print(f"  {el.sym:>3} shell={el.shell} vec64={v_str}  B/A={el.ba_mev:.3f}")
    print()

    model, X, Y = train(elements, epochs=50000, lr=0.01)
    report(model, elements, X, Y)
    inspect_weights(model)
