# Corrections Checklist for run_all_validations.py

**Estimated Time:** 50 minutes
**Priority:** HIGH (Required before publication/sharing)
**Difficulty:** LOW (Search and replace)

---

## Quick Fixes Required

### 1. Organization Block Header (Lines 17-50)

**Location:** Top of file, in main docstring

**Current (WRONG):**
```python
Organization (mirrors paper sections):

    Section II   -- Theoretical Foundations
                    Characteristic scale convergence (two routes to r_e)

    Section III  -- The (3+1)^2 Foundation
                    Coupling hierarchy, structural states, prefactor, spin,
                    structural identification (S = C, five-point proof),
                    mass as closure energy (omega_closure, omega_state,
                    m = hbar/(Nrc), Compton frequency identity)

    Section IV   -- The (3+1) Equations
                    G from topology, G(d), exponent sensitivity, force hierarchy

    Section VI   -- The Fine Structure Constant
                    Alpha as scale ratio, integer 137, face-channels,
                    alpha from topological breadth, alpha from physical rates,
                    Hamiltonian grounding of the breadth (every integer traced
                    to bimetric Hamiltonian: DOFs, evaluation sites, channels)

    Section VII  -- Dark Matter and the Hubble Constant
                    Dark matter (a_0, mu(x), deep-MOND, flat rotation,
                    dark fraction, corrective lens, aperture, rotation
                    curves), Hubble constant prediction (H from topology)

    Section VIII -- Conclusion
                    Beta_n determination (covariant completion: parity,
                    metric exchange, odd-parity vanishing, coupling polynomial,
                    V(S) = e_0 + 16*e_2 + e_4, weighted channel count),
                    electron mass (exactly determined system),
                    round-trip test, precision table
```

**Replace with (CORRECT):**
```python
Organization (mirrors paper sections):

    Section 2  -- Why Gravity Has Topology
                  Characteristic scale convergence (two routes to r_e)

    Section 3  -- The Dual Tetrahedron
                  Spin from face ratio (two routes), 28 geometric elements,
                  structural identification (S = C, five-point proof)

    Section 4  -- The Coupling Polynomial
                  f(k) = 1 + k + k^2 = 21, structural states (21, 17, 13),
                  prefactor 17/13 = (k^2+1)/(kd+1)

    Section 5  -- Equations from the Dual Tetrahedron Topology
                  G from topology, G(d), exponent sensitivity, force hierarchy,
                  mass as closure energy (omega_closure, omega_state,
                  m = hbar/(Nrc), Compton frequency identity)

    Section 6  -- The Fine-Structure Constant
                  Alpha as scale ratio, integer 137, face-channels,
                  alpha from topological breadth, alpha from physical rates,
                  Hamiltonian grounding of the breadth (every integer traced
                  to bimetric Hamiltonian: DOFs, evaluation sites, channels)

    Section 7  -- Dark Matter and the Hubble Constant
                  Dark matter (a_0, mu(x), deep-MOND, flat rotation,
                  dark fraction, corrective lens, aperture, rotation
                  curves), Hubble constant prediction (H from topology)

    Section 8  -- Covariant Completion
                  Beta_n determination (parity, metric exchange,
                  odd-parity vanishing, coupling polynomial),
                  V(S) = e_0 + 16*e_2 + e_4, weighted channel count

    Section 9  -- The Electron Mass
                  Two-equation exactly determined system,
                  r^3 = 16*pi^(3/2)*alpha*hbar*G/(c^2*H),
                  m = alpha*hbar/(rc), round-trip test

    Section 10 -- Discussion and Conclusion
                  One-loop correction (Schwinger), precision table,
                  logic chain, empirical validation summary
```

---

### 2. Section Header Comments

**Search for:** `# SECTION II:`
**Replace with:** `# SECTION 2:`

**Search for:** `# SECTION III:`
**Replace with:** `# SECTION 3:`

**Search for:** `# SECTION IV:`
**Replace with:** `# SECTION 5:`

