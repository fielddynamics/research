/**
 * =============================================================================
 * Module01_Geometry.js
 * Field Geometry Visualization
 * 
 * Shows the Merkaba structure with two interpenetrating tetrahedra
 * and 8 binary-encoded vertices.
 * =============================================================================
 */

class Module01_Geometry extends Module {
    constructor(id, renderer, store, ui) {
        super(id, renderer, store, ui);
        this.name = 'Field Geometry';
        this.title = 'Module 01: Field Geometry';

        // Animation state
        this.highlightPhase = 0;
        this.showingTetA = true;
    }

    setup() {
        super.setup();

        // Show both tetrahedra clearly
        this.renderer.setTetAOpacity(0.4);
        this.renderer.setTetBOpacity(0.4);

        // Enable auto-rotation for good viewing
        this.renderer.setAutoRotate(true);
        this.renderer.setRotationSpeed(0.18);  // radians per second

        // Start vertex highlight animation
        this.startVertexAnimation();
    }

    cleanup() {
        super.cleanup();
        this.stopAnimation();
    }

    startVertexAnimation() {
        const vertices = Object.keys(CONSTANTS.vertices.encoding);
        let index = 0;

        const animate = () => {
            if (!this.isActive) return;

            // Reset previous vertex
            const prevIndex = (index - 1 + vertices.length) % vertices.length;
            this.renderer.unhighlightVertex(vertices[prevIndex]);

            // Highlight current vertex
            const binary = vertices[index];
            const data = CONSTANTS.vertices.encoding[binary];
            const color = data.tet === 'A' ? CONSTANTS.colors.tetA : CONSTANTS.colors.tetB;
            this.renderer.highlightVertex(binary, color);
            this.renderer.pulseVertex(binary, 400);

            // Update info display
            this.updateVertexInfo(binary, data);

            index = (index + 1) % vertices.length;

            // Continue animation
            setTimeout(() => {
                if (this.isActive) {
                    requestAnimationFrame(animate);
                }
            }, 1500);
        };

        animate();
    }

    updateVertexInfo(binary, data) {
        // Create dynamic content showing current vertex
        const direction = CONSTANTS.vertices.labels[binary];
        const tetColor = data.tet === 'A' ? 'color-tet-a' : 'color-tet-b';

        // Update a portion of the info panel
        const additionalInfo = `
            <div class="info-section mt-md">
                <h3>Current Vertex</h3>
                <div class="binary-display">${binary.split('').map((b, i) =>
            `<span class="${b === '1' ? 'bit-1' : 'bit-0'}">${b}</span>`
        ).join('')}</div>
                <p class="mt-sm">Position: <span class="${tetColor}">${direction}</span></p>
                <p>Tetrahedron: <span class="${tetColor}">Tet ${data.tet}</span></p>
                <p>Coordinates: (${data.x > 0 ? '+' : ''}${data.x}, ${data.y > 0 ? '+' : ''}${data.y}, ${data.z > 0 ? '+' : ''}${data.z})</p>
            </div>
        `;

        // Find or create the dynamic content area
        let dynamicArea = document.getElementById('module-dynamic-content');
        if (!dynamicArea) {
            dynamicArea = document.createElement('div');
            dynamicArea.id = 'module-dynamic-content';
            document.getElementById('info-content').appendChild(dynamicArea);
        }
        dynamicArea.innerHTML = additionalInfo;
    }

    renderInfoContent() {
        // Add vertex encoding table
        const tableHTML = this.createVertexTable();
        this.ui.appendInfoContent(tableHTML);
    }

    createVertexTable() {
        return `
            <div class="info-section mt-md">
                <h3>Vertex Encoding</h3>
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Binary</th>
                            <th>X</th>
                            <th>Y</th>
                            <th>Z</th>
                            <th>Tet</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${CONSTANTS.vertices.tetA.map(b => this.createVertexRow(b, 'A')).join('')}
                        ${CONSTANTS.vertices.tetB.map(b => this.createVertexRow(b, 'B')).join('')}
                    </tbody>
                </table>
                <p class="mt-sm text-muted" style="font-size: 11px;">
                    Tet A = even parity (even number of 1s)<br>
                    Tet B = odd parity (odd number of 1s)
                </p>
            </div>
        `;
    }

    createVertexRow(binary, tet) {
        const data = CONSTANTS.vertices.encoding[binary];
        const colorClass = tet === 'A' ? 'color-tet-a' : 'color-tet-b';
        return `
            <tr>
                <td><span class="${colorClass}">${binary}</span></td>
                <td>${data.x > 0 ? '+' : ''}${data.x}</td>
                <td>${data.y > 0 ? '+' : ''}${data.y}</td>
                <td>${data.z > 0 ? '+' : ''}${data.z}</td>
                <td><span class="${colorClass}">${tet}</span></td>
            </tr>
        `;
    }

    onStep(stepResult) {
        // Highlight the vertex from the step
        this.renderer.highlightVertex(stepResult.vertex, CONSTANTS.colors.current);
    }

    onReset() {
        super.onReset();
        this.startVertexAnimation();
    }
}

// Make available globally
window.Module01_Geometry = Module01_Geometry;
