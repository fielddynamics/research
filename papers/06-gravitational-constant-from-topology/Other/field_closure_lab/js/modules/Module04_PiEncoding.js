/**
 * =============================================================================
 * Module04_PiEncoding.js
 * Pi Encoding & Traversal Visualization
 * 
 * Animates the step-by-step traversal of Merkaba vertices driven by pi's
 * base-8 digits. This is the core field closure mechanism.
 * =============================================================================
 */

class Module04_PiEncoding extends Module {
    constructor(id, renderer, store, ui) {
        super(id, renderer, store, ui);
        this.name = 'Pi Encoding';
        this.title = 'Module 04: Pi Encoding & Traversal';
    }

    setup() {
        super.setup();

        // Reset to show both tetrahedra
        this.renderer.setTetAOpacity(0.3);
        this.renderer.setTetBOpacity(0.3);

        // Enable rotation
        this.renderer.setAutoRotate(true);
        this.renderer.setRotationSpeed(0.12);  // radians per second

        // Subscribe to state changes
        this.subscribe('currentVertex', (vertex, prevVertex) => {
            this.onVertexChange(vertex, prevVertex);
        });

        // Reset and prepare for traversal
        this.store.reset();
        this.updateTraversalInfo();
    }

    cleanup() {
        super.cleanup();
        this.renderer.clearPaths();
    }

    onVertexChange(vertex, prevVertex) {
        // This is called by the store subscription when step happens
        this.updateTraversalInfo();
    }

    onStep(stepResult) {
        if (!stepResult) return;

        // Check for orbit completion
        if (stepResult.orbitCompleted) {
            this.ui.notify(`Orbit ${this.store.get('orbitsComplete')} complete!`, 'success');
        }

        // Check for closure
        if (stepResult.isClosure) {
            this.ui.showOverlay(
                'Field Closure!',
                `Position returned to origin (000) at step ${stepResult.step}. ` +
                `Total cumulative sum: ${stepResult.cumSum}`
            );
        }

        this.updateTraversalInfo();
    }

    onReset() {
        super.onReset();
        this.updateTraversalInfo();
    }

    updateTraversalInfo() {
        const state = this.store.getAll();
        const piDigits = CONSTANTS.pi.digits_base8;

        // Show recent history
        const recentHistory = state.history.slice(-10);

        let historyHTML = '';
        if (recentHistory.length > 0) {
            historyHTML = `
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Step</th>
                            <th>Digit</th>
                            <th>Sum</th>
                            <th>Pos</th>
                            <th>Vertex</th>
                            <th>Tet</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${recentHistory.map((h, i) => {
                const isLast = i === recentHistory.length - 1;
                const tetClass = h.tet === 'A' ? 'color-tet-a' : 'color-tet-b';
                return `
                                <tr class="${isLast ? 'highlight' : ''}">
                                    <td>${h.step}</td>
                                    <td>${h.digit}</td>
                                    <td>${h.cumSum}</td>
                                    <td>${h.position}</td>
                                    <td>${h.vertex}</td>
                                    <td class="${tetClass}">${h.tet}</td>
                                </tr>
                            `;
            }).join('')}
                    </tbody>
                </table>
            `;
        } else {
            historyHTML = '<p class="text-muted">Press STEP or PLAY to begin traversal</p>';
        }

        // Show upcoming digits
        const nextDigits = piDigits.slice(state.step, state.step + 5);
        const upcomingHTML = nextDigits.length > 0 ?
            `<p class="text-mono">Next: ${nextDigits.join(', ')}</p>` :
            '<p class="text-muted">End of sequence</p>';

        const html = `
            <div class="info-section mt-md">
                <h3>Traversal History</h3>
                ${historyHTML}
            </div>
            
            <div class="info-section mt-md">
                <h3>Upcoming Digits (Base 8)</h3>
                ${upcomingHTML}
            </div>
            
            <div class="info-section mt-md">
                <h3>Statistics</h3>
                <p>Orbit Progress: ${state.cumSum % 8} / 8</p>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: ${(state.cumSum % 8) / 8 * 100}%"></div>
                </div>
                <p class="mt-sm">Phase Balance:</p>
                <p>Tet A: ${state.tetACount} (${state.tetACount + state.tetBCount > 0 ?
                ((state.tetACount / (state.tetACount + state.tetBCount)) * 100).toFixed(1) : '0'}%)</p>
                <p>Tet B: ${state.tetBCount} (${state.tetACount + state.tetBCount > 0 ?
                ((state.tetBCount / (state.tetACount + state.tetBCount)) * 100).toFixed(1) : '0'}%)</p>
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
                <h3>The Encoding Mechanism</h3>
                <div class="formula">
                    vertex = (cumsum mod 8) in binary
                </div>
                <p class="mt-sm" style="font-size: 12px;">
                    Each pi digit (base 8) is added to the cumulative sum.
                    The sum mod 8 gives the vertex index (0-7), which
                    maps directly to binary coordinates.
                </p>
            </div>
            
            <div class="info-section mt-md">
                <h3>Why Base 8?</h3>
                <ul style="margin-left: 20px; font-size: 12px;">
                    <li>8 vertices = 2³ = 3-bit binary</li>
                    <li>Octal digits (0-7) map directly</li>
                    <li>Matches Merkaba topology</li>
                    <li>BBP algorithm uses base 16 = 2⁴</li>
                </ul>
            </div>
        `;
        this.ui.appendInfoContent(html);
    }
}

// Make available globally
window.Module04_PiEncoding = Module04_PiEncoding;
