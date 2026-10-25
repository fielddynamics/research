/**
 * =============================================================================
 * Module02_PortSystem.js
 * The 3+1 Port System Visualization
 * 
 * Shows how each tetrahedron has 4 faces acting as coupling ports:
 * 3 spatial + 1 temporal.
 * =============================================================================
 */

class Module02_PortSystem extends Module {
    constructor(id, renderer, store, ui) {
        super(id, renderer, store, ui);
        this.name = 'Port System (3+1)';
        this.title = 'Module 02: The Port System';

        this.currentFace = 0;
        this.currentTet = 'A';
        this.portTimer = null;
        this.pulseAnimationId = null;
        
        // Custom colors matching Triforce module
        this.tetAColor = 0x4488ff;  // Blue
        this.tetBColor = 0xffcc00;  // Gold
    }

    setup() {
        super.setup();

        // Hide vertex markers for cleaner view
        this.renderer.hideVertexMarkers();
        
        // Set custom tetrahedron colors: Blue and Gold
        this.renderer.setTetAColor(this.tetAColor);
        this.renderer.setTetBColor(this.tetBColor);

        // Show Tet A prominently, dim Tet B
        this.renderer.setTetAOpacity(0.25);
        this.renderer.setTetBOpacity(0.08);

        // Slower rotation for inspection
        this.renderer.setAutoRotate(true);
        this.renderer.setRotationSpeed(0.06);

        // Initialize
        this.currentTet = 'A';
        this.currentFace = 0;

        // Start face highlighting animation
        this.startFaceAnimation();
    }

    cleanup() {
        super.cleanup();
        
        // Cancel any running pulse animation
        if (this.pulseAnimationId) {
            cancelAnimationFrame(this.pulseAnimationId);
            this.pulseAnimationId = null;
        }
        
        if (this.portTimer) {
            clearTimeout(this.portTimer);
            this.portTimer = null;
        }
        
        this.renderer.resetFaces();
        
        // Restore vertex markers for other modules
        this.renderer.showVertexMarkers();
        this.renderer.resetAllVertices();
        
        // Restore default tetrahedron colors
        this.renderer.resetTetrahedronColors();
    }

    startFaceAnimation() {
        // Pulse the first face immediately
        this.pulseCurrentFace();

        const animate = () => {
            if (!this.isActive) return;

            // Advance to next face
            this.currentFace++;
            if (this.currentFace >= 4) {
                this.currentFace = 0;
                // Switch tetrahedra after showing all 4 ports
                this.currentTet = this.currentTet === 'A' ? 'B' : 'A';
                
                // Update tetrahedron visibility
                if (this.currentTet === 'A') {
                    this.renderer.setTetAOpacity(0.25);
                    this.renderer.setTetBOpacity(0.08);
                } else {
                    this.renderer.setTetAOpacity(0.08);
                    this.renderer.setTetBOpacity(0.25);
                }
            }

            this.pulseCurrentFace();

            // Schedule next (1.8 seconds per port, matching Triforce timing)
            this.portTimer = setTimeout(() => {
                if (this.isActive) {
                    requestAnimationFrame(animate);
                }
            }, 1800);
        };

        // Start after initial delay
        this.portTimer = setTimeout(() => {
            if (this.isActive) {
                requestAnimationFrame(animate);
            }
        }, 1800);
    }

    pulseCurrentFace() {
        // Reset all faces
        this.renderer.resetFaces();
        
        // Get the face mesh
        const faceMeshes = this.currentTet === 'A' 
            ? this.renderer.faceMeshes.tetA 
            : this.renderer.faceMeshes.tetB;
        
        const mesh = faceMeshes[this.currentFace];
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
                mesh.material.opacity = 0.2 + (0.8 * t);  // Brighten
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
        
        // Update info panel
        this.updatePortInfo();
    }

