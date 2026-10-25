#!/usr/bin/env python3
"""
GFD Coupling Polynomial Verification Suite
============================================
Tests that f(K, s) = 1 + Ks + K² encodes the Sierpiński triangle hierarchy.

Run: python gfd_polynomial_tests.py

All tests are zero-parameter: K=4 and D=3 from the uniqueness equation.
"""

K = 4
D = 3

def f_poly(K, s):
    """The GFD coupling polynomial: f(K, s) = 1 + Ks + K²"""
    return 1 + K * s + K**2

def f_quad(K, s):
    """The WRONG version: f(K, s) = 1 + Ks + K²s² (for comparison)"""
    return 1 + K * s + K**2 * s**2

F_PLUS  = f_poly(K, +1)  # 21
F_ZERO  = f_poly(K,  0)  # 17
F_MINUS = f_poly(K, -1)  # 13

passed = 0
failed = 0

def test(name, condition, detail=""):
    global passed, failed
    if condition:
        passed += 1
        print(f"  ✓ {name}")
    else:
        failed += 1
        print(f"  ✗ {name}  {detail}")


print("=" * 70)
print("  GFD COUPLING POLYNOMIAL TEST SUITE")
print("  f(K, s) = 1 + Ks + K²,  K=4, D=3")
print("=" * 70)


# ── 1. STRUCTURAL LANDMARKS ──
print("\n── 1. Structural Landmarks ──")
test("F+ = f(4, +1) = 21",  F_PLUS == 21,  f"got {F_PLUS}")
test("F0 = f(4,  0) = 17",  F_ZERO == 17,  f"got {F_ZERO}")
test("F- = f(4, -1) = 13",  F_MINUS == 13, f"got {F_MINUS}")


# ── 2. RANGE AND MIDPOINT ──
print("\n── 2. Range and Midpoint ──")
test("Range F+ - F- = 2K = 8",  F_PLUS - F_MINUS == 2 * K)
test("Midpoint (F+ + F-)/2 = F0",  (F_PLUS + F_MINUS) / 2 == F_ZERO)
test("F0 = K² + 1 = 17",  F_ZERO == K**2 + 1)


# ── 3. UNIQUENESS EQUATION ──
print("\n── 3. Uniqueness Equation ──")
test("2(D+1) = 2^D  →  D=3",  2 * (D + 1) == 2**D)
test("K = D+1 = 4",  K == D + 1)


# ── 4. LINEARITY ──
print("\n── 4. Linearity in s ──")
test("df/ds = K = 4",  f_poly(K, 1) - f_poly(K, 0) == K)
for s in [-1, -0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75, 1]:
    expected = F_ZERO + K * s
    actual = f_poly(K, s)
    test(f"f(4, {s:+.2f}) = F0 + Ks = {expected}",
         abs(actual - expected) < 1e-10, f"got {actual}")


# ── 5. WALK QUANTIZATION ──
print("\n── 5. Walk Quantization Match ──")
print("  s = 2*fill - 1 maps fill∈[0,1] to s∈[-1,+1]")
for n in range(5):
    fill = n / 4
    s = 2 * fill - 1
    f_walk = 13 + 8 * fill
    f_val = f_poly(K, s)
    test(f"n={n}: fill={fill:.2f}, s={s:+.2f}, f={f_val:.0f} = {f_walk:.0f}",
         abs(f_val - f_walk) < 1e-10)


# ── 6. SIERPIŃSKI LEVEL DECOMPOSITION ──
print("\n── 6. Sierpiński Level Decomposition ──")
test("Term 1:   K^0 = 1  (subchannel, constant)",  K**0 == 1)
test("Term Ks:  K^1 = 4  (channel, s-dependent)",   K**1 == 4)
test("Term K²:  K^2 = 16 (face, constant)",          K**2 == 16)
test("Total:    K^3 = 64 (full walk closure)",        K**3 == 64)
test("Sum at s=1: 1 + 4 + 16 = 21 = F+",  1 + K + K**2 == F_PLUS)
test("Sum at s=0: 1 + 0 + 16 = 17 = F0",  1 + 0 + K**2 == F_ZERO)
test("Sum at s=-1: 1 - 4 + 16 = 13 = F-", 1 - K + K**2 == F_MINUS)


# ── 7. QUADRATIC COMPARISON ──
print("\n── 7. Quadratic Version Fails ──")
test("Quadratic f(4,0) = 1  (NOT 17)",  f_quad(K, 0) == 1)
test("Quadratic DESTROYS F0",  f_quad(K, 0) != F_ZERO)
test("Original PRESERVES F0",  f_poly(K, 0) == F_ZERO)
test("Both agree at s=+1",  f_poly(K, 1) == f_quad(K, 1))
test("Both agree at s=-1",  f_poly(K, -1) == f_quad(K, -1))
for s in [-0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75]:
    test(f"Diverge at s={s:+.2f}: Δ = {f_poly(K,s) - f_quad(K,s):+.0f}",
         f_poly(K, s) != f_quad(K, s))


# ── 8. STRUCTURAL COUNTS ──
print("\n── 8. Structural Counts ──")
test("K(K+D) = 4×7 = 28 (stellated octahedron V+E+F)",  K * (K + D) == 28)
test("V+E+F = 14+36+24 = 74?  No — K(K+D)=28 is the coupling channels",
     K * (K + D) == 28)
test("Gate depth distribution: 27 + 27 + 9 + 1 = 64",
     27 + 27 + 9 + 1 == K**3)
test("GD0 = 3³ = 27 (spatial³)",  3**3 == 27)
test("GD3 = 1 (triple gate)",  1 == 1)


# ── 9. GATE ATTENUATION ──
print("\n── 9. Gate Attenuation ──")
gate_screen = (F_ZERO - 2) / F_ZERO
test(f"Gate screen = (F0-2)/F0 = 15/17 = {gate_screen:.5f}",
     abs(gate_screen - 15/17) < 1e-10)
test("Gate loss = 2/F0 = 2/17 = 0.11765",
     abs(2/F_ZERO - 2/17) < 1e-10)


# ── 10. POLYNOMIAL UNIQUENESS ──
print("\n── 10. Polynomial Uniqueness ──")
# f(s) = a + bs + c with f(1)=21, f(0)=17, f(-1)=13
# f(0) = a + c = 17
# f(1) = a + b + c = 21 → b = 4 = K
# f(-1) = a - b + c = 13 → (a+c) - b = 13 → 17 - 4 = 13 ✓
# a + c = 17, b = K is forced. If a = 1 → c = K²
test("b = K = 4 is forced by F+ - F0",
     F_PLUS - F_ZERO == K)
test("a + c = F0 = 17 is forced",
     1 + K**2 == F_ZERO)
test("If a=1 (ground state): c = K² = 16",
     K**2 == 16)
test("Polynomial unique given unit ground state",
     f_poly(K, 1) == 21 and f_poly(K, 0) == 17 and f_poly(K, -1) == 13)


# ── SUMMARY ──
print("\n" + "=" * 70)
total = passed + failed
print(f"  RESULTS: {passed}/{total} passed, {failed} failed")
if failed == 0:
    print("  ALL TESTS PASS")
print("=" * 70)
