/**
 * =============================================================================
 * MerkabaRenderer.js
 * Core 3D rendering class for the Merkaba structure
 * 
 * This class encapsulates all Three.js rendering logic for the Merkaba,
 * including vertex markers, tetrahedra, paths, and animations.
 * 
 * ARCHITECTURE:
 * - Uses a single container group for synchronized rotation
 * - All child groups are nested under the container
 * - Uses THREE.Clock for frame-rate independent animations
 * - Proper event listener cleanup in dispose()
 * 
 * Usage:
 *   const renderer = new MerkabaRenderer(containerElement);
 *   renderer.init();
 *   renderer.highlightVertex('101');
 *   renderer.drawPath('000', '101');
 * =============================================================================
 */

class MerkabaRenderer {
    constructor(container) {
        this.container = container;
        this.scene = null;
        this.camera = null;
        this.renderer = null;

        // THREE.Clock for frame-rate independent animations
        this.clock = null;

        // Main container group - ALL objects rotate together via this
        this.containerGroup = null;

        // Child groups for organized management (nested under containerGroup)
        this.groups = {
            tetA: null,         // Tetrahedron A
            tetB: null,         // Tetrahedron B
            vertices: null,     // Vertex markers
            paths: null,        // Traversal paths
            labels: null,       // Text labels
            sphere: null,       // Enclosing sphere
            triforce: null,     // Triforce subdivisions
            effects: null,      // Visual effects
        };

        // Vertex meshes for direct access
        this.vertexMeshes = {};

        // Edge lines for highlighting
        this.edgeLines = {
            tetA: [],
            tetB: [],
        };

        // Face meshes
        this.faceMeshes = {
            tetA: [],
            tetB: [],
        };

        // Animation state
        this.animationId = null;
        this.isDragging = false;
        this.prevMouse = { x: 0, y: 0 };
        this.autoRotate = true;
        this.rotationSpeed = 0.5; // radians per second (frame-rate independent)

        // Damping for smooth rotation
        this.rotationVelocity = { x: 0, y: 0 };
        this.dampingFactor = 0.95;

        // Axis lock - when true, only Y-axis rotation allowed (spin only)
        // This keeps the TIME floor at the bottom
        this.axisLocked = false;
        this._lockedSpinAngle = 0;

        // Scale
        this.scale = 2.0;

        // Current tetrahedron colors (can be overridden by modules)
        this.currentTetAColor = CONSTANTS.colors.tetA;
        this.currentTetBColor = CONSTANTS.colors.tetB;

        // Store tetrahedral vertices for Triforce calculations
        this.tetAVertices = null;
        this.tetBVertices = null;

        // Event handler references for cleanup
        this._boundHandlers = {
            mousedown: null,
            mousemove: null,
            mouseup: null,
            mouseleave: null,
            wheel: null,
            resize: null,
            touchstart: null,
            touchmove: null,
            touchend: null,
        };

        // Callbacks
        this.onVertexHover = null;
        this.onVertexClick = null;
    }

    // =========================================================================
    // INITIALIZATION
    // =========================================================================

    init() {
        this._createClock();
        this._createScene();
        this._createCamera();
        this._createRenderer();
        this._createLights();
        this._createContainerGroup();
        this._createGroups();
        this._createMerkaba();
        this._createVertexMarkers();
        this._createEnclosingSphere();
        this._setupControls();
        this._setupResizeHandler();
        this._startAnimation();

        return this;
    }

    _createClock() {
        // THREE.Clock for delta time calculations
        this.clock = new THREE.Clock();
    }

    _createScene() {
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(CONSTANTS.colors.background);
    }

    _createCamera() {
        const aspect = this.container.clientWidth / this.container.clientHeight;
        this.camera = new THREE.PerspectiveCamera(60, aspect, 0.1, 100);
        this.camera.position.set(4, 3, 4);
        this.camera.lookAt(0, 0, 0);
    }

    _createRenderer() {
        this.renderer = new THREE.WebGLRenderer({
            antialias: true,
            alpha: true,
            powerPreference: 'high-performance'
        });
        this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
        this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        this.container.appendChild(this.renderer.domElement);
    }

    _createLights() {
        const ambient = new THREE.AmbientLight(0xffffff, 0.6);
        this.scene.add(ambient);

        const directional = new THREE.DirectionalLight(0xffffff, 0.4);
        directional.position.set(5, 10, 5);
        this.scene.add(directional);
    }

    _createContainerGroup() {
        // Main container that holds all Merkaba-related objects
        // This is the ONLY group that rotates - all children rotate with it
        this.containerGroup = new THREE.Group();
        this.containerGroup.name = 'merkaba-container';
        this.scene.add(this.containerGroup);
    }

    _createGroups() {
        // Create all child groups and add to container (not scene)
        Object.keys(this.groups).forEach(key => {
            this.groups[key] = new THREE.Group();
            this.groups[key].name = key;
            this.containerGroup.add(this.groups[key]);
        });
    }

    // =========================================================================
    // MERKABA GEOMETRY
    // =========================================================================

    /**
     * MERKABA (Star Tetrahedron) Geometry:
     * 
     * A Merkaba consists of two interpenetrating tetrahedra whose 8 vertices
     * together form the corners of a cube. This is the dual of an octahedron.
     * 
     * Using binary encoding where each bit represents a spatial axis:
     *   bit 2 (MSB) = X axis: 0 = negative, 1 = positive
     *   bit 1       = Y axis: 0 = negative, 1 = positive  
     *   bit 0 (LSB) = Z axis: 0 = negative, 1 = positive
     * 
     * Tet A (even parity - even number of 1s): 000, 011, 101, 110
     * Tet B (odd parity - odd number of 1s):  001, 010, 100, 111
     * 
     * This creates two tetrahedra that share no vertices but whose combined
     * 8 vertices form a perfect cube.
     */

    _createMerkaba() {
        const s = this.scale;

        // Build vertex position map from binary encoding (cube corners)
        // Each binary code maps to a corner of the cube
        this.vertexPositions = {};
        Object.entries(CONSTANTS.vertices.encoding).forEach(([binary, data]) => {
            this.vertexPositions[binary] = new THREE.Vector3(
                data.x * s,
                data.y * s,
                data.z * s
            );
        });

        // CRITICAL: Vertex arrays must have APEX at index 0 for edge/face drawing!
        // The _createTetrahedronEdges assumes [0,1], [0,2], [0,3] are apex-to-base edges.

        // Tet A vertices (ODD parity - 1 or 3 bits set)
        // Apex at V7 (111) = Right, Front, Up
        // Base at V1 (001), V2 (010), V4 (100)
        this.tetAVertices = [
            this.vertexPositions['111'],  // index 0 = APEX
            this.vertexPositions['001'],  // index 1 = base vertex
            this.vertexPositions['010'],  // index 2 = base vertex
            this.vertexPositions['100']   // index 3 = base vertex
        ];

        // Tet B vertices (EVEN parity - 0 or 2 bits set)
        // Apex at V0 (000) = Left, Back, Down
        // Base at V3 (011), V5 (101), V6 (110)
        this.tetBVertices = [
            this.vertexPositions['000'],  // index 0 = APEX
            this.vertexPositions['011'],  // index 1 = base vertex
            this.vertexPositions['101'],  // index 2 = base vertex
            this.vertexPositions['110']   // index 3 = base vertex
        ];

        // Create edges for Tet A
        this._createTetrahedronEdges(this.tetAVertices, CONSTANTS.colors.tetA, this.groups.tetA, 'tetA');

        // Create edges for Tet B
        this._createTetrahedronEdges(this.tetBVertices, CONSTANTS.colors.tetB, this.groups.tetB, 'tetB');

        // Create transparent faces for each tetrahedron
        this._createTetrahedronFaces(this.tetAVertices, CONSTANTS.colors.tetA, 0.15, this.groups.tetA, 'A');
        this._createTetrahedronFaces(this.tetBVertices, CONSTANTS.colors.tetB, 0.15, this.groups.tetB, 'B');

        // Add clock tick marks to TIME faces
        this._createTimeFaceClockTicks(this.tetAVertices, CONSTANTS.colors.tetA, this.groups.tetA, 'A');
        this._createTimeFaceClockTicks(this.tetBVertices, CONSTANTS.colors.tetB, this.groups.tetB, 'B');
    }

