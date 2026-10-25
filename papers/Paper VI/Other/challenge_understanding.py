#!/usr/bin/env python3
"""
CHALLENGE: Where do we ACTUALLY start?

Let me think about this with complete mathematical rigor.
"""

import numpy as np

print('='*75)
print('CHALLENGING THE UNDERSTANDING: WHERE DO WE START?')
print('='*75)
print()

# Define the geometry
VERTICES = {
    0: np.array([0, 0, 0]),  # Earth  - Tet B apex
    1: np.array([0, 0, 1]),  # Thunder
    2: np.array([0, 1, 0]),  # Water
    3: np.array([0, 1, 1]),  # Mountain/Wind
    4: np.array([1, 0, 0]),  # Lake/Thunder
    5: np.array([1, 0, 1]),  # Fire
    6: np.array([1, 1, 0]),  # Wind/Lake
    7: np.array([1, 1, 1]),  # Heaven - Tet A apex
}

KINGS_CHAMBER = np.array([0.5, 0.5, 0.5])

TET_A = {1, 2, 4, 7}  # Odd parity
TET_B = {0, 3, 5, 6}  # Even parity

TIME_A7 = {1, 2, 4}  # Tet A TIME face
TIME_B0 = {3, 5, 6}  # Tet B TIME face

print('LOCATION COMPARISON:')
print('-'*75)
print(f'V0 (Tet B apex):     {tuple(VERTICES[0])}')
print(f'V3 (Wind):           {tuple(VERTICES[3])}')
print(f'Kings Chamber:       {tuple(KINGS_CHAMBER)}')
print()

print('QUESTION 1: What does cumsum=0 represent?')
print('-'*75)
print()
print('The algorithm from field_closure_complete_validation.py says:')
print('  "1. Start at position 0"')
print('  "2. For each pi digit d: add d to cumulative sum, position = cumsum mod 8"')
print()
print('If cumsum = 0:')
print('  position = 0 mod 8 = 0')
print('  This points to V0 = (0,0,0)')
print()
print('So mathematically, cumsum=0 -> V0')
print()

print('QUESTION 2: Is V0 the Kings Chamber?')
print('-'*75)
print()
dist_v0_to_kc = np.linalg.norm(VERTICES[0] - KINGS_CHAMBER)
dist_v3_to_kc = np.linalg.norm(VERTICES[3] - KINGS_CHAMBER)
print(f'Distance from V0 to Kings Chamber: {dist_v0_to_kc:.4f}')
print(f'Distance from V3 to Kings Chamber: {dist_v3_to_kc:.4f}')
print()
print('V0 is at (0,0,0), Kings Chamber is at (0.5, 0.5, 0.5)')
print('These are DIFFERENT locations!')
print()
print('V0 is the APEX of Tet B - a corner vertex.')
print('Kings Chamber is the CENTER - where tetrahedra intersect.')
print()

print('QUESTION 3: What is the first OPERATION?')
print('-'*75)
print()
print('Algorithm execution:')
print('  cumsum = 0        (initial state)')
print('  digit = 3         (first pi digit)')
print('  cumsum = 0 + 3    (add digit)')
print('  position = 3      (compute position)')
print('  VISIT V3          (first operation)')
print()
print('So the first OPERATION visits V3, not V0.')
print()

print('='*75)
print('THE KEY DISTINCTION')
print('='*75)
print()
print('There are TWO different questions:')
print()
print('Q1: Where does cumsum=0 point to?')
print('A1: V0 = (0,0,0) = Tet B apex')
print()
print('Q2: What is the first vertex VISITED by an operation?')
print('A2: V3 = (0,1,1) = Wind, after adding digit 3')
print()
print('Neither V0 nor V3 is the Kings Chamber!')
print()

print('='*75)
print('BUT WAIT - WHAT IS THE KINGS CHAMBER REALLY?')
print('='*75)
print()
print('The Kings Chamber is NOT a vertex. It is a REGION - the center.')
print('It is where the two tetrahedra COUPLE.')
print()
print('The TIME faces point TOWARD the Kings Chamber:')
print(f'  TIME face A7 = {TIME_A7} (opposite Tet A apex V7)')
print(f'  TIME face B0 = {TIME_B0} (opposite Tet B apex V0)')
print()

# Calculate centroids of TIME faces
centroid_A7 = np.mean([VERTICES[v] for v in TIME_A7], axis=0)
centroid_B0 = np.mean([VERTICES[v] for v in TIME_B0], axis=0)

