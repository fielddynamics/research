#!/usr/bin/env python3
"""
GFD Gate Depth NN: a=b=c locked, d free
==========================================
B/A = 27a + 27a + 9a + 1d = 63a + d

63 non-gate positions contribute equally.
1 triple-gate position is unconstrained.

Two unknowns, 28 data points. Zero degeneracy.

Part 1: Analytical (linear regression)
Part 2: NN confirmation (should converge to same answer every seed)

Stephen Nelson — Gravity Field Dynamics
"""

import csv
import numpy as np
import torch
import torch.nn as nn
import time

# ═══════════════════════════════════════
# LOAD DATA
# ═══════════════════════════════════════

data = []
with open('gfd_fill_ratios_A1_64.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        ba = row['BA_MeV'].strip()
        if ba == '':
            continue
        data.append({
            'A': int(row['A']),
            'BA': float(ba),
            'inputs': [
                float(row['face_pct']),
                float(row['chan_pct']),
                float(row['sub_pct']),
            ],
        })

print(f"Loaded {len(data)} elements with known B/A")
print(f"A range: {data[0]['A']} to {data[-1]['A']}")
print(f"B/A range: {min(d['BA'] for d in data):.3f} to {max(d['BA'] for d in data):.3f}")

n_el = len(data)
BAs = np.array([d['BA'] for d in data])

syms_map = {
    4:'He',7:'Li',9:'Be',11:'B',12:'C',14:'N',16:'O',19:'F',20:'Ne',
    23:'Na',24:'Mg',27:'Al',28:'Si',31:'P',32:'S',35:'Cl',39:'K',40:'Ar/Ca',
    45:'Sc',48:'Ti',51:'V',52:'Cr',55:'Mn',56:'Fe',58:'Ni',59:'Co',
    63:'Cu',64:'Zn',
}

M_E = 0.51099895
K = 4
F_ZERO = K*K + 1  # 17


# ═══════════════════════════════════════
# PART 1: ANALYTICAL SOLUTION
# B/A = 63a + d  →  linear regression
# ═══════════════════════════════════════

print(f"\n{'='*90}")
print(f"  PART 1: ANALYTICAL — B/A = 63a + d")
print(f"  a=b=c (locked), d free. 2 unknowns, {n_el} data points.")
print(f"{'='*90}")

# For each element, we need the mask to know how many
# of the 63 non-gate positions and 1 gate position are filled
def gate_depth(i):
    F = i // 16
    C = (i % 16) // 4
    S = i % 4
    return sum(1 for x in (F, C, S) if x == 3)

def masks(A):
    m = [0, 0, 0, 0]
    for i in range(min(A, 64)):
        m[gate_depth(i)] += 1
    return m

# B_total = A × B/A = n_nongd3 × a_total + n_gd3 × d
# where n_nongd3 = n0 + n1 + n2, a_total contributes as (27+27+9)/63 per position
# Actually simpler: B/A = 63a + d only holds at A=64.
# For partial fill: B_total = (n0+n1+n2) × a_uniform + n3 × d
# where a_uniform is the same for all non-gate positions
# B/A = [(n0+n1+n2) × a_uniform + n3 × d] / A

# Build regression: B/A × A = n_nongate × a + n_gate × d
X_an = np.zeros((n_el, 2))
Y_an = np.zeros(n_el)

for i, d_el in enumerate(data):
    A = d_el['A']
    m = masks(A)
    n_nongate = m[0] + m[1] + m[2]  # positions at gd=0,1,2
    n_gate = m[3]                     # positions at gd=3
    X_an[i] = [n_nongate, n_gate]
    Y_an[i] = d_el['BA'] * A  # B_total

coeffs_an = np.linalg.lstsq(X_an, Y_an, rcond=None)[0]
a_an, d_an = coeffs_an

preds_an = (X_an @ coeffs_an) / np.array([d_el['A'] for d_el in data])
errs_an = np.abs(preds_an - BAs)
pcts_an = errs_an / BAs * 100
ss_tot = np.sum((BAs - BAs.mean())**2)
r2_an = 1 - np.sum((preds_an - BAs)**2) / ss_tot

print(f"\n  SOLVED:")
print(f"    a (all non-gate positions) = {a_an:.6f} MeV per position")
print(f"    d (triple-gate position)   = {d_an:.6f} MeV per position")
print(f"    a / m_e = {a_an / M_E:.4f}")
print(f"    d / m_e = {d_an / M_E:.4f}")
print(f"    d / a   = {d_an / a_an:.4f}")
print(f"")
print(f"  At full cycle (A=64):")
print(f"    63a = {63*a_an:.4f} MeV  ({63*a_an/(63*a_an+d_an)*100:.1f}%)")
print(f"     1d = {d_an:.4f} MeV  ({d_an/(63*a_an+d_an)*100:.1f}%)")
print(f"    Total = {63*a_an + d_an:.4f} MeV (known Zn = 8.756)")
print(f"")
print(f"  R²  = {r2_an:.6f}")
print(f"  MAE = {errs_an.mean()*1000:.1f} keV")
print(f"  Max = {errs_an.max()*1000:.1f} keV")
print(f"  ≤0.5%: {np.sum(pcts_an<=0.5)}/{n_el}")
print(f"  ≤1%:   {np.sum(pcts_an<=1)}/{n_el}")
print(f"  ≤2%:   {np.sum(pcts_an<=2)}/{n_el}")

print(f"\n  PER-ELEMENT:")
print(f"  {'Sym':>5} {'A':>3}  {'known':>6} {'pred':>6} {'ΔkeV':>6}  {'n63':>3} {'n1':>2} {'63a':>6} {'1d':>5}")
print(f"  {'─'*5} {'─'*3}  {'─'*6} {'─'*6} {'─'*6}  {'─'*3} {'─'*2} {'─'*6} {'─'*5}")

for i, d_el in enumerate(data):
    A = d_el['A']
    BA = d_el['BA']
    m = masks(A)
    n_ng = m[0]+m[1]+m[2]
    n_g = m[3]
    pred = preds_an[i]
    delta = (pred - BA) * 1000
    sym = syms_map.get(A, '?')
    flag = ' ★' if abs(delta) < 10 else (' ●' if abs(delta) < 50 else '')
    print(f"  {sym:>5} {A:>3}  {BA:>6.3f} {pred:>6.3f} {delta:>+6.0f}  "
          f"{n_ng:>3} {n_g:>2} {n_ng*a_an:>6.2f} {n_g*d_an:>5.2f}{flag}")


# ═══════════════════════════════════════
# PART 2: NN CONFIRMATION
# Network outputs 2 values: a_uniform, d
# B_total = n_nongate × a + n_gate × d
# ═══════════════════════════════════════

print(f"\n{'='*90}")
print(f"  PART 2: NN WITH 9:6:3:1 LOCKED RATIOS")
print(f"  Input: 3 Sierpinski levels (face_pct, chan_pct, sub_pct)")
print(f"  Output: k (single value)")
print(f"  a=k/3, b=2k/9, c=k/3, d=k  →  B_total = n0(k/3)+n1(2k/9)+n2(k/3)+n3(k)")
print(f"  Network: 3 → 32 → 32 → 32 → 1 (SiLU)")
print(f"{'='*90}")

X_nn = torch.tensor([d_el['inputs'] for d_el in data], dtype=torch.float32)
Y_nn = torch.tensor([d_el['BA'] for d_el in data], dtype=torch.float32).unsqueeze(1)

# Mask tensors: per-position weights from 9:6:3:1
# w_pos = [9/27, 6/27, 3/9, 1/1] = [1/3, 2/9, 1/3, 1]
POS_W = torch.tensor([1.0/3, 2.0/9, 1.0/3, 1.0], dtype=torch.float32)

# Build weighted mask sum for each element: Σ n_g × w_g
mask_sums = []
for d_el in data:
    m = masks(d_el['A'])
    ws = sum(m[g] * POS_W[g].item() for g in range(4))
    mask_sums.append(ws)
W_mask = torch.tensor(mask_sums, dtype=torch.float32).unsqueeze(1)
A_tensor = torch.tensor([d_el['A'] for d_el in data], dtype=torch.float32).unsqueeze(1)

# At full fill: Σ = 27/3 + 27×2/9 + 9/3 + 1 = 9+6+3+1 = 19
print(f"  Full cycle mask sum: {sum(GD_COUNTS[g]*POS_W[g].item() for g in range(4)):.1f} (should be 19)")


class LockedRatioNN(nn.Module):
    def __init__(self, hidden=32):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(3, hidden),
            nn.SiLU(),
            nn.Linear(hidden, hidden),
            nn.SiLU(),
            nn.Linear(hidden, hidden),
            nn.SiLU(),
            nn.Linear(hidden, 1),  # output: k
        )

    def forward(self, x, w_mask, A_vals):
        k = self.net(x)  # (batch, 1)
        B_total = k * w_mask  # k × Σ(n_g × pos_weight_g)
        ba_pred = B_total / A_vals
        return k, ba_pred