    /**
     * Create clock tick marks on the TIME face (base) of a tetrahedron
     * This visually distinguishes the temporal port from spatial ports
     */
    _createTimeFaceClockTicks(vertices, color, group, tetId) {
        // TIME face is the base: vertices [1], [2], [3] (indices into tetAVertices/tetBVertices)
        // which corresponds to face index 3: [1, 3, 2]
        const v1 = vertices[1];
        const v2 = vertices[2];
        const v3 = vertices[3];

        // Calculate centroid of the TIME face
        const centroid = new THREE.Vector3()
            .add(v1).add(v2).add(v3)
            .divideScalar(3);

        // Calculate the face normal (points toward apex for Tet A, away for Tet B)
        const edge1 = new THREE.Vector3().subVectors(v2, v1);
        const edge2 = new THREE.Vector3().subVectors(v3, v1);
        const normal = new THREE.Vector3().crossVectors(edge1, edge2).normalize();

        // Offset the clock slightly above the face surface
        const offsetAmount = 0.02;
        const clockCenter = centroid.clone().add(normal.clone().multiplyScalar(offsetAmount));

        // Calculate radius for the clock (about 16% of distance from centroid to vertex)
        // This is 60% smaller than the original 40%
        const distToVertex = centroid.distanceTo(v1);
        const clockRadius = distToVertex * 0.16;
        const innerRadius = clockRadius * 0.7;  // Inner tick start
        const outerRadius = clockRadius * 0.95; // Outer tick end

        // Create a basis for drawing in the face plane
        // Use edge1 as the X direction (normalized)
        const xAxis = edge1.clone().normalize();
        // Y axis is perpendicular to both normal and X
        const yAxis = new THREE.Vector3().crossVectors(normal, xAxis).normalize();

        // Create 12 tick marks (like clock hours)
        const numTicks = 12;
        const tickGeometries = [];

        for (let i = 0; i < numTicks; i++) {
            const angle = (i / numTicks) * Math.PI * 2;
            const cos = Math.cos(angle);
            const sin = Math.sin(angle);

            // Calculate tick start and end points
            const innerPoint = clockCenter.clone()
                .add(xAxis.clone().multiplyScalar(cos * innerRadius))
                .add(yAxis.clone().multiplyScalar(sin * innerRadius));

            const outerPoint = clockCenter.clone()
                .add(xAxis.clone().multiplyScalar(cos * outerRadius))
                .add(yAxis.clone().multiplyScalar(sin * outerRadius));

            // Create line geometry for this tick
            const tickGeo = new THREE.BufferGeometry().setFromPoints([innerPoint, outerPoint]);
            tickGeometries.push(tickGeo);
        }

        // Create lines for all ticks
        tickGeometries.forEach(geo => {
            const material = new THREE.LineBasicMaterial({
                color: color,
                transparent: true,
                opacity: 0.9
            });
            const line = new THREE.Line(geo, material);
            line.userData = { type: 'clock-tick', tetId };
            group.add(line);
        });

        // Add a small circle outline to connect the ticks visually
        const circlePoints = [];
        const circleSegments = 32;
        for (let i = 0; i <= circleSegments; i++) {
            const angle = (i / circleSegments) * Math.PI * 2;
            const point = clockCenter.clone()
                .add(xAxis.clone().multiplyScalar(Math.cos(angle) * clockRadius))
                .add(yAxis.clone().multiplyScalar(Math.sin(angle) * clockRadius));
            circlePoints.push(point);
        }

        const circleGeo = new THREE.BufferGeometry().setFromPoints(circlePoints);
        const circleMat = new THREE.LineBasicMaterial({
            color: color,
            transparent: true,
            opacity: 0.5
        });
        const circle = new THREE.Line(circleGeo, circleMat);
        circle.userData = { type: 'clock-circle', tetId };
        group.add(circle);
    }

    _createTetrahedronEdges(vertices, color, group, groupId) {
        // CRITICAL: vertices[0] must be the APEX for correct edge drawing
        // Edges connect apex to each base vertex, then base vertices to each other
        const edges = [
            [0, 1], [0, 2], [0, 3],  // apex (index 0) to 3 base vertices
            [1, 2], [2, 3], [3, 1]   // base triangle edges
        ];

        edges.forEach(([i, j]) => {
            const geometry = new THREE.BufferGeometry().setFromPoints([
                vertices[i], vertices[j]
            ]);

            // Note: linewidth > 1 only works in some browsers/contexts
            // For wider lines, consider using Line2 from three/examples/jsm/lines/
            const material = new THREE.LineBasicMaterial({
                color: color,
                transparent: true,
                opacity: 1.0
            });

            const line = new THREE.Line(geometry, material);
            line.userData = { type: 'edge', groupId };
            group.add(line);

            // Store reference
            if (groupId === 'tetA') {
                this.edgeLines.tetA.push(line);
            } else {
                this.edgeLines.tetB.push(line);
            }
        });
    }

    _createTetrahedronFaces(vertices, color, opacity, group, tetId) {
        // CRITICAL: vertices[0] must be the APEX
        // Faces 0-2 are the 3 side faces (each includes apex)
        // Face 3 is the base (opposite to apex) = TIME port
        const faces = [
            [0, 1, 2],  // Side face (apex + 2 base verts) - opposite to base[3]
            [0, 2, 3],  // Side face (apex + 2 base verts) - opposite to base[1]
            [0, 3, 1],  // Side face (apex + 2 base verts) - opposite to base[2]
            [1, 3, 2]   // Base face (3 base verts) - opposite to apex[0]
        ];

        faces.forEach((faceIndices, faceIndex) => {
            const geometry = new THREE.BufferGeometry();
            const positions = new Float32Array([
                vertices[faceIndices[0]].x, vertices[faceIndices[0]].y, vertices[faceIndices[0]].z,
                vertices[faceIndices[1]].x, vertices[faceIndices[1]].y, vertices[faceIndices[1]].z,
                vertices[faceIndices[2]].x, vertices[faceIndices[2]].y, vertices[faceIndices[2]].z,
            ]);
            geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
            geometry.computeVertexNormals();

            const material = new THREE.MeshBasicMaterial({
                color: color,
                transparent: true,
                opacity: opacity,
                side: THREE.DoubleSide,
                depthWrite: false
            });

            const mesh = new THREE.Mesh(geometry, material);
            mesh.userData = { type: 'face', tetId, faceIndex };
            group.add(mesh);

            // Store reference
            if (tetId === 'A') {
                this.faceMeshes.tetA.push(mesh);
            } else {
                this.faceMeshes.tetB.push(mesh);
            }
        });
    }

    // =========================================================================
    // VERTEX MARKERS
    // =========================================================================

    _createVertexMarkers() {
        // Use the same vertex positions as the tetrahedra (computed in _createMerkaba)
        Object.entries(CONSTANTS.vertices.encoding).forEach(([binary, data]) => {
            // Get position from vertexPositions map (set up in _createMerkaba)
            const position = this.vertexPositions[binary];

            // Determine color based on tetrahedron
            const color = data.tet === 'A' ? CONSTANTS.colors.tetA : CONSTANTS.colors.tetB;

            // Create sphere marker - size proportional to scale
            const geometry = new THREE.SphereGeometry(0.15, 16, 12);
            const material = new THREE.MeshBasicMaterial({ color: color });
            const mesh = new THREE.Mesh(geometry, material);
            mesh.position.copy(position);
            mesh.userData = {
                type: 'vertex',
                binary: binary,
                tet: data.tet,
                originalColor: color,
                originalScale: 1,
                position: position.clone()
            };

            this.groups.vertices.add(mesh);
            this.vertexMeshes[binary] = mesh;
        });
    }

    _createEnclosingSphere() {
        // Wireframe sphere that passes through all cube corners
        // Cube corner distance from origin = scale * sqrt(3)
        const sphereRadius = this.scale * Math.sqrt(3);
        const geometry = new THREE.SphereGeometry(sphereRadius, 24, 16);
        const material = new THREE.MeshBasicMaterial({
            color: CONSTANTS.colors.grid,
            wireframe: true,
            transparent: true,
            opacity: 0.1
        });
        const sphere = new THREE.Mesh(geometry, material);
        sphere.userData = { type: 'enclosingSphere' };
        this.groups.sphere.add(sphere);
    }