**Search for:** `# SECTION VI:`
**Replace with:** `# SECTION 6:`

**Search for:** `# SECTION VII:`
**Replace with:** `# SECTION 7:`

**Search for:** `# SECTION VIII:`
**Replace with:** `# SECTIONS 8, 9, 10:`

#### Specific Line Numbers:

- [ ] Line 137: `# SECTION II: THEORETICAL FOUNDATIONS` → `# SECTION 2: WHY GRAVITY HAS TOPOLOGY`
- [ ] Line 207: `# SECTION III: THE (3+1)^2 FOUNDATION` → `# SECTION 3: THE DUAL TETRAHEDRON`
- [ ] Line 639: `# SECTION IV: THE (3+1) EQUATIONS` → `# SECTION 5: EQUATIONS FROM THE DUAL TETRAHEDRON TOPOLOGY`
- [ ] Line 789: `# SECTION VI: THE FINE STRUCTURE CONSTANT` → `# SECTION 6: THE FINE-STRUCTURE CONSTANT`
- [ ] Line 1188: `# SECTION VIII: CONCLUSION` → `# SECTIONS 8, 9, 10: COVARIANT COMPLETION, ELECTRON MASS, CONCLUSION`

---

### 3. Print Statement Headers

**Search for:** `"SECTION II`
**Replace with:** `"SECTION 2`

**Search for:** `"SECTION III`
**Replace with:** `"SECTION 3`

**Search for:** `"SECTION IV`
**Replace with:** `"SECTION 5`

**Search for:** `"SECTION VI`
**Replace with:** `"SECTION 6`

**Search for:** `"SECTION VII`
**Replace with:** `"SECTION 7`

**Search for:** `"SECTION VIII`
**Replace with:** `"SECTION 8` or `"SECTION 9` or `"SECTION 10` (context-dependent)

#### Specific Examples:

- [ ] Line 159: `"SECTION II.D: CLASSICAL ELECTRON RADIUS"` → `"SECTION 2.5: CLASSICAL ELECTRON RADIUS"`
- [ ] Line 191: `"SECTION II.D: GRAVITATIONAL ELECTRON RADIUS"` → `"SECTION 2.5: GRAVITATIONAL ELECTRON RADIUS"`
- [ ] Line 230: `"SECTION III.E: COUPLING HIERARCHY"` → `"SECTION 4.1: COUPLING HIERARCHY"`
- [ ] Line 267: `"SECTION III.F: THREE STRUCTURAL STATES"` → `"SECTION 4.4: THREE STRUCTURAL STATES"`
- [ ] Line 314: `"SECTION III.F: PREFACTOR DECOMPOSITION"` → `"SECTION 4.4: PREFACTOR DECOMPOSITION"`
- [ ] Line 348: `"SECTION III.F: SPIN FROM FACE RATIO"` → `"SECTION 3.3: SPIN FROM FACE RATIO"`
- [ ] Line 410: `"SECTION III.G: STRUCTURAL IDENTIFICATION"` → `"SECTION 3.2: STRUCTURAL IDENTIFICATION"`
- [ ] Line 527: `"SECTION III.E: MASS AS THE ENERGY COST OF FIELD CLOSURE"` → `"SECTION 5: MASS AS CLOSURE ENERGY"`
- [ ] Line 664: `"SECTION IV.A: RESULT 1 -- G FROM TETRAD TOPOLOGY"` → `"SECTION 5.1: RESULT 1 -- G FROM TETRAD TOPOLOGY"`
- [ ] Line 703: `"SECTION IV.A: G IN TERMS OF d"` → `"SECTION 5.1: G IN TERMS OF d"`
- [ ] Line 734: `"SECTION IV.A: EXPONENT SENSITIVITY"` → `"SECTION 5.1: EXPONENT SENSITIVITY"`
- [ ] Line 767: `"SECTION IV.D: RESULT 4 -- FORCE HIERARCHY"` → `"SECTION 5.2: RESULT 4 -- FORCE HIERARCHY"`

---

### 4. Function Docstrings

