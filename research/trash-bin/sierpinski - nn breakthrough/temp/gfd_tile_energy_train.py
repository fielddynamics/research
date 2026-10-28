#!/usr/bin/env python3
"""
GFD Per-Tile Energy: ε × A = BE
=================================
The network outputs energy per tile (ε).
The prediction is: BE = A × ε, so B/A = ε.

This forces the network to learn per-tile coupling,
not memorize B/A directly.

Training loss: (A × ε − known_BE)²
"""

import csv, json, torch, torch.nn as nn, torch.optim as optim, os, sys
import numpy as np

def load_data(csv_path):
    elements = []
    with open(csv_path, 'r') as f:
        for row in csv.DictReader(f):
            vec256 = [float(c) for c in row['Vec256']]
            A = int(row['A'])
            ba = float(row['BA_MeV'])
            elements.append({
                'sym': row['Sym'], 'A': A,
                'ba': ba, 'be': ba * A,
                'shell': int(row['Shell']),
                'sub': vec256,
            })
    return elements

class TileEnergyModel(nn.Module):
    """
    256-dim walk vector → 12 hidden → 1 output (ε = energy per tile).
    Physical prediction: BE = A × ε, B/A = ε.
    """
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(256, 12),
            nn.ReLU(),
            nn.Linear(12, 1),
        )

    def forward(self, x):
        return self.net(x)  # returns ε per tile

def train(elements, epochs=80000, lr=0.01, n_restarts=10, print_every=20000):
    X = torch.tensor([el['sub'] for el in elements], dtype=torch.float32)
    A_vec = torch.tensor([el['A'] for el in elements], dtype=torch.float32).unsqueeze(1)
    Y_BE = torch.tensor([el['be'] for el in elements], dtype=torch.float32).unsqueeze(1)
    Y_BA = torch.tensor([el['ba'] for el in elements], dtype=torch.float32).unsqueeze(1)

    best_r2 = -999
    best_model = None

    for restart in range(n_restarts):
        torch.manual_seed(restart * 97 + int(torch.randint(0, 1000000, (1,)).item()))
        model = TileEnergyModel()
        optimizer = optim.Adam(model.parameters(), lr=lr)
        scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=20000, gamma=0.5)

        for epoch in range(epochs + 1):
            eps = model(X)              # energy per tile
            pred_BE = A_vec * eps       # total BE = A × ε
            loss = nn.MSELoss()(pred_BE, Y_BE)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            scheduler.step()

            if epoch % print_every == 0 and restart == 0:
                with torch.no_grad():
                    e = model(X)
                    p_be = A_vec * e
                    p_ba = e  # B/A = ε
                    err_ba = (p_ba - Y_BA).abs()
                    mae = err_ba.mean().item()
                    mx = err_ba.max().item()
                    err_be = (p_be - Y_BE).abs()
                    mae_be = err_be.mean().item()
                    pcts = (err_ba / Y_BA).abs() * 100
                    w05 = (pcts <= 0.5).sum().item()
                    w1 = (pcts <= 1.0).sum().item()
                    print(f"  ep={epoch:>6d}  MSE_BE={loss.item():.2f}  "
                          f"MAE_BA={mae*1000:.0f}keV  MAE_BE={mae_be:.0f}keV  "
                          f"Max_BA={mx:.3f}  ≤0.5%:{w05}/{len(elements)}  ≤1%:{w1}/{len(elements)}")

        with torch.no_grad():
            e = model(X)
            p_ba = e
            ss_res = ((p_ba - Y_BA)**2).sum().item()
            ss_tot = ((Y_BA - Y_BA.mean())**2).sum().item()
            r2 = 1 - ss_res / ss_tot
            mae = (p_ba - Y_BA).abs().mean().item()

        m = f"  restart={restart} R²={r2:.6f}  MAE_BA={mae*1000:.0f}keV"
        if r2 > best_r2:
            best_r2 = r2
            best_model = TileEnergyModel()
            best_model.load_state_dict(model.state_dict())
            print(f"{m} ◄ best")
        else:
            print(m)

    return best_model, X, A_vec, Y_BE, Y_BA

