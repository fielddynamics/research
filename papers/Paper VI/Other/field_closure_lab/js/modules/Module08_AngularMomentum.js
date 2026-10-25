/**
 * =============================================================================
 * Module08_AngularMomentum.js
 * Angular Momentum & Chirality Visualization
 * 
 * Explains why the electron vortexes right-handed due to pi's positive
 * digits and relates it to angular momentum quantization.
 * =============================================================================
 */

class Module08_AngularMomentum extends Module {
    constructor(id, renderer, store, ui) {
        super(id, renderer, store, ui);
        this.name = 'Angular Momentum';
        this.title = 'Module 08: Angular Momentum & Chirality';

        this.rotationIndicator = null;
    }

    setup() {
        super.setup();

        this.renderer.setTetAOpacity(0.4);
        this.renderer.setTetBOpacity(0.4);

        // Faster rotation to show chirality
        this.renderer.setAutoRotate(true);
        this.renderer.setRotationSpeed(0.30);  // radians per second (fast for angular momentum visualization)

        this.subscribe('cumSum', () => {
            this.updateAngularMomentumInfo();
        });

        this.store.reset();
        this.updateAngularMomentumInfo();
    }

    cleanup() {
        super.cleanup();
    }

    onStep(stepResult) {
        if (!stepResult) return;
        this.updateAngularMomentumInfo();
    }

    onReset() {
        super.onReset();
        this.updateAngularMomentumInfo();
    }

    updateAngularMomentumInfo() {
        const state = this.store.getAll();
        const physics = CONSTANTS.physics;
        const derived = CONSTANTS.derived;

        // Calculate accumulated angular momentum
        const portsActivated = state.step;
        const L_accumulated = portsActivated * derived.L_port;
        const L_spin = physics.hbar / 2;  // Electron spin
        const spins_accumulated = L_accumulated / L_spin;

        // Chirality analysis
        const piDigits = CONSTANTS.pi.digits_base8.slice(0, Math.max(state.step, 20));
        const forwardCount = piDigits.filter(d => d > 0).length;
        const zeroCount = piDigits.filter(d => d === 0).length;

        const html = `
            <div class="info-section mt-md">
                <h3>Why Right-Handed?</h3>
                <div class="insight-box">
                    <p style="font-size: 13px; font-weight: bold;">
                        Pi is positive-definite.
                    </p>
                    <p style="font-size: 12px; margin-top: 8px;">
                        Every digit of pi (in any base) is non-negative.
                        The cumulative sum can only increase or stay the same,
                        never decrease. This creates unidirectional rotation.
                    </p>
                </div>
            </div>
            
            <div class="info-section mt-md">
                <h3>Chirality Analysis</h3>
                <table class="data-table">
                    <thead>
                        <tr><th>Statistic</th><th>Value</th></tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Digits analyzed</td>
                            <td>${piDigits.length}</td>
                        </tr>
                        <tr>
                            <td>Forward moves (d > 0)</td>
                            <td style="color: var(--accent-success);">${forwardCount} (${(forwardCount / piDigits.length * 100).toFixed(1)}%)</td>
                        </tr>
                        <tr>
                            <td>Stationary (d = 0)</td>
                            <td>${zeroCount} (${(zeroCount / piDigits.length * 100).toFixed(1)}%)</td>
                        </tr>
                        <tr>
                            <td>Backward moves</td>
                            <td style="color: var(--accent-error);">0 (impossible)</td>
                        </tr>
                    </tbody>
                </table>
                <p class="mt-sm text-muted" style="font-size: 11px;">
                    100% forward bias → right-handed helicity
                </p>
            </div>
            
            <div class="info-section mt-md">
                <h3>Angular Momentum Quantization</h3>
                <table class="data-table">
                    <thead>
                        <tr><th>Quantity</th><th>Value</th></tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>L per port (ℏ/4)</td>
                            <td>${derived.L_port.toExponential(2)} J·s</td>
                        </tr>
                        <tr>
                            <td>L per orbit (2ℏ)</td>
                            <td>${(physics.hbar * 2).toExponential(2)} J·s</td>
                        </tr>
                        <tr>
                            <td>Electron spin (ℏ/2)</td>
                            <td>${L_spin.toExponential(2)} J·s</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            
            <div class="info-section mt-md">
                <h3>Spin-1/2 Emergence</h3>
                <div class="formula">
                    L<sub>port</sub> / L<sub>spin</sub> = (ℏ/4) / (ℏ/2) = 0.5
                </div>
                <p class="mt-sm" style="font-size: 12px;">
                    Each port activation contributes <strong>half</strong> a spin quantum.
                    The electron samples one tetrahedron's worth of the Merkaba,
                    giving rise to its spin-1/2 nature.
                </p>
            </div>
            
            <div class="info-section mt-md">
                <h3>Current Accumulation</h3>
                <p>Steps: ${state.step}</p>
                <p>Accumulated L: ${L_accumulated.toExponential(2)} J·s</p>
                <p>Equivalent spins: ${spins_accumulated.toFixed(2)}</p>
                <div class="progress-bar mt-sm">
                    <div class="progress-fill" style="width: ${Math.min((spins_accumulated % 1) * 100, 100)}%;"></div>
                </div>
                <p class="text-muted" style="font-size: 11px;">Progress to next full spin</p>
            </div>
            
            <div class="info-section mt-md">
                <h3>Cosmological Implication</h3>
                <p style="font-size: 12px;">
                    The universe's handedness is encoded in the positivity of pi.
                    Matter-antimatter asymmetry may trace to this fundamental chirality.
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
        // Main content is in updateAngularMomentumInfo
    }
}

// Make available globally
window.Module08_AngularMomentum = Module08_AngularMomentum;