    // =========================================================================
    // VERTEX HIGHLIGHTING & SELECTION
    // =========================================================================

    highlightVertex(binary, color = CONSTANTS.colors.current) {
        const mesh = this.vertexMeshes[binary];
        if (mesh) {
            mesh.material.color.setHex(color);
            mesh.scale.set(1.5, 1.5, 1.5);
        }
    }

    unhighlightVertex(binary) {
        const mesh = this.vertexMeshes[binary];
        if (mesh) {
            mesh.material.color.setHex(mesh.userData.originalColor);
            mesh.scale.set(1, 1, 1);
        }
    }

    resetAllVertices() {
        Object.values(this.vertexMeshes).forEach(mesh => {
            mesh.material.color.setHex(mesh.userData.originalColor);
            mesh.scale.set(1, 1, 1);
        });
    }

    setVertexVisited(binary) {
        const mesh = this.vertexMeshes[binary];
        if (mesh) {
            mesh.userData.visited = true;
        }
    }

    // =========================================================================
    // PATH DRAWING
    // =========================================================================

    drawPath(fromBinary, toBinary, color = CONSTANTS.colors.activeVertex) {
        const fromMesh = this.vertexMeshes[fromBinary];
        const toMesh = this.vertexMeshes[toBinary];

        if (!fromMesh || !toMesh) return null;

        const geometry = new THREE.BufferGeometry().setFromPoints([
            fromMesh.position,
            toMesh.position
        ]);

        const material = new THREE.LineBasicMaterial({
            color: color,
            transparent: true,
            opacity: 0.8
        });

        const line = new THREE.Line(geometry, material);
        line.userData = { type: 'path', from: fromBinary, to: toBinary };
        this.groups.paths.add(line);

        return line;
    }

    clearPaths() {
        // Dispose and remove all path children
        const children = [...this.groups.paths.children];
        children.forEach(child => {
            this.groups.paths.remove(child);
            if (child.geometry) child.geometry.dispose();
            if (child.material) child.material.dispose();
        });
    }

    // =========================================================================
    // FACE HIGHLIGHTING
    // =========================================================================

    highlightFace(tetId, faceIndex, color, opacity = 0.5) {
        const faces = tetId === 'A' ? this.faceMeshes.tetA : this.faceMeshes.tetB;
        if (faces[faceIndex]) {
            faces[faceIndex].material.color.setHex(color);
            faces[faceIndex].material.opacity = opacity;
        }
    }

    resetFaces() {
        this.faceMeshes.tetA.forEach(mesh => {
            mesh.material.color.setHex(this.currentTetAColor);
            mesh.material.opacity = 0.1;
        });
        this.faceMeshes.tetB.forEach(mesh => {
            mesh.material.color.setHex(this.currentTetBColor);
            mesh.material.opacity = 0.1;
        });
    }

    // =========================================================================
    // TETRAHEDRON VISIBILITY
    // =========================================================================

    setTetAVisible(visible) {
        this.groups.tetA.visible = visible;
    }

    setTetBVisible(visible) {
        this.groups.tetB.visible = visible;
    }

    setTetAOpacity(opacity) {
        this.groups.tetA.children.forEach(child => {
            if (child.material) {
                child.material.opacity = Math.min(opacity, 1);
                child.material.transparent = opacity < 1;
            }
        });
    }

    setTetBOpacity(opacity) {
        this.groups.tetB.children.forEach(child => {
            if (child.material) {
                child.material.opacity = Math.min(opacity, 1);
                child.material.transparent = opacity < 1;
            }
        });
    }

    highlightTetrahedron(tetId) {
        if (tetId === 'A') {
            this.setTetAOpacity(0.8);
            this.setTetBOpacity(0.2);
        } else {
            this.setTetAOpacity(0.2);
            this.setTetBOpacity(0.8);
        }
    }

    resetTetrahedronOpacity() {
        this.setTetAOpacity(0.3);
        this.setTetBOpacity(0.3);
    }

    // =========================================================================
    // VERTEX MARKER VISIBILITY
    // =========================================================================

    /**
     * Show or hide all vertex markers
     * @param {boolean} visible - true to show, false to hide
     */
    setVertexMarkersVisible(visible) {
        this.groups.vertices.visible = visible;
    }

    /**
     * Show vertex markers (convenience method for modules)
     */
    showVertexMarkers() {
        this.setVertexMarkersVisible(true);
    }

    /**
     * Hide vertex markers (convenience method for modules)
     */
    hideVertexMarkers() {
        this.setVertexMarkersVisible(false);
    }

    // =========================================================================
    // TETRAHEDRON COLOR CUSTOMIZATION
    // =========================================================================

    /**
     * Set the color of Tetrahedron A edges and faces
     * @param {number} color - Hex color value (e.g., 0x4488ff)
     */
    setTetAColor(color) {
        this.currentTetAColor = color;
        this.groups.tetA.children.forEach(child => {
            if (child.material) {
                child.material.color.setHex(color);
            }
        });
    }

    /**
     * Set the color of Tetrahedron B edges and faces
     * @param {number} color - Hex color value (e.g., 0xffcc00)
     */
    setTetBColor(color) {
        this.currentTetBColor = color;
        this.groups.tetB.children.forEach(child => {
            if (child.material) {
                child.material.color.setHex(color);
            }
        });
    }

    /**
     * Reset tetrahedron colors to defaults
     */
    resetTetrahedronColors() {
        this.currentTetAColor = CONSTANTS.colors.tetA;
        this.currentTetBColor = CONSTANTS.colors.tetB;
        this.setTetAColor(CONSTANTS.colors.tetA);
        this.setTetBColor(CONSTANTS.colors.tetB);
    }

    // =========================================================================
    // TRIFORCE VISUALIZATION
    // =========================================================================