seed = torch.seed()
print(f"  Random seed: {seed}")

model = LockedRatioNN(hidden=32)
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=200000, eta_min=1e-6)

EPOCHS = 200000
REPORT = 10000

print(f"\n  {'epoch':>7} {'loss':>10} {'R²':>8} {'MAE':>7} "
      f"{'≤0.5%':>6} {'≤1%':>5} {'≤2%':>5} {'lr':>9}")
print(f"  {'─'*7} {'─'*10} {'─'*8} {'─'*7} {'─'*6} {'─'*5} {'─'*5} {'─'*9}")

t0 = time.time()

for epoch in range(1, EPOCHS + 1):
    model.train()
    k_out, ba_pred = model(X_nn, W_mask, A_tensor)
    loss = nn.MSELoss()(ba_pred, Y_nn)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    scheduler.step()

    if epoch % REPORT == 0 or epoch == 1:
        model.eval()
        with torch.no_grad():
            _, ba_e = model(X_nn, W_mask, A_tensor)
            preds = ba_e.squeeze().numpy()
            known = Y_nn.squeeze().numpy()
            errs = np.abs(preds - known)
            pcts = errs / known * 100
            r2 = 1 - np.sum((preds - known)**2) / np.sum((known - known.mean())**2)
            mae = errs.mean() * 1000
            lr = optimizer.param_groups[0]['lr']
            print(f"  {epoch:>7} {loss.item():>10.6f} {r2:>8.4f} "
                  f"{mae:>6.1f} {np.sum(pcts<=0.5):>5}/{n_el} "
                  f"{np.sum(pcts<=1):>4}/{n_el} {np.sum(pcts<=2):>4}/{n_el} "
                  f"{lr:>9.2e}")

