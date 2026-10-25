"""
Get 3 closure cycles from pi (continuous, not restarting).
Output JavaScript array for Module07.
"""

PI = [1,1,0,3,7,5,5,2,4,2,1,0,2,6,4,3,0,2,1,5,1,4,2,3,0,6,3,0,5,0,5,6,0,0,6,7,0,1,6,3,2,1,1,2,2,0,1,4,6,5,4,5,1,7,4,2,4,3,1,5,3,5,2,5,1,0,6,7,5,4,2,5,4,5,3,6,6,4,1,7,5,5,0,6,3,5,2,6,5,5,4,4,5,7,2,3,5,6,5,4]

FACES = {
    'A1': {2,4,7}, 'A2': {1,4,7}, 'A4': {1,2,7}, 'A7': {1,2,4},
    'B0': {3,5,6}, 'B3': {0,5,6}, 'B5': {0,3,6}, 'B6': {0,3,5}
}

def get_cycles(n=3):
    cycles = []
    face_seen = {f: set() for f in FACES}
    cum = 0
    cycle_events = []
    faces_done = set()
    
    for step in range(1, len(PI)+1):
        cum += PI[step-1]
        v = cum % 8
        completed = []
        
        for fn, verts in FACES.items():
            if fn not in faces_done and v in verts:
                face_seen[fn].add(v)
                if len(face_seen[fn]) == 3:
                    faces_done.add(fn)
                    tet = 'A' if fn.startswith('A') else 'B'
                    role = 'TIME' if fn in ['A7','B0'] else 'SPATIAL'
                    completed.append({'name':fn,'tetId':tet,'role':role})
        
        if completed:
            completed.sort(key=lambda x: x['name'])
            has_time = any(f['role']=='TIME' for f in completed)
            cycle_events.append({'piStep':step,'vertex':v,'faces':completed,'kingsChamber':has_time})
        
        if len(faces_done) == 8:
            cycles.append(cycle_events)
            if len(cycles) >= n:
                break
            # Reset for next cycle  
            face_seen = {f: set() for f in FACES}
            faces_done = set()
            cycle_events = []
    
    return cycles

cycles = get_cycles(3)

print("this.closureCycles = [")
for i, c in enumerate(cycles):
    tet_a = []
    tet_b = []
    for e in c:
        for f in e['faces']:
            if f['tetId'] == 'A':
                tet_a.append(f['name'] + (' (T)' if f['role']=='TIME' else ''))
            else:
                tet_b.append(f['name'] + (' (T)' if f['role']=='TIME' else ''))
    
    print(f"    // CLOSURE {i+1}: Tet A [{len(tet_a)}]: {', '.join(tet_a)} | Tet B [{len(tet_b)}]: {', '.join(tet_b)}")
    print("    {")
    print("        events: [")
    for j, e in enumerate(c):
        faces_js = ', '.join(["{ name: '%s', tetId: '%s', role: '%s' }" % (f['name'],f['tetId'],f['role']) for f in e['faces']])
        comma = ',' if j < len(c)-1 else ''
        print(f"            {{ piStep: {e['piStep']}, vertex: {e['vertex']}, faces: [{faces_js}], kingsChamber: {'true' if e['kingsChamber'] else 'false'} }}{comma}")
    print("        ]")
    comma2 = ',' if i < len(cycles)-1 else ''
    print(f"    }}{comma2}")

print("];")
