/**
 * =============================================================================
 * UIController.js
 * Manages all UI interactions for the Field Closure Engine Lab
 * 
 * Handles:
 * - Navigation panel interactions
 * - Info panel content updates
 * - Animation controls
 * - Metrics display
 * - Overlay management
 * =============================================================================
 */

class UIController {
    constructor() {
        // DOM element references
        this.elements = {
            // Navigation
            moduleButtons: null,

            // Metrics
            metricStep: null,
            metricDigit: null,
            metricPosition: null,
            metricCumsum: null,
            metricTet: null,
            metricOrbits: null,

            // Info panel
            infoTitle: null,
            conceptText: null,
            visualText: null,
            insightText: null,

            // Controls
            btnPrev: null,
            btnNext: null,
            btnStep: null,
            btnPlay: null,
            btnReset: null,
            speedSlider: null,

            // Overlay
            explanationOverlay: null,
            explanationTitle: null,
            explanationText: null,
            btnDismiss: null,

            // Loading
            loadingScreen: null,
        };

        // Current state
        this.currentModule = 1;
        this.isPlaying = false;
        this.playInterval = null;
        this.playSpeed = 1.0;

        // Callbacks
        this.onModuleChange = null;
        this.onStep = null;
        this.onPlay = null;
        this.onPause = null;
        this.onReset = null;
        this.onSpeedChange = null;
        this.onAxisLockToggle = null;
    }

    // =========================================================================
    // INITIALIZATION
    // =========================================================================

    init() {
        this._cacheElements();
        this._bindEvents();
        this._subscribeToStore();
        return this;
    }

    _cacheElements() {
        // Navigation buttons
        this.elements.moduleButtons = document.querySelectorAll('.module-btn');

        // Metrics
        this.elements.metricStep = document.getElementById('metric-step');
        this.elements.metricDigit = document.getElementById('metric-digit');
        this.elements.metricPosition = document.getElementById('metric-position');
        this.elements.metricCumsum = document.getElementById('metric-cumsum');
        this.elements.metricTet = document.getElementById('metric-tet');
        this.elements.metricOrbits = document.getElementById('metric-orbits');

        // Info panel
        this.elements.infoTitle = document.getElementById('info-title');
        this.elements.conceptText = document.getElementById('concept-text');
        this.elements.visualText = document.getElementById('visual-text');
        this.elements.insightText = document.getElementById('insight-text');

        // Controls
        this.elements.btnPrev = document.getElementById('btn-prev');
        this.elements.btnNext = document.getElementById('btn-next');
        this.elements.btnStep = document.getElementById('btn-step');
        this.elements.btnPlay = document.getElementById('btn-play');
        this.elements.btnReset = document.getElementById('btn-reset');
        this.elements.speedSlider = document.getElementById('speed-slider');

        // Overlay
        this.elements.explanationOverlay = document.getElementById('explanation-overlay');
        this.elements.explanationTitle = document.getElementById('explanation-title');
        this.elements.explanationText = document.getElementById('explanation-text');
        this.elements.btnDismiss = document.getElementById('btn-dismiss');

        // Loading
        this.elements.loadingScreen = document.getElementById('loading-screen');
    }