print(f"\n  Training time: {time.time()-t0:.1f}s")


# ═══════════════════════════════════════
# NN FINAL RESULTS
# ═══════════════════════════════════════

model.eval()
with torch.no_grad():
    k_final, ba_final = model(X_nn, W_mask, A_tensor)
    k_np = k_final.squeeze().numpy()
    preds_nn = ba_final.squeeze().numpy()

print(f"\n{'='*90}")
print(f"  NN RESULTS — 9:6:3:1 LOCKED")
print(f"{'='*90}")

print(f"\n  {'Sym':>5} {'A':>3}  {'known':>6} {'pred':>6} {'ΔkeV':>6}  "
      f"{'k':>8}  {'a=k/3':>7} {'b=2k/9':>7} {'c=k/3':>7} {'d=k':>7}  "
      f"{'27a':>5} {'27b':>5} {'9c':>4} {'1d':>4}")
print(f"  {'─'*5} {'─'*3}  {'─'*6} {'─'*6} {'─'*6}  "
      f"{'─'*8}  {'─'*7} {'─'*7} {'─'*7} {'─'*7}  "
      f"{'─'*5} {'─'*5} {'─'*4} {'─'*4}")

for i, d_el in enumerate(data):
    A = d_el['A']
    BA = d_el['BA']
    pred = preds_nn[i]
    k = k_np[i]
    a = k / 3; b = 2*k/9; c = k/3; d = k
    m = masks(A)
    delta = (pred - BA) * 1000
    sym = syms_map.get(A, '?')
    flag = ' ★' if abs(delta) < 10 else (' ●' if abs(delta) < 50 else '')
    print(f"  {sym:>5} {A:>3}  {BA:>6.3f} {pred:>6.3f} {delta:>+6.0f}  "
          f"{k:>8.4f}  {a:>7.4f} {b:>7.4f} {c:>7.4f} {d:>7.4f}  "
          f"{m[0]*a:>5.2f} {m[1]*b:>5.2f} {m[2]*c:>4.2f} {m[3]*d:>4.2f}{flag}")

errs_nn = np.abs(preds_nn - BAs)
pcts_nn = errs_nn / BAs * 100
r2_nn = 1 - np.sum((preds_nn - BAs)**2) / ss_tot

print(f"\n  R²  = {r2_nn:.6f}")
print(f"  MAE = {errs_nn.mean()*1000:.1f} keV")
print(f"  Max = {errs_nn.max()*1000:.1f} keV")
print(f"  ≤0.5%: {np.sum(pcts_nn<=0.5)}/{n_el}")
print(f"  ≤1%:   {np.sum(pcts_nn<=1)}/{n_el}")
print(f"  ≤2%:   {np.sum(pcts_nn<=2)}/{n_el}")


# ═══════════════════════════════════════
# DEGENERACY + STRUCTURAL
# ═══════════════════════════════════════

print(f"\n{'='*90}")
print(f"  DEGENERACY TEST")
print(f"{'='*90}")
print(f"  k range: {k_np.min():.4f} to {k_np.max():.4f}")
print(f"  k mean:  {k_np.mean():.4f}")
print(f"  k std:   {k_np.std():.4f}")
print(f"  k CV:    {k_np.std()/abs(k_np.mean())*100:.1f}%")
print(f"  (Low CV = stable = NOT degenerate)")

print(f"\n  STRUCTURAL:")
print(f"  k / m_e = {k_np.mean() / M_E:.4f}")
print(f"  At Zn:  k = {k_np[-1]:.4f}  →  19k = {19*k_np[-1]:.4f}  (B/A = 8.756)")
print(f"  k(Zn)/m_e = {k_np[-1]/M_E:.4f}")
