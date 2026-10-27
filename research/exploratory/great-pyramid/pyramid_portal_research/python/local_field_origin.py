"""
Local Field Origin of a bounded closure (01.6).

Under postulate P1 (closure capacity carried across a level surface is
proportional to its area), the GFD state coordinate and coupling capacity
inside a bounded body are

    mu_B(z) = A(z) / A(0)
    s_B(z)  = 2 mu_B(z) - 1            (identity s = 2 mu - 1)
    f_B(z)  = 17 + 4 s_B(z) = 13 + 8 mu_B(z)

For an apex body with homothetic sections, A(z) = A(0) (1 - z/h)^2, and the
local Field Origin (s = 0, f = 17, mu = 1/2) lies at

    z*/h = 1 - 1/sqrt(2) = 0.292893...

independent of size and section shape.

The module compares this with Petrie's (1883) King's Chamber floor level.

Run:  python -m python.local_field_origin
"""

from __future__ import annotations

import math
from dataclasses import dataclass

K = 4
D = 3

# Petrie (1883)
PETRIE_HEIGHT_IN = 5776.0          # sec. 144, original height
PETRIE_HEIGHT_ERR_IN = 7.0
PETRIE_KC_FLOOR_RANGE_IN = (1691.4, 1693.7)   # sec. 148
PETRIE_KC_FLOOR_ERR_IN = 0.6
PETRIE_HALF_AREA_LEVEL_IN = 1691.7  # sec. 148
PETRIE_HALF_AREA_ERR_IN = 1.8
ROYAL_CUBIT_IN = 20.632             # sec. 52
INCH_M = 0.0254

FIELD_ORIGIN_FRACTION = 1.0 - 1.0 / math.sqrt(2.0)
VOLUMETRIC_FRACTION = 1.0 - 2.0 ** (-1.0 / 3.0)


# ---------------------------------------------------------------------------
# GFD maps
# ---------------------------------------------------------------------------

def mu_of_x(x: float) -> float:
    """Constitutive law mu(x) = x / (x + 1)."""
    return x / (x + 1.0)


def s_of_x(x: float) -> float:
    """Mobius state map s(x) = (x - 1) / (x + 1)."""
    return (x - 1.0) / (x + 1.0)


def s_of_mu(mu: float) -> float:
    """Identity s = 2 mu - 1."""
    return 2.0 * mu - 1.0


def coupling_capacity(s: float, k: int = K) -> float:
    """Coupling polynomial f(K, s) = 1 + sK + K^2."""
    return 1.0 + s * k + k * k


# ---------------------------------------------------------------------------
# Bounded apex body
# ---------------------------------------------------------------------------

def area_fraction(z: float, h: float) -> float:
    """A(z)/A(0) for an apex body with homothetic sections."""
    if not 0.0 <= z <= h:
        raise ValueError("z must lie in [0, h]")
    return (1.0 - z / h) ** 2


def local_state(z: float, h: float) -> tuple[float, float, float]:
    """Return (mu_B, s_B, f_B) at level z of an apex body of height h (P1)."""
    mu = area_fraction(z, h)
    s = s_of_mu(mu)
    return mu, s, coupling_capacity(s)


def local_field_origin_height(h: float) -> float:
    """Theorem 1: z* = h (1 - 1/sqrt 2)."""
    return h * FIELD_ORIGIN_FRACTION


def volumetric_balance_height(h: float) -> float:
    """Balance plane under the volumetric alternative: z = h (1 - 2^(-1/3))."""
    return h * VOLUMETRIC_FRACTION


# ---------------------------------------------------------------------------
# Comparison with the Great Pyramid
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Comparison:
    predicted_in: float
    predicted_err_in: float
    measured_in: float
    measured_err_in: float
    difference_in: float
    combined_err_in: float
    sigma: float
    predicted_cubits: float
    measured_cubits: float
    measured_fraction: float


def great_pyramid_comparison() -> Comparison:
    h, dh = PETRIE_HEIGHT_IN, PETRIE_HEIGHT_ERR_IN
    pred = local_field_origin_height(h)
    pred_err = dh * FIELD_ORIGIN_FRACTION
    lo, hi = PETRIE_KC_FLOOR_RANGE_IN
    meas = 0.5 * (lo + hi)
    # Treat the quoted range as an additional spread on the floor level.
    meas_err = math.hypot(PETRIE_KC_FLOOR_ERR_IN, 0.5 * (hi - lo))
    diff = meas - pred
    comb = math.hypot(pred_err, meas_err)
    return Comparison(
        predicted_in=pred,
        predicted_err_in=pred_err,
        measured_in=meas,
        measured_err_in=meas_err,
        difference_in=diff,
        combined_err_in=comb,
        sigma=diff / comb,
        predicted_cubits=pred / ROYAL_CUBIT_IN,
        measured_cubits=meas / ROYAL_CUBIT_IN,
        measured_fraction=meas / h,
    )


def showcase() -> None:
    c = great_pyramid_comparison()
    h = PETRIE_HEIGHT_IN
    print("Local Field Origin of a bounded closure (01.6)")
    print("-" * 60)
    print(f"z*/h = 1 - 1/sqrt(2)            = {FIELD_ORIGIN_FRACTION:.6f}")
    print(f"Volumetric alternative          = {VOLUMETRIC_FRACTION:.6f}")
    print()
    for z, label in [(0.0, "base"), (local_field_origin_height(h), "z*"), (h, "apex")]:
        mu, s, f = local_state(z, h)
        print(f"{label:>5}: mu_B = {mu:5.3f}  s_B = {s:+6.3f}  f_B = {f:6.3f}")
    print()
    print(f"Predicted z*   = {c.predicted_in:7.1f} +/- {c.predicted_err_in:.1f} in "
          f"({c.predicted_cubits:.2f} cubits)")
    print(f"KC floor       = {c.measured_in:7.1f} +/- {c.measured_err_in:.1f} in "
          f"({c.measured_cubits:.2f} cubits)")
    print(f"Difference     = {c.difference_in:+.1f} in  ({c.sigma:+.2f} sigma)")
    print(f"Fraction of h  = predicted {FIELD_ORIGIN_FRACTION:.5f}, "
          f"measured {c.measured_fraction:.5f}")
    vol = volumetric_balance_height(h)
    print(f"Volumetric balance plane = {vol:.1f} in ({vol * INCH_M:.1f} m): "
          f"no chamber at this level")


if __name__ == "__main__":
    showcase()
