"""
Investigate: Should the integer "3" of pi be included in the traversal?

Pi (base 8) = 3.110375524210264302151423...

Two interpretations:
1. FRACTIONAL ONLY: Start with [1,1,0,3,7,5,5,2,4,2,...] - skip the "3"
2. INCLUDE INTEGER: Start with [3,1,1,0,3,7,5,5,2,4,2,...] - include the "3"

The user suggests: The "3" might encode the "3" in 3+1 (3 spatial + 1 time)
"""

FACES = {
    'A1': {2,4,7}, 'A2': {1,4,7}, 'A4': {1,2,7}, 'A7': {1,2,4},  # Tet A (TIME=A7)
    'B0': {3,5,6}, 'B3': {0,5,6}, 'B5': {0,3,6}, 'B6': {0,3,5}   # Tet B (TIME=B0)
}

def trace_traversal(pi_digits, label, max_steps=20):
    """Trace vertex traversal and face completions"""
    print(f"\n{'='*70}")
    print(f"{label}")
    print(f"Pi digits: {pi_digits[:20]}...")
    print(f"{'='*70}")
    
    face_seen = {f: set() for f in FACES}
    faces_done = set()
    cum = 0
    
    print(f"\n{'Step':<6}{'Digit':<7}{'CumSum':<8}{'Pos':<5}{'Vertex':<8}{'Tet':<5}{'Faces Completed':<30}{'Notes'}")
    print("-" * 100)
    
    for step in range(1, min(max_steps + 1, len(pi_digits) + 1)):
        digit = pi_digits[step - 1]
        cum += digit
        pos = cum % 8
        
        # Determine which tet
        tet = 'A' if pos in [1,2,4,7] else 'B'
        
        # Check orbit
        orbit_note = ""
        if cum > 0 and cum % 8 == 0:
            orbit_note = f"ORBIT {cum // 8}"
        
        # Check face completions
        completed = []
        for fn, verts in FACES.items():
            if fn not in faces_done and pos in verts:
                face_seen[fn].add(pos)
                if len(face_seen[fn]) == 3:
                    faces_done.add(fn)
                    role = "TIME" if fn in ['A7', 'B0'] else "spatial"
                    completed.append(f"{fn}({role})")
        
        completed_str = ", ".join(completed) if completed else ""
        
        # Special notes
        notes = []
        if orbit_note:
            notes.append(orbit_note)
        if pos == 5:
            notes.append("DRAIN")
        if pos == 0:
            notes.append("Tet B apex")
        if pos == 7:
            notes.append("Tet A apex")
        if any("TIME" in c for c in completed):
            notes.append("TIME FACE!")
        
        notes_str = ", ".join(notes)
        
        print(f"{step:<6}{digit:<7}{cum:<8}{pos:<5}V{pos:<7}{tet:<5}{completed_str:<30}{notes_str}")
        
        if len(faces_done) == 8:
            print(f"\n*** FULL CLOSURE at step {step} ***")
            break
    
    # Summary
    print(f"\nFace completion order:")
    return faces_done

# Interpretation 1: Fractional only (current approach)
PI_FRACTIONAL = [1,1,0,3,7,5,5,2,4,2,1,0,2,6,4,3,0,2,1,5]

# Interpretation 2: Include integer "3"
PI_WITH_INTEGER = [3,1,1,0,3,7,5,5,2,4,2,1,0,2,6,4,3,0,2,1,5]

print("\n" + "=" * 70)
print("INVESTIGATING: Should the integer '3' of pi be included?")
print("=" * 70)
print("\nPi (base 8) = 3.110375524210264302151423...")
print("\nThe '3' before the decimal might encode:")
print("  - The '3' in 3+1 spacetime (3 spatial + 1 time)")
print("  - The initial 3 spatial faces that must complete")
print("  - A starting position at V3 (Tet B)")

trace_traversal(PI_FRACTIONAL, "INTERPRETATION 1: FRACTIONAL DIGITS ONLY [1,1,0,3,7,...]")
trace_traversal(PI_WITH_INTEGER, "INTERPRETATION 2: INCLUDING INTEGER [3,1,1,0,3,7,...]")

# Additional analysis
print("\n" + "=" * 70)
print("ANALYSIS: What does starting with '3' mean physically?")
print("=" * 70)
print("""
If we START with digit 3:
  - First move: position = 3 mod 8 = 3 -> V3 (Tet B!)
  - This means traversal BEGINS in Tet B, not Tet A
  - V3 = binary 011 = Xun (Wind) in I Ching

If we SKIP the integer 3:
  - First move: position = 1 mod 8 = 1 -> V1 (Tet A)
  - Traversal begins in Tet A (the physical metric)
  - V1 = binary 001 = Zhen (Thunder) in I Ching

The 3+1 interpretation:
  - The '3' encodes that there are 3 SPATIAL faces per tetrahedron
  - It's metadata about the structure, not a traversal instruction
  - The fractional digits then drive the actual traversal

Key question: In the context of bimetric gravity,
  - Does the field closure START in Tet A (physical) or Tet B (reference)?
  - Current understanding: Tet A (physical) reads first, Tet B stabilizes
""")

# What about 31415 -> 3489?
print("\n" + "=" * 70)
print("EXPLORING: 31415 -> 3489 connection")
print("=" * 70)
print("""
The user mentioned: '31415 is 3489 which was key to understanding the Merkaba'

Let's explore possible transformations:
""")

# Various interpretations
print("31415 in decimal:")
print(f"  - As octal interpreted as decimal: oct(31415) = {oct(31415)}")
print(f"  - 3+1+4+1+5 = {3+1+4+1+5}")
print(f"  - 3*1*4*1*5 = {3*1*4*1*5}")

# 3489 analysis
print("\n3489 analysis:")
print(f"  - 3489 in binary: {bin(3489)}")
print(f"  - 3489 mod 8 = {3489 % 8}")
print(f"  - 3+4+8+9 = {3+4+8+9}")
print(f"  - Digits 3,4,8,9 -> positions in Merkaba?")

# Check if 3489 relates to face indices
print("\nIf 3,4,8,9 are significant positions:")
print("  - V3 = Tet B (011)")
print("  - V4 = Tet A (100)")  
print("  - V8 doesn't exist (only 0-7)")
print("  - Could 8,9 be face indices or step numbers?")

# First few digits of pi base 8 cumsum
print("\nCumulative sum of pi base 8 (with integer):")
pi_full = [3,1,1,0,3,7,5,5,2,4,2,1,0,2,6,4,3,0,2,1]
cumsum = 0
for i, d in enumerate(pi_full[:15]):
    cumsum += d
    print(f"  Step {i+1}: digit={d}, cumsum={cumsum}, pos={cumsum%8} (V{cumsum%8})")