    /**
     * Create Triforce subdivision on a face using 3 vertex binary codes.
     * @param {string[]} vertexBinaries - Array of 3 binary codes for face vertices
     * @param {string} oppositeBinary - Binary code of the opposite vertex (heart)
     * @param {string} tetId - 'A' or 'B'
     * @param {number} baseColor - Optional hex color for all sub-triangles (default uses port colors)
     */
    createTriforceFromVertices(vertexBinaries, oppositeBinary, tetId, baseColor = null) {
        if (!this.vertexPositions) {
            console.warn('Vertex positions not initialized');
            return;
        }

        // Get actual 3D positions from binary codes
        const v0 = this.vertexPositions[vertexBinaries[0]];
        const v1 = this.vertexPositions[vertexBinaries[1]];
        const v2 = this.vertexPositions[vertexBinaries[2]];

        if (!v0 || !v1 || !v2) {
            console.warn('Invalid vertex binaries:', vertexBinaries);
            return;
        }

        // Calculate midpoints for Triforce subdivision
        const m01 = new THREE.Vector3().addVectors(v0, v1).multiplyScalar(0.5);
        const m12 = new THREE.Vector3().addVectors(v1, v2).multiplyScalar(0.5);
        const m20 = new THREE.Vector3().addVectors(v2, v0).multiplyScalar(0.5);

        // Store midpoints and vertex mapping for sub-triangle highlighting
        this.triforceData = {
            tetId,
            vertexBinaries,
            oppositeBinary,
            midpoints: { m01, m12, m20 },
            // Map vertex binary to sub-triangle ID
            vertexToSubTri: {
                [vertexBinaries[0]]: 'corner_0',
                [vertexBinaries[1]]: 'corner_1',
                [vertexBinaries[2]]: 'corner_2',
                [oppositeBinary]: 'center'
            },
            subTriMeshes: {}
        };

        // Create 4 sub-triangles
        // If baseColor is provided, use it for all; otherwise use distinct port colors
        const useUniformColor = baseColor !== null;
        const subTriangles = [
            {
                verts: [v0, m01, m20], id: 'corner_0', vertexBinary: vertexBinaries[0],
                color: useUniformColor ? baseColor : CONSTANTS.colors.portSpatial1, label: 'C1'
            },
            {
                verts: [v1, m12, m01], id: 'corner_1', vertexBinary: vertexBinaries[1],
                color: useUniformColor ? baseColor : CONSTANTS.colors.portSpatial2, label: 'C2'
            },
            {
                verts: [v2, m20, m12], id: 'corner_2', vertexBinary: vertexBinaries[2],
                color: useUniformColor ? baseColor : CONSTANTS.colors.portSpatial3, label: 'C3'
            },
            {
                verts: [m01, m12, m20], id: 'center', vertexBinary: oppositeBinary,
                color: useUniformColor ? baseColor : CONSTANTS.colors.portTime, label: 'H'
            },
        ];

        // Store base color for animations
        this.triforceData.baseColor = baseColor;

        subTriangles.forEach(tri => {
            const geometry = new THREE.BufferGeometry();
            const positions = new Float32Array([
                tri.verts[0].x, tri.verts[0].y, tri.verts[0].z,
                tri.verts[1].x, tri.verts[1].y, tri.verts[1].z,
                tri.verts[2].x, tri.verts[2].y, tri.verts[2].z,
            ]);
            geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
            geometry.computeVertexNormals();

            const material = new THREE.MeshBasicMaterial({
                color: tri.color,
                transparent: true,
                opacity: 0.2,  // Start dimmed
                side: THREE.DoubleSide,
                depthWrite: false
            });

            const mesh = new THREE.Mesh(geometry, material);
            mesh.userData = {
                type: 'triforce',
                tetId,
                subTriId: tri.id,
                vertexBinary: tri.vertexBinary,
                originalColor: tri.color,
                originalOpacity: 0.2
            };
            this.groups.triforce.add(mesh);

            // Store reference for highlighting
            this.triforceData.subTriMeshes[tri.id] = mesh;
        });

        // Add edge lines for Triforce inner triangle (more visible)
        const innerEdges = [
            [m01, m12], [m12, m20], [m20, m01]
        ];

        innerEdges.forEach(([a, b]) => {
            const geo = new THREE.BufferGeometry().setFromPoints([a, b]);
            const mat = new THREE.LineBasicMaterial({
                color: 0xffffff,
                opacity: 0.8,
                transparent: true
            });
            const line = new THREE.Line(geo, mat);
            line.userData = { type: 'triforce-edge' };
            this.groups.triforce.add(line);
        });

        // Add outer edge lines for face boundary
        const outerEdges = [
            [v0, v1], [v1, v2], [v2, v0]
        ];

        outerEdges.forEach(([a, b]) => {
            const geo = new THREE.BufferGeometry().setFromPoints([a, b]);
            const mat = new THREE.LineBasicMaterial({
                color: tetId === 'A' ? this.currentTetAColor : this.currentTetBColor,
                opacity: 1.0,
                transparent: false
            });
            const line = new THREE.Line(geo, mat);
            line.userData = { type: 'triforce-edge-outer' };
            this.groups.triforce.add(line);
        });
    }

    /**
     * Highlight a specific sub-triangle of the triforce
     * @param {string} subTriId - 'corner_0', 'corner_1', 'corner_2', or 'center'
     * @param {boolean} highlight - true to highlight, false to reset
     */
    highlightSubTriangle(subTriId, highlight = true) {
        if (!this.triforceData || !this.triforceData.subTriMeshes[subTriId]) {
            return;
        }

        const mesh = this.triforceData.subTriMeshes[subTriId];
        if (highlight) {
            mesh.material.opacity = 0.8;  // Bright when highlighted
        } else {
            mesh.material.opacity = mesh.userData.originalOpacity;
        }
    }

    /**
     * Highlight the sub-triangle that corresponds to a vertex binary code
     * @param {string} vertexBinary - The binary code of the vertex
     * @param {boolean} highlight - true to highlight, false to reset
     */
    highlightSubTriangleForVertex(vertexBinary, highlight = true) {
        if (!this.triforceData || !this.triforceData.vertexToSubTri[vertexBinary]) {
            return;
        }

        const subTriId = this.triforceData.vertexToSubTri[vertexBinary];
        this.highlightSubTriangle(subTriId, highlight);
    }

    /**
     * Reset all sub-triangles to default state
     */
    resetAllSubTriangles() {
        if (!this.triforceData || !this.triforceData.subTriMeshes) {
            return;
        }

        Object.values(this.triforceData.subTriMeshes).forEach(mesh => {
            mesh.material.opacity = mesh.userData.originalOpacity;
        });
    }

    // Legacy method for backward compatibility
    createTriforceOnFace(tetId, faceIndex) {
        // Map face index to vertex binaries using the new face definitions
        const faceOrder = tetId === 'A'
            ? CONSTANTS.ports.tetA_faceOrder
            : CONSTANTS.ports.tetB_faceOrder;
        const faces = tetId === 'A'
            ? CONSTANTS.ports.tetA_faces
            : CONSTANTS.ports.tetB_faces;

        const faceId = faceOrder[faceIndex];
        if (!faceId || !faces[faceId]) {
            console.warn(`Invalid face index: ${faceIndex}`);
            return;
        }

        const faceData = faces[faceId];
        this.createTriforceFromVertices(faceData.vertices, faceData.opposite, tetId);
    }

    clearTriforce() {
        const children = [...this.groups.triforce.children];
        children.forEach(child => {
            this.groups.triforce.remove(child);
            if (child.geometry) child.geometry.dispose();
            if (child.material) child.material.dispose();
        });
        this.triforceData = null;
    }

    /**
     * Create triforce heart triangle lines on all 8 faces of both tetrahedra.
     * This shows where each face is subdivided, making the structure clearer.
     */
    createTriforceHeartLinesOnAllFaces() {
        if (!this.tetAVertices || !this.tetBVertices) {
            console.warn('Tetrahedron vertices not initialized');
            return;
        }

        // Store references for cleanup
        this.triforceHeartLines = [];

        // Face definitions: indices into tetAVertices/tetBVertices
        // vertices[0] = APEX, vertices[1,2,3] = BASE
        const faceVertexIndices = [
            [0, 1, 2],  // Face 0
            [0, 2, 3],  // Face 1
            [0, 3, 1],  // Face 2
            [1, 3, 2],  // Face 3 (TIME floor)
        ];

        // Create heart lines for Tet A (darker/muted blue)
        faceVertexIndices.forEach((indices, faceIdx) => {
            const v0 = this.tetAVertices[indices[0]];
            const v1 = this.tetAVertices[indices[1]];
            const v2 = this.tetAVertices[indices[2]];
            this._addHeartTriangleLines(v0, v1, v2, 0x2255aa, 0.7);
        });

        // Create heart lines for Tet B (darker/muted gold)
        faceVertexIndices.forEach((indices, faceIdx) => {
            const v0 = this.tetBVertices[indices[0]];
            const v1 = this.tetBVertices[indices[1]];
            const v2 = this.tetBVertices[indices[2]];
            this._addHeartTriangleLines(v0, v1, v2, 0xaa8800, 0.7);
        });
    }

    /**
     * Add the inner heart triangle lines for a single face
     */
    _addHeartTriangleLines(v0, v1, v2, color, opacity) {
        // Calculate midpoints
        const m01 = new THREE.Vector3().addVectors(v0, v1).multiplyScalar(0.5);
        const m12 = new THREE.Vector3().addVectors(v1, v2).multiplyScalar(0.5);
        const m20 = new THREE.Vector3().addVectors(v2, v0).multiplyScalar(0.5);

        // Inner triangle edges (the heart)
        const edges = [
            [m01, m12],
            [m12, m20],
            [m20, m01]
        ];

        edges.forEach(([a, b]) => {
            const geometry = new THREE.BufferGeometry().setFromPoints([a, b]);
            const material = new THREE.LineBasicMaterial({
                color: color,
                opacity: opacity,
                transparent: true
            });
            const line = new THREE.Line(geometry, material);
            line.userData = { type: 'triforce-heart-line' };
            this.groups.triforce.add(line);
            this.triforceHeartLines.push(line);
        });
    }

    /**
     * Clear only the triforce heart lines (not the full triforce)
     */
    clearTriforceHeartLines() {
        if (this.triforceHeartLines) {
            this.triforceHeartLines.forEach(line => {
                this.groups.triforce.remove(line);
                if (line.geometry) line.geometry.dispose();
                if (line.material) line.material.dispose();
            });
            this.triforceHeartLines = [];
        }
    }

