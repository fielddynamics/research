#!/usr/bin/env python3
"""
GFD Gate Depth NN: Predict a, b, c, d from Sierpinski fill levels
===================================================================
Input:  3 Sierpinski fill levels (face_pct, chan_pct, sub_pct)
Output: a, b, c, d (4 values)
Loss:   27a + 27b + 9c + 1d  must equal observed B/A (MeV)

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

X = torch.tensor([d['inputs'] for d in data], dtype=torch.float32)
Y = torch.tensor([d['BA'] for d in data], dtype=torch.float32).unsqueeze(1)
n_el = len(data)

syms_map = {
    4:'He',7:'Li',9:'Be',11:'B',12:'C',14:'N',16:'O',19:'F',20:'Ne',
    23:'Na',24:'Mg',27:'Al',28:'Si',31:'P',32:'S',35:'Cl',39:'K',40:'Ar/Ca',
    45:'Sc',48:'Ti',51:'V',52:'Cr',55:'Mn',56:'Fe',58:'Ni',59:'Co',
    63:'Cu',64:'Zn',
}

W_GD = torch.tensor([27.0, 27.0, 9.0, 1.0], dtype=torch.float32)


# ═══════════════════════════════════════
# NETWORK
# ═══════════════════════════════════════

class GateDepthNN(nn.Module):
    def __init__(self, hidden=32):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(3, hidden),
            nn.SiLU(),
            nn.Linear(hidden, hidden),
            nn.SiLU(),
            nn.Linear(hidden, hidden),
            nn.SiLU(),
            nn.Linear(hidden, 4),
        )

    def forward(self, x):
        abcd = self.net(x)
        ba_pred = (abcd * W_GD).sum(dim=1, keepdim=True)
        return abcd, ba_pred


# ═══════════════════════════════════════
# TRAINING
# ═══════════════════════════════════════

seed = torch.seed()
print(f"Random seed: {seed}")
model = GateDepthNN(hidden=32)
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=200000, eta_min=1e-6)

EPOCHS = 200000
REPORT = 10000

print(f"\n{'='*90}")
print(f"  TRAINING: {EPOCHS} epochs, report every {REPORT}")
print(f"  Input: 3 Sierpinski levels (face_pct, chan_pct, sub_pct)")
print(f"  Output: a, b, c, d → 27a + 27b + 9c + 1d = B/A")
print(f"  Network: 3 → 32 → 32 → 32 → 4 (SiLU)")
print(f"{'='*90}")

print(f"\n  {'epoch':>7} {'loss':>10} {'R2':>8} {'MAE':>7} "
      f"{'<=0.5%':>6} {'<=1%':>5} {'<=2%':>5} {'lr':>9}")
print(f"  {'---':>7} {'---':>10} {'---':>8} {'---':>7} {'---':>6} {'---':>5} {'---':>5} {'---':>9}")

t0 = time.time()

for epoch in range(1, EPOCHS + 1):
    model.train()
    abcd, ba_pred = model(X)
    loss = nn.MSELoss()(ba_pred, Y)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    scheduler.step()

    if epoch % REPORT == 0 or epoch == 1:
        model.eval()
        with torch.no_grad():
            _, ba_e = model(X)
            preds = ba_e.squeeze().numpy()
            known = Y.squeeze().numpy()
            errs = np.abs(preds - known)
            pcts = errs / known * 100
            ss_res = np.sum((preds - known)**2)
            ss_tot = np.sum((known - known.mean())**2)
            r2 = 1 - ss_res / ss_tot
            mae = errs.mean() * 1000
            lr = optimizer.param_groups[0]['lr']
            print(f"  {epoch:>7} {loss.item():>10.6f} {r2:>8.4f} "
                  f"{mae:>6.1f} {np.sum(pcts<=0.5):>5}/{n_el} "
                  f"{np.sum(pcts<=1):>4}/{n_el} {np.sum(pcts<=2):>4}/{n_el} "
                  f"{lr:>9.2e}")

print(f"\n  Training time: {time.time()-t0:.1f}s")


# ═══════════════════════════════════════
# FINAL RESULTS
# ═══════════════════════════════════════

model.eval()
with torch.no_grad():
    abcd_final, ba_final = model(X)
    abcd_np = abcd_final.numpy()
    preds_np = ba_final.squeeze().numpy()
    known_np = Y.squeeze().numpy()

print(f"\n{'='*90}")
print(f"  FINAL RESULTS")
print(f"{'='*90}")

print(f"\n  {'Sym':>5} {'A':>3}  {'known':>6} {'pred':>6} {'dkeV':>6}  "
      f"{'a':>8} {'b':>8} {'c':>8} {'d':>8}  "
      f"{'27a':>6} {'27b':>6} {'9c':>5} {'1d':>5}")
print(f"  {'---':>5} {'---':>3}  {'---':>6} {'---':>6} {'---':>6}  "
      f"{'---':>8} {'---':>8} {'---':>8} {'---':>8}  "
      f"{'---':>6} {'---':>6} {'---':>5} {'---':>5}")

for i, d in enumerate(data):
    A = d['A']
    BA = d['BA']
    pred = preds_np[i]
    a, b, c, dd = abcd_np[i]
    delta = (pred - BA) * 1000
    sym = syms_map.get(A, '?')
    flag = ' *' if abs(delta) < 5 else (' .' if abs(delta) < 50 else '')
    print(f"  {sym:>5} {A:>3}  {BA:>6.3f} {pred:>6.3f} {delta:>+6.0f}  "
          f"{a:>8.4f} {b:>8.4f} {c:>8.4f} {dd:>8.4f}  "
          f"{27*a:>6.2f} {27*b:>6.2f} {9*c:>5.2f} {1*dd:>5.2f}{flag}")

errs = np.abs(preds_np - known_np)
pcts = errs / known_np * 100
r2 = 1 - np.sum((preds_np - known_np)**2) / np.sum((known_np - known_np.mean())**2)

print(f"\n  R2  = {r2:.6f}")
print(f"  MAE = {errs.mean()*1000:.1f} keV")
print(f"  Max = {errs.max()*1000:.1f} keV ({syms_map.get(data[np.argmax(errs)]['A'], '?')})")
print(f"  <=0.5%: {np.sum(pcts<=0.5)}/{n_el}")
print(f"  <=1%:   {np.sum(pcts<=1)}/{n_el}")
print(f"  <=2%:   {np.sum(pcts<=2)}/{n_el}")


# ═══════════════════════════════════════
# ANALYSIS
# ═══════════════════════════════════════

print(f"\n{'='*90}")
print(f"  ANALYSIS: Gate depth contributions")
print(f"{'='*90}")

for label, idx in [('Carbon (A=12)', 12), ('Iron (A=56)', 56), ('Zinc (A=64)', 64)]:
    i = next(j for j, d in enumerate(data) if d['A'] == idx)
    a, b, c, dd = abcd_np[i]
    total = 27*a + 27*b + 9*c + dd
    print(f"\n  {label}:")
    print(f"    a={a:.4f}  27a={27*a:.3f} ({27*a/total*100:.1f}%)")
    print(f"    b={b:.4f}  27b={27*b:.3f} ({27*b/total*100:.1f}%)")
    print(f"    c={c:.4f}   9c={9*c:.3f} ({9*c/total*100:.1f}%)")
    print(f"    d={dd:.4f}   1d={dd:.3f} ({dd/total*100:.1f}%)")

print(f"\n  Coefficient ranges:")
for g, label in enumerate(['a(gd=0)', 'b(gd=1)', 'c(gd=2)', 'd(gd=3)']):
    vals = abcd_np[:, g]
    print(f"    {label}: min={vals.min():.4f}  max={vals.max():.4f}  "
          f"std={vals.std():.4f}  CV={vals.std()/abs(vals.mean())*100:.1f}%")

print(f"\n  Ordering at key elements:")
for A_check in [4, 12, 16, 27, 56, 64]:
    i = next((j for j, d in enumerate(data) if d['A'] == A_check), None)
    if i is None:
        continue
    vals = abcd_np[i]
    order = np.argsort(-vals)
    labels = ['a(gd0)', 'b(gd1)', 'c(gd2)', 'd(gd3)']
    ordering = ' > '.join(labels[j] for j in order)
    sym = syms_map.get(A_check, '?')
    print(f"    {sym:>5} A={A_check:>2}: {ordering}")
