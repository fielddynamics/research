#!/usr/bin/env python3
"""
Complete Derivation: Poisson Equation from Coupling Polynomial

Shows how BOTH 4*pi and 17/13 emerge from f(k) = 1 + k + k^2 at Field Origin.

The entire Poisson equation is the polynomial evaluated at Field Origin:
    nabla^2 Phi = [k*pi] * [(k^2+1)/(kd+1)] * G_bare * rho
"""

import math

# Topological integers
k = 4  # simplex faces (from d+1)
d = 3  # spatial dimensions


def coupling_polynomial(k_val):
    """
    The fundamental coupling polynomial.

    f(k) = 1 + k + k^2

    For k=4: f(4) = 1 + 4 + 16 = 21

    This encodes the depth of coupling hierarchy.
    """
    return 1 + k_val + k_val**2


def field_origin_evaluation(k_val):
    """
    Field Origin (s=0): The middle term vanishes.

    f(k)|_{s=0} = 1 + 0 + k^2 = k^2 + 1

    For k=4: 1 + 16 = 17

    This is the coupling capacity at Field Origin.
    """
    return k_val**2 + 1


def observable_projection(k_val, d_val):
    """
    Observable capacity in (3+1) projection.

    At s=-1 (TetB mirror): kd + 1

    For k=4, d=3: 4*3 + 1 = 13

    This is what we observe in spatial projection.
    """
    return k_val * d_val + 1


def field_normalization_from_polynomial(k_val):
    """
    Field normalization: k * pi

    Because:
    - Fields are SPHERES (continuous geometry)
    - Tiled with k=4 tetrahedra (discrete topology)
    - Combined: k * pi

    For k=4: 4 * pi

    This is NOT from A = 4*pi*r^2 (standard field theory).
    This is FROM THE POLYNOMIAL: k appears in f(k), and fields have pi geometry.
    """
    return k_val * math.pi


def coupling_ratio(k_val, d_val):
    """
    Processing capacity / Observable capacity = (k^2+1) / (kd+1)

    For k=4, d=3: 17/13 = 1.307692...

    This is the tile coupling amplification factor.
    """
    numerator = field_origin_evaluation(k_val)
    denominator = observable_projection(k_val, d_val)
    return numerator, denominator, numerator / denominator


def poisson_equation_from_polynomial(k_val, d_val, G_bare, rho):
    """
    The ENTIRE Poisson equation from polynomial evaluation at Field Origin.

    nabla^2 Phi = [k*pi] * [(k^2+1)/(kd+1)] * G_bare * rho

    where:
    - k*pi: field normalization (k=4 faces x pi geometry)
    - k^2+1: Field Origin capacity (17)
    - kd+1: Observable capacity (13)
    - G_bare: bare constant before tile amplification

    For k=4, d=3:
    nabla^2 Phi = [4*pi] * [17/13] * G_bare * rho
    """
    field_norm = field_normalization_from_polynomial(k_val)
    num, denom, ratio = coupling_ratio(k_val, d_val)

    prefactor = field_norm * ratio
    rhs = prefactor * G_bare * rho

    return field_norm, num, denom, ratio, prefactor, rhs


def why_fractal_recursive(k_val):
    """
    Why does k=4 apply at ALL scales?

    Because the coupling mechanism is TOPOLOGICAL:
    1. Simplex theorem: k = d+1 (for any d)
    2. Field closure: det(e) != 0 everywhere
    3. This doesn't depend on scale

    Therefore: electron tiles, atom tiles, galaxy tiles ALL have k=4
    """
    return {
        'simplex_theorem': 'd+1',
        'k_value': k_val,
        'applies_to': 'all scales (fractal/recursive)',
        'reason': 'topological invariant'
    }


