/**
 * =============================================================================
 * app.js
 * Main application controller for the Field Closure Engine Lab
 * 
 * Initializes all components and coordinates module switching.
 * =============================================================================
 */

class FieldClosureLab {
    constructor() {
        this.renderer = null;
        this.store = null;
        this.ui = null;
        this.modules = {};
        this.activeModule = null;

        // Guard against recursive module changes
        this._isChangingModule = false;

        // Bind methods
        this.onStep = this.onStep.bind(this);
        this.onReset = this.onReset.bind(this);
        this.onModuleChange = this.onModuleChange.bind(this);
    }

    // =========================================================================
    // INITIALIZATION
    // =========================================================================

    async init() {
        console.log('Field Closure Engine Lab: Initializing...');

        try {
            // Get container element
            const container = document.getElementById('canvas-container');
            if (!container) {
                throw new Error('Canvas container not found');
            }

            // Initialize core components
            this.store = window.dataStore;
            this.renderer = new MerkabaRenderer(container).init();
            this.ui = window.uiController.init();

            // Register all modules
            this.registerModules();

            // Set up UI callbacks
            this.ui.onModuleChange = this.onModuleChange;
            this.ui.onStep = this.onStep;
            this.ui.onReset = this.onReset;

            // Set up viewport controls
            this.setupViewportControls();

            // Activate first module
            this.onModuleChange(1);

            // Hide loading screen
            setTimeout(() => {
                this.ui.hideLoading();
            }, 500);

            console.log('Field Closure Engine Lab: Initialized successfully');

        } catch (error) {
            console.error('Failed to initialize:', error);
            this.showError('Failed to initialize the application. Please refresh the page.');
        }
    }

    // =========================================================================
    // VIEWPORT CONTROLS
    // =========================================================================

    setupViewportControls() {
        const axisLockBtn = document.getElementById('btn-axis-lock');
        const btnLabel = axisLockBtn ? axisLockBtn.querySelector('.btn-label') : null;

        const updateButtonState = (isLocked) => {
            if (!axisLockBtn) return;
            if (isLocked) {
                axisLockBtn.classList.add('active');
                if (btnLabel) btnLabel.textContent = 'Locked';
                axisLockBtn.title = 'Unlock rotation (allow full 3D rotation)';
            } else {
                axisLockBtn.classList.remove('active');
                if (btnLabel) btnLabel.textContent = 'Free';
                axisLockBtn.title = 'Lock Time Floor to Bottom (spin only)';
            }
        };

        const toggleAxisLock = () => {
            const isLocked = this.renderer.toggleAxisLock();
            updateButtonState(isLocked);
            return isLocked;
        };

        // Button click handler
        if (axisLockBtn) {
            axisLockBtn.addEventListener('click', toggleAxisLock);
        }

        // Keyboard shortcut handler (L key)
        this.ui.onAxisLockToggle = toggleAxisLock;
    }

    // =========================================================================
    // MODULE REGISTRATION
    // =========================================================================

    registerModules() {
        // Register all 10 modules
        this.modules = {
            1: new Module01_Geometry(1, this.renderer, this.store, this.ui),
            2: new Module02_PortSystem(2, this.renderer, this.store, this.ui),
            3: new Module03_Triforce(3, this.renderer, this.store, this.ui),
            4: new Module04_PiEncoding(4, this.renderer, this.store, this.ui),
            5: new Module05_Settlement(5, this.renderer, this.store, this.ui),
            6: new Module06_TileFrequency(6, this.renderer, this.store, this.ui),
            7: new Module07_PortAperture(7, this.renderer, this.store, this.ui),
            8: new Module08_AngularMomentum(8, this.renderer, this.store, this.ui),
            9: new Module09_Information(9, this.renderer, this.store, this.ui),
            10: new Module10_CompleteEngine(10, this.renderer, this.store, this.ui),
        };
    }

    // =========================================================================
    // MODULE SWITCHING
    // =========================================================================

