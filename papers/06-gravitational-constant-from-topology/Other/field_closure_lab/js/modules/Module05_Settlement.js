/**
 * =============================================================================
 * Module05_Settlement.js
 * Settlement Sequence Visualization
 * 
 * Demonstrates the interleaved settlement of Tet A and Tet B and their
 * phase balance over time.
 * =============================================================================
 */

class Module05_Settlement extends Module {
    constructor(id, renderer, store, ui) {
        super(id, renderer, store, ui);
        this.name = 'Settlement Sequence';
        this.title = 'Module 05: Settlement Sequence';
    }

    setup() {
        super.setup();

        // Start with both visible but dim
        this.renderer.setTetAOpacity(0.3);
        this.renderer.setTetBOpacity(0.3);

        this.renderer.setAutoRotate(true);
        this.renderer.setRotationSpeed(0.12);  // radians per second

        // Subscribe to active tet changes
        this.subscribe('activeTet', (tet) => {
            this.onTetChange(tet);
        });

        // Subscribe to visit counts for balance updates
        this.subscribe('visitCounts', () => {
            this.updateSettlementInfo();
        });

        this.store.reset();
        this.updateSettlementInfo();
    }

    cleanup() {
        super.cleanup();
        this.renderer.resetTetrahedronOpacity();
    }

    onTetChange(tet) {
        // Highlight active tetrahedron
        if (tet === 'A') {
            this.renderer.setTetAOpacity(0.7);
            this.renderer.setTetBOpacity(0.15);
        } else if (tet === 'B') {
            this.renderer.setTetAOpacity(0.15);
            this.renderer.setTetBOpacity(0.7);
        }

        this.updateSettlementInfo();
    }

    onStep(stepResult) {
        if (!stepResult) return;

        // Highlight vertices of active tetrahedron
        const activeVerts = stepResult.tet === 'A' ?
            CONSTANTS.vertices.tetA : CONSTANTS.vertices.tetB;

        activeVerts.forEach(v => {
            if (v !== stepResult.vertex) {
                const color = stepResult.tet === 'A' ?
                    CONSTANTS.colors.tetA : CONSTANTS.colors.tetB;
                this.renderer.highlightVertex(v, color);
            }
        });

        this.updateSettlementInfo();
    }

    onReset() {
        super.onReset();
        this.renderer.resetTetrahedronOpacity();
        this.updateSettlementInfo();
    }

    updateSettlementInfo() {
        const state = this.store.getAll();
        const balance = this.store.getPhaseBalance();
        const total = state.tetACount + state.tetBCount;

        // Calculate balance deviation from 50%
        const deviation = total > 0 ? Math.abs(balance.tetA - 0.5) * 100 : 0;
        const balanceStatus = deviation < 5 ? 'Balanced' :
            deviation < 10 ? 'Slight imbalance' : 'Imbalanced';

        // Create visit distribution for each tet
        const tetAVisits = CONSTANTS.vertices.tetA.map(v => state.visitCounts[v]);
        const tetBVisits = CONSTANTS.vertices.tetB.map(v => state.visitCounts[v]);

        const html = `
            <div class="info-section mt-md">
                <h3>Phase Balance</h3>
                <div style="display: flex; gap: 20px; margin-bottom: 10px;">
                    <div style="flex: 1;">
                        <p class="color-tet-a" style="font-weight: bold;">Tet A</p>
                        <p style="font-size: 24px; font-weight: bold;" class="color-tet-a">
                            ${(balance.tetA * 100).toFixed(1)}%
                        </p>
                        <p class="text-muted">${state.tetACount} visits</p>
                    </div>
                    <div style="flex: 1;">
                        <p class="color-tet-b" style="font-weight: bold;">Tet B</p>
                        <p style="font-size: 24px; font-weight: bold;" class="color-tet-b">
                            ${(balance.tetB * 100).toFixed(1)}%
                        </p>
                        <p class="text-muted">${state.tetBCount} visits</p>
                    </div>
                </div>
                <div class="progress-bar" style="height: 12px;">
                    <div class="progress-fill" style="width: ${balance.tetA * 100}%; background: var(--tet-a-color);"></div>
                </div>
                <p class="mt-sm text-muted" style="font-size: 11px;">
                    Status: ${balanceStatus} (${deviation.toFixed(1)}% from equilibrium)
                </p>
            </div>
            
            <div class="info-section mt-md">
                <h3>Vertex Distribution</h3>
                <table class="data-table">
                    <thead>
                        <tr>
                            <th colspan="2" class="color-tet-a">Tet A</th>
                            <th colspan="2" class="color-tet-b">Tet B</th>
                        </tr>
                        <tr>
                            <th>Vertex</th>
                            <th>Visits</th>
                            <th>Vertex</th>
                            <th>Visits</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${[0, 1, 2, 3].map(i => `
                            <tr>
                                <td class="color-tet-a">${CONSTANTS.vertices.tetA[i]}</td>
                                <td>${state.visitCounts[CONSTANTS.vertices.tetA[i]]}</td>
                                <td class="color-tet-b">${CONSTANTS.vertices.tetB[i]}</td>
                                <td>${state.visitCounts[CONSTANTS.vertices.tetB[i]]}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
            
            <div class="info-section mt-md">
                <h3>Active Tetrahedron</h3>
                <p style="font-size: 20px; font-weight: bold;" class="${state.activeTet === 'A' ? 'color-tet-a' : 'color-tet-b'}">
                    ${state.activeTet ? `Tet ${state.activeTet}` : '—'}
                </p>
                <p class="text-muted mt-sm" style="font-size: 11px;">
                    Determined by parity: even 1-count = Tet A, odd = Tet B
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
        const html = `
            <div class="info-section mt-md">
                <h3>Parity Rule</h3>
                <div class="formula">
                    Tet = (count of 1s in binary) mod 2
                </div>
                <p class="mt-sm" style="font-size: 12px;">
                    <span class="color-tet-a">Tet A (even parity):</span> 000, 011, 101, 110<br>
                    <span class="color-tet-b">Tet B (odd parity):</span> 001, 010, 100, 111
                </p>
            </div>
        `;
        this.ui.appendInfoContent(html);
    }
}

// Make available globally
window.Module05_Settlement = Module05_Settlement;
