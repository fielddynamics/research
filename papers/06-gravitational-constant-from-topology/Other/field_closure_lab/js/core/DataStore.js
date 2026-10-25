/**
 * =============================================================================
 * DataStore.js
 * Centralized state management for the Field Closure Engine Lab
 * 
 * Implements a simple observable pattern for state changes.
 * All modules read from and write to this central store.
 * =============================================================================
 */

class DataStore {
    constructor() {
        // Core simulation state
        this.state = {
            // Current step in pi traversal
            step: 0,

            // Current pi digit (base 8)
            currentDigit: null,

            // Cumulative sum of digits
            cumSum: 0,

            // Current vertex position (binary string)
            currentVertex: '000',

            // Previous vertex (for path drawing)
            previousVertex: null,

            // Which tetrahedron is currently active
            activeTet: null,  // 'A' or 'B'

            // Orbits completed
            orbitsComplete: 0,

            // Visit counts per vertex
            visitCounts: {
                '000': 0, '001': 0, '010': 0, '011': 0,
                '100': 0, '101': 0, '110': 0, '111': 0
            },

            // Tet A vs Tet B balance
            tetACount: 0,
            tetBCount: 0,

            // History of all steps
            history: [],

            // Currently active module
            activeModule: 1,

            // Animation state
            isPlaying: false,
            playSpeed: 1.0,

            // Closure events detected
            closureEvents: [],
        };

        // Listeners for state changes
        this.listeners = new Map();

        // Computed values cache
        this._computed = {};
    }

    // =========================================================================
    // STATE ACCESS
    // =========================================================================

    get(key) {
        return this.state[key];
    }

    getAll() {
        return { ...this.state };
    }

    // =========================================================================
    // STATE MUTATION
    // =========================================================================

    set(key, value) {
        const oldValue = this.state[key];
        this.state[key] = value;
        this._notifyListeners(key, value, oldValue);
        this._invalidateComputed();
    }

    update(updates) {
        const changes = [];
        Object.entries(updates).forEach(([key, value]) => {
            const oldValue = this.state[key];
            if (oldValue !== value) {
                this.state[key] = value;
                changes.push({ key, value, oldValue });
            }
        });

        changes.forEach(({ key, value, oldValue }) => {
            this._notifyListeners(key, value, oldValue);
        });

        if (changes.length > 0) {
            this._invalidateComputed();
        }
    }

    // =========================================================================
    // SIMULATION CONTROL
    // =========================================================================

    /**
     * Execute one step of the pi traversal
     * @returns {Object} Step result with all relevant data
     */
    step() {
        const piDigits = CONSTANTS.pi.digits_base8;
        const currentStep = this.state.step;

        if (currentStep >= piDigits.length) {
            return null;  // No more digits
        }

        const digit = piDigits[currentStep];
        const prevSum = this.state.cumSum;
        const newSum = prevSum + digit;
        const newPosition = newSum % 8;
        const newVertex = newPosition.toString(2).padStart(3, '0');

        // Determine which tetrahedron this vertex belongs to
        const vertexData = CONSTANTS.vertices.encoding[newVertex];
        const activeTet = vertexData.tet;

        // Check for orbit completion (cumSum is multiple of 8)
        const prevOrbits = Math.floor(prevSum / 8);
        const newOrbits = Math.floor(newSum / 8);
        const orbitCompleted = newOrbits > prevOrbits;

        // Check for closure (position = 0)
        const isClosure = newPosition === 0 && currentStep > 0;

        // Create step record
        const stepRecord = {
            step: currentStep,
            digit: digit,
            cumSum: newSum,
            position: newPosition,
            vertex: newVertex,
            tet: activeTet,
            orbitCompleted,
            isClosure,
            timestamp: Date.now()
        };

        // Update state
        this.update({
            step: currentStep + 1,
            currentDigit: digit,
            cumSum: newSum,
            previousVertex: this.state.currentVertex,
            currentVertex: newVertex,
            activeTet: activeTet,
            orbitsComplete: newOrbits,
            tetACount: this.state.tetACount + (activeTet === 'A' ? 1 : 0),
            tetBCount: this.state.tetBCount + (activeTet === 'B' ? 1 : 0),
        });

        // Update visit count
        const visitCounts = { ...this.state.visitCounts };
        visitCounts[newVertex]++;
        this.set('visitCounts', visitCounts);

        // Add to history
        const history = [...this.state.history, stepRecord];
        this.set('history', history);

        // Record closure event
        if (isClosure) {
            const closureEvents = [...this.state.closureEvents, {
                step: currentStep,
                cumSum: newSum,
                orbits: newOrbits
            }];
            this.set('closureEvents', closureEvents);
        }

        return stepRecord;
    }

