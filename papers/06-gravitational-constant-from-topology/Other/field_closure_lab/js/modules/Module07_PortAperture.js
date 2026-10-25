/**
 * =============================================================================
 * Module07_PortAperture.js
 * Port Aperture & Coupling Visualization
 * 
 * =============================================================================
 * 3 COMPLETE CLOSURE CYCLES (WITH INTEGER "3" INCLUDED)
 * Generated from continuous Pi (base 8) traversal
 * Pi (base 8) = 3.110375... -> sequence [3, 1, 1, 0, 3, 7, ...]
 * 
 * CRITICAL: The "3" IS the "3" in "3+1" (d=3 spatial dimensions)
 * First positions (3,4) form I Ching complementary pair (sum=7)
 * See: Field_Closure_Complete_Read_Sequence_Proof.md Section 13.2
 * =============================================================================
 * 
 * CLOSURE 1 (Steps 0-15): B -> A -> A -> B
 *   Step  4: V0 (Tet B) -> [B6]
 *   Step  7: V1 (Tet A) -> [A2]
 *   Step 11: V2 (Tet A) -> [A1, A4, A7(T)] KC!
 *   Step 15: V6 (Tet B) -> [B0(T), B3, B5] KC!
 * 
 * CLOSURE 2 (Steps 16-44): A -> B -> B -> A
 *   Step 21: V2 (Tet A) -> [A7(T)] KC!
 *   Step 23: V0 (Tet B) -> [B5]
 *   Step 35: V5 (Tet B) -> [B0(T), B3, B6] KC!
 *   Step 44: V7 (Tet A) -> [A1, A2, A4]
 * 
 * CLOSURE 3 (Steps 45-65): B -> B -> A -> A
 *   Step 48: V6 (Tet B) -> [B0(T)] KC!
 *   Step 54: V0 (Tet B) -> [B3, B5, B6]
 *   Step 58: V4 (Tet A) -> [A7(T)] KC!
 *   Step 65: V7 (Tet A) -> [A1, A2, A4]
 * 
 * Each closure = 8 unique faces (4 Tet A + 4 Tet B)
 * =============================================================================
 */