    // =========================================================================
    // PORT APERTURE CIRCLES (on enclosing sphere)
    // =========================================================================

    /**
     * Calculate the face centroid and outward normal for a tetrahedron face
     * @param {string} tetId - 'A' or 'B'
     * @param {number} faceIndex - 0-3 (0-2 are spatial walls, 3 is TIME floor)
     * @returns {Object} {centroid: Vector3, normal: Vector3}
     */
    _getFaceCentroidAndNormal(tetId, faceIndex) {
        const vertices = tetId === 'A' ? this.tetAVertices : this.tetBVertices;
        if (!vertices) return null;

        // Face definitions (same as _createTetrahedronFaces)
        // vertices[0] = APEX, vertices[1,2,3] = BASE
        const faceIndices = [
            [0, 1, 2],  // Face 0: Side face, opposite to vertex[3]
            [0, 2, 3],  // Face 1: Side face, opposite to vertex[1]
            [0, 3, 1],  // Face 2: Side face, opposite to vertex[2]
            [1, 3, 2]   // Face 3: Base/TIME face, opposite to vertex[0] (apex)
        ];

        const face = faceIndices[faceIndex];
        const v0 = vertices[face[0]];
        const v1 = vertices[face[1]];
        const v2 = vertices[face[2]];

        // Calculate centroid
        const centroid = new THREE.Vector3()
            .add(v0).add(v1).add(v2)
            .divideScalar(3);

        // Calculate normal (cross product of two edges)
        const edge1 = new THREE.Vector3().subVectors(v1, v0);
        const edge2 = new THREE.Vector3().subVectors(v2, v0);
        const normal = new THREE.Vector3().crossVectors(edge1, edge2).normalize();

        // Ensure normal points outward (away from origin)
        if (normal.dot(centroid) < 0) {
            normal.negate();
        }

        return { centroid, normal };
    }

    /**
     * Create port aperture circles on the enclosing sphere for a tetrahedron
     * Each of the 4 faces gets a circle showing its "port domain boundary"
     * @param {string} tetId - 'A' or 'B'
     * @param {number} color - Hex color for the circles
     * @param {boolean} clearExisting - Whether to clear existing circles first (default true)
     * @param {number} baseOpacity - Base opacity for the circles (default 0.6)
     * @param {number} discOpacity - Base opacity for the filled disc (default 0.08)
     */
    createPortApertureCircles(tetId, color, clearExisting = true, baseOpacity = 0.6, discOpacity = 0.08) {
        // Clear existing port circles if requested
        if (clearExisting) {
            this.clearPortApertureCircles();
            // Initialize the data structure
            this.portApertureData = {
                tetA: { circles: [], meshes: [] },
                tetB: { circles: [], meshes: [] },
                allMeshes: []
            };
        }
        
        // Ensure data structure exists
        if (!this.portApertureData) {
            this.portApertureData = {
                tetA: { circles: [], meshes: [] },
                tetB: { circles: [], meshes: [] },
                allMeshes: []
            };
        }

        const sphereRadius = this.scale * Math.sqrt(3);
        
        // For k=4 packing: domain boundary is where adjacent port regions meet
        // Face normals of a tetrahedron are arccos(-1/3) = 109.47° apart
        // Domain boundary is at half that angle = 54.74° from each face normal
        const portAngularRadius = Math.acos(-1/3) / 2;  // ~54.74 degrees - correct k=4

        const tetData = tetId === 'A' ? this.portApertureData.tetA : this.portApertureData.tetB;

        // Create a circle on the sphere for each of the 4 faces
        for (let faceIndex = 0; faceIndex < 4; faceIndex++) {
            const faceData = this._getFaceCentroidAndNormal(tetId, faceIndex);
            if (!faceData) continue;

            // The port center on the sphere is where the face normal intersects it
            const portCenter = faceData.normal.clone().multiplyScalar(sphereRadius);

            // Create a circle on the sphere surface
            // We need to draw a circle perpendicular to the normal at the sphere surface
            const circlePoints = [];
            const numSegments = 48;

            // Create orthonormal basis for the circle plane
            const tangent1 = new THREE.Vector3();
            if (Math.abs(faceData.normal.x) < 0.9) {
                tangent1.set(1, 0, 0);
            } else {
                tangent1.set(0, 1, 0);
            }
            tangent1.cross(faceData.normal).normalize();
            const tangent2 = new THREE.Vector3().crossVectors(faceData.normal, tangent1).normalize();

            // Circle radius on the sphere (chord length for the angular radius)
            const circleRadius = sphereRadius * Math.sin(portAngularRadius);
            // How far back from the sphere surface the circle plane is
            const offsetFromCenter = sphereRadius * Math.cos(portAngularRadius);

            // Circle center is on the sphere surface, offset inward
            const circleCenter = faceData.normal.clone().multiplyScalar(offsetFromCenter);

            for (let i = 0; i <= numSegments; i++) {
                const angle = (i / numSegments) * Math.PI * 2;
                const point = circleCenter.clone()
                    .add(tangent1.clone().multiplyScalar(Math.cos(angle) * circleRadius))
                    .add(tangent2.clone().multiplyScalar(Math.sin(angle) * circleRadius));
                circlePoints.push(point);
            }

            // Create the circle line
            const circleGeo = new THREE.BufferGeometry().setFromPoints(circlePoints);
            const circleMat = new THREE.LineBasicMaterial({
                color: color,
                transparent: true,
                opacity: baseOpacity,
                linewidth: 2
            });
            const circleLine = new THREE.Line(circleGeo, circleMat);
            circleLine.userData = {
                type: 'port-aperture-circle',
                tetId,
                faceIndex,
                isTime: faceIndex === 3
            };
            this.groups.sphere.add(circleLine);
            tetData.meshes.push(circleLine);
            this.portApertureData.allMeshes.push(circleLine);

            // Also create a subtle filled disc to show the port area
            const discGeo = new THREE.CircleGeometry(circleRadius * 0.95, numSegments);
            const discMat = new THREE.MeshBasicMaterial({
                color: color,
                transparent: true,
                opacity: discOpacity,
                side: THREE.DoubleSide,
                depthWrite: false
            });
            const disc = new THREE.Mesh(discGeo, discMat);
            
            // Position and orient the disc
            disc.position.copy(circleCenter);
            disc.lookAt(circleCenter.clone().add(faceData.normal));
            disc.userData = {
                type: 'port-aperture-disc',
                tetId,
                faceIndex,
                isTime: faceIndex === 3
            };
            this.groups.sphere.add(disc);
            tetData.meshes.push(disc);
            this.portApertureData.allMeshes.push(disc);

            // Store data for highlighting
            tetData.circles.push({
                faceIndex,
                center: portCenter,
                normal: faceData.normal.clone(),
                line: circleLine,
                disc: disc,
                originalColor: color,
                baseOpacity: baseOpacity,
                discOpacity: discOpacity,
                tetId: tetId
            });
        }
    }
    
    /**
     * Create port aperture circles for BOTH tetrahedra
     * Tet A gets bright circles (physical coupling), Tet B gets dimmer (reference)
     * @param {number} tetAColor - Color for Tet A ports
     * @param {number} tetBColor - Color for Tet B ports
     */
    createDualPortApertureCircles(tetAColor, tetBColor) {
        // Clear all existing
        this.clearPortApertureCircles();
        
        // Create Tet A ports (bright - physical coupling)
        this.createPortApertureCircles('A', tetAColor, false, 0.7, 0.1);
        
        // Create Tet B ports (dimmer - reference/stabilization)
        this.createPortApertureCircles('B', tetBColor, false, 0.35, 0.04);
    }
    
