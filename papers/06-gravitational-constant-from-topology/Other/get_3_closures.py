"""
Get the first 3 closure cycles from pi.
Each cycle: restart pi from step 1, track until all 8 faces complete.
Verify unique coverage (no duplicates).
"""

PI_BASE8 = [
    1,1,0,3,7,5,5,2,4,2,1,0,2,6,4,3,0,2,1,5,
    1,4,2,3,0,6,3,0,5,0,5,6,0,0,6,7,0,1,6,3,
    2,1,1,2,2,0,1,4,6,5,4,5,1,7,4,2,4,3,1,5
]

FACES = {
    'A1': {'vertices': {2, 4, 7}, 'tetId': 'A', 'role': 'SPATIAL'},
    'A2': {'vertices': {1, 4, 7}, 'tetId': 'A', 'role': 'SPATIAL'},
    'A4': {'vertices': {1, 2, 7}, 'tetId': 'A', 'role': 'SPATIAL'},
    'A7': {'vertices': {1, 2, 4}, 'tetId': 'A', 'role': 'TIME'},
    'B0': {'vertices': {3, 5, 6}, 'tetId': 'B', 'role': 'TIME'},
    'B3': {'vertices': {0, 5, 6}, 'tetId': 'B', 'role': 'SPATIAL'},
    'B5': {'vertices': {0, 3, 6}, 'tetId': 'B', 'role': 'SPATIAL'},
    'B6': {'vertices': {0, 3, 5}, 'tetId': 'B', 'role': 'SPATIAL'},
}

def get_one_closure_cycle():
    """
    Start pi from step 1, track face completions until all 8 complete.
    Returns list of events, each event has: piStep, vertex, faces
    """
    face_seen = {name: set() for name in FACES}
    face_completed = set()
    events = []
    
    cum_sum = 0
    
    for step in range(1, len(PI_BASE8) + 1):
        digit = PI_BASE8[step - 1]
        cum_sum += digit
        vertex = cum_sum % 8
        
        faces_this_step = []
        
        for face_name, face_def in FACES.items():
            if face_name not in face_completed:
                if vertex in face_def['vertices']:
                    face_seen[face_name].add(vertex)
                    
                    if len(face_seen[face_name]) == 3:
                        face_completed.add(face_name)
                        faces_this_step.append({
                            'name': face_name,
                            'tetId': face_def['tetId'],
                            'role': face_def['role']
                        })
        
        if faces_this_step:
            # Sort for consistency
            faces_this_step.sort(key=lambda f: f['name'])
            
            has_time = any(f['role'] == 'TIME' for f in faces_this_step)
            
            events.append({
                'piStep': step,
                'vertex': vertex,
                'faces': faces_this_step,
                'kingsChamber': has_time
            })
        
        if len(face_completed) == 8:
            break
    
    return events


def main():
    print("=" * 70)
    print("GETTING 3 CLOSURE CYCLES (pi restarts each time)")
    print("=" * 70)
    
    # Since pi restarts each cycle, all 3 cycles are IDENTICAL
    cycle = get_one_closure_cycle()
    
    print("\nTHE CANONICAL CLOSURE CYCLE (same for all 3):")
    print("-" * 50)
    
    all_faces = []
    tet_a_faces = []
    tet_b_faces = []
    
    for i, event in enumerate(cycle):
        faces_str = ", ".join([f['name'] + (' (TIME)' if f['role'] == 'TIME' else '') for f in event['faces']])
        kc = " [King's Chamber]" if event['kingsChamber'] else ""
        print(f"Event {i+1}: Step {event['piStep']:2d}, V{event['vertex']} -> {faces_str}{kc}")
        
        for f in event['faces']:
            all_faces.append(f['name'])
            if f['tetId'] == 'A':
                tet_a_faces.append(f['name'])
            else:
                tet_b_faces.append(f['name'])
    
    print("\n" + "-" * 50)
    print("VALIDATION:")
    print(f"  Total faces: {len(all_faces)}")
    print(f"  Unique faces: {len(set(all_faces))}")
    print(f"  Tet A faces: {tet_a_faces} ({len(tet_a_faces)})")
    print(f"  Tet B faces: {tet_b_faces} ({len(tet_b_faces)})")
    
    # Check for duplicates
    if len(all_faces) != len(set(all_faces)):
        print("  ERROR: Duplicate faces!")
    else:
        print("  OK: All faces unique")
    
    # Check all 8 present
    expected = {'A1', 'A2', 'A4', 'A7', 'B0', 'B3', 'B5', 'B6'}
    if set(all_faces) == expected:
        print("  OK: All 8 faces covered")
    else:
        print(f"  ERROR: Missing {expected - set(all_faces)}")
    
    # Check Tet A and Tet B both present
    if len(tet_a_faces) == 4 and len(tet_b_faces) == 4:
        print("  OK: 4 Tet A + 4 Tet B")
    else:
        print("  ERROR: Imbalanced tetrahedra")
    
    print("\n" + "=" * 70)
    print("JAVASCRIPT DATA STRUCTURE:")
    print("=" * 70)
    print("""
// THE CANONICAL CLOSURE CYCLE (same for all 3 cycles)
this.closureCycle = {
    events: [""")
    
    for i, event in enumerate(cycle):
        faces_js = ",\n                    ".join([
            f"{{ name: '{f['name']}', tetId: '{f['tetId']}', role: '{f['role']}' }}"
            for f in event['faces']
        ])
        comma = "," if i < len(cycle) - 1 else ""
        print(f"""        {{
            piStep: {event['piStep']},
            vertex: {event['vertex']},
            faces: [
                    {faces_js}
            ],
            kingsChamber: {'true' if event['kingsChamber'] else 'false'}
        }}{comma}""")
    
    print("""    ],
    allFaces: [
        { name: 'A1', tetId: 'A', role: 'SPATIAL' },
        { name: 'A2', tetId: 'A', role: 'SPATIAL' },
        { name: 'A4', tetId: 'A', role: 'SPATIAL' },
        { name: 'A7', tetId: 'A', role: 'TIME' },
        { name: 'B0', tetId: 'B', role: 'TIME' },
        { name: 'B3', tetId: 'B', role: 'SPATIAL' },
        { name: 'B5', tetId: 'B', role: 'SPATIAL' },
        { name: 'B6', tetId: 'B', role: 'SPATIAL' }
    ]
};""")


if __name__ == "__main__":
    main()