    /**
     * Reset simulation to initial state
     */
    reset() {
        this.update({
            step: 0,
            currentDigit: null,
            cumSum: 0,
            currentVertex: '000',
            previousVertex: null,
            activeTet: null,
            orbitsComplete: 0,
            tetACount: 0,
            tetBCount: 0,
            history: [],
            closureEvents: [],
            visitCounts: {
                '000': 0, '001': 0, '010': 0, '011': 0,
                '100': 0, '101': 0, '110': 0, '111': 0
            },
        });
    }

    /**
     * Set the active module
     */
    setActiveModule(moduleId) {
        this.set('activeModule', moduleId);
    }

    /**
     * Set play state
     */
    setPlaying(isPlaying) {
        this.set('isPlaying', isPlaying);
    }

    /**
     * Set play speed
     */
    setPlaySpeed(speed) {
        this.set('playSpeed', speed);
    }

    // =========================================================================
    // COMPUTED VALUES
    // =========================================================================

    /**
     * Get phase balance between Tet A and Tet B
     */
    getPhaseBalance() {
        const total = this.state.tetACount + this.state.tetBCount;
        if (total === 0) return { tetA: 0.5, tetB: 0.5 };

        return {
            tetA: this.state.tetACount / total,
            tetB: this.state.tetBCount / total
        };
    }

    /**
     * Get current orbit progress (0-7)
     */
    getOrbitProgress() {
        return this.state.cumSum % 8;
    }

    /**
     * Get vertex with most visits
     */
    getMostVisitedVertex() {
        let maxVisits = 0;
        let maxVertex = null;

        Object.entries(this.state.visitCounts).forEach(([vertex, count]) => {
            if (count > maxVisits) {
                maxVisits = count;
                maxVertex = vertex;
            }
        });

        return { vertex: maxVertex, count: maxVisits };
    }

    /**
     * Calculate information content processed so far
     */
    getInformationBits() {
        // Each digit encodes log2(8) = 3 bits
        return this.state.step * 3;
    }

    /**
     * Get settlement frequency for display
     */
    getSettlementFrequency() {
        return CONSTANTS.derived.f_settlement;
    }

    /**
     * Format large numbers for display
     */
    formatScientific(num, decimals = 2) {
        if (num === 0) return '0';
        const exp = Math.floor(Math.log10(Math.abs(num)));
        const mantissa = num / Math.pow(10, exp);
        return `${mantissa.toFixed(decimals)} x 10^${exp}`;
    }

    // =========================================================================
    // OBSERVABLE PATTERN
    // =========================================================================

    /**
     * Subscribe to state changes
     * @param {string} key - State key to watch (or '*' for all)
     * @param {Function} callback - Called with (newValue, oldValue, key)
     * @returns {Function} Unsubscribe function
     */
    subscribe(key, callback) {
        if (!this.listeners.has(key)) {
            this.listeners.set(key, new Set());
        }
        this.listeners.get(key).add(callback);

        // Return unsubscribe function
        return () => {
            this.listeners.get(key).delete(callback);
        };
    }

    _notifyListeners(key, newValue, oldValue) {
        // Notify specific key listeners
        if (this.listeners.has(key)) {
            this.listeners.get(key).forEach(cb => cb(newValue, oldValue, key));
        }

        // Notify wildcard listeners
        if (this.listeners.has('*')) {
            this.listeners.get('*').forEach(cb => cb(newValue, oldValue, key));
        }
    }

    _invalidateComputed() {
        this._computed = {};
    }

    // =========================================================================
    // PERSISTENCE
    // =========================================================================

    /**
     * Export current state to JSON
     */
    exportState() {
        return JSON.stringify(this.state, null, 2);
    }

    /**
     * Import state from JSON
     */
    importState(json) {
        try {
            const imported = JSON.parse(json);
            Object.keys(imported).forEach(key => {
                if (key in this.state) {
                    this.set(key, imported[key]);
                }
            });
            return true;
        } catch (e) {
            console.error('Failed to import state:', e);
            return false;
        }
    }
}

// Create singleton instance
const dataStore = new DataStore();

// Make available globally
window.DataStore = DataStore;
window.dataStore = dataStore;
