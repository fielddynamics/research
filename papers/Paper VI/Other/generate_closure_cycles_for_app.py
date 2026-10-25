#!/usr/bin/env python3
"""
Generate the correct 3 closure cycles WITH the integer '3' included
for use in Module07_PortAperture.js

This must match the field_closure_complete_read_sequence_proof_validation.py
"""

# Pi base 8 WITH integer 3 (the "3" IS the "3" in "3+1")
PI_WITH_3 = [3, 1, 1, 0, 3, 7, 5, 5, 2, 4, 2, 1, 0, 2, 6, 4, 3, 0, 2, 1, 5, 1, 4, 2, 3,
             0, 6, 3, 0, 5, 0, 2, 6, 2, 5, 5, 1, 3, 5, 4, 4, 3, 7, 1, 6, 4, 0, 2, 1, 0,
             7, 5, 3, 1, 2, 1, 4, 1, 6, 5, 7, 3, 5, 0, 1, 6, 0, 2, 3, 2, 4, 0, 4, 4, 4,
             3, 1, 4, 5, 5, 2, 6, 6, 4, 0, 7, 6, 1, 4, 5, 5, 4, 3, 6, 2, 4, 0, 4, 6, 6]

# Tetrahedron assignments by parity
TET_A = {1, 2, 4, 7}  # Odd parity
TET_B = {0, 3, 5, 6}  # Even parity

# Face definitions
FACES = {
    'A1': frozenset({2, 4, 7}),
    'A2': frozenset({1, 4, 7}),
    'A4': frozenset({1, 2, 7}),
    'A7': frozenset({1, 2, 4}),  # TIME face
    'B0': frozenset({3, 5, 6}),  # TIME face
    'B3': frozenset({0, 5, 6}),
    'B5': frozenset({0, 3, 6}),
    'B6': frozenset({0, 3, 5}),
}

TIME_FACES = {'A7', 'B0'}

def get_closure_cycles(pi_digits, num_cycles=3):
    """Generate closure cycle data with face completion events."""
    cycles = []
    
    cumsum = 0
    face_vertices_seen = {f: set() for f in FACES}
    faces_completed_this_cycle = set()
    current_cycle_events = []
    cycle_start_step = 0
    
    for step, digit in enumerate(pi_digits):
        cumsum += digit
        vertex = cumsum % 8
        tet = 'A' if vertex in TET_A else 'B'
        
        # Check face completions
        faces_completed_this_step = []
        for face_name, face_verts in FACES.items():
            if vertex in face_verts:
                face_vertices_seen[face_name].add(vertex)
                
                # Check if face just completed
                if len(face_vertices_seen[face_name]) == 3 and face_name not in faces_completed_this_cycle:
                    faces_completed_this_cycle.add(face_name)
                    role = 'TIME' if face_name in TIME_FACES else 'SPATIAL'
                    tet_id = 'A' if face_name.startswith('A') else 'B'
                    faces_completed_this_step.append({
                        'name': face_name,
                        'tetId': tet_id,
                        'role': role
                    })
        
        # If faces completed this step, record an event
        if faces_completed_this_step:
            # Check if Kings Chamber fires (TIME face completed)
            kings_chamber = any(f['role'] == 'TIME' for f in faces_completed_this_step)
            
            current_cycle_events.append({
                'piStep': step,
                'digit': digit,
                'cumsum': cumsum,
                'vertex': vertex,
                'tet': tet,
                'faces': faces_completed_this_step,
                'kingsChamber': kings_chamber
            })
        
        # Check if closure is complete (all 8 faces done)
        if len(faces_completed_this_cycle) == 8:
            cycles.append({
                'cycleNum': len(cycles) + 1,
                'startStep': cycle_start_step,
                'endStep': step,
                'events': current_cycle_events
            })
            
            if len(cycles) >= num_cycles:
                break
            
            # Reset for next cycle
            faces_completed_this_cycle = set()
            face_vertices_seen = {f: set() for f in FACES}
            current_cycle_events = []
            cycle_start_step = step + 1
    
    return cycles


