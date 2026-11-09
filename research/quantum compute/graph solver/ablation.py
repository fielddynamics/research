"""Ablation control for the oscillator benchmark (run_all.py): is the oscillator doing the work?
Runs run_all.py with the integration steps set to zero, so the readout sees only the random starting phases.
Everything else (readout, restarts, candidate search, instances) is identical.
If a score survives, that score does not come from the oscillator.
Run: python ablation.py"""
import sys, os
import numpy as np
SOLVER = os.path.dirname(os.path.abspath(__file__)); MODE = 'nodyn'
sys.path.insert(0, SOLVER)
import gfd_oscillator as G
Orig = G.GFDOscillator

class Patched(Orig):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        if MODE == 'nodyn': self.steps = 0
    def run_amplitude(self, graph, x_drive, c_amp=0.3, depth=1, seed=42):
        return super().run_amplitude(graph, x_drive, c_amp, depth, seed)
G.GFDOscillator = Patched
for m in ['solve_maze','solve_maxcut','solve_coloring','solve_tsp','solve_community']:
    __import__(m).GFDOscillator = Patched
import run_all, io, contextlib
for name, fn in [('maze', run_all.test_maze), ('maxcut', run_all.test_maxcut), ('coloring', run_all.test_coloring),
                 ('tsp', run_all.test_tsp), ('community', run_all.test_community)]:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf): fn()
    print(f"dynamics off: {buf.getvalue().strip()}")
