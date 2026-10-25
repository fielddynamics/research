/**
 * =============================================================================
 * Module03_Triforce.js
 * Triforce Interface Visualization
 * 
 * Shows how each tetrahedral face subdivides into 4 triangles 
 * (Triforce pattern) for vertex sampling.
 * 
 * KEY CONCEPT: Each face of a tetrahedron has 3 vertices (corners)
 * and is OPPOSITE to the 4th vertex. The Triforce corners sample
 * the 3 face vertices, while the center (heart) points to the opposite.
 * =============================================================================
 */

class Module03_Triforce extends Module {
    constructor(id, renderer, store, ui) {
        super(id, renderer, store, ui);
        this.name = 'Triforce Interface';
        this.title = 'Module 03: Triforce Interface';

        this.currentTet = 'A';
        this.currentFaceIndex = 0;
        this.currentSubTriIndex = 0;
        this.animationTimer = null;
        this.subTriTimer = null;
        this.pulseAnimationId = null;
        
        // Custom colors for this module
        this.tetAColor = 0x4488ff;  // Blue
        this.tetBColor = 0xffcc00;  // Gold
    }

    setup() {
        super.setup();

        // Hide vertex markers for cleaner Triforce view
        this.renderer.hideVertexMarkers();
        
        // Set custom tetrahedron colors: Blue and Gold
        this.renderer.setTetAColor(this.tetAColor);
        this.renderer.setTetBColor(this.tetBColor);

        // Show Tet A prominently, dim Tet B
        this.renderer.setTetAOpacity(0.25);
        this.renderer.setTetBOpacity(0.08);

        // Slower rotation for detail viewing
        this.renderer.setAutoRotate(true);
        this.renderer.setRotationSpeed(0.04);

        // Start with first face of Tet A
        this.currentTet = 'A';
        this.currentFaceIndex = 0;
        this.currentSubTriIndex = 0;
        
        // Show initial face with triforce
        this.showCurrentFace();
        
        // Start sub-triangle animation
        this.startSubTriAnimation();
    }

    cleanup() {
        super.cleanup();
        
        // Cancel any running pulse animation
        if (this.pulseAnimationId) {
            cancelAnimationFrame(this.pulseAnimationId);
            this.pulseAnimationId = null;
        }
        
        this.renderer.clearTriforce();
        
        // Restore vertex markers for other modules
        this.renderer.showVertexMarkers();
        this.renderer.resetAllVertices();
        
        // Restore default tetrahedron colors
        this.renderer.resetTetrahedronColors();
        
        if (this.animationTimer) {
            clearTimeout(this.animationTimer);
            this.animationTimer = null;
        }
        if (this.subTriTimer) {
            clearTimeout(this.subTriTimer);
            this.subTriTimer = null;
        }
    }

    getCurrentFaceData() {
        const faces = this.currentTet === 'A' 
            ? CONSTANTS.ports.tetA_faces 
            : CONSTANTS.ports.tetB_faces;
        const faceOrder = this.currentTet === 'A'
            ? CONSTANTS.ports.tetA_faceOrder
            : CONSTANTS.ports.tetB_faceOrder;
        
        const faceId = faceOrder[this.currentFaceIndex];
        return { faceId, ...faces[faceId] };
    }

    showCurrentFace() {
        const faceData = this.getCurrentFaceData();
        
        // Clear previous triforce
        this.renderer.clearTriforce();
        
        // Create the Triforce visualization on this face
        // Pass the current tet color for the base sub-triangle colors
        const baseColor = this.currentTet === 'A' ? this.tetAColor : this.tetBColor;
        this.renderer.createTriforceFromVertices(
            faceData.vertices,
            faceData.opposite,
            this.currentTet,
            baseColor
        );
        
        // Reset sub-triangle index
        this.currentSubTriIndex = 0;
        
        // Show initial sub-triangle highlight with pulse
        this.pulseCurrentSubTri();
        
        // Update info panel
        this.updateFaceInfo(faceData);
    }

