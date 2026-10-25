/**
 * =============================================================================
 * Module09_Information.js
 * Information Content & Resonance Visualization
 * 
 * Calculates information content per cycle (3 bits/digit) and the total
 * bandwidth, plus fast/slow closure resonance conditions.
 * =============================================================================
 */

class Module09_Information extends Module {
    constructor(id, renderer, store, ui) {
        super(id, renderer, store, ui);
        this.name = 'Information Content';
        this.title = 'Module 09: Information & Resonance';
    }

    setup() {
        super.setup();

        this.renderer.setTetAOpacity(0.3);
        this.renderer.setTetBOpacity(0.3);

        this.renderer.setAutoRotate(true);
        this.renderer.setRotationSpeed(0.12);  // radians per second

        this.subscribe('step', () => {
            this.updateInformationInfo();
        });

        this.subscribe('closureEvents', () => {
            this.updateInformationInfo();
        });

        this.store.reset();
        this.updateInformationInfo();
    }

    cleanup() {
        super.cleanup();
    }

    onStep(stepResult) {
        if (!stepResult) return;
        this.updateInformationInfo();
    }

    onReset() {
        super.onReset();
        this.updateInformationInfo();
    }

    updateInformationInfo() {
        const state = this.store.getAll();
        const derived = CONSTANTS.derived;
        const physics = CONSTANTS.physics;

        // Calculate information metrics
        const bitsProcessed = state.step * derived.bits_per_digit;
        const orbitsComplete = state.orbitsComplete;
        const bitsPerOrbit = derived.bits_per_orbit;

        // Bandwidth calculation
        const bandwidth = derived.f_settlement * derived.bits_per_digit;

        // Closure analysis
        const closureEvents = state.closureEvents;
        const avgClosureTime = closureEvents.length > 1 ?
            (closureEvents[closureEvents.length - 1].step - closureEvents[0].step) / (closureEvents.length - 1) :
            null;

        // 137 connection
        const orbitsPerElectron = 137;
        const bitsPerElectron = orbitsPerElectron * bitsPerOrbit;

        const html = `
            <div class="info-section mt-md">
                <h3>Information per Digit</h3>
                <div class="formula">
                    bits = log<sub>2</sub>(8) = 3 bits/digit
                </div>
                <table class="data-table mt-sm">
                    <thead>
                        <tr><th>Scale</th><th>Information</th></tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Per digit</td>
                            <td>3 bits</td>
                        </tr>
                        <tr>
                            <td>Per orbit (8 digits)</td>
                            <td>24 bits</td>
                        </tr>
                        <tr>
                            <td>Per electron (137 orbits)</td>
                            <td>~3,288 bits</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            
            <div class="info-section mt-md">
                <h3>Bandwidth</h3>
                <div class="formula">
                    B = f × 3 = 3.19 × 10<sup>23</sup> bits/s
                </div>
                <p class="mt-sm" style="font-size: 12px;">
                    Each electron tile processes ~320 zettabits per second.
                    This is the field's "computation rate."
                </p>
            </div>
            
            <div class="info-section mt-md">
                <h3>The 137 Connection</h3>
                <div class="insight-box">
                    <table style="width: 100%; font-size: 12px;">
                        <tr>
                            <td>λ<sub>Compton</sub> / r<sub>e</sub></td>
                            <td style="font-weight: bold;">= 861</td>
                        </tr>
                        <tr>
                            <td>861 / 2π</td>
                            <td style="font-weight: bold;">= 137</td>
                        </tr>
                        <tr>
                            <td>1/α</td>
                            <td style="font-weight: bold;">= 137</td>
                        </tr>
                    </table>
                    <p style="margin-top: 8px; font-size: 11px;">
                        The electron contains exactly 137 Merkaba orbits = 1/α
                    </p>
                </div>
            </div>
            
            <div class="info-section mt-md">
                <h3>Current Session</h3>
                <table class="data-table">
                    <tbody>
                        <tr>
                            <td>Steps processed</td>
                            <td>${state.step}</td>
                        </tr>
                        <tr>
                            <td>Bits processed</td>
                            <td>${bitsProcessed}</td>
                        </tr>
                        <tr>
                            <td>Orbits complete</td>
                            <td>${orbitsComplete}</td>
                        </tr>
                        <tr>
                            <td>Closure events</td>
                            <td>${closureEvents.length}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            
            ${closureEvents.length > 0 ? `
            <div class="info-section mt-md">
                <h3>Closure Events</h3>
                <table class="data-table">
                    <thead>
                        <tr><th>Event</th><th>Step</th><th>Cumsum</th><th>Orbits</th></tr>
                    </thead>
                    <tbody>
                        ${closureEvents.slice(-5).map((e, i) => `
                            <tr>
                                <td>${closureEvents.length - 5 + i + 1}</td>
                                <td>${e.step}</td>
                                <td>${e.cumSum}</td>
                                <td>${e.orbits}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
            ` : ''}
            
            <div class="info-section mt-md">
                <h3>Resonance Conditions</h3>
                <p style="font-size: 12px;"><strong>Fast closure:</strong> Quick return to origin</p>
                <p style="font-size: 11px;" class="text-muted">
                    Indicates stable configuration, low radiation
                </p>
                <p style="font-size: 12px; margin-top: 8px;"><strong>Slow closure:</strong> Extended path before return</p>
                <p style="font-size: 11px;" class="text-muted">
                    Higher energy state, potential emission
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
        // Main content is in updateInformationInfo
    }
}

// Make available globally
window.Module09_Information = Module09_Information;
