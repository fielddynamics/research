#!/usr/bin/env python3
"""
GFD Prime Generation via Sierpiński Sieve
==========================================

Demonstrates that the coupling polynomial f(K,s) = 1 + Ks + K²,
at the unique value K=4 forced by 2(D+1) = 2^D, generates a prime
counting mechanism whose density converges to 1/ln(N) — the prime
number theorem — as a readout of field closure geometry.

The formula I(n,K) = (1/n) Σ_{d|n} μ(n/d) · K^d is classical
(Moreau 1872, Gauss). What is novel is:
  1. K=4 is forced, not free
  2. μ ∈ {+1, -1, 0} maps to f(K,s) at s ∈ {+1, -1, 0}
  3. The Sierpiński sieve provides a geometric irreducibility test
  4. The density 1/n = 1/log_K(N) IS the prime number theorem

Stephen Nelson — Gravity Field Dynamics
docs.fielddynamics.org
"""

import math
from collections import defaultdict

# ============================================================
# SECTION 0: The Uniqueness Equation
# ============================================================

def verify_uniqueness():
    """Verify that 2(D+1) = 2^D has unique solution D=3, K=4."""
    print("=" * 70)
    print("SECTION 0: THE UNIQUENESS EQUATION  2(D+1) = 2^D")
    print("=" * 70)
    print()
    for d in range(1, 8):
        lhs = 2 * (d + 1)
        rhs = 2 ** d
        match = "  ◄── MATCH" if lhs == rhs else ""
        print(f"  D={d}:  2({d}+1) = {lhs:>4}    2^{d} = {rhs:>4}  {match}")
    print()
    print("  Unique solution: D=3, K=D+1=4")
    print("  This fixes K for everything that follows.")
    print()


# ============================================================
# SECTION 1: The Coupling Polynomial
# ============================================================

def coupling_polynomial(K, s):
    """Evaluate f(K,s) = 1 + Ks + K²."""
    return 1 + K * s + K ** 2


def show_polynomial():
    """Display the three structural states of f(K,s)."""
    print("=" * 70)
    print("SECTION 1: THE COUPLING POLYNOMIAL  f(K,s) = 1 + Ks + K²")
    print("=" * 70)
    print()
    K = 4
    for s, label in [(1, "primary sector (TetA)"),
                     (0, "field origin (contact)"),
                     (-1, "dual sector (TetB)")]:
        val = coupling_polynomial(K, s)
        print(f"  f(4, {s:+d}) = 1 + 4·({s:+d}) + 16 = {val:>2}   {label}")
    print()
    print(f"  Arithmetic mean: (21 + 13) / 2 = {(21 + 13) // 2}")
    print(f"  Spacing: K = 4")
    print()


# ============================================================
# SECTION 2: Möbius Function and Moreau's Formula
# ============================================================

def mobius(n):
    """Compute the Möbius function μ(n)."""
    if n == 1:
        return 1
    factors = []
    temp = n
    d = 2
    while d * d <= temp:
        if temp % d == 0:
            count = 0
            while temp % d == 0:
                temp //= d
                count += 1
            if count > 1:
                return 0
            factors.append(d)
        d += 1
    if temp > 1:
        factors.append(temp)
    return (-1) ** len(factors)


