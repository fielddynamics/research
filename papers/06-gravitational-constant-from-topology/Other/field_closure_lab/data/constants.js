/**
 * =============================================================================
 * FIELD CLOSURE ENGINE LAB - Constants
 * Physical constants, pi digits, and vertex encodings
 * =============================================================================
 */

const CONSTANTS = {
    // =========================================================================
    // PHYSICAL CONSTANTS (CODATA 2018)
    // =========================================================================
    physics: {
        c: 2.998e8,              // Speed of light (m/s)
        h: 6.626e-34,            // Planck constant (J·s)
        hbar: 1.055e-34,         // Reduced Planck constant (J·s)
        G: 6.674e-11,            // Gravitational constant (m³/kg/s²)
        e: 1.602e-19,            // Elementary charge (C)
        eps0: 8.854e-12,         // Vacuum permittivity (F/m)
        m_e: 9.109e-31,          // Electron mass (kg)
        r_e: 2.818e-15,          // Classical electron radius (m)
        l_planck: 1.616e-35,     // Planck length (m)
        t_planck: 5.391e-44,     // Planck time (s)
        alpha: 1 / 137.036,        // Fine structure constant
        H: 2.27e-18,             // Hubble constant (1/s) ~ 70 km/s/Mpc
    },

    // =========================================================================
    // TETRAD TOPOLOGY
    // =========================================================================
    topology: {
        k: 4,                    // Number of coupling ports (tetrahedral faces)
        d: 3,                    // Spatial dimensions
        vertices: 8,             // Merkaba vertices (2^d = 2³ = 8)
        faces_per_tet: 4,        // Faces per tetrahedron
        total_faces: 8,          // Total faces in Merkaba (2 × 4)
        neighbors_close_pack: 12, // Close-packing neighbor count
    },

    // =========================================================================
    // DERIVED PARAMETERS
    // =========================================================================
    derived: {
        // Settlement frequency: f = c / r_e
        f_settlement: 2.998e8 / 2.818e-15,  // ~1.064e23 Hz

        // Port firing frequency: f_port = f_settlement / k
        f_port: (2.998e8 / 2.818e-15) / 4,  // ~2.66e22 Hz

        // Settlement period: T = r_e / c
        T_settlement: 2.818e-15 / 2.998e8,  // ~9.4e-24 s

        // Energy per settlement: E = h × f
        E_settlement: 6.626e-34 * (2.998e8 / 2.818e-15),  // ~7.05e-11 J

        // Angular momentum per port: L = hbar / k
        L_port: 1.055e-34 / 4,              // ~2.64e-35 J·s

        // Coupling strength per port: alpha / k
        alpha_port: (1 / 137.036) / 4,        // ~1.82e-3

        // Scale ratio: r_e / l_planck
        scale_ratio: 2.818e-15 / 1.616e-35, // ~1.74e20

        // Aperture factor: sqrt(k/pi)
        aperture_factor: Math.sqrt(4 / Math.PI), // ~1.128

        // Open ports vs blocked
        ports_open: 4,
        ports_blocked: 8,  // 12 - 4 in close-packing

        // Information per digit
        bits_per_digit: Math.log2(8),        // 3 bits
        bits_per_orbit: Math.log2(8) * 8,    // 24 bits

        // Orbits per electron (137 connection)
        orbits_per_electron: 137,
    },

    // =========================================================================
    // PI DIGITS (Base 10 for display, Base 8 for computation)
    // =========================================================================
    pi: {
        // First 100 digits of pi in base 10
        digits_base10: [
            3, 1, 4, 1, 5, 9, 2, 6, 5, 3,
            5, 8, 9, 7, 9, 3, 2, 3, 8, 4,
            6, 2, 6, 4, 3, 3, 8, 3, 2, 7,
            9, 5, 0, 2, 8, 8, 4, 1, 9, 7,
            1, 6, 9, 3, 9, 9, 3, 7, 5, 1,
            0, 5, 8, 2, 0, 9, 7, 4, 9, 4,
            4, 5, 9, 2, 3, 0, 7, 8, 1, 6,
            4, 0, 6, 2, 8, 6, 2, 0, 8, 9,
            9, 8, 6, 2, 8, 0, 3, 4, 8, 2,
            5, 3, 4, 2, 1, 1, 7, 0, 6, 7
        ],

        // First 100 digits of pi in base 8 (octal) - for Merkaba traversal
        // Pi in octal = 3.110375524210264302151423063050560067016321122011...
        digits_base8: [
            3, 1, 1, 0, 3, 7, 5, 5, 2, 4,
            2, 1, 0, 2, 6, 4, 3, 0, 2, 1,
            5, 1, 4, 2, 3, 0, 6, 3, 0, 5,
            0, 5, 6, 0, 0, 6, 7, 0, 1, 6,
            3, 2, 1, 1, 2, 2, 0, 1, 1, 4,
            6, 3, 3, 7, 6, 1, 7, 6, 7, 0,
            2, 1, 5, 7, 4, 5, 5, 6, 1, 1,
            0, 5, 0, 5, 6, 4, 4, 2, 5, 3,
            4, 5, 1, 4, 5, 3, 4, 0, 2, 6,
            5, 2, 2, 0, 5, 2, 0, 3, 5, 1
        ],
    },

    // =========================================================================
    // MERKABA VERTEX ENCODING (3-bit binary -> 3D coordinates)
    // =========================================================================
    vertices: {
        // Binary encoding: XYZ where each bit is 0 or 1
        // Bit 2 (MSB) = X axis: 0 = Left (-1), 1 = Right (+1)
        // Bit 1       = Y axis: 0 = Back (-1), 1 = Front (+1)
        // Bit 0 (LSB) = Z axis: 0 = Down (-1), 1 = Up (+1)
        //
        // PARITY determines tetrahedron assignment:
        //   ODD parity  (1 or 3 bits set) --> Tet A (pointing UP, apex at V7)
        //   EVEN parity (0 or 2 bits set) --> Tet B (pointing DOWN, apex at V0)
        encoding: {
            '000': { binary: '000', x: -1, y: -1, z: -1, tet: 'B', index: 0, parity: 0 },  // EVEN -> Tet B (apex)
            '001': { binary: '001', x: -1, y: -1, z: +1, tet: 'A', index: 1, parity: 1 },  // ODD -> Tet A
            '010': { binary: '010', x: -1, y: +1, z: -1, tet: 'A', index: 2, parity: 1 },  // ODD -> Tet A
            '011': { binary: '011', x: -1, y: +1, z: +1, tet: 'B', index: 3, parity: 2 },  // EVEN -> Tet B
            '100': { binary: '100', x: +1, y: -1, z: -1, tet: 'A', index: 4, parity: 1 },  // ODD -> Tet A
            '101': { binary: '101', x: +1, y: -1, z: +1, tet: 'B', index: 5, parity: 2 },  // EVEN -> Tet B
            '110': { binary: '110', x: +1, y: +1, z: -1, tet: 'B', index: 6, parity: 2 },  // EVEN -> Tet B
            '111': { binary: '111', x: +1, y: +1, z: +1, tet: 'A', index: 7, parity: 3 },  // ODD -> Tet A (apex)
        },

        // Tetrahedron assignments (per Python validation file)
        // Tet A (ODD parity - 1 or 3 bits set): 001, 010, 100, 111
        //   - Apex at V7 (111) = Right, Front, Up
        //   - Base at V1 (001), V2 (010), V4 (100)
        tetA: ['001', '010', '100', '111'],

        // Tet B (EVEN parity - 0 or 2 bits set): 000, 011, 101, 110
        //   - Apex at V0 (000) = Left, Back, Down
        //   - Base at V3 (011), V5 (101), V6 (110)
        tetB: ['000', '011', '101', '110'],

        // Directional labels for readability (X, Y, Z format)
        labels: {
            '000': 'LEFT-BACK-DOWN',
            '001': 'LEFT-BACK-UP',
            '010': 'LEFT-FRONT-DOWN',
            '011': 'LEFT-FRONT-UP',
            '100': 'RIGHT-BACK-DOWN',
            '101': 'RIGHT-BACK-UP',
            '110': 'RIGHT-FRONT-DOWN',
            '111': 'RIGHT-FRONT-UP',
        },
    },

    // =========================================================================
    // PORT/FACE DEFINITIONS (3+1 System)
    // Per Python validation file: each face is defined by 3 vertices
    // and is OPPOSITE to the 4th vertex of that tetrahedron
    // =========================================================================
    ports: {
        // Port IDs and their roles
        definitions: {
            'PORT_T': { id: 'T', name: 'Time', type: 'temporal', color: 0xFFD700 },
            'PORT_S1': { id: 'S1', name: 'Spatial 1', type: 'spatial', color: 0x4CAF50 },
            'PORT_S2': { id: 'S2', name: 'Spatial 2', type: 'spatial', color: 0x2196F3 },
            'PORT_S3': { id: 'S3', name: 'Spatial 3', type: 'spatial', color: 0x9C27B0 },
        },

        // Settlement order (time coordinates first)
        settlementOrder: ['PORT_T', 'PORT_S1', 'PORT_S2', 'PORT_S3'],

        // TET A FACES (Tet A has ODD parity vertices: 001, 010, 100, 111)
        // Each face contains 3 vertices and is OPPOSITE to one vertex
        tetA_faces: {
            'FACE_A1': { vertices: ['010', '100', '111'], opposite: '001', role: 'SPATIAL' },
            'FACE_A2': { vertices: ['001', '100', '111'], opposite: '010', role: 'SPATIAL' },
            'FACE_A4': { vertices: ['001', '010', '111'], opposite: '100', role: 'SPATIAL' },
            'FACE_A7': { vertices: ['001', '010', '100'], opposite: '111', role: 'TIME' },  // Base (floor)
        },

        // TET B FACES (Tet B has EVEN parity vertices: 000, 011, 101, 110)
        // Each face contains 3 vertices and is OPPOSITE to one vertex
        tetB_faces: {
            'FACE_B0': { vertices: ['011', '101', '110'], opposite: '000', role: 'TIME' },  // Base (floor)
            'FACE_B3': { vertices: ['000', '101', '110'], opposite: '011', role: 'SPATIAL' },
            'FACE_B5': { vertices: ['000', '011', '110'], opposite: '101', role: 'SPATIAL' },
            'FACE_B6': { vertices: ['000', '011', '101'], opposite: '110', role: 'SPATIAL' },
        },

        // Face order for animation (3 spatial + 1 time)
        tetA_faceOrder: ['FACE_A1', 'FACE_A2', 'FACE_A4', 'FACE_A7'],
        tetB_faceOrder: ['FACE_B3', 'FACE_B5', 'FACE_B6', 'FACE_B0'],
    },

    // =========================================================================
    // TRIFORCE SUBDIVISION (Face -> 4 sub-triangles)
    // =========================================================================
    triforce: {
        // Each face subdivides into 4 smaller triangles (Triforce pattern)
        // 3 corner triangles + 1 central inverted triangle
        subdivision: {
            corners: ['corner_0', 'corner_1', 'corner_2'],
            center: 'center_inverted',
        },

        // Sampling: Pi digit mod 4 selects which sub-triangle
        sampling_map: {
            0: 'center_inverted',  // Time tile (special)
            1: 'corner_0',
            2: 'corner_1',
            3: 'corner_2',
        },
    },

    // =========================================================================
    // VISUALIZATION COLORS
    // =========================================================================
    colors: {
        // Tetrahedra
        tetA: 0x4CAF50,          // Green
        tetB: 0xF44336,          // Red

        // Special vertices
        timeAxis: 0xFFD700,      // Gold
        activeVertex: 0x44aaff,  // Cyan

        // State colors
        visited: 0x666666,
        current: 0xFFFFFF,
        highlight: 0xFFEB3B,

        // Port colors
        portTime: 0xFFD700,
        portSpatial1: 0x4CAF50,
        portSpatial2: 0x2196F3,
        portSpatial3: 0x9C27B0,

        // Background
        background: 0x0a0a0f,
        grid: 0x333333,

        // Orbit colors (for closure visualization)
        orbit: [
            0x44aaff,   // Orbit 1 (cyan)
            0x9C27B0,   // Orbit 2 (purple)
            0x4CAF50,   // Orbit 3 (green)
            0xFF9800,   // Orbit 4 (orange)
            0xF44336,   // Orbit 5 (red)
        ],
    },

    // =========================================================================
    // CLOSURE MARKERS
    // =========================================================================
    closure: {
        // Positions where cumsum % 8 == 0 indicate orbit completion
        // Position == 0 indicates exact closure
        orbitSize: 8,  // 8 vertices per orbit

        // First 30 digits: closure analysis
        // Find where cumsum is multiple of 8
        closureDigits_base8: [5, 8, 13, 20], // Approximate digit indices

        // Key closure events in pi
        events: {
            firstOrbit: { digit: 5, cumsum: 8, meaning: 'First complete orbit' },
            fourthOrbit: { digit: 20, cumsum: 32, meaning: 'k=4 orbits complete' },
            eighth: { digit: 38, cumsum: 64, meaning: '2k=8 orbits = Merkaba cycle' },
        },
    },

    // =========================================================================
    // ANIMATION TIMING
    // =========================================================================
    animation: {
        stepDuration: 1000,      // ms per step at 1x speed
        transitionDuration: 300, // ms for transitions
        highlightDuration: 500,  // ms for highlights
        orbitPauseDuration: 1500, // ms pause at orbit completion
    },

    // =========================================================================
    // MODULE INFORMATION
    // =========================================================================
    modules: {
        1: {
            id: 1,
            name: 'Field Geometry',
            title: 'Module 01: Field Geometry',
            concept: 'The gravitational field is structured as a Merkaba - two interpenetrating tetrahedra forming 8 vertices.',
            visual: 'Two tetrahedra (green = Tet A, red = Tet B) sharing a common center, with 8 vertices labeled in binary coordinates.',
            insight: '8 vertices = 2^3 = all possible 3-bit binary combinations (000 to 111)',
        },
        2: {
            id: 2,
            name: 'Port System (3+1)',
            title: 'Module 02: The Port System',
            concept: 'Each tetrahedron has 4 faces acting as coupling ports: 3 spatial + 1 temporal.',
            visual: 'Faces highlighted showing the 3+1 port structure. Time face (gold) coordinates the 3 spatial faces.',
            insight: 'The time face enables settlement coordination across non-linear space.',
        },
        3: {
            id: 3,
            name: 'Triforce Interface',
            title: 'Module 03: Triforce Interface',
            concept: 'Each tetrahedral face subdivides into 4 triangles (Triforce pattern) for vertex sampling.',
            visual: 'Zoom into a single face showing Triforce subdivision and the 3 corner + 1 center triangle structure.',
            insight: 'The center triangle points inward, creating the "time tile" for temporal coordination.',
        },
        4: {
            id: 4,
            name: 'Pi Encoding',
            title: 'Module 04: Pi Encoding & Traversal',
            concept: 'Pi digits in base 8 directly map to Merkaba vertex positions, driving field traversal.',
            visual: 'Watch pi digits step through vertices: digit value mod 8 selects the next vertex binary code.',
            insight: 'Pi is positive-definite: every digit adds, never subtracts - creating unidirectional rotation.',
        },
        5: {
            id: 5,
            name: 'Settlement Sequence',
            title: 'Module 05: Settlement Sequence',
            concept: 'Tet A and Tet B alternate in an interleaved settlement pattern.',
            visual: 'Animation showing which tetrahedron is active based on vertex parity (even/odd 1-count).',
            insight: 'Even parity vertices (000, 011, 101, 110) belong to Tet A; odd to Tet B.',
        },
        6: {
            id: 6,
            name: 'Tile Size & Frequency',
            title: 'Module 06: Tile Size & Frequency',
            concept: 'The electron radius (2.818 fm) sets the fundamental tile size, yielding 10^23 Hz settlement.',
            visual: 'Scale comparison showing electron tile relative to Planck length, with frequency calculation.',
            insight: 'f = c / r_e = 1.064 × 10^23 Hz - the engine cycles 100 billion trillion times per second.',
        },
        7: {
            id: 7,
            name: 'Port Aperture',
            title: 'Module 07: Port Aperture & Coupling',
            concept: 'In 12-sphere close-packing, k=4 ports open while 8 remain blocked.',
            visual: 'Spheres showing 12 neighbors with 4 open channels (tetrahedral arrangement).',
            insight: 'sqrt(k/pi) = 1.128 - the aperture factor appears in the electron mass formula.',
        },
        8: {
            id: 8,
            name: 'Angular Momentum',
            title: 'Module 08: Angular Momentum & Chirality',
            concept: 'Each port activation contributes hbar/4 angular momentum, creating right-handed vortex.',
            visual: 'Rotation arrows showing angular momentum accumulation and helicity.',
            insight: 'Electron spin-1/2 emerges: sampling half the Merkaba (one tet worth) gives hbar/2.',
        },
        9: {
            id: 9,
            name: 'Information Content',
            title: 'Module 09: Information & Resonance',
            concept: 'Each digit encodes 3 bits; the electron contains ~3300 bits spanning 137 orbits.',
            visual: 'Information flow visualization with bandwidth calculation and resonance conditions.',
            insight: '137 = 1/alpha: the electron spans exactly 1/alpha Merkaba orbits.',
        },
        10: {
            id: 10,
            name: 'Complete Engine',
            title: 'Module 10: The Complete Engine',
            concept: 'All components working together: geometry, ports, pi encoding, settlement, and emergence.',
            visual: 'Full animated synthesis showing the complete 3+1 field closure cycle.',
            insight: 'Mass emerges from trapped information; the universe computes at the Planck scale.',
        },
    },
};

// Make available globally
window.CONSTANTS = CONSTANTS;