print(f'Centroid of TIME face A7: {tuple(centroid_A7)}')
print(f'Centroid of TIME face B0: {tuple(centroid_B0)}')
print(f'Kings Chamber (center):   {tuple(KINGS_CHAMBER)}')
print()
print('The Kings Chamber is the MIDPOINT between the two TIME face centroids!')
midpoint = (centroid_A7 + centroid_B0) / 2
print(f'Midpoint: {tuple(midpoint)}')
print()

print('='*75)
print('NEW INSIGHT: THE APEXES AND THE CENTER')
print('='*75)
print()
print('V0 = (0,0,0) = Tet B apex')
print('V7 = (1,1,1) = Tet A apex')
print()
print('The Kings Chamber is the midpoint of the V0-V7 axis!')
midpoint_apexes = (VERTICES[0] + VERTICES[7]) / 2
print(f'Midpoint of V0-V7: {tuple(midpoint_apexes)}')
print(f'Kings Chamber:     {tuple(KINGS_CHAMBER)}')
print()

print('So:')
print('  - V0 is one END of the axis (Tet B apex)')
print('  - V7 is the other END (Tet A apex)')
print('  - Kings Chamber is the MIDDLE')
print()

print('='*75)
print('RECONSIDERING: WHERE DOES THE FIELD START?')
print('='*75)
print()
print('If cumsum=0 points to V0 (Tet B apex):')
print('  - V0 is at one end of the central axis')
print('  - The Kings Chamber is in the middle of that axis')
print('  - V7 is at the other end')
print()
print('Physical interpretation:')
print('  - cumsum=0 -> V0 = the "ground state" at Tet B apex')
print('  - This is NOT the Kings Chamber')
print('  - First digit (3) moves us to V3')
print()

print('='*75)
print('ALTERNATIVE INTERPRETATION: CUMSUM AS DISPLACEMENT')
print('='*75)
print()
print('What if cumsum=0 means "zero displacement from center"?')
print()
print('In this view:')
print('  - The CENTER (Kings Chamber) is the reference')
print('  - cumsum = 0 means no displacement')
print('  - First digit (3) is a displacement FROM the center')
print()
print('But mathematically:')
print('  - position = cumsum mod 8')
print('  - position 0 = V0, not the center')
print('  - So this interpretation doesnt match the math')
print()

print('='*75)
print('FINAL MATHEMATICAL ANSWER')
print('='*75)
print()
print('Based on the algorithm:')
print()
print('1. cumsum starts at 0')
print('2. position = cumsum mod 8 = 0')
print('3. Position 0 corresponds to V0 = (0,0,0)')
print()
print('4. First digit is 3')
print('5. cumsum becomes 3')
print('6. position = 3 mod 8 = 3')
print('7. Position 3 corresponds to V3 = (0,1,1)')
print()
print('THEREFORE:')
print()
print('  - INITIAL POSITION (before any operation): V0 = (0,0,0)')
print('  - FIRST VISITED POSITION (after first digit): V3 = (0,1,1)')
print('  - NEITHER IS THE KINGS CHAMBER!')
print()
print('The Kings Chamber is at (0.5, 0.5, 0.5), which is:')
print('  - Not a vertex')
print('  - The center of the Merkaba')
print('  - The midpoint of the V0-V7 axis')
print()

print('='*75)
print('SO: "DO WE START IN THE KINGS CHAMBER OR V3?"')
print('='*75)
print()
print('ANSWER: Neither interpretation puts us IN the Kings Chamber.')
print()
print('  Option 1 (initial cumsum): We start at V0, not Kings Chamber')
print('  Option 2 (first operation): We visit V3 first, not Kings Chamber')
print()
print('The Kings Chamber is the CENTER. We never "start" there.')
print('We start at a VERTEX (V0 or V3 depending on interpretation).')
print()
print('HOWEVER:')
print('  - V3 is part of TIME face B0')
print('  - TIME face B0 points TOWARD the Kings Chamber')
print('  - So V3 is at the INTERFACE with the Kings Chamber')
print()
print('The traversal V3 -> V4 passes THROUGH the Kings Chamber!')
print(f'  V3 = {tuple(VERTICES[3])}')
print(f'  V4 = {tuple(VERTICES[4])}')
print(f'  Midpoint V3-V4 = {tuple((VERTICES[3] + VERTICES[4]) / 2)}')
print(f'  Kings Chamber = {tuple(KINGS_CHAMBER)}')
print()
print('The midpoint of V3-V4 IS the Kings Chamber!')
print('So we PASS THROUGH the Kings Chamber between steps 0 and 1.')