    /**
     * Pulse the current sub-triangle: flash white then fade back to base color
     */
    pulseCurrentSubTri() {
        const faceData = this.getCurrentFaceData();
        
        // Reset all sub-triangles first
        this.renderer.resetAllSubTriangles();
        
        // Determine which sub-triangle to pulse
        const subTriOrder = ['corner_0', 'corner_1', 'corner_2', 'center'];
        const currentSubTri = subTriOrder[this.currentSubTriIndex];
        
        // Get the mesh for this sub-triangle
        if (!this.renderer.triforceData || !this.renderer.triforceData.subTriMeshes) {
            return;
        }
        
        const mesh = this.renderer.triforceData.subTriMeshes[currentSubTri];
        if (!mesh) return;
        
        // Store original color
        const baseColor = this.currentTet === 'A' ? this.tetAColor : this.tetBColor;
        const originalColor = new THREE.Color(baseColor);
        const whiteColor = new THREE.Color(0xffffff);
        
        // Start pulse animation
        const startTime = performance.now();
        const pulseDuration = 300;  // Flash to white duration (ms)
        const fadeDuration = 900;   // Fade back duration (ms)
        const totalDuration = pulseDuration + fadeDuration;
        
        const animatePulse = (currentTime) => {
            if (!this.isActive) return;
            
            const elapsed = currentTime - startTime;
            
            if (elapsed < pulseDuration) {
                // Phase 1: Flash to white
                const t = elapsed / pulseDuration;
                mesh.material.color.lerpColors(originalColor, whiteColor, t);
                mesh.material.opacity = 0.3 + (0.7 * t);  // Brighten
            } else if (elapsed < totalDuration) {
                // Phase 2: Fade back to base color
                const t = (elapsed - pulseDuration) / fadeDuration;
                const easeOut = 1 - Math.pow(1 - t, 3);  // Cubic ease-out
                mesh.material.color.lerpColors(whiteColor, originalColor, easeOut);
                mesh.material.opacity = 1.0 - (0.5 * easeOut);  // Dim back down
            } else {
                // Animation complete - stay at highlighted state
                mesh.material.color.copy(originalColor);
                mesh.material.opacity = 0.5;  // Semi-bright for active state
                this.pulseAnimationId = null;
                return;
            }
            
            this.pulseAnimationId = requestAnimationFrame(animatePulse);
        };
        
        // Cancel any existing animation
        if (this.pulseAnimationId) {
            cancelAnimationFrame(this.pulseAnimationId);
        }
        
        this.pulseAnimationId = requestAnimationFrame(animatePulse);
        
        // Update the info panel
        let vertexBinary, label;
        if (this.currentSubTriIndex < 3) {
            vertexBinary = faceData.vertices[this.currentSubTriIndex];
            label = `C${this.currentSubTriIndex + 1}`;
        } else {
            vertexBinary = faceData.opposite;
            label = 'H (Heart)';
        }
        this.updateSubTriInfo(faceData, this.currentSubTriIndex, vertexBinary, label);
    }

    startSubTriAnimation() {
        const animateSubTri = () => {
            if (!this.isActive) return;

            // Move to next sub-triangle
            this.currentSubTriIndex = (this.currentSubTriIndex + 1) % 4;
            
            // After cycling through all 4 sub-triangles, move to next face
            if (this.currentSubTriIndex === 0) {
                this.advanceToNextFace();
            } else {
                this.pulseCurrentSubTri();
            }

            // Schedule next sub-triangle (1.8 seconds per sub-triangle)
            this.subTriTimer = setTimeout(() => {
                if (this.isActive) {
                    requestAnimationFrame(animateSubTri);
                }
            }, 1800);
        };

        // Start after initial delay
        this.subTriTimer = setTimeout(() => {
            if (this.isActive) {
                requestAnimationFrame(animateSubTri);
            }
        }, 1800);
    }

    advanceToNextFace() {
        const faceOrder = this.currentTet === 'A'
            ? CONSTANTS.ports.tetA_faceOrder
            : CONSTANTS.ports.tetB_faceOrder;
        
        this.currentFaceIndex = (this.currentFaceIndex + 1) % faceOrder.length;
        
        // After cycling through all 4 faces, switch tetrahedra
        if (this.currentFaceIndex === 0) {
            this.currentTet = this.currentTet === 'A' ? 'B' : 'A';
            
            // Update tetrahedron visibility and keep colors
            if (this.currentTet === 'A') {
                this.renderer.setTetAOpacity(0.25);
                this.renderer.setTetBOpacity(0.08);
            } else {
                this.renderer.setTetAOpacity(0.08);
                this.renderer.setTetBOpacity(0.25);
            }
        }
        
        this.showCurrentFace();
    }

    updateSubTriInfo(faceData, subTriIndex, vertexBinary, label) {
        const subTriNames = ['Corner 1 (C1)', 'Corner 2 (C2)', 'Corner 3 (C3)', 'Heart (H)'];
        const tetColorHex = this.currentTet === 'A' ? '#4488ff' : '#ffcc00';
        
        const currentName = subTriNames[subTriIndex];
        const vertexLabel = CONSTANTS.vertices.labels[vertexBinary] || vertexBinary;
        
        // Update the active sub-triangle indicator
        const indicator = document.getElementById('active-subtri-indicator');
        if (indicator) {
            indicator.innerHTML = `
                <div style="background: ${tetColorHex}22; border-left: 3px solid ${tetColorHex}; padding: 12px; border-radius: 4px;">
                    <p style="font-size: 14px; font-weight: bold; color: ${tetColorHex}; margin-bottom: 4px;">
                        ${currentName}
                    </p>
                    <p style="font-size: 12px; margin-bottom: 2px;">
                        Samples vertex: <span style="font-family: monospace; color: #fff;">${vertexBinary}</span>
                    </p>
                    <p style="font-size: 11px; color: var(--text-secondary);">
                        ${vertexLabel}
                    </p>
                    ${subTriIndex === 3 ? `
                        <p style="font-size: 11px; color: ${tetColorHex}; margin-top: 6px;">
                            Heart points to opposite vertex for coordination
                        </p>
                    ` : ''}
                </div>
            `;
        }
    }