class Module07_PortAperture extends Module {
    constructor(id, renderer, store, ui) {
        super(id, renderer, store, ui);
        this.name = 'Port Aperture';
        this.title = 'Module 07: Port Aperture & Coupling';

        this.currentEventIndex = 0;
        this.currentCycleIndex = 0;
        this.portTimer = null;
        this.animationFrameId = null;
        
        this.tetAColor = 0x4488ff;
        this.tetBColor = 0xffcc00;
        this.apertureFactorValue = Math.sqrt(4 / Math.PI);
        
        this.mode = 'step';
        
        this.faceIndexMap = {
            'A1': 1, 'A2': 2, 'A4': 0, 'A7': 3,
            'B0': 3, 'B3': 1, 'B5': 2, 'B6': 0,
        };
        
        // =================================================================
        // 3 CLOSURE CYCLES FROM PI (WITH INTEGER "3" INCLUDED)
        // Verified by field_closure_complete_read_sequence_proof_validation.py
        // Each cycle has DIFFERENT event groupings but same 8 unique faces
        // =================================================================
        this.closureCycles = [
            // CLOSURE 1: Steps 0-15
            // Tet A [4]: A2, A1, A4, A7 (T) | Tet B [4]: B6, B0 (T), B3, B5
            // Pattern: B -> A -> A -> B
            {
                events: [
                    { piStep: 4, vertex: 0, faces: [{ name: 'B6', tetId: 'B', role: 'SPATIAL' }], kingsChamber: false },
                    { piStep: 7, vertex: 1, faces: [{ name: 'A2', tetId: 'A', role: 'SPATIAL' }], kingsChamber: false },
                    { piStep: 11, vertex: 2, faces: [{ name: 'A1', tetId: 'A', role: 'SPATIAL' }, { name: 'A4', tetId: 'A', role: 'SPATIAL' }, { name: 'A7', tetId: 'A', role: 'TIME' }], kingsChamber: true },
                    { piStep: 15, vertex: 6, faces: [{ name: 'B0', tetId: 'B', role: 'TIME' }, { name: 'B3', tetId: 'B', role: 'SPATIAL' }, { name: 'B5', tetId: 'B', role: 'SPATIAL' }], kingsChamber: true }
                ]
            },
            // CLOSURE 2: Steps 16-44
            // Tet A [4]: A7 (T), A1, A2, A4 | Tet B [4]: B5, B0 (T), B3, B6
            // Pattern: A -> B -> B -> A
            {
                events: [
                    { piStep: 21, vertex: 2, faces: [{ name: 'A7', tetId: 'A', role: 'TIME' }], kingsChamber: true },
                    { piStep: 23, vertex: 0, faces: [{ name: 'B5', tetId: 'B', role: 'SPATIAL' }], kingsChamber: false },
                    { piStep: 35, vertex: 5, faces: [{ name: 'B0', tetId: 'B', role: 'TIME' }, { name: 'B3', tetId: 'B', role: 'SPATIAL' }, { name: 'B6', tetId: 'B', role: 'SPATIAL' }], kingsChamber: true },
                    { piStep: 44, vertex: 7, faces: [{ name: 'A1', tetId: 'A', role: 'SPATIAL' }, { name: 'A2', tetId: 'A', role: 'SPATIAL' }, { name: 'A4', tetId: 'A', role: 'SPATIAL' }], kingsChamber: false }
                ]
            },
            // CLOSURE 3: Steps 45-65
            // Tet A [4]: A7 (T), A1, A2, A4 | Tet B [4]: B0 (T), B3, B5, B6
            // Pattern: B -> B -> A -> A
            {
                events: [
                    { piStep: 48, vertex: 6, faces: [{ name: 'B0', tetId: 'B', role: 'TIME' }], kingsChamber: true },
                    { piStep: 54, vertex: 0, faces: [{ name: 'B3', tetId: 'B', role: 'SPATIAL' }, { name: 'B5', tetId: 'B', role: 'SPATIAL' }, { name: 'B6', tetId: 'B', role: 'SPATIAL' }], kingsChamber: false },
                    { piStep: 58, vertex: 4, faces: [{ name: 'A7', tetId: 'A', role: 'TIME' }], kingsChamber: true },
                    { piStep: 65, vertex: 7, faces: [{ name: 'A1', tetId: 'A', role: 'SPATIAL' }, { name: 'A2', tetId: 'A', role: 'SPATIAL' }, { name: 'A4', tetId: 'A', role: 'SPATIAL' }], kingsChamber: false }
                ]
            }
        ];
        
        this.pulseDuration = 1000;
        this.faceSequenceDelay = 100;
        this.eventPauseDelay = 600;
        this.cyclePauseDelay = 1200;
    }

    /**
     * Get all faces from a specific closure cycle
     */
    getAllFacesFromCycle(cycleIndex) {
        const cycle = this.closureCycles[cycleIndex];
        const allFaces = [];
        for (const event of cycle.events) {
            for (const face of event.faces) {
                allFaces.push(face);
            }
        }
        return allFaces;
    }

    setup() {
        super.setup();

        this.renderer.hideVertexMarkers();
        this.renderer.setTetAColor(this.tetAColor);
        this.renderer.setTetBColor(this.tetBColor);
        this.renderer.setTetAOpacity(0.25);
        this.renderer.setTetBOpacity(0.15);
        this.renderer.setAutoRotate(true);
        this.renderer.setRotationSpeed(0.06);

        this.renderer.createDualPortApertureCircles(this.tetAColor, this.tetBColor);
        this.renderer.createKingsChamberGlow(0xffffff);
        this.renderer.createTriforceHeartLinesOnAllFaces();
        
        this.currentEventIndex = 0;
        this.currentCycleIndex = 0;
        
        this.updateApertureInfo();
        this.startAnimation();
    }

    cleanup() {
        super.cleanup();
        this.stopAllAnimations();
        this.renderer.resetFaces();
        this.renderer.clearPortApertureCircles();
        this.renderer.clearKingsChamberGlow();
        this.renderer.clearTriforceHeartLines();
        this.renderer.showVertexMarkers();
        this.renderer.resetAllVertices();
        this.renderer.resetTetrahedronColors();
    }

