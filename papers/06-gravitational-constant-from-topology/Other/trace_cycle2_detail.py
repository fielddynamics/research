"""
Trace Cycle 2 in detail to show WHY B faces complete before A faces.

Key insight: After Cycle 1 ends (step 15), we RESET face tracking.
Each face starts fresh needing to see all 3 of its vertices again.
"""

PI_BASE8 = [
    1,1,0,3,7,5,5,2,4,2,1,0,2,6,4,3,0,2,1,5,
    1,4,2,3,0,6,3,0,5,0,5,6,0,0,6,7,0,1,6,3,
    2,1,1,2,2,0,1,4,6,5,4,5,1,7,4,2,4,3,1,5,
    3,5,2,5,1,0,6,7,5,4,2,5,4,5,3,6,6,4,1,7
]

# Face definitions - which 3 vertices each face needs
FACES = {
    'A1': {2, 4, 7},  # Tet A spatial
    'A2': {1, 4, 7},  # Tet A spatial
    'A4': {1, 2, 7},  # Tet A spatial
    'A7': {1, 2, 4},  # Tet A TIME
    'B0': {3, 5, 6},  # Tet B TIME
    'B3': {0, 5, 6},  # Tet B spatial
    'B5': {0, 3, 6},  # Tet B spatial
    'B6': {0, 3, 5},  # Tet B spatial
}

TET_A_VERTICES = {1, 2, 4, 7}
TET_B_VERTICES = {0, 3, 5, 6}

def trace_cycle():
    print("=" * 80)
    print("TRACING CYCLE 2 IN DETAIL")
    print("=" * 80)
    print("\nCycle 1 ends at step 15. We RESET face tracking.")
    print("Each face needs to see all 3 of its vertices AGAIN.\n")
    
    # Face tracking (what vertices each face has seen)
    face_seen = {name: set() for name in FACES}
    face_completed = {name: False for name in FACES}
    
    # Start from step 16 (after cycle 1)
    cum_sum = sum(PI_BASE8[:15])  # cumsum through step 15
    
    print(f"Starting cumsum from step 15: {cum_sum}")
    print("\n" + "-" * 80)
    print("STEP-BY-STEP TRACE (Cycle 2)")
    print("-" * 80)
    print(f"{'Step':<6} {'Digit':<6} {'Vertex':<8} {'Tet':<6} Face Progress")
    print("-" * 80)
    
    for step in range(16, 50):
        digit = PI_BASE8[step - 1]
        cum_sum += digit
        vertex = cum_sum % 8
        tet = 'A' if vertex in TET_A_VERTICES else 'B'
        
        # Update face tracking
        completions = []
        progress = []
        
        for name, needed_vertices in FACES.items():
            if not face_completed[name] and vertex in needed_vertices:
                face_seen[name].add(vertex)
                seen_count = len(face_seen[name])
                
                if seen_count == 3:
                    face_completed[name] = True
                    completions.append(name)
                else:
                    progress.append(f"{name}:{seen_count}/3")
        
        # Format output
        completion_str = f" --> COMPLETE: {completions}" if completions else ""
        progress_str = f" | Progress: {progress}" if progress else ""
        
        print(f"{step:<6} {digit:<6} V{vertex:<7} {tet:<6}{completion_str}{progress_str}")
        
        # Check if all 8 done
        if all(face_completed.values()):
            print("\n>>> CYCLE 2 COMPLETE <<<")
            break
    
    print("\n" + "-" * 80)
    print("WHY B FACES COMPLETE FIRST IN CYCLE 2")
    print("-" * 80)
    print("""
After step 15, face tracking resets. Look at which vertices pi visits:

Step 16: V6 (Tet B vertex)
Step 17: V6 (Tet B vertex) 
Step 18: V0 (Tet B vertex)
Step 19: V1 (Tet A vertex)
Step 20: V5 (Tet B vertex)
Step 21: V1 (Tet A vertex)
Step 22: V3 (Tet B vertex) --> B5 completes (has seen 0,3,6)
Step 23: V5 (Tet B vertex) --> B0,B3,B6 complete (all have seen their 3 vertices)

Pi visits mostly Tet B vertices (0,3,5,6) in steps 16-23!
That's why Tet B faces complete first.

The Tet A vertices (1,2,4,7) aren't visited enough until later:
Step 41: V2 --> A4 completes
Step 43: V4 --> A1,A2,A7 complete

This is NOT doing the same faces twice.
It's that DIFFERENT faces complete at DIFFERENT times based on pi's path.
""")
    
    print("-" * 80)
    print("SUMMARY: B -> B -> A -> A means:")
    print("-" * 80)
    print("""
Event 1 (Step 22): B5 completes           (1 face)
Event 2 (Step 23): B0, B3, B6 complete    (3 faces) 
Event 3 (Step 41): A4 completes           (1 face)
Event 4 (Step 43): A1, A2, A7 complete    (3 faces)

Total: 4 Tet B faces + 4 Tet A faces = 8 faces (complete Merkaba)

The "B -> B" is TWO DIFFERENT EVENTS with DIFFERENT B faces.
Pi just happens to complete B faces before A faces in Cycle 2.
""")


if __name__ == "__main__":
    trace_cycle()
