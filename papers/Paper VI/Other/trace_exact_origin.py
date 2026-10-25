#!/usr/bin/env python3
"""
Trace the EXACT origin point and path of the 3+1 coupling.
Where does the pointer START before any pi digits are processed?
"""

import numpy as np

print('='*75)
print('EXACT ORIGIN AND PATH TRACING')
print('='*75)
print()

# Vertex coordinates
VERTICES = {
    0: (0, 0, 0),  # Earth  000 - Tet B APEX
    1: (0, 0, 1),  # Thunder 001
    2: (0, 1, 0),  # Water  010
    3: (0, 1, 1),  # Mountain 011
    4: (1, 0, 0),  # Lake   100
    5: (1, 0, 1),  # Fire   101
    6: (1, 1, 0),  # Wind   110
    7: (1, 1, 1),  # Heaven 111 - Tet A APEX
}

TRIGRAMS = {
    0: 'Earth',
    1: 'Thunder', 
    2: 'Water',
    3: 'Mountain',
    4: 'Lake',
    5: 'Fire',
    6: 'Wind',
    7: 'Heaven',
}

TET_A = {1, 2, 4, 7}
TET_B = {0, 3, 5, 6}

TIME_A7 = {1, 2, 4}  # Tet A's TIME face (opposite apex 7)
TIME_B0 = {3, 5, 6}  # Tet B's TIME face (opposite apex 0)

# All faces
FACES = {
    'A1': {2, 4, 7}, 'A2': {1, 4, 7}, 'A4': {1, 2, 7}, 'A7': {1, 2, 4},
    'B0': {3, 5, 6}, 'B3': {0, 5, 6}, 'B5': {0, 3, 6}, 'B6': {0, 3, 5},
}

def get_faces_containing(vertex):
    """Get all faces that contain this vertex."""
    result = []
    for face_name, verts in FACES.items():
        if vertex in verts:
            is_time = face_name in ['A7', 'B0']
            result.append((face_name, is_time))
    return result

print('SECTION 1: UNDERSTANDING THE INITIAL STATE')
print('-'*75)
print()
print('Question: Before processing any pi digits, where is the "pointer"?')
print()
print('The cumulative sum starts at 0.')
print('Therefore: initial vertex = 0 mod 8 = 0')
print()
print('Vertex 0 properties:')
print(f'  Position: {VERTICES[0]}')
print(f'  Binary: 000')
print(f'  I Ching: {TRIGRAMS[0]} (all Yin)')
print(f'  Tetrahedron: Tet B (even parity)')
print(f'  Role: APEX of Tet B')
print()

faces_at_0 = get_faces_containing(0)
print('Faces containing vertex 0:')
for face, is_time in faces_at_0:
    time_str = ' (TIME face)' if is_time else ''
    print(f'  {face}{time_str}')
print()
print('NOTE: Vertex 0 is NOT in any TIME face!')
print('      It is the APEX of Tet B, opposite the TIME face B0.')
print()

print('='*75)
print('SECTION 2: THE EXACT PATH')
print('='*75)
print()

print('Pi (base 8) = 3.110375...')
print('Digits: [3, 1, 1, 0, 3, 7, 5, 5, 2, 4, ...]')
print()

PI = [3, 1, 1, 0, 3, 7, 5, 5, 2, 4]

print('INITIAL STATE (before any digits):')
print('-'*40)
cumsum = 0
vertex = 0
tet = 'B' if vertex in TET_B else 'A'
in_time = vertex in TIME_A7 or vertex in TIME_B0
print(f'  cumsum = {cumsum}')
print(f'  vertex = {vertex}')
print(f'  position = {VERTICES[vertex]}')
print(f'  I Ching = {TRIGRAMS[vertex]} ({bin(vertex)[2:].zfill(3)})')
print(f'  Tet = {tet} ({"APEX" if vertex in [0, 7] else "face vertex"})')
print(f'  In TIME face = {in_time}')
print()

print('STEP-BY-STEP TRAVERSAL:')
print('-'*40)