    stopAllAnimations() {
        if (this.portTimer) {
            clearTimeout(this.portTimer);
            this.portTimer = null;
        }
        if (this.animationFrameId) {
            cancelAnimationFrame(this.animationFrameId);
            this.animationFrameId = null;
        }
    }

    getFaceIndex(name) {
        return this.faceIndexMap[name] ?? 0;
    }

    // =========================================================================
    // STEP MODE
    // =========================================================================
    pulseSingleFace(face) {
        const idx = this.getFaceIndex(face.name);
        const tetId = face.tetId;
        
        this.renderer.pulsePortApertureCircle(tetId, idx, this.pulseDuration);
        
        const meshes = tetId === 'A' ? this.renderer.faceMeshes.tetA : this.renderer.faceMeshes.tetB;
        const mesh = meshes[idx];
        if (!mesh) return;
        
        const baseColor = tetId === 'A' ? this.tetAColor : this.tetBColor;
        const origColor = new THREE.Color(baseColor);
        const targetColor = tetId === 'A' ? new THREE.Color(0x66bbff) : new THREE.Color(0xffee44);
        const maxOp = tetId === 'A' ? 1.0 : 0.6;
        const baseOp = tetId === 'A' ? 0.25 : 0.15;
        
        const start = performance.now();
        const flashDur = this.pulseDuration * 0.25;
        const fadeDur = this.pulseDuration * 0.75;
        
        const anim = (t) => {
            if (!this.isActive) return;
            const elapsed = t - start;
            
            if (elapsed < flashDur) {
                const p = elapsed / flashDur;
                mesh.material.color.lerpColors(origColor, targetColor, p);
                mesh.material.opacity = baseOp + (maxOp - baseOp) * p;
            } else if (elapsed < flashDur + fadeDur) {
                const p = (elapsed - flashDur) / fadeDur;
                mesh.material.color.lerpColors(targetColor, origColor, p);
                mesh.material.opacity = maxOp - (maxOp - baseOp) * p;
            } else {
                mesh.material.color.copy(origColor);
                mesh.material.opacity = baseOp;
                return;
            }
            requestAnimationFrame(anim);
        };
        requestAnimationFrame(anim);
    }

    runStepMode() {
        if (!this.isActive) return;
        
        const cycle = this.closureCycles[this.currentCycleIndex];
        const event = cycle.events[this.currentEventIndex];
        const faces = event.faces;
        let faceIdx = 0;
        
        this.updateIndicator();
        
        const fireNext = () => {
            if (!this.isActive || faceIdx >= faces.length) {
                this.portTimer = setTimeout(() => {
                    this.currentEventIndex++;
                    if (this.currentEventIndex >= cycle.events.length) {
                        this.currentEventIndex = 0;
                        this.currentCycleIndex = (this.currentCycleIndex + 1) % this.closureCycles.length;
                        this.portTimer = setTimeout(() => this.runStepMode(), this.cyclePauseDelay);
                    } else {
                        this.portTimer = setTimeout(() => this.runStepMode(), this.eventPauseDelay);
                    }
                }, this.pulseDuration);
                return;
            }
            
            const face = faces[faceIdx];
            this.pulseSingleFace(face);
            
            if (face.role === 'TIME') {
                const c = face.tetId === 'A' ? this.tetAColor : this.tetBColor;
                this.renderer.pulseKingsChamber(this.pulseDuration * 0.8, c);
            }
            
            faceIdx++;
            if (faceIdx < faces.length) {
                this.portTimer = setTimeout(fireNext, this.faceSequenceDelay);
            } else {
                fireNext();
            }
        };
        
        fireNext();
    }