    /**
     * Create the King's Chamber glow at the center (0,0,0)
     * This represents the non-linear coupling point between tetrahedra
     * @param {number} color - Base color for the glow
     */
    createKingsChamberGlow(color = 0xffffff) {
        // Remove existing King's Chamber glow if any
        this.clearKingsChamberGlow();
        
        // Create a small glowing sphere at the origin
        const glowGeometry = new THREE.SphereGeometry(0.15, 32, 32);
        const glowMaterial = new THREE.MeshBasicMaterial({
            color: color,
            transparent: true,
            opacity: 0.3,
            depthWrite: false
        });
        this.kingsChamberGlow = new THREE.Mesh(glowGeometry, glowMaterial);
        this.kingsChamberGlow.position.set(0, 0, 0);
        this.kingsChamberGlow.userData = { type: 'kings-chamber-glow' };
        
        // Add an outer glow halo
        const haloGeometry = new THREE.SphereGeometry(0.3, 32, 32);
        const haloMaterial = new THREE.MeshBasicMaterial({
            color: color,
            transparent: true,
            opacity: 0.1,
            depthWrite: false,
            side: THREE.BackSide
        });
        this.kingsChamberHalo = new THREE.Mesh(haloGeometry, haloMaterial);
        this.kingsChamberHalo.position.set(0, 0, 0);
        this.kingsChamberHalo.userData = { type: 'kings-chamber-halo' };
        
        this.containerGroup.add(this.kingsChamberGlow);
        this.containerGroup.add(this.kingsChamberHalo);
    }
    
    /**
     * Clear the King's Chamber glow
     */
    clearKingsChamberGlow() {
        if (this.kingsChamberGlow) {
            this.containerGroup.remove(this.kingsChamberGlow);
            this.kingsChamberGlow.geometry.dispose();
            this.kingsChamberGlow.material.dispose();
            this.kingsChamberGlow = null;
        }
        if (this.kingsChamberHalo) {
            this.containerGroup.remove(this.kingsChamberHalo);
            this.kingsChamberHalo.geometry.dispose();
            this.kingsChamberHalo.material.dispose();
            this.kingsChamberHalo = null;
        }
    }
    
    /**
     * Pulse the King's Chamber glow (for TIME face firing)
     * @param {number} duration - Pulse duration in ms
     * @param {number} color - Pulse color (default white)
     */
    pulseKingsChamber(duration = 800, color = 0xffffff) {
        if (!this.kingsChamberGlow) return;
        
        const startTime = performance.now();
        const originalOpacity = 0.3;
        const maxOpacity = 0.9;
        const originalScale = 1.0;
        const maxScale = 2.0;
        
        const pulseColor = new THREE.Color(color);
        
        const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const t = Math.min(elapsed / duration, 1);
            
            // Ease out for smooth pulse
            const easeOut = 1 - Math.pow(1 - t, 3);
            
            if (t < 0.3) {
                // Expand and brighten
                const expandT = t / 0.3;
                const scale = originalScale + (maxScale - originalScale) * expandT;
                const opacity = originalOpacity + (maxOpacity - originalOpacity) * expandT;
                
                this.kingsChamberGlow.scale.set(scale, scale, scale);
                this.kingsChamberGlow.material.opacity = opacity;
                this.kingsChamberGlow.material.color.copy(pulseColor);
                
                this.kingsChamberHalo.scale.set(scale, scale, scale);
                this.kingsChamberHalo.material.opacity = opacity * 0.5;
            } else {
                // Contract and dim
                const contractT = (t - 0.3) / 0.7;
                const scale = maxScale - (maxScale - originalScale) * contractT;
                const opacity = maxOpacity - (maxOpacity - originalOpacity) * contractT;
                
                this.kingsChamberGlow.scale.set(scale, scale, scale);
                this.kingsChamberGlow.material.opacity = opacity;
                
                this.kingsChamberHalo.scale.set(scale, scale, scale);
                this.kingsChamberHalo.material.opacity = opacity * 0.3;
            }
            
            if (t < 1) {
                requestAnimationFrame(animate);
            } else {
                // Reset to default
                this.kingsChamberGlow.scale.set(1, 1, 1);
                this.kingsChamberGlow.material.opacity = originalOpacity;
                this.kingsChamberHalo.scale.set(1, 1, 1);
                this.kingsChamberHalo.material.opacity = 0.1;
            }
        };
        
