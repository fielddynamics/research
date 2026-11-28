# Original source preservation

The inspected original folder is pinned in `original_manifest.json`. The local runtime could not directly transfer the GitHub source bytes into this ZIP, so `snapshot/` is populated only by running `../restore_upstream.py`. This avoids presenting edited or reconstructed text as a byte-identical clone.

From your existing checkout:

```bash
python restore_upstream.py --repo /path/to/research --proofs
```

The command copies the six original AQUAL files into `upstream/snapshot/research/aqual/`, verifies their exact Git blob SHA-1 and length, and optionally copies relevant formal proof directories and supporting notes into the same relative structure. It never modifies the original checkout. With internet access, `python restore_upstream.py` downloads only the six originals from the pinned public revision. If your checkout lacks the pinned commit, fetch it first. For full Lean dependency builds use a complete pinned checkout, rather than assuming the selected copy includes every transitive package.