    // =========================================================================
    // FULL MODE - All 8 faces of current cycle pulse together
    // =========================================================================
    runFullMode() {
        if (!this.isActive) return;
        
        this.updateIndicator();
        
        const allFaces = this.getAllFacesFromCycle(this.currentCycleIndex);
        
        const meshData = [];
        const portData = [];
        
        for (const face of allFaces) {
            const tetId = face.tetId;
            const idx = this.getFaceIndex(face.name);
            
            const meshes = tetId === 'A' ? this.renderer.faceMeshes.tetA : this.renderer.faceMeshes.tetB;
            const mesh = meshes[idx];
            if (mesh) {
                const baseColor = tetId === 'A' ? this.tetAColor : this.tetBColor;
                meshData.push({
                    mesh: mesh,
                    origColor: new THREE.Color(baseColor),
                    targetColor: tetId === 'A' ? new THREE.Color(0x66bbff) : new THREE.Color(0xffee44),
                    baseOp: tetId === 'A' ? 0.25 : 0.15,
                    maxOp: tetId === 'A' ? 1.0 : 0.6
                });
            }
            
            const tetPortData = tetId === 'A' ? this.renderer.portApertureData?.tetA : this.renderer.portApertureData?.tetB;
            if (tetPortData?.circles?.[idx]) {
                const circle = tetPortData.circles[idx];
                const baseColor = tetId === 'A' ? this.tetAColor : this.tetBColor;
                portData.push({
                    line: circle.line,
                    disc: circle.disc,
                    origColor: new THREE.Color(circle.originalColor),
                    targetColor: tetId === 'A' ? new THREE.Color(0x66bbff) : new THREE.Color(0xffee44),
                    baseLineOp: circle.baseOpacity,
                    baseDiscOp: circle.discOpacity,
                    maxLineOp: tetId === 'A' ? 1.0 : 0.7,
                    maxDiscOp: tetId === 'A' ? 0.7 : 0.3
                });
            }
        }
        
        const kc = this.renderer.kingsChamberGlow;
        const kcHalo = this.renderer.kingsChamberHalo;
        
        const startTime = performance.now();
        const flashDur = this.pulseDuration * 0.25;
        const fadeDur = this.pulseDuration * 0.75;
        const totalDur = flashDur + fadeDur;
        
        const animate = (now) => {
            if (!this.isActive) return;
            
            const elapsed = now - startTime;
            let intensity;
            if (elapsed < flashDur) {
                intensity = elapsed / flashDur;
            } else if (elapsed < totalDur) {
                intensity = 1 - ((elapsed - flashDur) / fadeDur);
            } else {
                intensity = 0;
            }
            
            for (const m of meshData) {
                m.mesh.material.color.lerpColors(m.origColor, m.targetColor, intensity);
                m.mesh.material.opacity = m.baseOp + (m.maxOp - m.baseOp) * intensity;
            }
            
            for (const p of portData) {
                p.line.material.color.lerpColors(p.origColor, p.targetColor, intensity);
                p.line.material.opacity = p.baseLineOp + (p.maxLineOp - p.baseLineOp) * intensity;
                p.disc.material.color.lerpColors(p.origColor, p.targetColor, intensity);
                p.disc.material.opacity = p.baseDiscOp + (p.maxDiscOp - p.baseDiscOp) * intensity;
            }
            
            if (kc && kcHalo) {
                const scale = 1 + intensity;
                const op = 0.3 + 0.6 * intensity;
                kc.scale.setScalar(scale);
                kc.material.opacity = op;
                kcHalo.scale.setScalar(scale);
                kcHalo.material.opacity = op * 0.5;
            }
            
            if (elapsed < totalDur) {
                this.animationFrameId = requestAnimationFrame(animate);
            } else {
                for (const m of meshData) {
                    m.mesh.material.color.copy(m.origColor);
                    m.mesh.material.opacity = m.baseOp;
                }
                for (const p of portData) {
                    p.line.material.color.copy(p.origColor);
                    p.line.material.opacity = p.baseLineOp;
                    p.disc.material.color.copy(p.origColor);
                    p.disc.material.opacity = p.baseDiscOp;
                }
                if (kc && kcHalo) {
                    kc.scale.setScalar(1);
                    kc.material.opacity = 0.3;
                    kcHalo.scale.setScalar(1);
                    kcHalo.material.opacity = 0.1;
                }
                
                this.currentCycleIndex = (this.currentCycleIndex + 1) % this.closureCycles.length;
                this.portTimer = setTimeout(() => this.runFullMode(), this.cyclePauseDelay);
            }
        };
        
        this.animationFrameId = requestAnimationFrame(animate);
    }

