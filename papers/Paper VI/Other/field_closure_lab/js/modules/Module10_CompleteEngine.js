/**
 * =============================================================================
 * Module10_CompleteEngine.js
 * The Complete Engine Synthesis
 * 
 * Full animated synthesis showing all components working together in the
 * complete 3+1 field closure cycle.
 * =============================================================================
 */

class Module10_CompleteEngine extends Module {
    constructor(id, renderer, store, ui) {
        super(id, renderer, store, ui);
        this.name = 'Complete Engine';
        this.title = 'Module 10: The Complete Engine';

        this.engineState = {
            phase: 'idle',
            cycle: 0,
        };
    }

    setup() {
        super.setup();

        // Full visibility of both tetrahedra
        this.renderer.setTetAOpacity(0.4);
        this.renderer.setTetBOpacity(0.4);

        this.renderer.setAutoRotate(true);
        this.renderer.setRotationSpeed(0.18);  // radians per second

        // Subscribe to all relevant state changes
        this.subscribe('*', (value, oldValue, key) => {
            this.updateEngineDisplay();
        });

        this.store.reset();
        this.updateEngineDisplay();
    }

    cleanup() {
        super.cleanup();
    }

    onStep(stepResult) {
        if (!stepResult) return;

        // Update engine state based on step result
        if (stepResult.orbitCompleted) {
            this.engineState.cycle = stepResult.cumSum / 8;
        }

        this.updateEngineDisplay();
    }

    onReset() {
        super.onReset();
        this.engineState = { phase: 'idle', cycle: 0 };
        this.updateEngineDisplay();
    }

    updateEngineDisplay() {
        const state = this.store.getAll();
        const physics = CONSTANTS.physics;
        const derived = CONSTANTS.derived;

        // Calculate comprehensive statistics
        const balance = this.store.getPhaseBalance();
        const bitsProcessed = state.step * 3;
        const orbits = state.orbitsComplete;
        const orbitProgress = state.cumSum % 8;

        // Calculate equivalent physical time
        const physicalTime = state.step * derived.T_settlement;
        const angularMomentum = state.step * derived.L_port;
        const energy = state.step * derived.E_settlement;

        const html = `
            <div class="info-section">
                <h3 style="color: var(--accent-primary);">Engine Status</h3>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 12px;">
                    <div style="background: rgba(74,175,80,0.1); padding: 12px; border-radius: 8px; border-left: 3px solid var(--tet-a-color);">
                        <p style="font-size: 11px; color: var(--text-muted);">TET A</p>
                        <p style="font-size: 20px; font-weight: bold; color: var(--tet-a-color);">${state.tetACount}</p>
                        <p style="font-size: 11px;">${(balance.tetA * 100).toFixed(1)}%</p>
                    </div>
                    <div style="background: rgba(244,67,54,0.1); padding: 12px; border-radius: 8px; border-left: 3px solid var(--tet-b-color);">
                        <p style="font-size: 11px; color: var(--text-muted);">TET B</p>
                        <p style="font-size: 20px; font-weight: bold; color: var(--tet-b-color);">${state.tetBCount}</p>
                        <p style="font-size: 11px;">${(balance.tetB * 100).toFixed(1)}%</p>
                    </div>
                </div>
            </div>
            
            <div class="info-section mt-md">
                <h3>Cycle Progress</h3>
                <div style="display: flex; align-items: center; gap: 12px;">
                    <div style="flex: 1;">
                        <p style="font-size: 11px; color: var(--text-muted);">Orbit ${orbits + 1}</p>
                        <div class="progress-bar" style="height: 16px;">
                            <div class="progress-fill" style="width: ${(orbitProgress / 8) * 100}%;"></div>
                        </div>
                    </div>
                    <div style="text-align: center; min-width: 60px;">
                        <p style="font-size: 24px; font-weight: bold; color: var(--accent-primary);">${orbitProgress}/8</p>
                    </div>
                </div>
            </div>
            
            <div class="info-section mt-md">
                <h3>Real-Time Metrics</h3>
                <table class="data-table">
                    <tbody>
                        <tr>
                            <td>Current Vertex</td>
                            <td style="font-family: var(--font-mono); font-size: 16px; color: var(--accent-primary);">${state.currentVertex}</td>
                        </tr>
                        <tr>
                            <td>Active Tetrahedron</td>
                            <td class="${state.activeTet === 'A' ? 'color-tet-a' : 'color-tet-b'}" style="font-weight: bold;">
                                ${state.activeTet || '—'}
                            </td>
                        </tr>
                        <tr>
                            <td>Total Steps</td>
                            <td>${state.step}</td>
                        </tr>
                        <tr>
                            <td>Cumulative Sum</td>
                            <td>${state.cumSum}</td>
                        </tr>
                        <tr>
                            <td>Complete Orbits</td>
                            <td>${orbits}</td>
                        </tr>
                        <tr>
                            <td>Closure Events</td>
                            <td>${state.closureEvents.length}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            
            <div class="info-section mt-md">
                <h3>Physical Equivalents</h3>
                <table class="data-table">
                    <tbody>
                        <tr>
                            <td>Equivalent Time</td>
                            <td>${physicalTime.toExponential(2)} s</td>
                        </tr>
                        <tr>
                            <td>Angular Momentum</td>
                            <td>${angularMomentum.toExponential(2)} J·s</td>
                        </tr>
                        <tr>
                            <td>Energy Processed</td>
                            <td>${energy.toExponential(2)} J</td>
                        </tr>
                        <tr>
                            <td>Information</td>
                            <td>${bitsProcessed} bits</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            
            <div class="info-section mt-md">
                <h3>Vertex Visit Distribution</h3>
                <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px;">
                    ${Object.entries(state.visitCounts).map(([v, count]) => {
            const data = CONSTANTS.vertices.encoding[v];
            const colorClass = data.tet === 'A' ? 'color-tet-a' : 'color-tet-b';
            const maxCount = Math.max(...Object.values(state.visitCounts), 1);
            const intensity = count / maxCount;
            return `
                            <div style="text-align: center; padding: 8px; background: rgba(255,255,255,${0.02 + intensity * 0.1}); border-radius: 4px;">
                                <p class="${colorClass}" style="font-size: 12px; font-weight: bold;">${v}</p>
                                <p style="font-size: 16px; font-weight: bold;">${count}</p>
                            </div>
                        `;
        }).join('')}
                </div>
            </div>
            
            <div class="info-section mt-md">
                <h3>System Summary</h3>
                <div class="insight-box">
                    <p style="font-size: 12px;">
                        <strong>The gravity engine cycles through:</strong>
                    </p>
                    <ul style="font-size: 11px; margin-left: 15px; margin-top: 8px;">
                        <li>8 vertices encoding 3D positions</li>
                        <li>2 tetrahedra in phase balance</li>
                        <li>4 ports (3 spatial + 1 temporal)</li>
                        <li>Pi-driven deterministic traversal</li>
                        <li>10<sup>23</sup> Hz settlement frequency</li>
                        <li>3 bits per digit, 24 bits per orbit</li>
                        <li>137 orbits per electron (1/α)</li>
                    </ul>
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
        // Main content is in updateEngineDisplay
    }
}

// Make available globally
window.Module10_CompleteEngine = Module10_CompleteEngine;