    _bindEvents() {
        // Module navigation
        this.elements.moduleButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                const moduleId = parseInt(btn.dataset.module);
                this.selectModule(moduleId);
            });
        });

        // Previous/Next module
        if (this.elements.btnPrev) {
            this.elements.btnPrev.addEventListener('click', () => {
                if (this.currentModule > 1) {
                    this.selectModule(this.currentModule - 1);
                }
            });
        }

        if (this.elements.btnNext) {
            this.elements.btnNext.addEventListener('click', () => {
                if (this.currentModule < 10) {
                    this.selectModule(this.currentModule + 1);
                }
            });
        }

        // Animation controls
        if (this.elements.btnStep) {
            this.elements.btnStep.addEventListener('click', () => {
                if (this.onStep) this.onStep();
            });
        }

        if (this.elements.btnPlay) {
            this.elements.btnPlay.addEventListener('click', () => {
                this.togglePlay();
            });
        }

        if (this.elements.btnReset) {
            this.elements.btnReset.addEventListener('click', () => {
                this.stopPlay();
                if (this.onReset) this.onReset();
            });
        }

        // Speed slider
        if (this.elements.speedSlider) {
            this.elements.speedSlider.addEventListener('input', (e) => {
                this.playSpeed = parseFloat(e.target.value);
                if (this.onSpeedChange) this.onSpeedChange(this.playSpeed);

                // If playing, restart with new speed
                if (this.isPlaying) {
                    this.stopPlay();
                    this.startPlay();
                }
            });
        }

        // Overlay dismiss
        if (this.elements.btnDismiss) {
            this.elements.btnDismiss.addEventListener('click', () => {
                this.hideOverlay();
            });
        }

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            switch (e.key) {
                case ' ':  // Space - play/pause
                    e.preventDefault();
                    this.togglePlay();
                    break;
                case 'ArrowRight':  // Right arrow - step
                    e.preventDefault();
                    if (this.onStep) this.onStep();
                    break;
                case 'r':  // R - reset
                    e.preventDefault();
                    this.stopPlay();
                    if (this.onReset) this.onReset();
                    break;
                case 'ArrowUp':  // Up - next module
                    e.preventDefault();
                    if (this.currentModule < 10) {
                        this.selectModule(this.currentModule + 1);
                    }
                    break;
                case 'ArrowDown':  // Down - previous module
                    e.preventDefault();
                    if (this.currentModule > 1) {
                        this.selectModule(this.currentModule - 1);
                    }
                    break;
                case 'l':  // L - toggle axis lock (time floor down)
                case 'L':
                    e.preventDefault();
                    if (this.onAxisLockToggle) this.onAxisLockToggle();
                    break;
            }
        });
    }

    _subscribeToStore() {
        // Subscribe to relevant state changes
        dataStore.subscribe('step', (value) => {
            this.updateMetric('step', value);
        });

        dataStore.subscribe('currentDigit', (value) => {
            this.updateMetric('digit', value !== null ? value : '-');
        });

        dataStore.subscribe('currentVertex', (value) => {
            this.updateMetric('position', value);
        });

        dataStore.subscribe('cumSum', (value) => {
            this.updateMetric('cumsum', value);
        });

        dataStore.subscribe('activeTet', (value) => {
            this.updateMetric('tet', value || '-');
        });

        dataStore.subscribe('orbitsComplete', (value) => {
            this.updateMetric('orbits', value);
        });
    }

    // =========================================================================
    // MODULE SELECTION
    // =========================================================================

    selectModule(moduleId) {
        if (moduleId < 1 || moduleId > 10) return;

        this.currentModule = moduleId;

        // Update button states
        this.elements.moduleButtons.forEach(btn => {
            const btnModuleId = parseInt(btn.dataset.module);
            btn.classList.toggle('active', btnModuleId === moduleId);
        });

        // Update info panel content
        const moduleInfo = CONSTANTS.modules[moduleId];
        if (moduleInfo) {
            this.updateInfoPanel(moduleInfo);
        }

        // Update store
        dataStore.setActiveModule(moduleId);

        // Trigger callback
        if (this.onModuleChange) {
            this.onModuleChange(moduleId);
        }
    }

    updateInfoPanel(moduleInfo) {
        if (this.elements.infoTitle) {
            this.elements.infoTitle.textContent = moduleInfo.title;
        }
        if (this.elements.conceptText) {
            this.elements.conceptText.textContent = moduleInfo.concept;
        }
        if (this.elements.visualText) {
            this.elements.visualText.textContent = moduleInfo.visual;
        }
        if (this.elements.insightText) {
            this.elements.insightText.textContent = moduleInfo.insight;
        }
    }

    // =========================================================================
    // METRICS UPDATE
    // =========================================================================

    updateMetric(metric, value) {
        const elementMap = {
            'step': this.elements.metricStep,
            'digit': this.elements.metricDigit,
            'position': this.elements.metricPosition,
            'cumsum': this.elements.metricCumsum,
            'tet': this.elements.metricTet,
            'orbits': this.elements.metricOrbits,
        };

        const element = elementMap[metric];
        if (element) {
            element.textContent = value;

            // Add highlight animation
            element.classList.add('highlight');
            setTimeout(() => element.classList.remove('highlight'), 200);
        }
    }

    updateAllMetrics(state) {
        this.updateMetric('step', state.step);
        this.updateMetric('digit', state.currentDigit !== null ? state.currentDigit : '-');
        this.updateMetric('position', state.currentVertex);
        this.updateMetric('cumsum', state.cumSum);
        this.updateMetric('tet', state.activeTet || '-');
        this.updateMetric('orbits', state.orbitsComplete);
    }

    // =========================================================================
    // PLAY CONTROLS
    // =========================================================================

    togglePlay() {
        if (this.isPlaying) {
            this.stopPlay();
        } else {
            this.startPlay();
        }
    }

    startPlay() {
        if (this.isPlaying) return;

        this.isPlaying = true;
        dataStore.setPlaying(true);

        if (this.elements.btnPlay) {
            this.elements.btnPlay.textContent = 'PAUSE';
            this.elements.btnPlay.classList.add('playing');
        }

        const interval = CONSTANTS.animation.stepDuration / this.playSpeed;
        this.playInterval = setInterval(() => {
            if (this.onStep) {
                const result = this.onStep();
                if (!result) {
                    // End of sequence
                    this.stopPlay();
                }
            }
        }, interval);

        if (this.onPlay) this.onPlay();
    }

    stopPlay() {
        if (!this.isPlaying) return;

        this.isPlaying = false;
        dataStore.setPlaying(false);

        if (this.elements.btnPlay) {
            this.elements.btnPlay.textContent = 'PLAY';
            this.elements.btnPlay.classList.remove('playing');
        }

        if (this.playInterval) {
            clearInterval(this.playInterval);
            this.playInterval = null;
        }

        if (this.onPause) this.onPause();
    }

    // =========================================================================
    // OVERLAY MANAGEMENT
    // =========================================================================

    showOverlay(title, text) {
        if (this.elements.explanationOverlay) {
            this.elements.explanationTitle.textContent = title;
            this.elements.explanationText.textContent = text;
            this.elements.explanationOverlay.classList.remove('hidden');
        }
    }

    hideOverlay() {
        if (this.elements.explanationOverlay) {
            this.elements.explanationOverlay.classList.add('hidden');
        }
    }

    // =========================================================================
    // LOADING SCREEN
    // =========================================================================

    hideLoading() {
        if (this.elements.loadingScreen) {
            this.elements.loadingScreen.classList.add('hidden');

            // Remove from DOM after transition
            setTimeout(() => {
                if (this.elements.loadingScreen.parentNode) {
                    this.elements.loadingScreen.parentNode.removeChild(this.elements.loadingScreen);
                }
            }, 500);
        }
    }

    showLoading(message = 'Loading...') {
        if (this.elements.loadingScreen) {
            const p = this.elements.loadingScreen.querySelector('p');
            if (p) p.textContent = message;
            this.elements.loadingScreen.classList.remove('hidden');
        }
    }

    // =========================================================================
    // DYNAMIC CONTENT
    // =========================================================================

    /**
     * Update the info panel with custom HTML content
     */
    setInfoContent(html) {
        const infoContent = document.getElementById('info-content');
        if (infoContent) {
            infoContent.innerHTML = html;
        }
    }

    /**
     * Append content to info panel
     */
    appendInfoContent(html) {
        const infoContent = document.getElementById('info-content');
        if (infoContent) {
            const div = document.createElement('div');
            div.innerHTML = html;
            infoContent.appendChild(div);
        }
    }

    /**
     * Create a data table in the info panel
     */
    createDataTable(headers, rows, highlightIndex = -1) {
        let html = '<table class="data-table"><thead><tr>';
        headers.forEach(h => html += `<th>${h}</th>`);
        html += '</tr></thead><tbody>';

        rows.forEach((row, i) => {
            const rowClass = i === highlightIndex ? 'highlight' : '';
            html += `<tr class="${rowClass}">`;
            row.forEach(cell => html += `<td>${cell}</td>`);
            html += '</tr>';
        });

        html += '</tbody></table>';
        return html;
    }

    /**
     * Create a progress bar
     */
    createProgressBar(progress, label = '') {
        const percent = Math.min(100, Math.max(0, progress * 100));
        return `
            <div class="progress-container">
                ${label ? `<span class="progress-label">${label}</span>` : ''}
                <div class="progress-bar">
                    <div class="progress-fill" style="width: ${percent}%"></div>
                </div>
                <span class="progress-value">${percent.toFixed(1)}%</span>
            </div>
        `;
    }

    /**
     * Create a binary display with colored bits
     */
    createBinaryDisplay(binary) {
        let html = '<span class="binary-display">';
        binary.split('').forEach(bit => {
            const bitClass = bit === '1' ? 'bit-1' : 'bit-0';
            html += `<span class="${bitClass}">${bit}</span>`;
        });
        html += '</span>';
        return html;
    }

    /**
     * Create a formula display
     */
    createFormula(formula, description = '') {
        return `
            <div class="formula">
                <code>${formula}</code>
                ${description ? `<p class="formula-desc">${description}</p>` : ''}
            </div>
        `;
    }

    // =========================================================================
    // NOTIFICATIONS
    // =========================================================================

    /**
     * Show a temporary notification
     */
    notify(message, type = 'info', duration = 3000) {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: ${type === 'success' ? 'var(--accent-success)' :
                type === 'error' ? 'var(--accent-error)' :
                    type === 'warning' ? 'var(--accent-warning)' :
                        'var(--accent-primary)'};
            color: ${type === 'warning' ? '#000' : '#fff'};
            padding: 12px 24px;
            border-radius: 8px;
            z-index: 1000;
            animation: slideUp 0.3s ease;
        `;

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.style.animation = 'slideDown 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        }, duration);
    }

    // =========================================================================
    // TOOLTIP
    // =========================================================================

    showTooltip(x, y, content) {
        let tooltip = document.getElementById('tooltip');
        if (!tooltip) {
            tooltip = document.createElement('div');
            tooltip.id = 'tooltip';
            tooltip.className = 'tooltip';
            document.body.appendChild(tooltip);
        }

        tooltip.innerHTML = content;
        tooltip.style.left = `${x + 10}px`;
        tooltip.style.top = `${y + 10}px`;
        tooltip.style.display = 'block';
    }

    hideTooltip() {
        const tooltip = document.getElementById('tooltip');
        if (tooltip) {
            tooltip.style.display = 'none';
        }
    }
}

// Create singleton instance
const uiController = new UIController();

// Make available globally
window.UIController = UIController;
window.uiController = uiController;