**Pattern to find:** `Section II`, `Section III`, `Section IV`, `Section VI`, `Section VII`, `Section VIII`

**Replace with:** `Section 2`, `Section 3`, `Section 5`, `Section 6`, `Section 7`, `Section 8/9/10`

#### Key Functions to Update:

- [ ] `validate_classical_electron_radius()` line 150: `Section II.D` → `Section 2.5`
- [ ] `validate_gravitational_electron_radius()` line 181: `Section II.D` → `Section 2.5`
- [ ] `validate_coupling_hierarchy()` line 220: `Section III.E` → `Section 4.1`
- [ ] `validate_structural_states()` line 254: `Section III.F` → `Section 4.4`
- [ ] `validate_prefactor()` line 303: `Section III.F` → `Section 4.4`
- [ ] `validate_spin()` line 335: `Section III.F` → `Section 3.3`
- [ ] `validate_structural_identification()` line 392: `Section III.G` → `Section 3.2`
- [ ] `validate_mass_closure_energy()` line 503: `Section III.E` → `Section 5 (Mass Closure)`
- [ ] `validate_G_from_topology()` line 652: `Section IV.A` → `Section 5.1`
- [ ] `validate_G_general_d()` line 695: `Section IV.A` → `Section 5.1`
- [ ] `validate_exponent_sensitivity()` line 726: `Section IV.A` → `Section 5.1`
- [ ] `validate_force_hierarchy()` line 758: `Section IV.D` → `Section 5.2`
- [ ] `validate_alpha_scale_ratio()` line 802: `Section VI.A` → `Section 6.1`
- [ ] `validate_integer_137()` line 837: `Section VI.B` → `Section 6.2`
- [ ] `validate_face_channel_count()` line 875: `Section VI.B` → `Section 6.2`
- [ ] `validate_alpha_topological()` line 921: `Section VI.B` → `Section 6.2`
- [ ] `validate_alpha_from_rates()` line 968: `Section VI.C` → `Section 6.4`
- [ ] `validate_hamiltonian_grounding()` line 1032: `Section VI.B` → `Section 6.2`
- [ ] `validate_beta_determination()` line 1204: `Section VIII (Covariant Completion)` → `Section 8`
- [ ] `validate_a0()` line 1372: `Section VII` → `Section 7.1`
- [ ] `validate_cosmological_connection()` line 1405: `Section VII` → `Section 7.2`
- [ ] `validate_mu_detailed_balance()` line 1445: `Section VII` → `Section 7.1`
- [ ] `validate_deep_mond_limit()` line 1495: `Section VII` → `Section 7.1`
- [ ] `validate_flat_rotation()` line 1541: `Section VII` → `Section 7.1`
- [ ] `validate_dark_fraction()` line 1583: `Section VII` → `Section 7.1`
- [ ] `validate_corrective_lens()` line 1622: `Section VII` → `Section 7.1`
- [ ] `validate_aperture_correction()` line 1671: `Section VII` → `Section 7.2`
- [ ] `validate_H_from_topology()` line 1703: `Section VII` → `Section 7.2`
- [ ] `validate_rotation_curves()` line 1762: `Section VII` → `Section 7.1`
- [ ] `validate_precision_table()` line 1815: `Section VIII.D` → `Section 10.3`
- [ ] `validate_one_loop_correction()` line 1916: `Section VIII.D` → `Section 10.1`
- [ ] `validate_electron_mass()` line 2015: `Section VIII.E` → `Section 9.1`
- [ ] `validate_round_trip()` line 2095: `Section VIII` → `Section 10`

---

### 5. Main Function Updates

**Location:** Lines 2206-2267 (main function)

**Current section headers:**
```python
# ===== Section II: Theoretical Foundations =====
# ===== Section III: The (3+1)^2 Foundation =====
# ===== Section IV: The (3+1) Equations =====
# ===== Section VI: The Fine Structure Constant =====
# ===== Section VII: Dark Matter and the Hubble Constant =====
# ===== Section VIII: Conclusion =====
```

