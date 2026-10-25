/**
 * =============================================================================
 * Module.js
 * Base class for all visualization modules
 * 
 * Each module provides a specific visualization and educational content.
 * Modules implement the same interface for consistent behavior.
 * =============================================================================
 */

class Module {
    /**
     * Create a new module
     * @param {number} id - Module ID (1-10)
     * @param {MerkabaRenderer} renderer - The 3D renderer instance
     * @param {DataStore} store - The data store instance
     * @param {UIController} ui - The UI controller instance
     */
    constructor(id, renderer, store, ui) {
        this.id = id;
        this.renderer = renderer;
        this.store = store;
        this.ui = ui;

        // Module metadata (override in subclasses)
        this.name = 'Base Module';
        this.title = 'Module';
        this.description = '';

        // Module state
        this.isActive = false;
        this.animationFrameId = null;
        this.subscriptions = [];
    }

    // =========================================================================
    // LIFECYCLE METHODS (Override in subclasses)
    // =========================================================================

    /**
     * Called when module is activated
     * Set up visualizations and event listeners
     */
    activate() {
        this.isActive = true;
        this.setup();
        this.updateInfoPanel();
    }

    /**
     * Called when module is deactivated
     * Clean up visualizations and event listeners
     */
    deactivate() {
        this.isActive = false;
        this.cleanup();

        // Unsubscribe from all store subscriptions
        this.subscriptions.forEach(unsub => unsub());
        this.subscriptions = [];

        // Cancel any pending animations
        if (this.animationFrameId) {
            cancelAnimationFrame(this.animationFrameId);
            this.animationFrameId = null;
        }
    }

    /**
     * Set up module-specific visualizations
     * Override in subclasses
     */
    setup() {
        // Default: reset renderer to standard view
        this.renderer.resetAllVertices();
        this.renderer.resetFaces();
        this.renderer.clearPaths();
        this.renderer.clearTriforce();
        this.renderer.setTetAVisible(true);
        this.renderer.setTetBVisible(true);
        this.renderer.resetTetrahedronOpacity();
        this.renderer.resetCamera();
    }

    /**
     * Clean up module-specific visualizations
     * Override in subclasses
     */
    cleanup() {
        this.renderer.clearPaths();
        this.renderer.clearTriforce();
    }

    /**
     * Called on each simulation step
     * @param {Object} stepResult - Result from dataStore.step()
     */
    onStep(stepResult) {
        // Override in subclasses to handle step updates
    }

    /**
     * Called when simulation is reset
     */
    onReset() {
        // Override in subclasses
        this.setup();
    }

    // =========================================================================
    // INFO PANEL CONTENT
    // =========================================================================

    /**
     * Update the info panel with module-specific content
     */
    updateInfoPanel() {
        const moduleInfo = CONSTANTS.modules[this.id];
        if (moduleInfo) {
            this.ui.updateInfoPanel(moduleInfo);
        }

        // Add additional module-specific content
        this.renderInfoContent();
    }

    /**
     * Render additional info panel content
     * Override in subclasses for custom content
     */
    renderInfoContent() {
        // Default implementation does nothing
        // Subclasses can override to add tables, formulas, etc.
    }

    // =========================================================================
    // STORE SUBSCRIPTIONS
    // =========================================================================

    /**
     * Subscribe to a store key with automatic cleanup
     */
    subscribe(key, callback) {
        const unsub = this.store.subscribe(key, callback);
        this.subscriptions.push(unsub);
        return unsub;
    }

    // =========================================================================
    // ANIMATION HELPERS
    // =========================================================================

    /**
     * Start a module-specific animation loop
     */
    startAnimation(animateFunction) {
        const animate = () => {
            if (!this.isActive) return;
            animateFunction();
            this.animationFrameId = requestAnimationFrame(animate);
        };
        this.animationFrameId = requestAnimationFrame(animate);
    }

    /**
     * Stop the module animation
     */
    stopAnimation() {
        if (this.animationFrameId) {
            cancelAnimationFrame(this.animationFrameId);
            this.animationFrameId = null;
        }
    }

    /**
     * Animate with a delay between frames
     */
    animateWithDelay(frames, delayMs, onComplete) {
        let index = 0;

        const next = () => {
            if (!this.isActive || index >= frames.length) {
                if (onComplete) onComplete();
                return;
            }

            frames[index]();
            index++;
            setTimeout(next, delayMs);
        };

        next();
    }

    // =========================================================================
    // VISUALIZATION HELPERS
    // =========================================================================

    /**
     * Highlight vertices of a specific tetrahedron
     */
    highlightTetVertices(tetId, color) {
        const vertices = tetId === 'A' ? CONSTANTS.vertices.tetA : CONSTANTS.vertices.tetB;
        vertices.forEach(binary => {
            this.renderer.highlightVertex(binary, color);
        });
    }

    /**
     * Show visit distribution as vertex colors
     */
    showVisitDistribution() {
        const visitCounts = this.store.get('visitCounts');
        const maxVisits = Math.max(...Object.values(visitCounts), 1);

        Object.entries(visitCounts).forEach(([binary, count]) => {
            const intensity = count / maxVisits;
            const color = this.interpolateColor(
                CONSTANTS.colors.visited,
                CONSTANTS.colors.highlight,
                intensity
            );
            if (count > 0) {
                this.renderer.highlightVertex(binary, color);
            }
        });
    }

    /**
     * Interpolate between two colors
     */
    interpolateColor(color1, color2, factor) {
        const r1 = (color1 >> 16) & 0xff;
        const g1 = (color1 >> 8) & 0xff;
        const b1 = color1 & 0xff;

        const r2 = (color2 >> 16) & 0xff;
        const g2 = (color2 >> 8) & 0xff;
        const b2 = color2 & 0xff;

        const r = Math.round(r1 + (r2 - r1) * factor);
        const g = Math.round(g1 + (g2 - g1) * factor);
        const b = Math.round(b1 + (b2 - b1) * factor);

        return (r << 16) | (g << 8) | b;
    }

    /**
     * Format a number for display
     */
    formatNumber(num, decimals = 2) {
        if (Math.abs(num) >= 1e6 || (Math.abs(num) < 1e-3 && num !== 0)) {
            return num.toExponential(decimals);
        }
        return num.toFixed(decimals);
    }

    /**
     * Format scientific notation with proper display
     */
    formatScientific(num, decimals = 2) {
        if (num === 0) return '0';
        const exp = Math.floor(Math.log10(Math.abs(num)));
        const mantissa = num / Math.pow(10, exp);
        return `${mantissa.toFixed(decimals)} × 10<sup>${exp}</sup>`;
    }
}

// Make available globally
window.Module = Module;