for step, digit in enumerate(PI[:5]):
    prev_vertex = cumsum % 8
    cumsum += digit
    vertex = cumsum % 8
    tet = 'B' if vertex in TET_B else 'A'
    in_time_A7 = vertex in TIME_A7
    in_time_B0 = vertex in TIME_B0
    
    print(f'Step {step}: digit = {digit}')
    print(f'  cumsum: {cumsum - digit} + {digit} = {cumsum}')
    print(f'  vertex: {prev_vertex} -> {vertex}')
    print(f'  position: {VERTICES[prev_vertex]} -> {VERTICES[vertex]}')
    print(f'  I Ching: {TRIGRAMS[prev_vertex]} -> {TRIGRAMS[vertex]}')
    print(f'  Tet: {"B" if prev_vertex in TET_B else "A"} -> {tet}')
    
    if in_time_A7:
        print(f'  ** IN TIME FACE A7 **')
    if in_time_B0:
        print(f'  ** IN TIME FACE B0 **')
    
    # Check if apex
    if vertex == 0:
        print(f'  ** AT TET B APEX **')
    if vertex == 7:
        print(f'  ** AT TET A APEX **')
    print()

print('='*75)
print('SECTION 3: THE PRECISE ORIGIN')
print('='*75)
print()

print('THE POINTER ORIGIN IS:')
print()
print('  Vertex 0 = (0,0,0)')
print('  Tet B APEX')
print('  I Ching: EARTH (000) - Pure Yin, absolute ground state')
print()
print('This is NOT:')
print('  - A face (it is an apex/corner)')
print('  - A TIME face vertex (TIME face B0 = {3,5,6} excludes 0)')
print('  - The Heart Chamber (center is at 0.5, 0.5, 0.5)')
print()
print('The origin is the GROUNDING POINT of Tet B.')
print()

print('='*75)
print('SECTION 4: THE COMPLETE PATH')
print('='*75)
print()

print('ORIGIN -> FIRST POSITION -> SECOND POSITION')
print()
print('  [ORIGIN]        [STEP 0: +3]       [STEP 1: +1]')
print('  Vertex 0   -->   Vertex 3    -->   Vertex 4')
print('  (0,0,0)          (0,1,1)           (1,0,0)')
print('  Tet B APEX       Tet B             Tet A')
print('  Earth (000)      Mountain (011)    Lake (100)')
print('  NOT in TIME      IN TIME B0        IN TIME A7')
print()

print('GEOMETRIC INTERPRETATION:')
print()
print('  1. ORIGIN at Tet B apex (vertex 0)')
print('     - The "ground state" / "zero point"')
print('     - Pure Yin (Earth) - undifferentiated')
print('     - At the tip of Tet B, furthest from Tet A')
print()
print('  2. FIRST MOVE (+3) to vertex 3')
print('     - Moves to TIME face B0')
print('     - Now at the Kings Chamber INTERFACE')
print('     - Still in Tet B but at the "door"')
print()
print('  3. SECOND MOVE (+1) to vertex 4')
print('     - Crosses THROUGH Heart Chamber to Tet A')
print('     - Arrives at TIME face A7')
print('     - Now in physical space')
print()

print('='*75)
print('SECTION 5: SPATIAL VISUALIZATION')
print('='*75)
print()

# Calculate distances
v0 = np.array(VERTICES[0])
v3 = np.array(VERTICES[3])
v4 = np.array(VERTICES[4])
center = np.array([0.5, 0.5, 0.5])

dist_0_to_3 = np.linalg.norm(v3 - v0)
dist_3_to_4 = np.linalg.norm(v4 - v3)
dist_0_to_center = np.linalg.norm(center - v0)
dist_3_to_center = np.linalg.norm(center - v3)
dist_4_to_center = np.linalg.norm(center - v4)

print('Distances from Heart Chamber (center):')
print(f'  Vertex 0 (origin):  {dist_0_to_center:.4f} (furthest in Tet B)')
print(f'  Vertex 3 (step 0):  {dist_3_to_center:.4f} (TIME face B0)')
print(f'  Vertex 4 (step 1):  {dist_4_to_center:.4f} (TIME face A7)')
print()
print(f'Path segment distances:')
print(f'  V0 -> V3: {dist_0_to_3:.4f}')
print(f'  V3 -> V4: {dist_3_to_4:.4f}')
print()

