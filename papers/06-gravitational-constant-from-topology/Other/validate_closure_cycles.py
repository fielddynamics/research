"""
Validate closure cycle building from pi base-8
A closure cycle = all 8 faces of the Merkaba have completed once
"""

# Pi base-8 digits (after decimal point)
pi_base8 = [
    1,1,0,3,7,5,5,2,4,2,1,0,2,6,4,3,0,2,1,5,
    1,4,2,3,0,6,3,0,5,0,5,6,0,0,6,7,0,1,6,3,
    2,1,1,2,2,0,1,4,6,5,4,5,1,7,4,2,4,3,1,5,
    3,5,2,5,1,0,6,7,5,4,2,5,4,5,3,6,6,4,1,7,
    5,5,0,6,3,5,2,6,5,5,4,4,5,7,2,3,5,6,5,4,
    2,3,1,4,1,3,4,5,4,2,5,2,4,2,4,1,7,5,5,6,
    3,1,7,0,5,3,7,1,5,5,3,6,0,6,0,0,3,5,2,4,
    1,5,4,6,3,5,5
]

# Face definitions (vertices that make up each face)
FACE_DEFS = {
    'A1': {'vertices': {2,4,7}, 'tet': 'A', 'role': 'SPATIAL'},
    'A2': {'vertices': {1,4,7}, 'tet': 'A', 'role': 'SPATIAL'},
    'A4': {'vertices': {1,2,7}, 'tet': 'A', 'role': 'SPATIAL'},
    'A7': {'vertices': {1,2,4}, 'tet': 'A', 'role': 'TIME'},
    'B0': {'vertices': {3,5,6}, 'tet': 'B', 'role': 'TIME'},
    'B3': {'vertices': {0,5,6}, 'tet': 'B', 'role': 'SPATIAL'},
    'B5': {'vertices': {0,3,6}, 'tet': 'B', 'role': 'SPATIAL'},
    'B6': {'vertices': {0,3,5}, 'tet': 'B', 'role': 'SPATIAL'},
}

def build_closure_cycles(num_cycles=3):
    """Build closure cycles by simulating pi traversal"""
    
    cycles = []
    all_events = []
    
    # Track which vertices each face has seen
    face_vertices_seen = {name: set() for name in FACE_DEFS}
    
    cum_sum = 0
    cycle_num = 1
    faces_completed_in_cycle = 0
    current_cycle_faces = []
    current_cycle_events = []
    
    print("=" * 70)
    print(f"BUILDING {num_cycles} CLOSURE CYCLES FROM PI")
    print("=" * 70)
    
    for step in range(1, len(pi_base8) + 1):
        if cycle_num > num_cycles:
            break
            
        digit = pi_base8[step - 1]
        cum_sum += digit
        vertex = cum_sum % 8
        
        faces_completed_this_step = []
        
        # Check each face
        for face_name, face_def in FACE_DEFS.items():
            if vertex in face_def['vertices']:
                if vertex not in face_vertices_seen[face_name]:
                    face_vertices_seen[face_name].add(vertex)
                    
                    # Face completes when it has seen all 3 vertices
                    if len(face_vertices_seen[face_name]) == 3:
                        faces_completed_this_step.append({
                            'name': face_name,
                            'tet': face_def['tet'],
                            'role': face_def['role']
                        })
        
        if faces_completed_this_step:
            # Sort by face name for consistency
            faces_completed_this_step.sort(key=lambda f: f['name'])
            
            event = {
                'step': step,
                'digit': digit,
                'vertex': vertex,
                'cycle': cycle_num,
                'faces': faces_completed_this_step
            }
            
            all_events.append(event)
            current_cycle_events.append(event)
            current_cycle_faces.extend(faces_completed_this_step)
            faces_completed_in_cycle += len(faces_completed_this_step)
            
            tet_a = [f['name'] for f in faces_completed_this_step if f['tet'] == 'A']
            tet_b = [f['name'] for f in faces_completed_this_step if f['tet'] == 'B']
            
            print(f"\nStep {step:3d} | V{vertex} | Cycle {cycle_num} | Faces completed: {faces_completed_in_cycle}/8")
            if tet_a:
                print(f"         Tet A: {', '.join(tet_a)}")
            if tet_b:
                print(f"         Tet B: {', '.join(tet_b)}")
            
            # Check if cycle complete
            if faces_completed_in_cycle >= 8:
                print(f"\n>>> CYCLE {cycle_num} COMPLETE <<<")
                
                # Verify we have exactly 4 Tet A and 4 Tet B
                cycle_tet_a = [f for f in current_cycle_faces if f['tet'] == 'A']
                cycle_tet_b = [f for f in current_cycle_faces if f['tet'] == 'B']
                
                print(f"    Tet A faces ({len(cycle_tet_a)}): {[f['name'] for f in cycle_tet_a]}")
                print(f"    Tet B faces ({len(cycle_tet_b)}): {[f['name'] for f in cycle_tet_b]}")
                print(f"    Steps: {current_cycle_events[0]['step']} - {step}")
                
                cycles.append({
                    'cycle_num': cycle_num,
                    'faces': current_cycle_faces.copy(),
                    'events': current_cycle_events.copy(),
                    'start_step': current_cycle_events[0]['step'],
                    'end_step': step
                })
                
                # Reset for next cycle
                cycle_num += 1
                faces_completed_in_cycle = 0
                current_cycle_faces = []
                current_cycle_events = []
                face_vertices_seen = {name: set() for name in FACE_DEFS}
    
    return cycles, all_events


def main():
    cycles, events = build_closure_cycles(3)
    
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    print(f"\nTotal completion events: {len(events)}")
    print(f"Total closure cycles: {len(cycles)}")
    
    for cycle in cycles:
        print(f"\n--- Cycle {cycle['cycle_num']} (steps {cycle['start_step']}-{cycle['end_step']}) ---")
        tet_a = [f['name'] for f in cycle['faces'] if f['tet'] == 'A']
        tet_b = [f['name'] for f in cycle['faces'] if f['tet'] == 'B']
        print(f"  Tet A: {tet_a}")
        print(f"  Tet B: {tet_b}")
        print(f"  Events in cycle: {len(cycle['events'])}")
        for e in cycle['events']:
            face_names = [f['name'] for f in e['faces']]
            print(f"    Step {e['step']}: {face_names}")
    
    # Validate each cycle has all 8 unique faces
    print("\n" + "=" * 70)
    print("VALIDATION")
    print("=" * 70)
    
    all_face_names = {'A1', 'A2', 'A4', 'A7', 'B0', 'B3', 'B5', 'B6'}
    
    for cycle in cycles:
        face_names_in_cycle = {f['name'] for f in cycle['faces']}
        missing = all_face_names - face_names_in_cycle
        extra = face_names_in_cycle - all_face_names
        
        if missing or extra or len(cycle['faces']) != 8:
            print(f"CYCLE {cycle['cycle_num']}: INVALID")
            if missing:
                print(f"  Missing faces: {missing}")
            if extra:
                print(f"  Extra faces: {extra}")
            if len(cycle['faces']) != 8:
                print(f"  Face count: {len(cycle['faces'])} (expected 8)")
        else:
            print(f"CYCLE {cycle['cycle_num']}: VALID - All 8 faces present")


if __name__ == "__main__":
    main()