    onModuleChange(moduleId) {
        // Guard against recursive calls (UIController.selectModule calls this callback)
        if (this._isChangingModule) return;
        this._isChangingModule = true;

        console.log(`Switching to module ${moduleId}`);

        try {
            // Deactivate current module
            if (this.activeModule) {
                this.activeModule.deactivate();
            }

            // Stop any playing animation
            this.ui.stopPlay();

            // Get new module
            const newModule = this.modules[moduleId];
            if (!newModule) {
                console.error(`Module ${moduleId} not found`);
                return;
            }

            // Activate new module
            this.activeModule = newModule;
            this.activeModule.activate();

            // Update UI (this will call onModuleChange again, but guard prevents recursion)
            this.ui.selectModule(moduleId);
        } finally {
            this._isChangingModule = false;
        }
    }

    // =========================================================================
    // SIMULATION CONTROL
    // =========================================================================

    onStep() {
        const result = this.store.step();

        if (!result) {
            // End of sequence
            this.ui.showOverlay(
                'Sequence Complete',
                `Processed ${this.store.get('step')} pi digits, completing ${this.store.get('orbitsComplete')} orbits.`
            );
            return false;
        }

        // Update renderer
        this.updateVisualization(result);

        // Notify active module
        if (this.activeModule) {
            this.activeModule.onStep(result);
        }

        // Check for special events
        if (result.isClosure) {
            this.onClosure(result);
        }

        if (result.orbitCompleted) {
            this.onOrbitComplete(result);
        }

        return true;
    }

    onReset() {
        // Reset store
        this.store.reset();

        // Reset renderer
        this.renderer.resetAllVertices();
        this.renderer.clearPaths();

        // Notify active module
        if (this.activeModule) {
            this.activeModule.onReset();
        }

        // Update UI metrics
        this.ui.updateAllMetrics(this.store.getAll());
    }

    // =========================================================================
    // VISUALIZATION UPDATES
    // =========================================================================

    updateVisualization(stepResult) {
        const { vertex, previousVertex, tet } = stepResult;

        // Unhighlight previous vertex
        if (previousVertex) {
            this.renderer.unhighlightVertex(previousVertex);
            this.renderer.setVertexVisited(previousVertex);
        }

        // Highlight current vertex
        this.renderer.highlightVertex(vertex, CONSTANTS.colors.current);

        // Draw path from previous to current
        if (previousVertex && previousVertex !== vertex) {
            const pathColor = tet === 'A' ? CONSTANTS.colors.tetA : CONSTANTS.colors.tetB;
            this.renderer.drawPath(previousVertex, vertex, pathColor);
        }

        // Pulse effect on current vertex
        this.renderer.pulseVertex(vertex);
    }

    // =========================================================================
    // SPECIAL EVENTS
    // =========================================================================

    onClosure(result) {
        console.log(`Closure at step ${result.step}, cumsum ${result.cumSum}`);

        // Brief pause and highlight
        this.ui.notify('Field Closure!', 'success', 2000);
    }

    onOrbitComplete(result) {
        const orbits = this.store.get('orbitsComplete');
        console.log(`Orbit ${orbits} complete at step ${result.step}`);

        // Every 8 orbits (Merkaba cycle), show special message
        if (orbits % 8 === 0 && orbits > 0) {
            this.ui.notify(`Merkaba cycle ${orbits / 8} complete!`, 'info', 2000);
        }
    }

    // =========================================================================
    // ERROR HANDLING
    // =========================================================================

    showError(message) {
        const overlay = document.getElementById('explanation-overlay');
        if (overlay) {
            document.getElementById('explanation-title').textContent = 'Error';
            document.getElementById('explanation-text').textContent = message;
            overlay.classList.remove('hidden');
        }
    }
}

// =========================================================================
// APPLICATION STARTUP
// =========================================================================

// Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', () => {
    // Create and initialize the application
    const app = new FieldClosureLab();
    app.init();

    // Make app globally accessible for debugging
    window.app = app;
});
