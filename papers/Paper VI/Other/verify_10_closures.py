"""
Verify closure cycles from pi - show 10 complete closures.
Each closure = all 8 faces completed (4 Tet A + 4 Tet B).
"""

# First 200 FRACTIONAL digits of pi (octal, base-8)
# Pi (base 8) = 3.110375524210264302151423...
# We use ONLY the fractional digits after the decimal point
PI_200 = [
    1,1,0,3,7,5,5,2,4,2,1,0,2,6,4,3,0,2,1,5,
    1,4,2,3,0,6,3,0,5,0,5,6,0,0,6,7,0,1,6,3,
    2,1,1,2,2,0,1,4,6,5,4,5,1,7,4,2,4,3,1,5,
    3,5,2,5,1,0,6,7,5,4,2,5,4,5,3,6,6,4,1,7,
    5,5,0,6,3,5,2,6,5,5,4,4,5,7,2,3,5,6,5,4,
    3,2,1,4,4,1,4,7,0,6,3,4,6,5,0,5,4,1,3,6,
    6,7,5,0,6,4,7,1,5,0,7,1,0,5,0,5,1,3,6,5,
    3,1,3,2,1,5,1,5,4,6,4,4,5,3,2,0,6,1,7,5,
    7,1,1,0,7,6,2,1,1,5,0,1,7,7,3,6,7,5,0,6,
    4,2,6,2,0,5,1,5,0,2,5,6,1,6,2,0,5,1,6,5
]

FACES = {
    'A1': {2,4,7}, 'A2': {1,4,7}, 'A4': {1,2,7}, 'A7': {1,2,4},  # Tet A (TIME=A7)
    'B0': {3,5,6}, 'B3': {0,5,6}, 'B5': {0,3,6}, 'B6': {0,3,5}   # Tet B (TIME=B0)
}

def get_closures(n=10):
    cycles = []
    face_seen = {f: set() for f in FACES}
    cum = 0
    cycle_events = []
    faces_done = set()
    
    for step in range(1, len(PI_200)+1):
        cum += PI_200[step-1]
        v = cum % 8
        completed = []
        
        for fn, verts in FACES.items():
            if fn not in faces_done and v in verts:
                face_seen[fn].add(v)
                if len(face_seen[fn]) == 3:
                    faces_done.add(fn)
                    tet = 'A' if fn.startswith('A') else 'B'
                    role = 'TIME' if fn in ['A7','B0'] else 'SPATIAL'
                    completed.append({'name':fn, 'tetId':tet, 'role':role, 'step':step, 'vertex':v})
        
        if completed:
            completed.sort(key=lambda x: x['name'])
            cycle_events.append({
                'piStep': step,
                'vertex': v,
                'faces': completed
            })
        
        if len(faces_done) == 8:
            cycles.append({
                'events': cycle_events,
                'startStep': cycle_events[0]['piStep'],
                'endStep': cycle_events[-1]['piStep']
            })
            if len(cycles) >= n:
                break
            # Reset for next cycle
            face_seen = {f: set() for f in FACES}
            faces_done = set()
            cycle_events = []
    
    return cycles

def analyze_pattern(events):
    """Get the A/B pattern from events"""
    pattern = []
    for e in events:
        tets = set(f['tetId'] for f in e['faces'])
        if len(tets) == 1:
            pattern.append(list(tets)[0])
        else:
            pattern.append('A+B')
    return '->'.join(pattern)

def main():
    print("=" * 70)
    print("10 CLOSURE CYCLES FROM PI (continuous traversal)")
    print("=" * 70)
    print()
    
    cycles = get_closures(10)
    
    for i, cycle in enumerate(cycles):
        events = cycle['events']
        pattern = analyze_pattern(events)
        
        # Collect faces by tet
        tet_a = []
        tet_b = []
        for e in events:
            for f in e['faces']:
                label = f['name'] + (' (T)' if f['role'] == 'TIME' else '')
                if f['tetId'] == 'A':
                    tet_a.append(label)
                else:
                    tet_b.append(label)
        
        print(f"CLOSURE {i+1} (steps {cycle['startStep']}-{cycle['endStep']}): {pattern}")
        print(f"  Tet A [{len(tet_a)}]: {', '.join(tet_a)}")
        print(f"  Tet B [{len(tet_b)}]: {', '.join(tet_b)}")
        
        # Show event details
        print(f"  Events:")
        for j, e in enumerate(events):
            faces_str = ', '.join([f['name'] + ('*' if f['role']=='TIME' else '') for f in e['faces']])
            print(f"    {j+1}. Step {e['piStep']}, V{e['vertex']}: {faces_str}")
        print()
    
    # Summary
    print("=" * 70)
    print("PATTERN SUMMARY")
    print("=" * 70)
    patterns = {}
    for i, cycle in enumerate(cycles):
        p = analyze_pattern(cycle['events'])
        if p not in patterns:
            patterns[p] = []
        patterns[p].append(i+1)
    
    for p, nums in patterns.items():
        print(f"  {p}: Closures {nums}")
    
    print()
    print("Note: Each closure has exactly 8 unique faces (4 Tet A + 4 Tet B)")
    print("      Pattern varies based on pi's cumulative vertex traversal")

if __name__ == "__main__":
    main()
