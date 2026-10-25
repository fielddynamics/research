/**
 * =============================================================================
 * Module06_TileFrequency.js
 * Tile Size & Frequency Visualization
 * 
 * Shows the derivation of the electron tile size (r_e) and the resulting
 * 10^23 Hz settlement frequency.
 * =============================================================================
 */

class Module06_TileFrequency extends Module {
    constructor(id, renderer, store, ui) {
        super(id, renderer, store, ui);
        this.name = 'Tile Size & Frequency';
        this.title = 'Module 06: Tile Size & Frequency';
    }

    setup() {
        super.setup();

        // Standard Merkaba view
        this.renderer.setTetAOpacity(0.3);
        this.renderer.setTetBOpacity(0.3);

        this.renderer.setAutoRotate(true);
        this.renderer.setRotationSpeed(0.12);  // radians per second

        // Show scale visualization
        this.updateScaleInfo();
    }

    cleanup() {
        super.cleanup();
    }

    updateScaleInfo() {
        const physics = CONSTANTS.physics;
        const derived = CONSTANTS.derived;

        const html = `
            <div class="info-section mt-md">
                <h3>Fundamental Scales</h3>
                <table class="data-table">
                    <thead>
                        <tr><th>Parameter</th><th>Value</th><th>Units</th></tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Electron radius (r<sub>e</sub>)</td>
                            <td>2.818 × 10<sup>-15</sup></td>
                            <td>m</td>
                        </tr>
                        <tr>
                            <td>Planck length (l<sub>P</sub>)</td>
                            <td>1.616 × 10<sup>-35</sup></td>
                            <td>m</td>
                        </tr>
                        <tr>
                            <td>Scale ratio (r<sub>e</sub>/l<sub>P</sub>)</td>
                            <td>1.74 × 10<sup>20</sup></td>
                            <td>—</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            
            <div class="info-section mt-md">
                <h3>Settlement Frequency</h3>
                <div class="formula">
                    f = c / r<sub>e</sub> = 1.064 × 10<sup>23</sup> Hz
                </div>
                <p class="mt-sm" style="font-size: 12px;">
                    The field settles 100 sextillion times per second at the electron tile scale.
                </p>
                
                <table class="data-table mt-md">
                    <thead>
                        <tr><th>Frequency</th><th>Value</th><th>Meaning</th></tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>f<sub>settlement</sub></td>
                            <td>1.064 × 10<sup>23</sup> Hz</td>
                            <td>Full cycle rate</td>
                        </tr>
                        <tr>
                            <td>f<sub>port</sub></td>
                            <td>2.66 × 10<sup>22</sup> Hz</td>
                            <td>Per-port rate (f/k)</td>
                        </tr>
                        <tr>
                            <td>T<sub>settlement</sub></td>
                            <td>9.4 × 10<sup>-24</sup> s</td>
                            <td>Cycle period</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            
            <div class="info-section mt-md">
                <h3>Why Electron Scale?</h3>
                <div class="insight-box">
                    <p style="font-size: 12px;">
                        The electron radius is the <strong>Goldilocks scale</strong>:
                    </p>
                    <ul style="font-size: 11px; margin-left: 15px; margin-top: 8px;">
                        <li>Large enough for c-speed settlement in finite time</li>
                        <li>Small enough for quantum coherence</li>
                        <li>Matches MOND crossover at field boundaries</li>
                        <li>Provides fractal floor - no infinite recursion</li>
                    </ul>
                </div>
            </div>
            
            <div class="info-section mt-md">
                <h3>Energy per Settlement</h3>
                <div class="formula">
                    E = h × f = 7.05 × 10<sup>-11</sup> J
                </div>
                <p class="mt-sm" style="font-size: 12px;">
                    Each settlement cycle processes this quantum of energy.
                </p>
            </div>
            
            <div class="info-section mt-md">
                <h3>The Two Routes to r<sub>e</sub></h3>
                <p style="font-size: 12px;"><strong>Route 1: Top-down</strong></p>
                <p style="font-size: 11px;" class="text-muted">
                    From Hubble constant and electron charge via the mass formula
                </p>
                <p style="font-size: 12px; margin-top: 8px;"><strong>Route 2: Bottom-up</strong></p>
                <p style="font-size: 11px;" class="text-muted">
                    From k=4 tetrahedral topology meeting MOND acceleration
                </p>
                <p style="font-size: 12px; margin-top: 8px;">
                    <strong>Both routes converge on the same value: 2.818 fm</strong>
                </p>
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
        // Main content is in updateScaleInfo
    }
}

// Make available globally
window.Module06_TileFrequency = Module06_TileFrequency;