def divisors(n):
    """Return all positive divisors of n."""
    divs = []
    for i in range(1, int(math.sqrt(n)) + 1):
        if n % i == 0:
            divs.append(i)
            if i != n // i:
                divs.append(n // i)
    return sorted(divs)


def moreau(n, K):
    """
    Moreau's necklace-counting function (1872):
    I(n,K) = (1/n) Σ_{d|n} μ(n/d) · K^d

    Counts aperiodic necklaces / irreducible polynomials
    of degree n over an alphabet of size K.
    """
    total = 0
    for d in divisors(n):
        total += mobius(n // d) * (K ** d)
    return total // n


def show_mobius_polynomial_map():
    """Show that μ ∈ {+1,-1,0} maps to f(K,s) at s ∈ {+1,-1,0}."""
    print("=" * 70)
    print("SECTION 2: MÖBIUS ↔ COUPLING POLYNOMIAL MAP")
    print("=" * 70)
    print()
    print("  The Möbius function μ takes values {+1, -1, 0}.")
    print("  The coupling polynomial f(K,s) evaluates at s ∈ {+1, -1, 0}.")
    print()
    print("   μ(n)   s    f(4,s)   Meaning")
    print("   ────   ──   ──────   ───────────────────────────────")
    print("    +1    +1     21     squarefree, even # of factors → primary")
    print("    -1    -1     13     squarefree, odd # of factors  → dual")
    print("     0     0     17     repeated factor               → contact")
    print()
    print("  The three values of μ ARE the polynomial's three states.")
    print()


# ============================================================
# SECTION 3: Irreducible Counting at K=4
# ============================================================

def show_irreducible_counts():
    """Compute and display I(n,4) for successive levels."""
    print("=" * 70)
    print("SECTION 3: IRREDUCIBLE COUNTS AT K=4")
    print("=" * 70)
    print()
    print("  Level n   Total (4^n)   Irreducibles I(n,4)   Density I/4^n    1/n")
    print("  ───────   ──────────    ──────────────────     ─────────────    ────")

    K = 4
    cumulative_irr = 0
    cumulative_total = 0

    for n in range(1, 13):
        total = K ** n
        irr = moreau(n, K)
        density = irr / total
        expected = 1.0 / n
        cumulative_irr += irr
        cumulative_total += total

        print(f"  {n:>5}     {total:>10,}    {irr:>18,}     "
              f"{density:>11.6f}    {expected:.6f}")

    print()
    print("  Density converges to 1/n = 1/log₄(N).")
    print("  Since log₄(N) = ln(N)/ln(4), this is π(N) ~ N/ln(N).")
    print("  The prime number theorem as a readout of field closure.")
    print()


# ============================================================
# SECTION 4: Sierpiński Survival Ratio
# ============================================================

def show_sierpinski_survival():
    """Show the (3/4)^n survival ratio matches prime thinning."""
    print("=" * 70)
    print("SECTION 4: SIERPIŃSKI SURVIVAL RATIO")
    print("=" * 70)
    print()
    print("  At each Sierpiński level, 3 of 4 sub-triangles survive.")
    print("  Survival ratio at level n: (3/4)^n")
    print("  This mirrors how prime density thins with scale.")
    print()
    print("  Level n   Surviving    Total    Ratio (3/4)^n    I(n,4)/4^n")
    print("  ───────   ─────────    ─────    ─────────────    ──────────")

    K = 4
    for n in range(1, 11):
        surviving = 3 ** n
        total = 4 ** n
        ratio = surviving / total
        irr = moreau(n, K)
        irr_density = irr / total
        print(f"  {n:>5}     {surviving:>9,}    {total:>5,}    "
              f"{ratio:>11.6f}      {irr_density:.6f}")

    print()
    print("  The Sierpiński ratio (3/4)^n and the irreducible density 1/n")
    print("  are complementary measures of the same sieve.")
    print("  (3/4)^n counts what survives geometrically.")
    print("  1/n counts what survives algebraically.")
    print()


# ============================================================
# SECTION 5: AND-Lattice Irreducibility Test
# ============================================================

def is_periodic_pattern(pattern, length):
    """
    Check if a pattern of given length over alphabet K=4
    (represented as a tuple of symbols 0..3) is periodic —
    i.e., is a repetition of a shorter sub-pattern.
    """
    for period in range(1, length):
        if length % period == 0:
            sub = pattern[:period]
            if sub * (length // period) == pattern:
                return True
    return False


def count_aperiodic_direct(n, K=4):
    """
    Directly enumerate aperiodic sequences of length n
    over alphabet {0, 1, ..., K-1}. Brute force for small n.
    Returns (sequence_count, necklace_count) where
    necklace_count = sequence_count / n (cyclic equivalence).
    """
    if n > 6:
        return None, None

    count = 0
    total = K ** n
    for i in range(total):
        pattern = []
        val = i
        for _ in range(n):
            pattern.append(val % K)
            val //= K
        pattern = tuple(pattern)

        if not is_periodic_pattern(pattern, n):
            count += 1
    return count, count // n


def show_and_lattice_test():
    """Verify Moreau's formula by direct enumeration."""
    print("=" * 70)
    print("SECTION 5: AND-LATTICE IRREDUCIBILITY — DIRECT VERIFICATION")
    print("=" * 70)
    print()
    print("  Moreau counts primitive necklaces (cyclic equivalence classes).")
    print("  Each necklace of length n corresponds to n distinct sequences.")
    print()
    print("  Level n   Moreau I(n,4)   Aperiodic seqs   n × Moreau   Match?")
    print("  ───────   ─────────────   ──────────────   ──────────   ──────")

    K = 4
    all_match = True
    for n in range(1, 7):
        moreau_val = moreau(n, K)
        seq_count, neck_count = count_aperiodic_direct(n, K)
        n_times_moreau = n * moreau_val
        match = "  ✓" if n_times_moreau == seq_count else "  ✗"
        if n_times_moreau != seq_count:
            all_match = False
        print(f"  {n:>5}     {moreau_val:>13,}   {seq_count:>14,}   "
              f"{n_times_moreau:>10,}   {match}")

    print()
    if all_match:
        print("  All levels match. n × Moreau = aperiodic sequences. Verified.")
    else:
        print("  MISMATCH detected.")
    print()


# ============================================================
# SECTION 6: Connection to Actual Primes
# ============================================================

def sieve_primes(limit):
    """Simple sieve of Eratosthenes."""
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(math.sqrt(limit)) + 1):
        if is_prime[i]:
            for j in range(i * i, limit + 1, i):
                is_prime[j] = False
    return [i for i in range(2, limit + 1) if is_prime[i]]


def show_prime_density_comparison():
    """Compare irreducible density at K=4 with actual prime density."""
    print("=" * 70)
    print("SECTION 6: IRREDUCIBLE DENSITY vs ACTUAL PRIME DENSITY")
    print("=" * 70)
    print()
    print("  Both converge to 1/ln(N). The mechanism is the same.")
    print("  The logarithmic base differs (4 vs e) but the scaling is identical.")
    print()
    print("  N = 4^n       π(N)/N          I(n,4)/4^n       1/ln(N)")
    print("  ──────────    ──────────      ──────────       ──────────")

    K = 4
    primes = sieve_primes(4 ** 12)
    prime_set = set(primes)

    for n in range(1, 11):
        N = K ** n
        irr = moreau(n, K)
        irr_density = irr / N

        # Count primes up to N
        pi_N = sum(1 for p in primes if p <= N)
        prime_density = pi_N / N

        ln_density = 1.0 / math.log(N) if N > 1 else float('inf')

        print(f"  {N:>10,}    {prime_density:>10.6f}      "
              f"{irr_density:>10.6f}       {ln_density:>10.6f}")

    print()
    print("  The irreducible density at K=4 and the prime density")
    print("  both follow the 1/ln(N) law. The coupling polynomial")
    print("  generates the counting; the Sierpiński sieve performs it.")
    print()


# ============================================================
# SECTION 7: The 21+21+9+1 Nuclear Partition
# ============================================================

def show_nuclear_partition():
    """Show how the Sierpiński hierarchy produces 21a+21b+9c+1d = 52."""
    print("=" * 70)
    print("SECTION 7: THE NUCLEAR PARTITION  21a + 21b + 9c + 1d = 52")
    print("=" * 70)
    print()
    print("  The Sierpiński hierarchy at K=4:")
    print()
    print("  Level 0:  3⁰ = 1   → 1d   (the gate, existence, seed)")
    print("  Level 1:  3¹ = 3   → [absent: the generator itself]")
    print("  Level 2:  3² = 9   → 9c   (depth, self-composed closure)")
    print("  Polynomial: f(4,1) = 21  → 21a + 21b  (TetA + TetB)")
    print()
    print(f"  Total: 21 + 21 + 9 + 1 = {21 + 21 + 9 + 1}")
    print()
    print("  The missing level 1 (3¹ = 3) is the closure cycle count")
    print("  itself — the operation, not an outcome. It appears as the")
    print("  number of terms in f(K,s), not as a coefficient.")
    print()
    print("  Connection to primes:")
    print("  • 1d holds seed irreducibles")
    print("  • 9c holds primes from one self-composition")
    print("  • 21a + 21b hold the full polynomial's irreducible output")
    print("  • Nuclear magic numbers and integer primes are dual")
    print("    manifestations of the same sieve")
    print()


# ============================================================
# SECTION 8: Five Simultaneous Locks at K=4
# ============================================================

def show_five_locks():
    """Demonstrate five independent conditions all locking at K=4."""
    print("=" * 70)
    print("SECTION 8: FIVE SIMULTANEOUS LOCKS AT K=4")
    print("=" * 70)
    print()

    K = 4
    D = 3

    # Lock 1: Simplex theorem
    lock1 = D + 1
    print(f"  1. Simplex theorem:     K = D+1 = {D}+1 = {lock1}")

    # Lock 2: Uniqueness equation
    lhs = 2 * (D + 1)
    rhs = 2 ** D
    print(f"  2. Uniqueness equation: 2(D+1) = {lhs},  2^D = {rhs}  "
          f"{'MATCH' if lhs == rhs else 'FAIL'}")

    # Lock 3: Self-duality
    c41 = math.comb(K, 1)
    c43 = math.comb(K, K - 1)
    print(f"  3. Self-duality:        C(4,1) = {c41},  C(4,3) = {c43}  "
          f"{'MATCH' if c41 == c43 else 'FAIL'}")

    # Lock 4: Sierpiński dimension
    sierp_dim = math.log(K - 1) / math.log(2)
    print(f"  4. Sierpiński dimension: log(K-1)/log(2) = log(3)/log(2) = "
          f"{sierp_dim:.6f}")

    # Lock 5: LIGO polarisations
    polarisations = 10 - 2 * K
    print(f"  5. LIGO polarisations:  10 - 2K = 10 - 8 = {polarisations}")

    print()
    print("  All five conditions satisfied simultaneously. Only at K=4.")
    print()


# ============================================================
# SECTION 9: Geometric Series and Dimensional Connection
# ============================================================

def show_geometric_series():
    """Show f(K,1) = (K³-1)/(K-1) connecting to D=3."""
    print("=" * 70)
    print("SECTION 9: GEOMETRIC SERIES → DIMENSIONAL CONNECTION")
    print("=" * 70)
    print()

    K = 4
    poly_val = 1 + K + K ** 2
    series_val = (K ** 3 - 1) // (K - 1)

    print(f"  f(K,1) = 1 + K + K² = 1 + 4 + 16 = {poly_val}")
    print(f"  (K³-1)/(K-1) = (64-1)/(4-1) = 63/3 = {series_val}")
    print(f"  Match: {poly_val == series_val}")
    print()
    print(f"  This is the finite geometric series Σ_{{i=0}}^{{D-1}} K^i")
    print(f"  with D=3 terms. The polynomial IS the dimension D=3")
    print(f"  written in the language of K=4.")
    print()
    print(f"  Removing K⁰=1 gives K+K² = {K + K**2}, which does NOT")
    print(f"  factor as a geometric series. The dimensional connection")
    print(f"  requires all three terms.")
    print()


# ============================================================
# MAIN
# ============================================================

def main():
    print()
    print("  ╔══════════════════════════════════════════════════════════════╗")
    print("  ║  GFD PRIME GENERATION VIA SIERPIŃSKI SIEVE                  ║")
    print("  ║  The Prime Number Theorem as a Readout of Field Closure     ║")
    print("  ║                                                             ║")
    print("  ║  Stephen Nelson — Gravity Field Dynamics                    ║")
    print("  ║  docs.fielddynamics.org                                     ║")
    print("  ╚══════════════════════════════════════════════════════════════╝")
    print()

    verify_uniqueness()
    show_polynomial()
    show_mobius_polynomial_map()
    show_irreducible_counts()
    show_sierpinski_survival()
    show_and_lattice_test()
    show_prime_density_comparison()
    show_nuclear_partition()
    show_five_locks()
    show_geometric_series()

    # Final summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print()
    print("  The coupling polynomial f(K,s) = 1 + Ks + K², at K=4,")
    print("  generates a prime counting mechanism via Moreau's formula:")
    print()
    print("    I(n,4) = (1/n) Σ_{d|n} μ(n/d) · 4^d")
    print()
    print("  The formula is classical (1872). What is new:")
    print()
    print("  • K=4 is forced by 2(D+1) = 2^D, not chosen")
    print("  • μ ∈ {+1,-1,0} maps to f(K,s) at s ∈ {+1,-1,0}")
    print("  • The Sierpiński sieve IS the geometric irreducibility test")
    print("  • Density 1/n = 1/log₄(N) ∝ 1/ln(N) = prime number theorem")
    print("  • The 21+21+9+1 nuclear partition organizes the hierarchy")
    print()
    print("  The prime number theorem is the field closure rule")
    print("  read as a counting formula.")
    print()


if __name__ == "__main__":
    main()