    updatePortInfo() {
        const tetColorHex = this.currentTet === 'A' ? '#4488ff' : '#ffcc00';
        const tetName = this.currentTet === 'A' ? 'Tetrahedron A (Blue)' : 'Tetrahedron B (Gold)';
        
        // Determine port type based on face index
        // Face 3 is TIME (base), faces 0-2 are SPATIAL (walls)
        const isTime = this.currentFace === 3;
        const portNames = ['Wall 1 (S1)', 'Wall 2 (S2)', 'Wall 3 (S3)', 'Floor (T)'];
        const portName = portNames[this.currentFace];
        const portType = isTime ? 'TEMPORAL' : 'SPATIAL';

        const html = `
            <div class="info-section mt-md">
                <h3>Active Port</h3>
                <div style="background: ${tetColorHex}22; border-left: 3px solid ${tetColorHex}; padding: 12px; border-radius: 4px;">
                    <p style="font-size: 12px; color: var(--text-secondary); margin-bottom: 4px;">
                        ${tetName}
                    </p>
                    <p style="font-size: 16px; font-weight: bold; color: ${tetColorHex}; margin-bottom: 4px;">
                        ${portName}
                    </p>
                    <p style="font-size: 12px;">
                        Type: <strong>${portType}</strong>
                    </p>
                    ${isTime ? `
                        <p style="font-size: 11px; color: #ffcc00; margin-top: 8px;">
                            The TIME port coordinates settlement across the 3 spatial ports
                        </p>
                    ` : ''}
                </div>
            </div>
            
            <div class="info-section mt-md">
                <h3>3+1 Structure</h3>
                <table class="data-table">
                    <thead>
                        <tr><th>Port</th><th>Type</th><th>Role</th></tr>
                    </thead>
                    <tbody>
                        <tr ${this.currentFace === 0 ? `style="background: ${tetColorHex}22;"` : ''}>
                            <td>Wall 1</td>
                            <td>SPATIAL</td>
                            <td>X-coupling</td>
                        </tr>
                        <tr ${this.currentFace === 1 ? `style="background: ${tetColorHex}22;"` : ''}>
                            <td>Wall 2</td>
                            <td>SPATIAL</td>
                            <td>Y-coupling</td>
                        </tr>
                        <tr ${this.currentFace === 2 ? `style="background: ${tetColorHex}22;"` : ''}>
                            <td>Wall 3</td>
                            <td>SPATIAL</td>
                            <td>Z-coupling</td>
                        </tr>
                        <tr ${this.currentFace === 3 ? `style="background: rgba(255,215,0,0.2);"` : ''}>
                            <td style="color: #FFD700;">Floor</td>
                            <td style="color: #FFD700;">TEMPORAL</td>
                            <td>Coordination</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            
            <div class="info-section mt-md">
                <h3>Settlement Order</h3>
                <div class="formula">
                    S1 → S2 → S3 → T → (next tet)
                </div>
                <p class="mt-sm" style="font-size: 12px;">
                    Spatial walls process first, then TIME floor coordinates and exits to other tetrahedron.
                </p>
            </div>
            
            <div class="info-section mt-md">
                <h3>Tetrahedra</h3>
                <div style="display: flex; gap: 12px;">
                    <div style="padding: 8px 16px; background: ${this.currentTet === 'A' ? 'rgba(68,136,255,0.3)' : 'rgba(68,136,255,0.1)'}; border-radius: 4px; border-left: 3px solid #4488ff;">
                        <span style="color: #4488ff;">●</span> Tet A
                    </div>
                    <div style="padding: 8px 16px; background: ${this.currentTet === 'B' ? 'rgba(255,204,0,0.3)' : 'rgba(255,204,0,0.1)'}; border-radius: 4px; border-left: 3px solid #ffcc00;">
                        <span style="color: #ffcc00;">●</span> Tet B
                    </div>
                </div>
            </div>
        `;

        let dynamicArea = document.getElementById('module-dynamic-content');
        if (!dynamicArea) {
            dynamicArea = document.createElement('div');
            dynamicArea.id = 'module-dynamic-content';
            document.getElementById('info-content').appendChild(dynamicArea);
        }
        dynamicArea.innerHTML = html;
    }

    renderInfoContent() {
        const html = `
            <div class="info-section mt-md">
                <h3>About the 3+1 System</h3>
                <p style="font-size: 12px;">
                    Each tetrahedron has 4 faces that act as coupling ports.
                    Watch as each face pulses white to show the port sequence.
                </p>
                <p style="font-size: 12px; margin-top: 8px;">
                    <span style="color: #4488ff;"><strong>Tet A</strong></span> = Blue &nbsp;|&nbsp;
                    <span style="color: #ffcc00;"><strong>Tet B</strong></span> = Gold
                </p>
            </div>
        `;
        this.ui.appendInfoContent(html);
    }
}

// Make available globally
window.Module02_PortSystem = Module02_PortSystem;
