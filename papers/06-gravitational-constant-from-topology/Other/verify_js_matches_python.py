"""
Verify that the JavaScript buildCompletionCyclesFromPi() would produce
the same output as our Python validation.

This script mirrors the exact JS logic to verify correctness.
"""

# Pi base-8 digits - MUST match the JS exactly
PI_BASE8_JS = [
    1,1,0,3,7,5,5,2,4,2,1,0,2,6,4,3,0,2,1,5,
    1,4,2,3,0,6,3,0,5,0,5,6,0,0,6,7,0,1,6,3,
    2,1,1,2,2,0,1,4,6,5,4,5,1,7,4,2,4,3,1,5,
    3,5,2,5,1,0,6,7,5,4,2,5,4,5,3,6,6,4,1,7,
    5,5,0,6,3,5,2,6,5,5,4,4,5,7,2,3,5,6,5,4,
    2,3,1,4,1,3,4,5,4,2,5,2,4,2,4,1,7,5,5,6,
    3,1,7,0,5,3,7,1,5,5,3,6,0,6,0,0,3,5,2,4,
    1,5,4,6,3,5,5
]

# Face definitions - MUST match the JS exactly
FACE_DEFINITIONS = {
    'A1': {'vertices': {2, 4, 7}, 'tetId': 'A', 'role': 'SPATIAL'},
    'A2': {'vertices': {1, 4, 7}, 'tetId': 'A', 'role': 'SPATIAL'},
    'A4': {'vertices': {1, 2, 7}, 'tetId': 'A', 'role': 'SPATIAL'},
    'A7': {'vertices': {1, 2, 4}, 'tetId': 'A', 'role': 'TIME'},
    'B0': {'vertices': {3, 5, 6}, 'tetId': 'B', 'role': 'TIME'},
    'B3': {'vertices': {0, 5, 6}, 'tetId': 'B', 'role': 'SPATIAL'},
    'B5': {'vertices': {0, 3, 6}, 'tetId': 'B', 'role': 'SPATIAL'},
    'B6': {'vertices': {0, 3, 5}, 'tetId': 'B', 'role': 'SPATIAL'},
}


def build_completion_cycles_from_pi(num_cycles):
    """
    Mirror of JS buildCompletionCyclesFromPi()
    """
    events = []
    cycles = []
    
    face_vertices_seen = {}
    cum_sum = 0
    cycle_num = 1
    faces_completed_in_cycle = 0
    current_cycle_faces = []
    current_cycle_events = []
    
    def reset_face_tracking():
        nonlocal face_vertices_seen
        face_vertices_seen = {name: set() for name in FACE_DEFINITIONS}
    
    reset_face_tracking()
    
    step = 0
    while step < len(PI_BASE8_JS) and cycle_num <= num_cycles:
        step += 1
        digit = PI_BASE8_JS[step - 1]
        cum_sum += digit
        vertex = cum_sum % 8
        
        faces_completed_this_step = []
        
        for face_name, face_def in FACE_DEFINITIONS.items():
            if vertex in face_def['vertices']:
                if vertex not in face_vertices_seen[face_name]:
                    face_vertices_seen[face_name].add(vertex)
                    
                    if len(face_vertices_seen[face_name]) == 3:
                        faces_completed_this_step.append({
                            'name': face_name,
                            'tetId': face_def['tetId'],
                            'role': face_def['role']
                        })
        
        if faces_completed_this_step:
            # Sort by name (JS uses localeCompare which is alphabetical)
            faces_completed_this_step.sort(key=lambda f: f['name'])
            
            has_time_face = any(f['role'] == 'TIME' for f in faces_completed_this_step)
            tet_ids = list(set(f['tetId'] for f in faces_completed_this_step))
            
            event = {
                'piStep': step,
                'digit': digit,
                'vertex': vertex,
                'cycle': cycle_num,
                'faces': faces_completed_this_step,
                'tetIds': tet_ids,
                'kingsChamber': has_time_face,
                'faceCount': len(faces_completed_this_step)
            }
            
            events.append(event)
            current_cycle_events.append(event)
            current_cycle_faces.extend(faces_completed_this_step)
            faces_completed_in_cycle += len(faces_completed_this_step)
            
            if faces_completed_in_cycle >= 8:
                tet_a_faces = [f for f in current_cycle_faces if f['tetId'] == 'A']
                tet_b_faces = [f for f in current_cycle_faces if f['tetId'] == 'B']
                
                cycles.append({
                    'cycleNum': cycle_num,
                    'faces': list(current_cycle_faces),
                    'events': list(current_cycle_events),
                    'startStep': current_cycle_events[0]['piStep'],
                    'endStep': step,
                    'tetAFaces': tet_a_faces,
                    'tetBFaces': tet_b_faces
                })
                
                cycle_num += 1
                faces_completed_in_cycle = 0
                current_cycle_faces = []
                current_cycle_events = []
                reset_face_tracking()
    
    return {'events': events, 'cycles': cycles}


