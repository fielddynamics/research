#!/usr/bin/env python3
"""
GFD Sub-Only Test: B/A = NN(256→12→1)
=======================================
Only the 256-dim subchannel walk vector. No face, no channel.
If this matches R²=0.999986, the hierarchical decomposition is redundant.
"""

import csv, json, torch, torch.nn as nn, torch.optim as optim, os, sys
import numpy as np

def load_data(csv_path):
    elements = []
    with open(csv_path, 'r') as f:
        for row in csv.DictReader(f):
            vec256 = [float(c) for c in row['Vec256']]
            elements.append({
                'sym': row['Sym'], 'A': int(row['A']),
                'ba': float(row['BA_MeV']), 'shell': int(row['Shell']),
                'sub': vec256,
            })
    return elements

class SubOnlyModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(256, 12),
            nn.ReLU(),
            nn.Linear(12, 1),
        )
    def forward(self, x):
        return self.net(x)

def train(elements, epochs=80000, lr=0.01, n_restarts=10, print_every=20000):
    X = torch.tensor([el['sub'] for el in elements], dtype=torch.float32)
    Y = torch.tensor([el['ba'] for el in elements], dtype=torch.float32).unsqueeze(1)

    best_r2 = -999
    best_model = None

    for restart in range(n_restarts):
        torch.manual_seed(restart * 97 + int(torch.randint(0, 1000000, (1,)).item()))
        model = SubOnlyModel()
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
            mae = (bp - Y).abs().mean().item()

        m = f"  restart={restart} R²={r2:.6f}  MAE={mae*1000:.0f}keV"
        if r2 > best_r2:
            best_r2 = r2
            best_model = SubOnlyModel()
            best_model.load_state_dict(model.state_dict())
            print(f"{m} ◄ best")
        else:
            print(m)

    return best_model, X, Y

if __name__ == '__main__':
    basedir = os.path.dirname(__file__) or '.'
    csv_path = os.path.join(basedir, 'gfd_3scale_vectors.csv')
    print(f"Loading {csv_path}")
    elements = load_data(csv_path)
    print(f"Loaded {len(elements)} elements")
    print(f"--all: training on ALL {len(elements)} elements\n")

    print("=" * 90)
    print("  TRAINING: B/A = NN(256→12→1)  [sub-channel vector only, no face/chan]")
    print("=" * 90)

    model, X, Y = train(elements, epochs=80000, lr=0.01, n_restarts=10)

    # Final stats
    model.eval()
    with torch.no_grad():
        bp = model(X)
        errs = (bp - Y).abs()
        ss_res = ((bp - Y)**2).sum().item()
        ss_tot = ((Y - Y.mean())**2).sum().item()
        r2 = 1 - ss_res / ss_tot

    print(f"\n{'='*90}")
    print(f"  RESULT: Sub-only 256→12→1")
    print(f"  R²  = {r2:.6f}")
    print(f"  MAE = {errs.mean().item()*1000:.1f} keV/n")
    print(f"  Max = {errs.max().item()*1000:.1f} keV/n")
    print(f"\n  COMPARISON:")
    print(f"  3-scale (16→4 + 64→4 + 256→4 = 3 outputs): R² = 0.999986  MAE = 1 keV")
    print(f"  1-scale combined (336→12→1):                 R² = 0.999986  MAE = 1 keV")
    print(f"  Sub-only (256→12→1):                         R² = {r2:.6f}  MAE = {errs.mean().item()*1000:.0f} keV")
    if r2 > 0.99998:
        print(f"\n  ✓ Sub-only MATCHES → face and channel vectors are redundant")
        print(f"    The 256-dim walk vector contains ALL the information.")
    elif r2 > 0.9999:
        print(f"\n  ~ Sub-only is CLOSE → face/channel add minor information")
    else:
        print(f"\n  ✗ Sub-only WORSE → hierarchical structure IS needed")
    print(f"{'='*90}")

    torch.save(model.state_dict(), os.path.join(basedir, 'gfd_subonly_model.pt'))
    print(f"  Model saved to gfd_subonly_model.pt")
