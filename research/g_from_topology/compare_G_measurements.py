"""
The fixed prediction for G, compared with each measurement in the CODATA 2022 adjustment.

    G = (17/13) * alpha^21 * hbar c / m_e^2 * (1 + alpha / 2 pi)

Inputs are CODATA 2022 values only. Nothing here is adjusted to the measurements.
The 16 measurements are Table XXX of the CODATA 2022 adjustment (Mohr et al., arXiv:2409.03787),
identical to the 2018 input set.

Run: python compare_G_measurements.py        (standard library only)
"""
import math

ALPHA = 1 / 137.035999177          # CODATA 2022
HBAR = 1.054571817e-34             # exact
C = 299792458.0                    # exact
M_E = 9.1093837139e-31             # CODATA 2022

TREE = 17 / 13 * ALPHA ** 21 * HBAR * C / M_E ** 2
ONE_LOOP = TREE * (1 + ALPHA / (2 * math.pi))

# identifier, G / 1e-11 m^3 kg^-1 s^-2, standard uncertainty (same units)
MEASUREMENTS = [
    ("NIST-82", 6.67248, 0.00043), ("TR&D-96", 6.6729, 0.0005), ("LANL-97", 6.67398, 0.00070),
    ("UWash-00", 6.674255, 0.000092), ("BIPM-01", 6.67559, 0.00027), ("UWup-02", 6.67422, 0.00098),
    ("MSL-03", 6.67387, 0.00027), ("HUST-05", 6.67222, 0.00087), ("UZur-06", 6.67425, 0.00012),
    ("HUST-09", 6.67349, 0.00018), ("BIPM-14", 6.67554, 0.00016), ("LENS-14", 6.67191, 0.00099),
    ("UCI-14", 6.67435, 0.00013), ("HUSTT-18", 6.674184, 0.000078), ("HUSTA-18", 6.674484, 0.000077),
    ("JILA-18", 6.67260, 0.00025),
]
CODATA = (6.67430, 0.00015)        # 2022 recommended value (= 2018), uncertainty expanded by 3.9

if __name__ == "__main__":
    p = ONE_LOOP * 1e11
    print(f"prediction: tree {TREE * 1e11:.6f}, one loop {p:.6f}  (x 1e-11 m^3 kg^-1 s^-2)")
    print(f"uncertainty from the inputs (alpha, m_e): about {21 * 1.5e-10 + 2 * 3e-10:.0e} relative, negligible\n")
    print(f"{'experiment':10s} {'G':>9s} {'sigma':>8s} {'pred - G':>10s} {'z':>6s}")
    for name, g, s in sorted(MEASUREMENTS, key=lambda r: r[2]):
        print(f"{name:10s} {g:9.6f} {s:8.6f} {1e6 * (p - g) / g:+8.1f}ppm {(p - g) / s:+6.1f}")
    g, s = CODATA
    print(f"\nCODATA 2022: {g:.5f}({s * 1e5:.0f})  prediction {1e6 * (p - g) / g:+.1f} ppm, z = {(p - g) / s:+.2f}")
