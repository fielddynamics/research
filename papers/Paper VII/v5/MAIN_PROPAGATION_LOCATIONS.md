# Main Propagation Discussion Locations

**Created:** 2026-02-11
**Purpose:** Identify the 3-4 key places discussing propagation scales/speed c for simplification

---

## PROPOSED FIELD ORIGIN DEFINITION

**Simple, clear, pedagogical:**

```latex
\noindent\textbf{Field Origin:} The coupling point at $r = 0$ where propagation time vanishes ($\tau = 0$). This enables field objects to achieve field closure with the ambient gravitational field—the distributed field components can settle into a consistent state without waiting for light-speed signals to propagate across the object's extent.
```

**Key features:**
- ✅ Short and clear (2 sentences)
- ✅ Explains WHAT it is (coupling point at r=0, τ=0)
- ✅ Explains WHY it matters (enables field closure without propagation delay)
- ✅ Uses concrete language (not over-technical)
- ✅ Relational (couples with ambient field)
- ✅ No jargon like "nonlinear boundary" in definition

---

## THE 4 MAIN LOCATIONS

### Location 1: Introduction / Full State Snapshot Explanation
**Line:** ~447
**Section:** Introduction explaining Field Origin and Full State Snapshot
**Current problems:**
- "all field components of the quantum mass body couple" (sounds internal)
- "within field objects" vs "between field objects" (spatial framing)
- "at one scale... at another scale" (creates two scales dichotomy)
- Heavy use of "quantum mass body" (jargon)

**Current text excerpt:**
```
The Field Origin resolves this through topology, not propagation. At r = 0, where spatial
separation vanishes, all field components of the quantum mass body couple through the
nonlinear boundary simultaneously, enabling the Full State Snapshot that FC_Σ requires.
This is not faster-than-light signaling. FC_Σ still propagates causally at speed c between
separated quantum mass bodies. Rather, the Field Origin provides a coupling boundary where
τ_prop = 0, allowing atomic read of the unified configuration. The Field Origin operates
at one scale (the coupling boundary enabling Full State Snapshot within field objects),
while FC_Σ propagates at another scale (linear transport at speed c between field objects).
Both are necessary: propagation ensures causal consistency between separated field objects,
while the Field Origin enables the atomic Full State Snapshot required for FC_Σ within each
unified configuration.
```

**Needs:**
- Remove "quantum mass body" → use "field object" or "electron" (concrete)
- Remove "within" vs "between" spatial framing
- Simplify the "two scales" explanation
- Don't over-state "propagates at speed c" (they know this)
- Focus on Field Origin enabling field closure, trust reader on rest

---

### Location 2: Definition Box
**Line:** 470-476
**Section:** Key Concepts definition box
**Current problems:**
- Title: "Two Propagation Scales" (creates dichotomy)
- "Field coupling" vs "Field propagation" (better than within/between but still creates framework)
- Uses s=0, s=±1 parameters (too technical for definition box)
- "TetA-TetB coupling provides nonlinear boundary" (jargon)
- "All field objects maintain closure through Field Origin" (good, keep this idea)

**Current text:**
```
\noindent\textbf{Two Propagation Scales:}
\begin{itemize}[leftmargin=1.5em,itemsep=1pt,topsep=2pt]
\item \textbf{Field coupling} ($s = 0$): Field closure settles through Field Origin at
$r = 0$ where $\tau_{\text{prop}} = 0$. TetA-TetB coupling provides nonlinear boundary
enabling Full State Snapshot. All field objects maintain closure through Field Origin.
\item \textbf{Field propagation} ($s = \pm 1$): Fields propagate causally at speed $c$
through $k = 4$ face channels. Information about field changes travels at light speed
through spacetime.
\end{itemize}

\noindent Both scales necessary: propagation governs how fields move through spacetime;
coupling governs how fields settle into closed configurations. Every field object couples
through its Field Origin.
```

**Needs:**
- Maybe remove "Two Propagation Scales" title entirely?
- Or rename to just "Field Origin" and keep it simple
- Remove s=0, s=±1 parameters (too technical)
- Remove "TetA-TetB coupling" jargon
- Keep the good parts: "All field objects," "Every field object couples through Field Origin"
- Simplify drastically - this is just defining Field Origin for undergrads

---

### Location 3: Section 4.4 (Polynomial States Discussion)
**Line:** ~826
**Section:** After explaining polynomial in TetA, Field Origin, TetB
**Current problems:**
- Long paragraph explaining "propagation regime" vs "coupling regime"
- Somewhat technical but context-appropriate (just defined polynomial states)
- Generally GOOD framing (functional, not spatial)
- Maybe slightly repetitive on "propagates causally at speed c"

