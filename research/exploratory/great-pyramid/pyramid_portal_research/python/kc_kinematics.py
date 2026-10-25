"""
kc_kinematics.py
=================

King's Chamber kinematics: per-mode time scales, wavelengths, axis-roundtrip
times, adjacent-mode beats, rotating-frame effects (Coriolis splitting,
Sagnac phase per roundtrip), and per-mode vortex circulation.

This module is purely kinematic — no Q-factors, no dissipation, no energy
budgets.  All quantities are geometric or temporal descriptions of motion.

The vortex identity from AW 17 says each chamber mode is its own vortex
with

    ω_mode  =  2π v_wave / λ_mode

i.e. the standard dispersion relation ω = v|k|.  λ_mode is the mode's
closure-cycle length under the vortex picture.  Therefore "21 modes" =
"21 distinct vortices with their own circulation".

Kinematic output:
  - per-mode wavelength, period, angular frequency, phase velocity
  - per-axis acoustic roundtrip times (L, W, H, body diagonal)
  - adjacent-mode beat frequencies and beat periods
  - vortex circulation Γ = v_wave · λ_mode for each mode
  - Coriolis frequency split  Δω = 2 Ω_Earth · sin(latitude)
  - Sagnac phase per roundtrip on the chamber's loop area

Reference quantities (rotating-frame):
  - Earth angular speed Ω_Earth = 2π / (sidereal day) ≈ 7.292e-5 rad/s
  - Giza latitude φ ≈ 29.9792° N  →  sin φ ≈ 0.4997
  - Vertical component:  Ω_Earth · sin φ ≈ 3.644e-5 rad/s
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Tuple

import math

from python.pyramid_resonance import (
    ROYAL_CUBIT_M, KC_L_CUBITS, KC_W_CUBITS, KC_H_CUBITS,
    V_AIR, V_GRANITE_P, V_GRANITE_S,
    Mode, lowest_modes,
    kc_dimensions_m,
)


# ---------------------------------------------------------------------------
# Earth and site constants
# ---------------------------------------------------------------------------

SIDEREAL_DAY_S = 86164.0905              # seconds in one sidereal day
OMEGA_EARTH = 2.0 * math.pi / SIDEREAL_DAY_S    # rad/s, Earth's angular speed
GIZA_LATITUDE_DEG = 29.9792              # Great Pyramid latitude
GIZA_LATITUDE_RAD = math.radians(GIZA_LATITUDE_DEG)

# Vertical projection of Earth's rotation at Giza
OMEGA_EARTH_VERTICAL = OMEGA_EARTH * math.sin(GIZA_LATITUDE_RAD)
# Horizontal projection (along local north)
OMEGA_EARTH_HORIZONTAL = OMEGA_EARTH * math.cos(GIZA_LATITUDE_RAD)


# ---------------------------------------------------------------------------
# Per-mode kinematics
# ---------------------------------------------------------------------------

def k_vector_magnitude_m_inv(mode: Mode) -> float:
    """|k| in inverse metres for a standing-wave mode (n_x, n_y, n_z)."""
    L_m = KC_L_CUBITS * ROYAL_CUBIT_M
    W_m = KC_W_CUBITS * ROYAL_CUBIT_M
    H_m = KC_H_CUBITS * ROYAL_CUBIT_M
    return math.pi * math.sqrt(
        (mode.n_x / L_m) ** 2 + (mode.n_y / W_m) ** 2 + (mode.n_z / H_m) ** 2
    )


def mode_wavelength_m(mode: Mode, v_wave: float = V_AIR) -> float:
    """λ_mode = v_wave / f_mode = 2π / |k| in metres."""
    return 2.0 * math.pi / k_vector_magnitude_m_inv(mode)


def mode_period_s(mode: Mode, v_wave: float = V_AIR) -> float:
    """T_mode = 1 / f_mode in seconds."""
    return 1.0 / mode.frequency_hz(v_wave)


def mode_angular_frequency_rad_per_s(mode: Mode, v_wave: float = V_AIR) -> float:
    """ω = 2π f in rad/s."""
    return 2.0 * math.pi * mode.frequency_hz(v_wave)


def mode_phase_velocity_m_per_s(mode: Mode, v_wave: float = V_AIR) -> float:
    """Phase velocity v_phase = ω/|k| = v_wave in a non-dispersive medium."""
    return v_wave


# ---------------------------------------------------------------------------
# Roundtrip times
# ---------------------------------------------------------------------------

def axis_roundtrip_time_s(axis_length_cubits: float, v_wave: float = V_AIR) -> float:
    """Time for a wave to cross axis_length and return: T_rt = 2L / v."""
    return 2.0 * axis_length_cubits * ROYAL_CUBIT_M / v_wave


def all_axis_roundtrips(v_wave: float = V_AIR) -> Dict[str, float]:
    """Roundtrip times along L, W, H axes, plus space-diagonal."""
    L, W, H = kc_dimensions_m()
    diag = math.sqrt(L * L + W * W + H * H)
    return {
        "L_axis_s": 2.0 * L / v_wave,
        "W_axis_s": 2.0 * W / v_wave,
        "H_axis_s": 2.0 * H / v_wave,
        "diagonal_s": 2.0 * diag / v_wave,
    }


# ---------------------------------------------------------------------------
# Adjacent-mode beats
# ---------------------------------------------------------------------------

@dataclass
class BeatEntry:
    mode_lo: Mode
    mode_hi: Mode
    f_lo: float
    f_hi: float
    delta_f: float
    beat_period_s: float


def adjacent_mode_beats(v_wave: float = V_AIR, k: int = 21) -> List[BeatEntry]:
    """Δf and beat period between rank-adjacent modes."""
    modes = lowest_modes(k)
    out: List[BeatEntry] = []
    for i in range(len(modes) - 1):
        lo = modes[i]
        hi = modes[i + 1]
        f_lo = lo.frequency_hz(v_wave)
        f_hi = hi.frequency_hz(v_wave)
        df = f_hi - f_lo
        T = 1.0 / df if df > 0 else float("inf")
        out.append(BeatEntry(
            mode_lo=lo, mode_hi=hi, f_lo=f_lo, f_hi=f_hi,
            delta_f=df, beat_period_s=T,
        ))
    return out


# ---------------------------------------------------------------------------
# Vortex circulation per mode
# ---------------------------------------------------------------------------

def mode_circulation_m2_per_s(mode: Mode, v_wave: float = V_AIR) -> float:
    """Γ_mode = v_wave × λ_mode.  Each mode is its own vortex; this is its
    natural circulation in m²/s under the AW 17 vortex identity."""
    return v_wave * mode_wavelength_m(mode, v_wave)


# ---------------------------------------------------------------------------
# Rotating-frame effects — pure kinematics (no forces / no Q)
# ---------------------------------------------------------------------------

def coriolis_split_rad_per_s(
    mode: Mode, omega_earth_vertical: float = OMEGA_EARTH_VERTICAL
) -> float:
    """Coriolis frequency split for a circularly-polarized mode.

    For modes with chirality ±1, the Earth's rotating frame shifts the
    frequency by ±2Ω_Earth · sin(latitude) (the vertical component).
    The split between left- and right-circular polarizations is
        Δω = 2 · Ω_E · sin(φ_lat)
    independent of mode frequency (kinematic, not dynamic).
    """
    return 2.0 * omega_earth_vertical


def coriolis_split_hz(
    mode: Mode, omega_earth_vertical: float = OMEGA_EARTH_VERTICAL
) -> float:
    """Coriolis split in Hz."""
    return coriolis_split_rad_per_s(mode, omega_earth_vertical) / (2.0 * math.pi)


def sagnac_phase_per_roundtrip_rad(
    mode: Mode, v_wave: float = V_AIR,
    omega_earth_vertical: float = OMEGA_EARTH_VERTICAL,
) -> float:
    """Sagnac phase shift per circulation in the chamber.

    For a wave traversing a closed loop of vector area A in a frame
    rotating at Ω, the Sagnac phase is
        Δφ = 4 Ω · A / (v λ)  =  4 Ω · A · k / v
    For the chamber's L×W footprint as the relevant loop:
        A_footprint = L_m × W_m   (horizontal cross-section)
    """
    L, W, _ = kc_dimensions_m()
    A_footprint = L * W
    k_mag = k_vector_magnitude_m_inv(mode)
    return 4.0 * omega_earth_vertical * A_footprint * k_mag / v_wave


# ---------------------------------------------------------------------------
# Per-mode kinematics table
# ---------------------------------------------------------------------------

@dataclass
class KinematicEntry:
    mode: Mode
    f_hz: float
    period_s: float
    wavelength_m: float
    k_magnitude_inv_m: float
    circulation_m2_per_s: float
    coriolis_split_hz: float
    sagnac_phase_rad: float


def mode_kinematics(mode: Mode, v_wave: float = V_AIR) -> KinematicEntry:
    return KinematicEntry(
        mode=mode,
        f_hz=mode.frequency_hz(v_wave),
        period_s=mode_period_s(mode, v_wave),
        wavelength_m=mode_wavelength_m(mode, v_wave),
        k_magnitude_inv_m=k_vector_magnitude_m_inv(mode),
        circulation_m2_per_s=mode_circulation_m2_per_s(mode, v_wave),
        coriolis_split_hz=coriolis_split_hz(mode),
        sagnac_phase_rad=sagnac_phase_per_roundtrip_rad(mode, v_wave),
    )


def all_modes_kinematics(
    k: int = 21, v_wave: float = V_AIR
) -> List[KinematicEntry]:
    return [mode_kinematics(m, v_wave) for m in lowest_modes(k)]


# ---------------------------------------------------------------------------
# Showcase
# ---------------------------------------------------------------------------

def showcase_kc_kinematics() -> List[str]:
    """One-call kinematic summary."""
    lines: List[str] = []
    lines.append("=" * 84)
    lines.append("  KING'S CHAMBER KINEMATICS  (per-mode times, beats, Sagnac, Coriolis)")
    lines.append("=" * 84)

    L, W, H = kc_dimensions_m()
    diag = math.sqrt(L * L + W * W + H * H)
    lines.append("")
    lines.append(f"  Site & geometry:")
    lines.append(f"    L = {L:.3f} m   W = {W:.3f} m   H = {H:.3f} m   diag = {diag:.3f} m")
    lines.append(f"    Giza latitude φ = {GIZA_LATITUDE_DEG:.4f}°")
    lines.append(f"    Ω_E = 2π/T_sidereal = {OMEGA_EARTH:.4e} rad/s")
    lines.append(f"    Ω_E·sin(φ) (vertical) = {OMEGA_EARTH_VERTICAL:.4e} rad/s")
    lines.append(f"    f_Earth (vertical) = {OMEGA_EARTH_VERTICAL/(2*math.pi):.4e} Hz")

    # Axis roundtrips
    rt_air = all_axis_roundtrips(V_AIR)
    rt_gran = all_axis_roundtrips(V_GRANITE_P)
    lines.append("")
    lines.append("  Axis roundtrip times (2 L_axis / v_wave):")
    lines.append(f"    axis     |  air ({V_AIR:.0f} m/s)  |  granite-P ({V_GRANITE_P:.0f} m/s)")
    lines.append(f"    L = 20c  |  {rt_air['L_axis_s']*1000:7.3f} ms     |  {rt_gran['L_axis_s']*1000:7.3f} ms")
    lines.append(f"    W = 10c  |  {rt_air['W_axis_s']*1000:7.3f} ms     |  {rt_gran['W_axis_s']*1000:7.3f} ms")
    lines.append(f"    H = 5√5c |  {rt_air['H_axis_s']*1000:7.3f} ms     |  {rt_gran['H_axis_s']*1000:7.3f} ms")
    lines.append(f"    diagonal |  {rt_air['diagonal_s']*1000:7.3f} ms     |  {rt_gran['diagonal_s']*1000:7.3f} ms")

    # Per-mode kinematics (air)
    entries = all_modes_kinematics(21, V_AIR)
    lines.append("")
    lines.append("  Per-mode kinematics (air, v = 343 m/s):")
    lines.append("    rank | (n_x,n_y,n_z) | f (Hz) | period (ms) | λ (m) | Γ (m²/s) | Sagnac (rad)")
    lines.append("    -----+---------------+--------+-------------+-------+----------+-------------")
    for i, e in enumerate(entries):
        m = e.mode
        lines.append(
            f"    {i+1:4d} | ({m.n_x:2d},{m.n_y:2d},{m.n_z:2d})    "
            f"| {e.f_hz:6.2f} | {e.period_s*1000:9.3f}  "
            f"| {e.wavelength_m:5.3f} | {e.circulation_m2_per_s:7.3f}  "
            f"| {e.sagnac_phase_rad:11.3e}"
        )

    # Adjacent-mode beats
    beats = adjacent_mode_beats(V_AIR, 21)
    lines.append("")
    lines.append("  Adjacent-mode beats (air, sorted by ascending Δf):")
    lines.append("    rank | mode_lo         | mode_hi         | Δf (Hz) | T_beat (s)")
    lines.append("    -----+-----------------+-----------------+---------+-----------")
    sorted_beats = sorted(beats, key=lambda b: b.delta_f)
    for i, b in enumerate(sorted_beats[:10]):    # show 10 smallest gaps
        mlo = b.mode_lo
        mhi = b.mode_hi
        lines.append(
            f"    {i+1:4d} | ({mlo.n_x},{mlo.n_y},{mlo.n_z}) at {b.f_lo:5.2f} | "
            f"({mhi.n_x},{mhi.n_y},{mhi.n_z}) at {b.f_hi:5.2f} | "
            f"{b.delta_f:6.3f}  | {b.beat_period_s:7.3f}"
        )

    # Coriolis (same for every mode — it's kinematic)
    cs_hz = coriolis_split_hz(entries[0].mode)
    cs_period = 1.0 / cs_hz if cs_hz > 0 else float("inf")
    lines.append("")
    lines.append("  Coriolis split (every chirality-distinguishing mode):")
    lines.append(f"    Δω = 2 Ω_E sin(φ) = {2*OMEGA_EARTH_VERTICAL:.4e} rad/s")
    lines.append(f"    Δf = Δω / 2π     = {cs_hz:.4e} Hz")
    lines.append(f"    T_period         = 1/Δf = {cs_period:.1f} s (≈ {cs_period/3600:.2f} h)")
    lines.append("    → Coriolis splits each mode into ω_mode ± Ω_E sin(φ) for")
    lines.append("      its left- and right-circular polarizations.  Magnitude")
    lines.append("      is mode-independent (it's a pure rotating-frame kinematics).")

    # Sagnac for fundamental mode
    s = entries[0].sagnac_phase_rad
    lines.append("")
    lines.append("  Sagnac phase per chamber roundtrip (footprint L·W):")
    lines.append(f"    fundamental (1,1,1): Δφ = {s:.4e} rad/roundtrip")
    lines.append(f"    21st mode (5,1,2):   Δφ = {entries[-1].sagnac_phase_rad:.4e} rad/roundtrip")
    lines.append("    → grows with mode index because Δφ ∝ |k|; chamber as a")
    lines.append("      large-area gyroscope sensitive at higher modes.")

    # Vortex circulation
    lines.append("")
    lines.append("  Per-mode vortex circulation  Γ = v_wave · λ_mode:")
    Gammas = [e.circulation_m2_per_s for e in entries]
    lines.append(f"    range: Γ ∈ [{min(Gammas):.3f}, {max(Gammas):.3f}] m²/s")
    lines.append(f"    ratio max/min = {max(Gammas)/min(Gammas):.3f}")
    lines.append(f"    Γ_fundamental / Γ_21 = {Gammas[0]/Gammas[-1]:.3f}")
    lines.append("    Each mode IS its own vortex under the AW 17 identity")
    lines.append("    ω = 2π v_read / ℓ_closure, with ℓ_closure = λ_mode.")

    return lines


__all__ = [
    "OMEGA_EARTH", "GIZA_LATITUDE_DEG", "GIZA_LATITUDE_RAD",
    "OMEGA_EARTH_VERTICAL", "OMEGA_EARTH_HORIZONTAL",
    "k_vector_magnitude_m_inv",
    "mode_wavelength_m", "mode_period_s",
    "mode_angular_frequency_rad_per_s", "mode_phase_velocity_m_per_s",
    "axis_roundtrip_time_s", "all_axis_roundtrips",
    "BeatEntry", "adjacent_mode_beats",
    "mode_circulation_m2_per_s",
    "coriolis_split_rad_per_s", "coriolis_split_hz",
    "sagnac_phase_per_roundtrip_rad",
    "KinematicEntry", "mode_kinematics", "all_modes_kinematics",
    "showcase_kc_kinematics",
]