def main():
    print("=" * 80)
    print("VERIFYING JS LOGIC PRODUCES CORRECT CLOSURE CYCLES")
    print("=" * 80)
    
    result = build_completion_cycles_from_pi(3)
    events = result['events']
    cycles = result['cycles']
    
    print(f"\nTotal events: {len(events)}")
    print(f"Total cycles: {len(cycles)}")
    
    print("\n" + "-" * 80)
    print("ALL COMPLETION EVENTS (what Step mode shows)")
    print("-" * 80)
    
    for i, event in enumerate(events):
        face_names = [f['name'] for f in event['faces']]
        tet_ids = event['tetIds']
        kc = " [KC]" if event['kingsChamber'] else ""
        print(f"Event {i+1:2d} | Cycle {event['cycle']} | Step {event['piStep']:2d} | V{event['vertex']} | {tet_ids} | {face_names}{kc}")
    
    print("\n" + "-" * 80)
    print("CLOSURE CYCLES (what Full mode shows)")
    print("-" * 80)
    
    for cycle in cycles:
        print(f"\n{'='*60}")
        print(f"CYCLE {cycle['cycleNum']} | Steps {cycle['startStep']}-{cycle['endStep']}")
        print(f"{'='*60}")
        
        print(f"\nTet A faces ({len(cycle['tetAFaces'])}):")
        for f in cycle['tetAFaces']:
            role_tag = " (TIME)" if f['role'] == 'TIME' else ""
            print(f"  - {f['name']}{role_tag}")
        
        print(f"\nTet B faces ({len(cycle['tetBFaces'])}):")
        for f in cycle['tetBFaces']:
            role_tag = " (TIME)" if f['role'] == 'TIME' else ""
            print(f"  - {f['name']}{role_tag}")
        
        print(f"\nEvents in this cycle ({len(cycle['events'])}):")
        for e in cycle['events']:
            face_names = [f['name'] for f in e['faces']]
            print(f"  Step {e['piStep']:2d}: {face_names}")
    
    # Validation checks
    print("\n" + "-" * 80)
    print("VALIDATION CHECKS")
    print("-" * 80)
    
    all_valid = True
    
    for cycle in cycles:
        # Check 8 faces total
        total_faces = len(cycle['faces'])
        if total_faces != 8:
            print(f"ERROR: Cycle {cycle['cycleNum']} has {total_faces} faces, expected 8")
            all_valid = False
        
        # Check 4 Tet A + 4 Tet B
        if len(cycle['tetAFaces']) != 4:
            print(f"ERROR: Cycle {cycle['cycleNum']} has {len(cycle['tetAFaces'])} Tet A faces, expected 4")
            all_valid = False
        
        if len(cycle['tetBFaces']) != 4:
            print(f"ERROR: Cycle {cycle['cycleNum']} has {len(cycle['tetBFaces'])} Tet B faces, expected 4")
            all_valid = False
        
        # Check all 8 unique faces
        face_names = {f['name'] for f in cycle['faces']}
        expected_faces = {'A1', 'A2', 'A4', 'A7', 'B0', 'B3', 'B5', 'B6'}
        if face_names != expected_faces:
            print(f"ERROR: Cycle {cycle['cycleNum']} missing faces: {expected_faces - face_names}")
            all_valid = False
    
    if all_valid:
        print("ALL CHECKS PASSED - Closure cycles are correctly built!")
    else:
        print("SOME CHECKS FAILED")
    
    print("\n" + "-" * 80)
    print("SUMMARY FOR VISUALIZATION")
    print("-" * 80)
    print(f"""
COMPLETION STEP MODE will show:
  - {len(events)} total events across 3 cycles
  - Each event fires 1-3 faces sequentially (100ms between)
  - 600ms pause between events
  - Events loop: 1 → 2 → ... → {len(events)} → 1 → ...

COMPLETION FULL MODE will show:
  - 3 closure cycles
  - Each cycle fires all 8 faces simultaneously
  - 600ms pause between cycles
  - Cycles loop: 1 → 2 → 3 → 1 → ...

Cycle details:
  Cycle 1: Steps {cycles[0]['startStep']}-{cycles[0]['endStep']}, {len(cycles[0]['events'])} events
  Cycle 2: Steps {cycles[1]['startStep']}-{cycles[1]['endStep']}, {len(cycles[1]['events'])} events  
  Cycle 3: Steps {cycles[2]['startStep']}-{cycles[2]['endStep']}, {len(cycles[2]['events'])} events
""")


if __name__ == "__main__":
    main()