**Current text:**
```
This structural distinction has a physical consequence. As established in
Section~\ref{subsec:origin}, the Field Origin enables coherent field configurations by
providing a coupling point where $\tau_{\text{prop}} = 0$. Meanwhile, FC$_{\Sigma}$
propagates causally at speed $c$ through the $k = 4$ face channels. The three structural
states map onto this physics: TetA and TetB represent propagation through spatial extent
(causal, requiring $r > 0$), while the Field Origin represents the coupling boundary where
coherence is established (structural, at $r = 0$). One is linear transport through channels;
the other is nonlinear coupling at a point. The state coefficient $s$ does not merely count
active channels. It distinguishes whether the field operates in the propagation regime
($s = \pm 1$, where face channels carry information causally) or the coupling regime
($s = 0$, where the boundary enforces coherence). Both regimes are necessary: propagation
governs how fields move through spacetime; coupling governs how fields settle into coherent
configurations.
```

**Assessment:**
- Actually mostly GOOD - uses functional framing ("propagation regime" vs "coupling regime")
- Context-appropriate (explaining polynomial states just defined)
- Could be slightly simplified but not urgent
- Maybe: "enables coherent field configurations" → "enables field configurations to couple with ambient field" (more relational)

**Needs:**
- Minor: Add relational framing ("couple with ambient field")
- Otherwise mostly correct

---

### Location 4: Section 9.1 (Mass-Energy Conversion)
**Line:** 1194-1196
**Section:** Discussing Field Origin in context of electron mass
**Current problems:**
- "quantum mass body" used multiple times (jargon)
- Long, complex paragraph mixing several ideas
- "at tile scale" still appears in one spot
- Generally tries to explain too much at once

**Current text (line 1194):**
```
Now consider what happens during mass-energy conversion. The preceding equations describe
how much energy mass contains. The next question is: in what form does that energy emerge?
Energy stored at the Field Origin must propagate outward through the bimetric structure.
But first, observe what the Field Origin enables for field object configurations at all
scales. As established in Sections~\ref{subsec:origin} and~\ref{subsec:states}, field
closure requires Full State Snapshot: all components of a field object configuration must
achieve consistent state simultaneously during FC$_{\Sigma}$. FC$_{\Sigma}$ propagates
causally at speed $c$ through spacetime. Meanwhile, the Field Origin enables field objects
to couple with the ambient field at $\tau_{\text{prop}} = 0$, regardless of whether the
configuration spans a single tile or many tiles.
```

**Current text (line 1196):**
```
The tile has characteristic scale $r$, which for the electron is the Compton wavelength
$r \sim h/(mc) \approx 2.4 \times 10^{-12}$ m. This is the gravity topology scale where
electrons manifest. For FC$_{\Sigma}$ to complete across this tile, all parts of the field
object configuration must read consistent state simultaneously. If this Full State Snapshot
were limited by causal propagation at speed $c$, field closure could not complete:
information would require time $\tau \sim r/c$ to traverse the tile, but FC$_{\Sigma}$
must complete in a single snapshot. Partial reads produce inconsistent state; FC$_{\Sigma}$
is atomic. The Field Origin resolves this constraint: at $r = 0$, where
$\tau_{\text{prop}} = 0$, all field components of the quantum mass body couple through
the nonlinear boundary simultaneously, enabling the Full State Snapshot that FC$_{\Sigma}$
requires. This is not internal electron coherence. Electrons are manifestations of gravity
topology at tile scale. Rather, this is field closure operating on the field object
configuration that constitutes the quantum mass body. Meanwhile, field propagation occurs
causally at speed $c$ through the face channels. Both scales are necessary: the Field
Origin (coupling regime, $s = 0$) enables Full State Snapshot for all field objects, while
causal propagation (propagation regime, $s = \pm 1$) governs how fields move through
spacetime.
```

**Assessment:**
- Line 1194 is actually pretty GOOD now (says "at all scales" correctly!)
- Line 1196 is LONG and complex
- Multiple uses of "quantum mass body" (should use "electron" in this context)
- "all field components of the quantum mass body couple" (sounds internal, should be relational)
- Generally correct physics, just wordy and uses jargon

**Needs:**
- Replace "quantum mass body" with "electron" (we're specifically talking about electrons here)
- Simplify the long explanation
- Make relational: "couple with ambient field" not just "couple"
- Trust reader more, explain less

---

## SUMMARY

**4 Main Locations:**
1. **Line 447** - Introduction/Full State Snapshot explanation
2. **Line 470-476** - Definition box (PRIMARY TARGET)
3. **Line 826** - Section 4.4 polynomial states discussion (mostly good)
4. **Line 1194-1196** - Section 9.1 mass-energy conversion (wordy, uses jargon)

**Common issues across all:**
- "Quantum mass body" jargon (use "electron" or "field object")
- Sometimes sounds internal ("components couple") rather than relational ("couples with ambient field")
- Over-stating "propagates at speed c" (obvious from relativity)
- Creating "two scales" framework when simpler explanation would work

**Simplification priorities:**
1. **HIGHEST:** Definition box (lines 470-476) - most visible, sets tone
2. **HIGH:** Introduction (line 447) - first explanation, creates mental model
3. **MEDIUM:** Section 9.1 (lines 1194-1196) - wordy, uses jargon, but context is electrons
4. **LOW:** Section 4.4 (line 826) - mostly correct, just minor tweaks

---

**Ready to discuss simplification approach for each location?**