**Replace with:**
```python
# ===== Section 2: Why Gravity Has Topology =====
# ===== Section 3: The Dual Tetrahedron =====
# ===== Section 4: The Coupling Polynomial =====
# ===== Section 5: Equations from the Dual Tetrahedron Topology =====
# ===== Section 6: The Fine-Structure Constant =====
# ===== Section 7: Dark Matter and the Hubble Constant =====
# ===== Section 8: Covariant Completion =====
# ===== Section 9: The Electron Mass =====
# ===== Section 10: Discussion and Conclusion =====
```

**Also update print statements:**
```python
# Line 2207-2209:
print(f"\n\n{'':=<78}")
print(f"  SECTION 2: WHY GRAVITY HAS TOPOLOGY")
print(f"{'':=<78}")

# Line 2213-2215:
print(f"\n\n{'':=<78}")
print(f"  SECTION 3: THE DUAL TETRAHEDRON")
print(f"{'':=<78}")

# ADD NEW:
print(f"\n\n{'':=<78}")
print(f"  SECTION 4: THE COUPLING POLYNOMIAL")
print(f"{'':=<78}")

# Line 2224-2226:
print(f"\n\n{'':=<78}")
print(f"  SECTION 5: EQUATIONS FROM THE DUAL TETRAHEDRON TOPOLOGY")
print(f"{'':=<78}")

# Line 2233-2235:
print(f"\n\n{'':=<78}")
print(f"  SECTION 6: THE FINE-STRUCTURE CONSTANT")
print(f"{'':=<78}")

# Line 2244-2246:
print(f"\n\n{'':=<78}")
print(f"  SECTION 7: DARK MATTER AND THE HUBBLE CONSTANT")
print(f"{'':=<78}")

# Line 2259-2261:
print(f"\n\n{'':=<78}")
print(f"  SECTION 8: COVARIANT COMPLETION")
print(f"{'':=<78}")

# ADD NEW:
print(f"\n\n{'':=<78}")
print(f"  SECTION 9: THE ELECTRON MASS")
print(f"{'':=<78}")

# ADD NEW:
print(f"\n\n{'':=<78}")
print(f"  SECTION 10: DISCUSSION AND CONCLUSION")
print(f"{'':=<78}")
```

---

## Testing After Corrections

### Quick Verification

1. **Run the script:**
   ```bash
   python run_all_validations.py > output.txt
   ```

2. **Check output headers match paper sections:**
   ```bash
   grep "SECTION [0-9]" output.txt
   ```
   Should show: SECTION 2, SECTION 3, SECTION 4, SECTION 5, SECTION 6, SECTION 7, SECTION 8, SECTION 9, SECTION 10

3. **Verify no Roman numerals remain:**
   ```bash
   grep -i "section ii\|section iii\|section iv\|section vi\|section vii\|section viii" run_all_validations.py
   ```
   Should return: (empty)

4. **Check all docstrings:**
   ```bash
   grep "Section II\|Section III\|Section IV\|Section VI\|Section VII\|Section VIII" run_all_validations.py
   ```
   Should return: (empty)

---

## Completion Checklist

- [ ] Updated organization block (lines 17-50)
- [ ] Updated all section header comments (6 locations)
- [ ] Updated all print statement headers (~30 locations)
- [ ] Updated all function docstrings (~33 functions)
- [ ] Reorganized main() to include Sections 4, 8, 9, 10 explicitly
- [ ] Ran script to verify output
- [ ] Verified no Roman numerals remain in code
- [ ] Verified section numbers match paper (1-10, not II-VIII)

---

## Optional Enhancements (Future)

- [ ] Add `validate_ligo_polarization_count()` for Section 2.1
- [ ] Add `validate_geometric_series_argument()` for Section 4.2
- [ ] Add input validation for constants
- [ ] Add better summary statistics by section
- [ ] Generate LaTeX table output for direct paper inclusion

---

**Status:** Ready for corrections
**Next Action:** Implement all checked items above
**Estimated Time:** 50 minutes
