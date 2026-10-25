"""
constants.py
============

Physical constants and shared numerical parameters for the GFD / pyramid-portal
algebra package.

Values follow the conventions of the legacy monolith (CODATA-style references)
so that the new modular structure reproduces the legacy numerics exactly.
"""

from __future__ import annotations

from math import pi


# ----------------------------------------------------------------------------
# Mathematical constants
# ----------------------------------------------------------------------------

TAU = 2 * pi


# ----------------------------------------------------------------------------
# Empirical / framework constants
# ----------------------------------------------------------------------------

ALPHA = 1 / 137.035999084          # fine-structure constant
G_E_OVER_2 = 1.00115965218128      # electron g-factor over 2


# ----------------------------------------------------------------------------
# CODATA-style physical constants (SI)
# ----------------------------------------------------------------------------

HBAR = 1.054571817e-34             # J*s, reduced Planck constant
C_LIGHT = 299_792_458.0            # m/s, speed of light
M_E = 9.1093837015e-31             # kg, electron rest mass
G_OBSERVED = 6.67430e-11           # m^3 kg^-1 s^-2, Newton's gravitational constant