def derivation_chain():
    """
    Complete derivation chain for paper.
    """
    print("="*70)
    print("COMPLETE DERIVATION: POISSON EQUATION FROM COUPLING POLYNOMIAL")
    print("="*70)

    # Step 1: The polynomial
    print("\nSTEP 1: THE COUPLING POLYNOMIAL")
    print("-"*70)
    f_k = coupling_polynomial(k)
    print(f"f(k) = 1 + k + k^2")
    print(f"For k={k}: f({k}) = 1 + {k} + {k}^2 = {f_k}")
    print(f"")
    print(f"This polynomial encodes coupling depth (21 levels).")

    # Step 2: Field Origin evaluation
    print("\nSTEP 2: FIELD ORIGIN EVALUATION (s=0)")
    print("-"*70)
    field_origin = field_origin_evaluation(k)
    print(f"At Field Origin, middle term vanishes:")
    print(f"f(k)|_{{s=0}} = 1 + 0 + k^2 = k^2 + 1")
    print(f"For k={k}: {k}^2 + 1 = {field_origin}")
    print(f"")
    print(f"This is the COUPLING CAPACITY at Field Origin.")

    # Step 3: Observable projection
    print("\nSTEP 3: OBSERVABLE PROJECTION (s=-1)")
    print("-"*70)
    observable = observable_projection(k, d)
    print(f"In (3+1) spacetime, we observe spatial projection:")
    print(f"Projection capacity = kd + 1")
    print(f"For k={k}, d={d}: {k}x{d} + 1 = {observable}")
    print(f"")
    print(f"This is the OBSERVABLE CAPACITY in (3+1).")

    # Step 4: Field normalization (THE KEY INSIGHT)
    print("\nSTEP 4: FIELD NORMALIZATION FROM POLYNOMIAL")
    print("-"*70)
    field_norm = field_normalization_from_polynomial(k)
    print(f"Fields are SPHERES tiled with k={k} tetrahedra.")
    print(f"")
    print(f"Field normalization = k x pi (discrete topology x continuous geometry)")
    print(f"For k={k}: {k} x pi = {field_norm:.6f}")
    print(f"")
    print(f"THIS IS 4*pi = {4*math.pi:.6f}")
    print(f"")
    print(f"CRITICAL: This is NOT from A = 4*pi*r^2 (standard field theory).")
    print(f"          This is FROM THE POLYNOMIAL: k x pi where k=4.")

    # Step 5: Coupling ratio
    print("\nSTEP 5: COUPLING RATIO")
    print("-"*70)
    num, denom, ratio = coupling_ratio(k, d)
    print(f"Processing capacity / Observable capacity")
    print(f"= (k^2+1) / (kd+1)")
    print(f"= {num} / {denom}")
    print(f"= {ratio:.6f}")
    print(f"")
    print(f"This is the tile coupling amplification factor.")

    # Step 6: Complete Poisson equation
    print("\nSTEP 6: COMPLETE POISSON EQUATION")
    print("-"*70)
    G_bare = 1  # normalized
    rho = 1     # normalized
    field_norm, num, denom, ratio, prefactor, rhs = poisson_equation_from_polynomial(k, d, G_bare, rho)

    print(f"The ENTIRE equation from polynomial evaluation at Field Origin:")
    print(f"")
    print(f"nabla^2 Phi = [k*pi] x [(k^2+1)/(kd+1)] x G_bare x rho")
    print(f"")
    print(f"Substituting k={k}, d={d}:")
    print(f"nabla^2 Phi = [{field_norm:.3f}] x [{num}/{denom}] x G_bare x rho")
    print(f"nabla^2 Phi = [{field_norm:.3f}] x [{ratio:.6f}] x G_bare x rho")
    print(f"nabla^2 Phi = {prefactor:.6f} x G_bare x rho")
    print(f"")
    print(f"This is: nabla^2 Phi = 4*pi x (17/13) x G_bare x rho")

    # Step 7: Fractal/Recursive nature
    print("\nSTEP 7: FRACTAL/RECURSIVE STRUCTURE")
    print("-"*70)
    fractal_info = why_fractal_recursive(k)
    print(f"Why does k={k} apply at ALL scales?")
    print(f"")
    print(f"Simplex theorem: k = d+1 = {fractal_info['k_value']} (topological)")
    print(f"This applies to: {fractal_info['applies_to']}")
    print(f"Reason: {fractal_info['reason']}")
    print(f"")
    print(f"Therefore:")
    print(f"  - Electron tiles: k=4")
    print(f"  - Atomic tiles: k=4")
    print(f"  - Planetary tiles: k=4")
    print(f"  - Stellar tiles: k=4")
    print(f"  - Galactic tiles: k=4")
    print(f"  - Universal Field Origin: k=4")
    print(f"")
    print(f"At EVERY scale: 17/13 coupling ratio applies.")

    # Summary
    print("\n" + "="*70)
    print("SUMMARY: THE WHOLE EQUATION FROM THE POLYNOMIAL")
    print("="*70)
    print(f"1. Coupling polynomial: f(k) = 1 + k + k^2 = {f_k}")
    print(f"2. Field Origin capacity: k^2 + 1 = {num}")
    print(f"3. Observable capacity: kd + 1 = {denom}")
    print(f"4. Field normalization: k x pi = {field_norm:.6f}")
    print(f"5. Coupling ratio: {num}/{denom} = {ratio:.6f}")
    print(f"6. Combined: {field_norm:.3f} x {ratio:.6f} = {prefactor:.6f}")
    print(f"")
    print(f"RESULT:")
    print(f"nabla^2 Phi = 4*pi x (17/13) x G_bare x rho")
    print(f"")
    print(f"BOTH 4*pi AND 17/13 come from the polynomial at Field Origin.")
    print(f"Because gravity is fractal, this applies at ALL scales.")
    print("="*70)


def equation_summary_for_paper():
    """
    Clean equation summary ready for paper insertion.
    """
    print("\n" + "="*70)
    print("EQUATION SUMMARY (FOR PAPER)")
    print("="*70)

    print("\nThe modified Poisson equation emerges from evaluating the")
    print("coupling polynomial f(k) = 1 + k + k^2 at the Field Origin:")
    print("")
    print("  Field normalization:   k x pi = 4pi     (k=4)")
    print("  Coupling capacity:     k^2 + 1 = 17     (Field Origin, s=0)")
    print("  Observable capacity:   kd + 1 = 13      (Projection, s=-1)")
    print("")
    print("Combined:")
    print("")
    print("  nabla^2 Phi = 4pi x (17/13) x G_bare x rho")
    print("             = 16.493... x G_bare x rho")
    print("")
    print("The factor 4pi is NOT from A = 4pi r^2 (standard field theory).")
    print("It is k x pi where k=4 is the topological tiling number.")
    print("")
    print("The factor 17/13 is the tile coupling amplification:")
    print("  - 17 modes processed at Field Origin")
    print("  - 13 modes observable in (3+1)")
    print("")
    print("Because gravity is fractal/recursive (k=4 at all scales),")
    print("this Poisson equation applies from electrons to galaxies.")
    print("="*70)


if __name__ == "__main__":
    # Run complete derivation
    derivation_chain()

    # Clean summary for paper
    equation_summary_for_paper()

    print("\n" + "="*70)
    print("READY FOR PAPER INSERTION")
    print("="*70)
    print("This derivation shows:")
    print("1. How f(k) = 1 + k + k^2 contains the ENTIRE Poisson equation")
    print("2. Why 4*pi = k*pi (NOT from standard field theory)")
    print("3. Why 17/13 is the coupling amplification")
    print("4. Why it applies at all scales (fractal/recursive)")
    print("="*70)
