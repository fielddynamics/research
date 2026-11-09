# Wide Binaries

*A pre-registered test of GFD's covariant action against Gaia DR4 · Gravity Field Dynamics (GFD) · Field Dynamics Research*

`wide-binaries` `gaia` `modified-gravity` `external-field-effect` `pre-registration` `aqual`

---

Pairs of stars thousands of AU apart are the cleanest test of gravity at low acceleration. They contain no dark matter, so any departure from Newton's law there is a change in gravity itself. They also sit inside the Milky Way's field, so predicting them needs GFD's full field equation, not only its spherical limit, the SST.

This folder solves that equation for a binary in the Galactic field and fixes the result before Gaia's fourth data release on 2 December 2026:

| | Prediction |
|---|---|
| Close pairs, 1–2 kau | Newtonian, within 1–5% |
| Wide pairs, beyond 10 kau | gravity 42% stronger, orbits 19% faster |
| Pre-registered ratio $R$ of typical normalised velocities, wide over close | **1.163** (Newton: 1.000) |

The full statement, inputs, approximations and pass/fail criteria are in [`PREREGISTRATION.md`](PREREGISTRATION.md).

## Contents

| File | Contents |
|---|---|
| [`PREREGISTRATION.md`](PREREGISTRATION.md) | The prediction and the criteria that decide it |
| [`gfd_field_solver.py`](gfd_field_solver.py) | Axisymmetric solver for the full nonlinear field equation, a point mass in a uniform external field |
| [`validate_solver.py`](validate_solver.py) | Checks against the exact isolated solution and the analytic far field (5/5) |
| [`wide_binary_prediction.py`](wide_binary_prediction.py) | The gravity boost versus separation, and the statistic $R$ |

```bash
pip install numpy scipy
python validate_solver.py          # about 1 minute
python wide_binary_prediction.py   # about 2 minutes
```

## Related

- [The covariant-completion supplement to Letter 3](../../papers/letter-3-field-closure-of-tetrad-frame/Supplementary/supplementary_covariant_completion.tex): the action and the field equation solved here.
- [The radial acceleration relation letter](../../papers/letter-radial-acceleration-relation-sparc/): the same law tested on 164 galaxies.
