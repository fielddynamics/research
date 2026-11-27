#!/usr/bin/env python3
"""Run the nine Great Pyramid core-framework verifiers and summarise.

    python run_all.py            # from this folder

Each verifier runs in its own folder and prints PASS/FAIL per check; this
script reports the per-proof totals and exits non-zero if any check fails.
Requires: sympy, mpmath, numpy, scipy (GP-9 also pytest).
"""
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROOFS = [
    ("GP-1", "gp1-half-section-balance-plane", "verify_gp1_half_section.py"),
    ("GP-2", "gp2-balance-plane-robustness", "verify_gp2_robustness.py"),
    ("GP-3", "gp3-coupling-signatures-and-hinge", "verify_gp3_signatures_hinge.py"),
    ("GP-4", "gp4-registration-and-coherence", "verify_gp4_registration_coherence.py"),
    ("GP-5", "gp5-two-site-transfer-bound", "verify_gp5_transfer_bound.py"),
    ("GP-6", "gp6-structural-boundary-response", "verify_gp6_boundary_response.py"),
    ("GP-7", "gp7-chamber-spectral-selection", "verify_gp7_chamber_spectrum.py"),
    ("GP-8", "gp8-reciprocal-resonator-matching", "verify_gp8_reciprocal_matching.py"),
    ("GP-9", "gp9-grand-gallery-spectral-selection", "verify_gp9_grand_gallery.py"),
]

total_pass = total = 0
failed = []
for key, folder, script in PROOFS:
    proc = subprocess.run([sys.executable, script], cwd=HERE / folder, capture_output=True, text=True)
    (HERE / folder / "verify_output.txt").write_text(proc.stdout)
    m = re.search(r"(\d+)/(\d+) checks passed", proc.stdout)
    p, n = (int(m.group(1)), int(m.group(2))) if m else (0, 0)
    total_pass += p
    total += n
    status = "ok" if proc.returncode == 0 and p == n and n > 0 else "FAILED"
    if status != "ok":
        failed.append(key)
    print(f"{key}  {folder:38s} {p:3d}/{n:3d}  {status}")

print(f"\nTotal: {total_pass}/{total} checks passed")
sys.exit(1 if failed else 0)