# Check if V0 and V3 are adjacent
hamming_0_3 = sum(a != b for a, b in zip(VERTICES[0], VERTICES[3]))
hamming_3_4 = sum(a != b for a, b in zip(VERTICES[3], VERTICES[4]))

print('Adjacency (Hamming distance):')
print(f'  V0 -> V3: {hamming_0_3} bits differ ({"adjacent" if hamming_0_3 == 1 else "NOT adjacent"})')
print(f'  V3 -> V4: {hamming_3_4} bits differ ({"adjacent" if hamming_3_4 == 1 else "NOT adjacent"})')
print()

print('='*75)
print('SECTION 6: THE PATH INTERPRETATION')
print('='*75)
print()

print('V0 (000) -> V3 (011):')
print('  Bits changed: positions 1 and 2 flip (00 -> 11)')
print('  This is movement along TWO axes simultaneously')
print('  Hamming distance = 2 (diagonal move on a face)')
print()

print('V3 (011) -> V4 (100):')
print('  Bits changed: ALL THREE flip (011 -> 100)')
print('  This is movement through the BODY DIAGONAL')
print('  Hamming distance = 3 (through center)')
print()

print('INTERPRETATION:')
print()
print('  The "3" in pi does TWO things simultaneously:')
print('  1. Sets cumsum to 3 (landing on vertex 3)')
print('  2. Represents a 2-step move from origin (V0 to V3)')
print()
print('  This 2-step move within Tet B brings us to the TIME face.')
print('  We move from the APEX (origin) to the PORTAL (TIME face).')
print()

print('='*75)
print('FINAL ANSWER: EXACT ORIGIN')
print('='*75)
print()

print('Q: Where does the pointer START?')
print()
print('A: VERTEX 0 (Tet B Apex)')
print()
print('   Location: (0, 0, 0)')
print('   I Ching:  Earth - Pure Yin')
print('   Role:     Ground state / Origin point')
print('   In Tet:   B (the subspace/reference tetrahedron)')
print('   Face:     NOT on any face - at the APEX')
print('   TIME:     NOT in any TIME face')
print()
print('   This is the absolute origin - the "zero" before differentiation.')
print()

print('Q: What is the first MOVEMENT?')
print()
print('A: +3 (the integer part of Pi)')
print()
print('   From:  V0 (0,0,0) - Tet B apex')
print('   To:    V3 (0,1,1) - Tet B TIME face')
print('   Effect: Moves from apex to the TIME face (Kings Chamber door)')
print()

print('Q: What is the second MOVEMENT?')
print()
print('A: +1 (the first fractional digit)')
print()
print('   From:  V3 (0,1,1) - Tet B TIME face')
print('   To:    V4 (1,0,0) - Tet A TIME face')
print('   Effect: Crosses through Heart Chamber to Tet A')
print()

print('='*75)
print('THE COMPLETE PICTURE')
print('='*75)
print()
print('''
    Tet A apex (V7)
    Heaven (111)
         *
        /|\\
       / | \\
      /  |  \\      TIME face A7 = {V1, V2, V4}
     /   |   \\            V4 <---- STEP 1 arrives here
    *----+----*               \\
    V1   |   V2                \\
         |                      \\
         |   HEART CHAMBER       \\
         |   (0.5, 0.5, 0.5)      \\
         |         *              \\
         |        /               \\
    *----+----*  /                 \\
    V6   |   V5                    |
     \\   |   /                     |
      \\  |  /       TIME face B0 = {V3, V5, V6}
       \\ | /              V3 <---- STEP 0 arrives here
        \\|/                ^
         *                  |
    Tet B apex (V0)         |
    Earth (000)        ORIGIN (cumsum=0)
    
    PATH:
    V0 (origin) --[+3]--> V3 (TIME face B0) --[+1]--> V4 (TIME face A7)
       apex              at portal              crossed to Tet A
''')
