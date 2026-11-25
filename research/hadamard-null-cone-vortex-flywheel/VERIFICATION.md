# Current verification guide

Run from the folder root after installing NumPy, SciPy, SymPy and Matplotlib.

```sh
python verify_open_throat.py
python verify_sustained_flywheel.py
```

Stage VIII: 160/160 new checks; [log](open_throat_verification_output.txt). Stage VII: 809 recorded new checks; [log](sustained_verification_output.txt). Earlier stages: 1,768 recorded checks, preserved in the [historical verification guide](archive/stages-I-VI/VERIFICATION.md). Total 2,737 recorded assertions across all eight stages, not independent theorems or a fresh cumulative run. Only Stage VIII was run for this edition. Stage VII imports its archived dependencies; original historical source is also retained. No Lean compilation or new browser verification.