        requestAnimationFrame(animate);
    }

    /**
     * Clear all port aperture circles from the sphere
     */
    clearPortApertureCircles() {
        if (this.portApertureData && this.portApertureData.allMeshes) {
            this.portApertureData.allMeshes.forEach(mesh => {
                this.groups.sphere.remove(mesh);
                if (mesh.geometry) mesh.geometry.dispose();
                if (mesh.material) mesh.material.dispose();
            });
        }
        this.portApertureData = null;
    }

    /**
     * Highlight/pulse a specific port aperture circle
     * @param {string} tetId - 'A' or 'B'
     * @param {number} faceIndex - 0-3
     * @param {boolean} highlight - true to highlight, false to reset
     * @param {number} highlightColor - optional highlight color
     */
    highlightPortApertureCircle(tetId, faceIndex, highlight = true, highlightColor = 0xffffff) {
        if (!this.portApertureData) return;
        
        const tetData = tetId === 'A' ? this.portApertureData.tetA : this.portApertureData.tetB;
        if (!tetData || !tetData.circles[faceIndex]) {
            return;
        }

        const circleData = tetData.circles[faceIndex];
        
        if (highlight) {
            circleData.line.material.color.setHex(highlightColor);
            circleData.line.material.opacity = 1.0;
            circleData.disc.material.color.setHex(highlightColor);
            circleData.disc.material.opacity = 0.6;  // Brighter highlight
        } else {
            circleData.line.material.color.setHex(circleData.originalColor);
            circleData.line.material.opacity = circleData.baseOpacity;
            circleData.disc.material.color.setHex(circleData.originalColor);
            circleData.disc.material.opacity = circleData.discOpacity;
        }
    }

    /**
     * Reset all port aperture circles to their default state
     */
    resetPortApertureCircles() {
        if (!this.portApertureData) return;

        ['tetA', 'tetB'].forEach(key => {
            const tetData = this.portApertureData[key];
            if (tetData && tetData.circles) {
                tetData.circles.forEach(circleData => {
                    circleData.line.material.color.setHex(circleData.originalColor);
                    circleData.line.material.opacity = circleData.baseOpacity;
                    circleData.disc.material.color.setHex(circleData.originalColor);
                    circleData.disc.material.opacity = circleData.discOpacity;
                });
            }
        });
    }

    /**
     * Animate a port aperture circle with a pulse effect
     * @param {string} tetId - 'A' or 'B'
     * @param {number} faceIndex - 0-3
     * @param {number} duration - pulse duration in ms
     * @param {number} flashColor - color to flash (default white for Tet A, original for Tet B)
     * @param {Function} onComplete - callback when animation completes
     */
    pulsePortApertureCircle(tetId, faceIndex, duration = 1200, flashColor = null, onComplete = null) {
        if (!this.portApertureData) return;
        
        const tetData = tetId === 'A' ? this.portApertureData.tetA : this.portApertureData.tetB;
        if (!tetData || !tetData.circles[faceIndex]) {
            return;
        }

        const circleData = tetData.circles[faceIndex];
        const originalColor = new THREE.Color(circleData.originalColor);
        // Tet A flashes white (bright), Tet B flashes its own color (softer)
        const targetColor = flashColor ? new THREE.Color(flashColor) : 
                           (tetId === 'A' ? new THREE.Color(0xffffff) : originalColor.clone().multiplyScalar(1.5));
        const startTime = performance.now();

        const pulseDuration = duration * 0.25;  // 25% flash to target
        const fadeDuration = duration * 0.75;   // 75% fade back
        const totalDuration = pulseDuration + fadeDuration;
        
        // Different max opacities for Tet A (bright) vs Tet B (softer)
        const maxLineOpacity = tetId === 'A' ? 1.0 : 0.7;
        const maxDiscOpacity = tetId === 'A' ? 0.7 : 0.3;

        const animatePulse = (currentTime) => {
            const elapsed = currentTime - startTime;

            if (elapsed < pulseDuration) {
                // Phase 1: Flash to target color
                const t = elapsed / pulseDuration;
                circleData.line.material.color.lerpColors(originalColor, targetColor, t);
                circleData.line.material.opacity = circleData.baseOpacity + ((maxLineOpacity - circleData.baseOpacity) * t);
                circleData.disc.material.color.lerpColors(originalColor, targetColor, t);
                circleData.disc.material.opacity = circleData.discOpacity + ((maxDiscOpacity - circleData.discOpacity) * t);
            } else if (elapsed < totalDuration) {
                // Phase 2: Fade back to base color
                const t = (elapsed - pulseDuration) / fadeDuration;
                const easeOut = 1 - Math.pow(1 - t, 3);
                circleData.line.material.color.lerpColors(targetColor, originalColor, easeOut);
                circleData.line.material.opacity = maxLineOpacity - ((maxLineOpacity - circleData.baseOpacity) * easeOut);
                circleData.disc.material.color.lerpColors(targetColor, originalColor, easeOut);
                circleData.disc.material.opacity = maxDiscOpacity - ((maxDiscOpacity - circleData.discOpacity) * easeOut);
            } else {
                // Animation complete
                circleData.line.material.color.copy(originalColor);
                circleData.line.material.opacity = circleData.baseOpacity;
                circleData.disc.material.color.copy(originalColor);
                circleData.disc.material.opacity = circleData.discOpacity;
                if (onComplete) onComplete();
                return;
            }

            requestAnimationFrame(animatePulse);
        };

        requestAnimationFrame(animatePulse);
    }
    
    /**
     * Pulse multiple port aperture circles simultaneously
     * @param {Array} ports - Array of {tetId, faceIndex} objects
     * @param {number} duration - Pulse duration in ms
     * @param {Function} onComplete - Callback when all animations complete
     */
    pulseMultiplePortApertureCircles(ports, duration = 1200, onComplete = null) {
        let completedCount = 0;
        const totalPorts = ports.length;
        
        const checkComplete = () => {
            completedCount++;
            if (completedCount >= totalPorts && onComplete) {
                onComplete();
            }
        };
        
        ports.forEach(port => {
            this.pulsePortApertureCircle(port.tetId, port.faceIndex, duration, null, checkComplete);
        });
    }

    // =========================================================================
    // CAMERA CONTROLS
    // =========================================================================

    _setupControls() {
        const domElement = this.renderer.domElement;

        // Mouse down
        this._boundHandlers.mousedown = (e) => {
            this.isDragging = true;
            this.prevMouse.x = e.clientX;
            this.prevMouse.y = e.clientY;
            // Stop auto-rotation momentum when user interacts
            this.rotationVelocity.x = 0;
            this.rotationVelocity.y = 0;
        };

        // Mouse move
        this._boundHandlers.mousemove = (e) => {
            if (!this.isDragging) return;

            const dx = e.clientX - this.prevMouse.x;
            const dy = e.clientY - this.prevMouse.y;

            if (this.axisLocked) {
                // Locked mode: only Y rotation (spin) around world up axis
                this._applyLockedYRotation(dx * 0.01);
                this.rotationVelocity.y = dx * 0.01;
                this.rotationVelocity.x = 0;
            } else {
                // Free mode: full rotation using Euler angles
                this.containerGroup.rotation.y += dx * 0.01;
                this.containerGroup.rotation.x += dy * 0.01;
                this.rotationVelocity.x = dy * 0.01;
                this.rotationVelocity.y = dx * 0.01;
            }

            this.prevMouse.x = e.clientX;
            this.prevMouse.y = e.clientY;
        };

        // Mouse up
        this._boundHandlers.mouseup = () => {
            this.isDragging = false;
        };

        // Mouse leave
        this._boundHandlers.mouseleave = () => {
            this.isDragging = false;
        };

        // Mouse wheel zoom (passive: false to allow preventDefault)
        this._boundHandlers.wheel = (e) => {
            e.preventDefault();
            const delta = e.deltaY > 0 ? 1.1 : 0.9;
            this.camera.position.multiplyScalar(delta);
            this.camera.position.clampLength(2, 15);
        };

        // Touch support
        this._boundHandlers.touchstart = (e) => {
            if (e.touches.length === 1) {
                this.isDragging = true;
                this.prevMouse.x = e.touches[0].clientX;
                this.prevMouse.y = e.touches[0].clientY;
                this.rotationVelocity.x = 0;
                this.rotationVelocity.y = 0;
            }
        };

        this._boundHandlers.touchmove = (e) => {
            if (!this.isDragging || e.touches.length !== 1) return;
            e.preventDefault();

            const dx = e.touches[0].clientX - this.prevMouse.x;
            const dy = e.touches[0].clientY - this.prevMouse.y;

            if (this.axisLocked) {
                // Locked mode: only Y rotation (spin) around world up axis
                this._applyLockedYRotation(dx * 0.01);
                this.rotationVelocity.y = dx * 0.01;
                this.rotationVelocity.x = 0;
            } else {
                // Free mode: full rotation using Euler angles
                this.containerGroup.rotation.y += dx * 0.01;
                this.containerGroup.rotation.x += dy * 0.01;
                this.rotationVelocity.x = dy * 0.01;
                this.rotationVelocity.y = dx * 0.01;
            }

            this.prevMouse.x = e.touches[0].clientX;
            this.prevMouse.y = e.touches[0].clientY;
        };

        this._boundHandlers.touchend = () => {
            this.isDragging = false;
        };

        // Add event listeners
        domElement.addEventListener('mousedown', this._boundHandlers.mousedown);
        domElement.addEventListener('mousemove', this._boundHandlers.mousemove);
        domElement.addEventListener('mouseup', this._boundHandlers.mouseup);
        domElement.addEventListener('mouseleave', this._boundHandlers.mouseleave);
        domElement.addEventListener('wheel', this._boundHandlers.wheel, { passive: false });
        domElement.addEventListener('touchstart', this._boundHandlers.touchstart, { passive: true });
        domElement.addEventListener('touchmove', this._boundHandlers.touchmove, { passive: false });
        domElement.addEventListener('touchend', this._boundHandlers.touchend, { passive: true });
    }

    _setupResizeHandler() {
        this._boundHandlers.resize = () => {
            const width = this.container.clientWidth;
            const height = this.container.clientHeight;

            if (width === 0 || height === 0) return;

            this.camera.aspect = width / height;
            this.camera.updateProjectionMatrix();
            this.renderer.setSize(width, height);
        };

        window.addEventListener('resize', this._boundHandlers.resize);
    }

    // =========================================================================
    // ANIMATION LOOP
    // =========================================================================

    _startAnimation() {
        const animate = () => {
            this.animationId = requestAnimationFrame(animate);

            // Get delta time for frame-rate independent animation
            const deltaTime = this.clock.getDelta();

            // Apply damping to rotation velocity when not dragging
            if (!this.isDragging) {
                // Apply damping
                this.rotationVelocity.x *= this.dampingFactor;
                this.rotationVelocity.y *= this.dampingFactor;

                if (this.axisLocked) {
                    // Locked mode: only Y rotation (spin)
                    if (Math.abs(this.rotationVelocity.y) > 0.0001) {
                        this._applyLockedYRotation(this.rotationVelocity.y);
                    }

                    // Auto-rotation in locked mode
                    if (this.autoRotate && Math.abs(this.rotationVelocity.y) < 0.001) {
                        this._applyLockedYRotation(this.rotationSpeed * deltaTime);
                    }
                } else {
                    // Free mode: full Euler rotation
                    if (Math.abs(this.rotationVelocity.x) > 0.0001) {
                        this.containerGroup.rotation.x += this.rotationVelocity.x;
                    }
                    if (Math.abs(this.rotationVelocity.y) > 0.0001) {
                        this.containerGroup.rotation.y += this.rotationVelocity.y;
                    }

                    // Auto-rotation when velocity is low
                    if (this.autoRotate &&
                        Math.abs(this.rotationVelocity.x) < 0.001 &&
                        Math.abs(this.rotationVelocity.y) < 0.001) {
                        this.containerGroup.rotation.y += this.rotationSpeed * deltaTime;
                    }
                }
            }

            this.renderer.render(this.scene, this.camera);
        };

        animate();
    }

    stopAnimation() {
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
            this.animationId = null;
        }
    }

    setAutoRotate(enabled) {
        this.autoRotate = enabled;
    }

    setRotationSpeed(speed) {
        // Speed in radians per second
        this.rotationSpeed = speed;
    }

    // =========================================================================
    // AXIS LOCK (TIME FLOOR DOWN)
    // =========================================================================

    /**
     * Lock rotation to Y-axis only, keeping Tet A's TIME floor horizontal at bottom.
     * 
     * Tet A is the "upright" tetrahedron with:
     * - Apex at vertex 111 = (1, 1, 1)
     * - TIME floor (base) at vertices 001, 010, 100
     * 
     * To orient with base flat on the XZ plane (like sitting on a table):
     * - The apex direction (1,1,1) must point straight up (+Y)
     * - Then spinning rotates around the world Y axis like a top
     */
    lockTimeFloor() {
        this.axisLocked = true;

        // Initialize spin angle (could extract from current rotation, but start fresh)
        this._lockedSpinAngle = 0;

        // Apply the correct orientation
        this._updateLockedOrientation();

        this.rotationVelocity.x = 0;
        this.rotationVelocity.y = 0;
    }

    /**
     * Update the container orientation for locked mode.
     * Combines the fixed alignment rotation with the current spin angle.
     */
    _updateLockedOrientation() {
        // Step 1: Create alignment quaternion
        // The apex of Tet A is at (1,1,1). To make the base horizontal (TIME floor flat),
        // we need the apex direction to point straight up (+Y).
        // 
        // Use Three.js setFromUnitVectors to directly compute this rotation.
        const apexDirection = new THREE.Vector3(1, 1, 1).normalize();
        const upDirection = new THREE.Vector3(0, 1, 0);
        const alignQuat = new THREE.Quaternion().setFromUnitVectors(apexDirection, upDirection);

        // Step 2: Create spin quaternion (rotation around WORLD Y axis)
        const spinQuat = new THREE.Quaternion().setFromAxisAngle(
            new THREE.Vector3(0, 1, 0),
            this._lockedSpinAngle
        );

        // Step 3: Combine - first align, then spin in world space
        // Total = spin * align (quaternion multiplication: right operand applied first)
        this.containerGroup.quaternion.copy(alignQuat).premultiply(spinQuat);
    }

    /**
     * Unlock rotation - allow full 3D rotation again
     */
    unlockAxis() {
        this.axisLocked = false;
        this._lockedSpinAngle = 0;
    }

    /**
     * Toggle axis lock state
     * @returns {boolean} New lock state
     */
    toggleAxisLock() {
        if (this.axisLocked) {
            this.unlockAxis();
        } else {
            this.lockTimeFloor();
        }
        return this.axisLocked;
    }

    /**
     * Check if axis is currently locked
     * @returns {boolean}
     */
    isAxisLocked() {
        return this.axisLocked;
    }

    /**
     * Apply Y rotation while maintaining locked alignment.
     * Updates the spin angle and recomputes the full orientation.
     */
    _applyLockedYRotation(deltaY) {
        this._lockedSpinAngle += deltaY;
        this._updateLockedOrientation();
    }

    // =========================================================================
    // CAMERA POSITIONING
    // =========================================================================

    setCameraPosition(x, y, z) {
        this.camera.position.set(x, y, z);
        this.camera.lookAt(0, 0, 0);
    }

    resetCamera() {
        this.camera.position.set(4, 3, 4);
        this.camera.lookAt(0, 0, 0);
        // Also reset container rotation
        this.containerGroup.rotation.set(0, 0, 0);
        this.rotationVelocity.x = 0;
        this.rotationVelocity.y = 0;
    }

    focusOnFace(tetId, faceIndex) {
        const vertices = tetId === 'A' ? this.tetAVertices : this.tetBVertices;
        if (!vertices) return;

        const faceIndices = [
            [0, 1, 2], [0, 2, 3], [0, 3, 1], [1, 3, 2]
        ][faceIndex];

        if (!faceIndices) return;

        const center = new THREE.Vector3();
        faceIndices.forEach(i => center.add(vertices[i]));
        center.divideScalar(3);

        // Normal pointing outward
        const normal = center.clone().normalize().multiplyScalar(5);

        this.camera.position.copy(normal);
        this.camera.lookAt(center);
    }

    // =========================================================================
    // EFFECTS (with delta-time based animations)
    // =========================================================================

    pulseVertex(binary, duration = 500) {
        const mesh = this.vertexMeshes[binary];
        if (!mesh) return;

        const startScale = 1;
        const maxScale = 2;
        const startTime = performance.now();

        const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);

            if (progress >= 1) {
                mesh.scale.set(startScale, startScale, startScale);
                return;
            }

            // Pulse: grow then shrink using sine wave
            const scale = startScale + Math.sin(progress * Math.PI) * (maxScale - startScale);
            mesh.scale.set(scale, scale, scale);

            requestAnimationFrame(animate);
        };

        requestAnimationFrame(animate);
    }

    flashPath(fromBinary, toBinary, color = CONSTANTS.colors.highlight, duration = 300) {
        const line = this.drawPath(fromBinary, toBinary, color);
        if (!line) return;

        const startTime = performance.now();

        const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);

            if (progress >= 1) {
                this.groups.paths.remove(line);
                line.geometry.dispose();
                line.material.dispose();
                return;
            }

            line.material.opacity = 1 - progress;
            requestAnimationFrame(animate);
        };

        requestAnimationFrame(animate);
    }

    // =========================================================================
    // CLEANUP
    // =========================================================================

    dispose() {
        // Stop animation loop
        this.stopAnimation();

        // Remove event listeners
        const domElement = this.renderer.domElement;
        if (this._boundHandlers.mousedown) {
            domElement.removeEventListener('mousedown', this._boundHandlers.mousedown);
        }
        if (this._boundHandlers.mousemove) {
            domElement.removeEventListener('mousemove', this._boundHandlers.mousemove);
        }
        if (this._boundHandlers.mouseup) {
            domElement.removeEventListener('mouseup', this._boundHandlers.mouseup);
        }
        if (this._boundHandlers.mouseleave) {
            domElement.removeEventListener('mouseleave', this._boundHandlers.mouseleave);
        }
        if (this._boundHandlers.wheel) {
            domElement.removeEventListener('wheel', this._boundHandlers.wheel);
        }
        if (this._boundHandlers.touchstart) {
            domElement.removeEventListener('touchstart', this._boundHandlers.touchstart);
        }
        if (this._boundHandlers.touchmove) {
            domElement.removeEventListener('touchmove', this._boundHandlers.touchmove);
        }
        if (this._boundHandlers.touchend) {
            domElement.removeEventListener('touchend', this._boundHandlers.touchend);
        }
        if (this._boundHandlers.resize) {
            window.removeEventListener('resize', this._boundHandlers.resize);
        }

        // Clear bound handlers
        this._boundHandlers = {};

        // Dispose all geometries and materials
        this.scene.traverse(object => {
            if (object.geometry) {
                object.geometry.dispose();
            }
            if (object.material) {
                if (Array.isArray(object.material)) {
                    object.material.forEach(m => m.dispose());
                } else {
                    object.material.dispose();
                }
            }
        });

        // Dispose renderer
        this.renderer.dispose();

        // Remove canvas from DOM
        if (this.renderer.domElement.parentNode) {
            this.renderer.domElement.parentNode.removeChild(this.renderer.domElement);
        }

        // Clear references
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.containerGroup = null;
        this.groups = {};
        this.vertexMeshes = {};
        this.edgeLines = { tetA: [], tetB: [] };
        this.faceMeshes = { tetA: [], tetB: [] };
        this.tetAVertices = null;
        this.tetBVertices = null;
    }

    // =========================================================================
    // UTILITY METHODS
    // =========================================================================

    getVertexPosition(binary) {
        const mesh = this.vertexMeshes[binary];
        return mesh ? mesh.position.clone() : null;
    }

    getVertexScreenPosition(binary) {
        const mesh = this.vertexMeshes[binary];
        if (!mesh) return null;

        // Get world position (accounting for container rotation)
        const worldPos = new THREE.Vector3();
        mesh.getWorldPosition(worldPos);

        // Project to screen
        worldPos.project(this.camera);

        return {
            x: (worldPos.x + 1) / 2 * this.container.clientWidth,
            y: -(worldPos.y - 1) / 2 * this.container.clientHeight
        };
    }

    // Get current rotation state
    getRotation() {
        return this.containerGroup.rotation.clone();
    }

    setRotation(rotation) {
        this.containerGroup.rotation.copy(rotation);
    }

    // Get the container group for external access if needed
    getContainerGroup() {
        return this.containerGroup;
    }
}

// Make available globally
window.MerkabaRenderer = MerkabaRenderer;