    // =========================================================================
    // MODE CONTROL
    // =========================================================================
    startAnimation() {
        if (this.mode === 'step') {
            this.runStepMode();
        } else {
            this.runFullMode();
        }
    }

    setMode(newMode) {
        if (this.mode === newMode) return;
        
        this.stopAllAnimations();
        this.mode = newMode;
        this.currentEventIndex = 0;
        this.currentCycleIndex = 0;
        
        this.renderer.resetFaces();
        this.renderer.resetPortApertureCircles();
        
        this.updateApertureInfo();
        this.startAnimation();
    }

    // =========================================================================
    // INDICATOR - Shows different info per cycle
    // =========================================================================
    updateIndicator() {
        const el = document.getElementById('active-port-indicator');
        if (!el) return;
        
        const cycle = this.closureCycles[this.currentCycleIndex];
        const allFaces = this.getAllFacesFromCycle(this.currentCycleIndex);
        const tetA = allFaces.filter(f => f.tetId === 'A');
        const tetB = allFaces.filter(f => f.tetId === 'B');
        
        // Get pi step range for this cycle
        const startStep = cycle.events[0].piStep;
        const endStep = cycle.events[cycle.events.length - 1].piStep;
        
        // Build face lists showing completion ORDER for this cycle
        const aList = tetA.map(f => f.name + (f.role === 'TIME' ? ' (T)' : '')).join(', ');
        const bList = tetB.map(f => f.name + (f.role === 'TIME' ? ' (T)' : '')).join(', ');
        
        // Build event order summary
        const eventOrder = cycle.events.map(e => {
            const names = e.faces.map(f => f.name).join(',');
            return names;
        }).join(' -> ');
        
        if (this.mode === 'step') {
            const event = cycle.events[this.currentEventIndex];
            const eventTetA = event.faces.filter(f => f.tetId === 'A');
            const eventTetB = event.faces.filter(f => f.tetId === 'B');
            
            let facesHtml = '';
            if (eventTetA.length) {
                const list = eventTetA.map(f => f.name + (f.role === 'TIME' ? ' (TIME)' : '')).join(', ');
                facesHtml += `<div style="color:#4488ff;margin-bottom:4px"><b>Tet A:</b> ${list}</div>`;
            }
            if (eventTetB.length) {
                const list = eventTetB.map(f => f.name + (f.role === 'TIME' ? ' (TIME)' : '')).join(', ');
                facesHtml += `<div style="color:#ffcc00"><b>Tet B:</b> ${list}</div>`;
            }
            
            const kc = event.kingsChamber ? '<div style="font-size:10px;color:#fff;margin-top:6px">King\'s Chamber</div>' : '';
            
            el.innerHTML = `
                <div style="background:rgba(100,100,100,0.2);border-left:3px solid ${eventTetA.length ? '#4488ff' : '#ffcc00'};padding:10px;border-radius:4px">
                    <div style="display:flex;justify-content:space-between;margin-bottom:8px">
                        <span style="font-size:13px;font-weight:bold">Closure ${this.currentCycleIndex + 1} of 3</span>
                        <span style="font-size:11px;color:#888">Event ${this.currentEventIndex + 1}/4</span>
                    </div>
                    <div style="font-size:10px;color:var(--text-secondary);margin-bottom:6px">Pi steps ${startStep}-${endStep}</div>
                    <div style="font-size:12px;margin-bottom:6px">${facesHtml}</div>
                    <div style="font-size:10px;color:var(--text-secondary)">Step ${event.piStep} | V${event.vertex}</div>
                    ${kc}
                </div>`;
        } else {
            el.innerHTML = `
                <div style="background:rgba(100,100,100,0.2);border-left:3px solid #fff;padding:10px;border-radius:4px">
                    <div style="display:flex;justify-content:space-between;margin-bottom:8px">
                        <span style="font-size:13px;font-weight:bold;color:#fff">Closure ${this.currentCycleIndex + 1} of 3</span>
                        <span style="font-size:10px;color:#fff">8 Faces</span>
                    </div>
                    <div style="font-size:10px;color:var(--text-secondary);margin-bottom:6px">Pi steps ${startStep}-${endStep}</div>
                    <div style="font-size:12px;margin-bottom:8px">
                        <div style="color:#4488ff;margin-bottom:4px"><b>Tet A [4]:</b> ${aList}</div>
                        <div style="color:#ffcc00"><b>Tet B [4]:</b> ${bList}</div>
                    </div>
                    <div style="font-size:9px;color:var(--text-secondary);margin-bottom:6px">Order: ${eventOrder}</div>
                    <div style="font-size:10px;color:#fff">King's Chamber</div>
                </div>`;
        }
    }