    updateFaceInfo(faceData) {
        const tetColorHex = this.currentTet === 'A' ? '#4488ff' : '#ffcc00';
        const tetName = this.currentTet === 'A' ? 'Tetrahedron A (Blue)' : 'Tetrahedron B (Gold)';
        
        const html = `
            <div class="info-section mt-md">
                <h3 style="color: ${tetColorHex};">${tetName}</h3>
                <p style="font-size: 14px; font-weight: bold;">${faceData.faceId}</p>
                <p class="mt-sm">Role: <strong>${faceData.role}</strong></p>
            </div>
            
            <div class="info-section mt-md">
                <h3>Active Sub-Triangle</h3>
                <div id="active-subtri-indicator">
                    <!-- Updated by animation -->
                </div>
            </div>
            
            <div class="info-section mt-md">
                <h3>Face Vertices</h3>
                <table class="data-table">
                    <thead>
                        <tr><th>Sub-Tri</th><th>Vertex</th><th>Location</th></tr>
                    </thead>
                    <tbody>
                        ${faceData.vertices.map((v, i) => {
                            const labels = CONSTANTS.vertices.labels[v];
                            return `
                                <tr>
                                    <td style="color: ${tetColorHex};">C${i+1}</td>
                                    <td style="font-family: monospace;">${v}</td>
                                    <td style="font-size: 11px;">${labels}</td>
                                </tr>
                            `;
                        }).join('')}
                        <tr>
                            <td style="color: ${tetColorHex};">H</td>
                            <td style="font-family: monospace;">${faceData.opposite}</td>
                            <td style="font-size: 11px;">${CONSTANTS.vertices.labels[faceData.opposite]}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            
            <div class="info-section mt-md">
                <h3>Triforce Structure</h3>
                <pre style="font-size: 10px; line-height: 1.2; color: var(--text-secondary); text-align: center;">
       /\\
      /  \\
     / C1 \\
    /------\\
   /\\      /\\
  /  \\  H /  \\
 / C2 \\  / C3 \\
/------\\/------\\
                </pre>
                <p style="font-size: 11px; margin-top: 8px; text-align: center;">
                    Sub-triangles pulse white then fade to <span style="color: ${tetColorHex};">${this.currentTet === 'A' ? 'blue' : 'gold'}</span>
                </p>
            </div>
            
            ${faceData.role === 'TIME' ? `
                <div class="insight-box mt-md">
                    <p style="font-size: 12px;">
                        <strong>TIME PORT:</strong> This is the base face of the tetrahedron.
                        The heart (H) points to the apex, enabling temporal coordination 
                        between the interpenetrating tetrahedra.
                    </p>
                </div>
            ` : ''}
        `;

        let dynamicArea = document.getElementById('module-dynamic-content');
        if (!dynamicArea) {
            dynamicArea = document.createElement('div');
            dynamicArea.id = 'module-dynamic-content';
            document.getElementById('info-content').appendChild(dynamicArea);
        }
        dynamicArea.innerHTML = html;
        
        // Immediately show first sub-triangle info
        const subTriNames = ['Corner 1 (C1)', 'Corner 2 (C2)', 'Corner 3 (C3)', 'Heart (H)'];
        this.updateSubTriInfo(faceData, 0, faceData.vertices[0], subTriNames[0]);
    }

    renderInfoContent() {
        const html = `
            <div class="info-section mt-md">
                <h3>About the Triforce</h3>
                <p style="font-size: 12px;">
                    Each tetrahedral face divides into 4 sub-triangles (Triforce pattern).
                    Watch as each sub-triangle pulses white then fades back.
                </p>
                <p style="font-size: 12px; margin-top: 8px;">
                    <span style="color: #4488ff;"><strong>Tet A</strong></span> = Blue &nbsp;|&nbsp;
                    <span style="color: #ffcc00;"><strong>Tet B</strong></span> = Gold
                </p>
                <p style="font-size: 12px; margin-top: 8px;">
                    <strong>C1, C2, C3</strong> = Corner triangles (sample face vertices)<br>
                    <strong>H</strong> = Heart/Center (points to opposite vertex)
                </p>
            </div>
        `;
        this.ui.appendInfoContent(html);
    }
}

// Make available globally
window.Module03_Triforce = Module03_Triforce;
