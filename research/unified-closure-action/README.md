# GFD — Three-subcycle settlement research extension

This folder collects the two new research notes and their standalone NumPy verification scripts from the geometric π-walk, weighted settlement and microscopic stiffness discussion. The original reference photograph (the 2008 Barbury Castle π crop formation) is third-party and is not reproduced here.

## Illustrated companion (new)

Open `VISUAL_MATHEMATICAL_COMPANION.html` in a browser. It contains the chat mathematics, nine recreated diagrams and the interactive closure-balance slider. MathML renders equations locally in modern browsers; no network is required. `VISUAL_MATHEMATICAL_COMPANION.md` contains the editable LaTeX source. `diagrams/` contains the nine vector SVGs and high-resolution PNGs, plus their regeneration script. The visuals are reconstructed, not chat screenshots.

## Reading order

1. `research/WEIGHTED_CLOSURE_SETTLEMENT.md` — three-level address geometry, weighted boundary conservation, 21 contrast modes and conditional gravitational/electron closure.
2. `research/MICROSCOPIC_STIFFNESS_DERIVATION.md` — H36 spectral stiffness, 21/17/13 exchange traces, balanced face-pair read, Walsh invariance and normalization.
3. `verification/` — standalone scripts and fresh execution logs.

The notes contain Mermaid diagrams. View in a Markdown renderer supporting Mermaid. Earlier GFD papers and the full historical repository are referenced by the notes but not included in this folder.

## Reproduce

Install Python 3 and NumPy, then run from this folder:

```sh
python -m pip install numpy
python verification/verify_weighted_closure.py
python verification/verify_microscopic_stiffness.py
```

Both scripts were run successfully when packaging. These verify the specified mathematical constructions, not independent empirical predictions. Native physical selection of the balanced π-walk, attenuation and dimensional normalization remains open. No GitHub files were modified.