def report(model, elements, X, A_vec, Y_BE, Y_BA):
    model.eval()

    print(f"\n{'='*90}")
    print(f"  PER-TILE ENERGY: ε × A = BE")
    print(f"{'='*90}")

    print(f"\n  {'Sym':>3} {'A':>3} {'Known BA':>8} {'ε (per tile)':>12} {'A×ε':>8} "
          f"{'Known BE':>8} {'ΔBE':>7} {'ΔBA':>7}")
    print(f"  {'─'*3} {'─'*3} {'─'*8} {'─'*12} {'─'*8} "
          f"{'─'*8} {'─'*7} {'─'*7}")

    with torch.no_grad():
        for i, el in enumerate(elements):
            eps = model(X[i].unsqueeze(0)).item()
            pred_be = el['A'] * eps
            pred_ba = eps
            delta_be = pred_be - el['be']
            delta_ba = pred_ba - el['ba']
            pct = abs(delta_ba / el['ba']) * 100 if el['ba'] > 0 else 0
            flag = " ★" if pct < 0.1 else (" ●" if pct < 0.5 else "")

            print(f"  {el['sym']:>3} {el['A']:>3} {el['ba']:>8.3f} {eps:>12.6f} "
                  f"{pred_be:>8.2f} {el['be']:>8.2f} {delta_be*1000:>+6.0f} "
                  f"{delta_ba*1000:>+6.0f}{flag}")

    # Stats
    with torch.no_grad():
        e = model(X)
        p_ba = e
        p_be = A_vec * e
        err_ba = (p_ba - Y_BA).abs()
        err_be = (p_be - Y_BE).abs()
        pcts = (err_ba / Y_BA) * 100
        ss_res = ((p_ba - Y_BA)**2).sum().item()
        ss_tot = ((Y_BA - Y_BA.mean())**2).sum().item()
        r2 = 1 - ss_res / ss_tot

    print(f"\n{'='*90}")
    print(f"  R² (B/A)  = {r2:.6f}")
    print(f"  MAE (B/A) = {err_ba.mean().item()*1000:.1f} keV/n")
    print(f"  MAE (BE)  = {err_be.mean().item()*1000:.1f} keV")
    print(f"  Max (B/A) = {err_ba.max().item()*1000:.1f} keV/n")
    for t in [0.05, 0.1, 0.5, 1.0]:
        cnt = (pcts <= t).sum().item()
        print(f"  ≤{t:.2f}%: {int(cnt)}/{len(elements)}")

    print(f"\n  ε statistics:")
    eps_all = e.numpy().flatten()
    print(f"    Mean ε = {np.mean(eps_all):.4f} MeV/tile")
    print(f"    Min ε  = {np.min(eps_all):.4f} ({elements[np.argmin(eps_all)]['sym']})")
    print(f"    Max ε  = {np.max(eps_all):.4f} ({elements[np.argmax(eps_all)]['sym']})")
    print(f"    ε(Zn)  = {eps_all[[i for i,el in enumerate(elements) if el['sym']=='Zn'][0]]:.6f}")
    print(f"    ε(Pb)  = {eps_all[[i for i,el in enumerate(elements) if el['sym']=='Pb'][0]]:.6f}")

    print(f"\n  COMPARISON:")
    print(f"  3-scale (3 outputs summed):     R² = 0.999986  MAE = 0.8 keV")
    print(f"  1-scale (1 output = B/A):        R² = 0.999986  MAE = 0.8 keV")
    print(f"  Per-tile (ε × A = BE):           R² = {r2:.6f}  MAE = {err_ba.mean().item()*1000:.1f} keV")

if __name__ == '__main__':
    basedir = os.path.dirname(__file__) or '.'
    csv_path = os.path.join(basedir, 'gfd_3scale_vectors.csv')
    print(f"Loading {csv_path}")
    elements = load_data(csv_path)
    print(f"Loaded {len(elements)} elements\n")

    print("=" * 90)
    print("  TRAINING: ε × A = BE  where ε = NN(256→12→1)")
    print("  Loss = (A × ε − known_BE)²")
    print("  Network learns energy per tile, physics provides A × ε = BE")
    print("=" * 90)

    model, X, A_vec, Y_BE, Y_BA = train(elements, epochs=80000, lr=0.01, n_restarts=10)
    report(model, elements, X, A_vec, Y_BE, Y_BA)

    torch.save(model.state_dict(), os.path.join(basedir, 'gfd_tile_energy_model.pt'))
    print(f"\n  Model saved to gfd_tile_energy_model.pt")