if __name__ == '__main__':
    cycles = get_closure_cycles(PI_WITH_3, 3)
    
    print('// =================================================================')
    print('// 3 COMPLETE CLOSURE CYCLES (WITH INTEGER "3" INCLUDED)')
    print('// Generated from continuous Pi (base 8) traversal')
    print('// Pi (base 8) = 3.110375... -> sequence [3, 1, 1, 0, 3, 7, ...]')
    print('//')
    print('// The "3" IS the "3" in "3+1" (d=3 spatial dimensions)')
    print('// First positions (3,4) form I Ching complementary pair (sum=7)')
    print('// =================================================================')
    print()
    
    for cycle in cycles:
        print(f'// === CLOSURE {cycle["cycleNum"]} (Steps {cycle["startStep"]}-{cycle["endStep"]}) ===')
        
        # Collect all faces for summary
        tet_a_faces = []
        tet_b_faces = []
        for event in cycle['events']:
            for face in event['faces']:
                if face['tetId'] == 'A':
                    tet_a_faces.append(face['name'] + (' (T)' if face['role'] == 'TIME' else ''))
                else:
                    tet_b_faces.append(face['name'] + (' (T)' if face['role'] == 'TIME' else ''))
        
        print(f'// Tet A [{len(tet_a_faces)}]: {", ".join(tet_a_faces)}')
        print(f'// Tet B [{len(tet_b_faces)}]: {", ".join(tet_b_faces)}')
        
        # Show event order pattern
        pattern = []
        for event in cycle['events']:
            tets = set(f['tetId'] for f in event['faces'])
            if len(tets) == 1:
                pattern.append(list(tets)[0])
            else:
                pattern.append('A+B')
        print(f'// Pattern: {" -> ".join(pattern)}')
        print()
        
        for event in cycle['events']:
            face_str = ', '.join([f['name'] + ('(T)' if f['role'] == 'TIME' else '') for f in event['faces']])
            kc = ' KC!' if event['kingsChamber'] else ''
            print(f'//   Step {event["piStep"]:2d}: V{event["vertex"]} (Tet {event["tet"]}) -> [{face_str}]{kc}')
        print()
    
    print()
    print('// JavaScript data structure for Module07_PortAperture.js:')
    print('this.closureCycles = [')
    
    for i, cycle in enumerate(cycles):
        # Summary comment
        tet_a_faces = []
        tet_b_faces = []
        for event in cycle['events']:
            for face in event['faces']:
                if face['tetId'] == 'A':
                    tet_a_faces.append(face['name'] + (' (T)' if face['role'] == 'TIME' else ''))
                else:
                    tet_b_faces.append(face['name'] + (' (T)' if face['role'] == 'TIME' else ''))
        
        print(f'    // CLOSURE {cycle["cycleNum"]}: Steps {cycle["startStep"]}-{cycle["endStep"]}')
        print(f'    // Tet A [{len(tet_a_faces)}]: {", ".join(tet_a_faces)} | Tet B [{len(tet_b_faces)}]: {", ".join(tet_b_faces)}')
        
        print('    {')
        print('        events: [')
        
        for j, event in enumerate(cycle['events']):
            faces_js = ', '.join([
                "{{ name: '{0}', tetId: '{1}', role: '{2}' }}".format(f['name'], f['tetId'], f['role'])
                for f in event['faces']
            ])
            comma = ',' if j < len(cycle['events']) - 1 else ''
            print(f'            {{ piStep: {event["piStep"]}, vertex: {event["vertex"]}, faces: [{faces_js}], kingsChamber: {str(event["kingsChamber"]).lower()} }}{comma}')
        
        print('        ]')
        comma = ',' if i < len(cycles) - 1 else ''
        print(f'    }}{comma}')
    
    print('];')