    updateApertureInfo() {
        const isStep = this.mode === 'step';
        
        const html = `
            <div class="info-section mt-md">
                <h3>Viewing Mode</h3>
                <div style="display:flex;gap:8px;margin-bottom:12px">
                    <button id="mode-step" style="flex:1;padding:10px 8px;border:1px solid ${isStep ? '#4488ff' : '#444'};background:${isStep ? 'rgba(68,136,255,0.2)' : 'transparent'};color:${isStep ? '#4488ff' : '#888'};border-radius:4px;cursor:pointer;font-size:12px">
                        Completion Step
                    </button>
                    <button id="mode-full" style="flex:1;padding:10px 8px;border:1px solid ${!isStep ? '#ffcc00' : '#444'};background:${!isStep ? 'rgba(255,204,0,0.2)' : 'transparent'};color:${!isStep ? '#ffcc00' : '#888'};border-radius:4px;cursor:pointer;font-size:12px">
                        Completion Full
                    </button>
                </div>
                <p style="font-size:10px;color:var(--text-secondary);line-height:1.4">
                    ${isStep 
                        ? '<b>Step:</b> Shows events sequentially within each closure cycle.'
                        : '<b>Full:</b> All 8 faces pulse together for each closure.'}
                </p>
            </div>
            
            <div class="info-section mt-md">
                <h3>Active</h3>
                <div id="active-port-indicator"></div>
            </div>
            
            <div class="info-section mt-md">
                <h3>3 Closure Cycles (from Pi with "3")</h3>
                <div style="font-size:10px;line-height:1.5;padding:8px;background:rgba(255,255,255,0.05);border-radius:4px">
                    <div style="margin-bottom:6px"><b>Closure 1</b> (steps 0-15): <span style="color:#ffcc00">B</span>-><span style="color:#4488ff">A</span>-><span style="color:#4488ff">A</span>-><span style="color:#ffcc00">B</span></div>
                    <div style="margin-bottom:6px"><b>Closure 2</b> (steps 16-44): <span style="color:#4488ff">A</span>-><span style="color:#ffcc00">B</span>-><span style="color:#ffcc00">B</span>-><span style="color:#4488ff">A</span></div>
                    <div><b>Closure 3</b> (steps 45-65): <span style="color:#ffcc00">B</span>-><span style="color:#ffcc00">B</span>-><span style="color:#4488ff">A</span>-><span style="color:#4488ff">A</span></div>
                </div>
                <p style="font-size:9px;color:var(--text-secondary);margin-top:6px">
                    Pi = 3.110375... (base 8), "3" = d=3 spatial
                </p>
            </div>
            
            <div class="info-section mt-md">
                <h3>Port Domain</h3>
                <div class="formula" style="font-size:12px">
                    Aperture = sqrt(k/pi) = ${this.apertureFactorValue.toFixed(3)}
                </div>
            </div>`;

        let area = document.getElementById('module-dynamic-content');
        if (!area) {
            area = document.createElement('div');
            area.id = 'module-dynamic-content';
            document.getElementById('info-content').appendChild(area);
        }
        area.innerHTML = html;
        
        document.getElementById('mode-step')?.addEventListener('click', () => this.setMode('step'));
        document.getElementById('mode-full')?.addEventListener('click', () => this.setMode('full'));
        
        this.updateIndicator();
    }

    renderInfoContent() {}
}

window.Module07_PortAperture = Module07_PortAperture;
