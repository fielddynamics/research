# Field Closure Update Plan

## Goal
Update Paper VII v5 to correctly frame the two propagation scales as **functional** (propagation vs coupling) rather than **spatial** (within vs between field objects).

**Reference:** See `FIELD_CLOSURE_DEFINITIONS.md` for complete technical understanding.

---

## Core Issue

**Current (incorrect) framing:**
- "Within field objects": Field Origin provides instantaneous coupling
- "Between field objects": FC_Σ propagates at speed c

**Problem:** This suggests FC_Σ happens differently in two spatial regimes, but actually ALL field closure happens through Field Origin (TetA-TetB coupling).

**Correct framing:**
- **Field propagation** (at speed c): How fields MOVE through spacetime
- **Field coupling** (at Field Origin): How fields SETTLE and achieve closure
- Both aspects present everywhere, distinction is functional not spatial

---

## Locations to Update

### 1. Definition Table (Lines 454-476) - PRIMARY TARGET

**Current text:**
```latex
\noindent\textbf{Two Propagation Scales:}
\begin{itemize}[leftmargin=1.5em,itemsep=1pt,topsep=2pt]
\item \textbf{Within field objects} ($s = 0$): Field Origin at $r = 0$ where $\tau_{\text{prop}} = 0$. Propagation is instantaneous (no time delay). Enables Full State Snapshot of the unified configuration.
\item \textbf{Between field objects} ($s = \pm 1$): FC$_{\Sigma}$ propagates causally at speed $c$ through $k = 4$ face channels. Information travels at light speed between separated objects.
\end{itemize}

\noindent Both scales necessary: propagation at speed $c$ ensures causal consistency between separated objects; Field Origin ($\tau_{\text{prop}} = 0$) enables atomic coupling within each unified configuration.
```

**Issues:**
- Uses spatial distinction: "Within" vs "Between"
- Suggests FC_Σ happens differently in the two regimes
- Conflicts with star-asteroid example (star can't maintain closure if FC_Σ with asteroid is at speed c)

**Proposed new text:**
```latex
\noindent\textbf{Two Propagation Scales:}
\begin{itemize}[leftmargin=1.5em,itemsep=1pt,topsep=2pt]
\item \textbf{Field propagation} ($s = \pm 1$): Gravitational fields propagate at speed $c$ through $k = 4$ face channels. Information about field changes travels at light speed, respecting causality.
\item \textbf{Field coupling} ($s = 0$): Field closure settles through the Field Origin at $r = 0$ where $\tau_{\text{prop}} = 0$. TetA-TetB coupling provides the nonlinear boundary enabling field closure $\det(e) \neq 0$.
\end{itemize}

\noindent Both scales necessary: propagation at speed $c$ governs how fields move through spacetime; Field Origin coupling governs how fields settle into closed configurations. Every field object maintains closure through its Field Origin.
```

**Character count check:**
- Current: ~420 characters
- Proposed: ~485 characters
- Need to tighten slightly to maintain similar length

**Tightened version:**
```latex
\noindent\textbf{Two Propagation Scales:}
\begin{itemize}[leftmargin=1.5em,itemsep=1pt,topsep=2pt]
\item \textbf{Field propagation} ($s = \pm 1$): Fields propagate at speed $c$ through $k = 4$ face channels. Information travels at light speed, respecting causality.
\item \textbf{Field coupling} ($s = 0$): Field closure settles through Field Origin at $r = 0$ where $\tau_{\text{prop}} = 0$. TetA-TetB coupling enables closure $\det(e) \neq 0$.
\end{itemize}

\noindent Both necessary: propagation governs how fields move; coupling governs how fields settle. All field objects maintain closure through Field Origin.
```

---

### 2. Line 447 Context - CHECK FOR CONSISTENCY

**Action:** Read surrounding context to verify it aligns with new framing.

**Expected content:** Discussion of Field Origin and how it resolves field closure.

**Check:** Does it use spatial framing (within/between) or functional framing (propagation/coupling)?

---

### 3. Line 826 - ALREADY CORRECT (verify and possibly reference)

**Current text (from summary):** Uses "coupling regime" (s=0) vs "propagation regime" (s=±1), states "One is linear transport through channels; the other is nonlinear coupling at a point"

**Action:**
- Verify this is correct
- Possibly add cross-reference to definition if not already present
- This is the CORRECT framing we want everywhere

---

### 4. Line 1196 - ALREADY CORRECT (verify and possibly reference)

**Current text (from summary):** "Both scales are necessary: the Field Origin (coupling regime, s = 0) enables Full State Snapshot within field object configurations, while causal propagation (propagation regime, s = ±1) governs interactions between configurations"

**Action:**
- Verify this is correct
- Check if "within field object configurations" and "between configurations" creates spatial framing issue
- If problematic, update to functional framing: "coupling regime settles closure" vs "propagation regime transports information"

---

## Search Strategy

### Step 3a: Find all instances of key phrases

Search for:
1. "Two Propagation Scales" (definition header)
2. "Within field objects" (spatial framing - should find 2-3)
3. "Between field objects" (spatial framing - should find 2-3)
4. "coupling regime" (correct framing - keep these)
5. "propagation regime" (correct framing - keep these)
6. "Field Origin" (verify all uses are consistent)

### Step 3b: Expected results (user estimate: 3 + definition table)
- Definition table (lines 454-476): PRIMARY UPDATE
- Line ~447: Check context
- Line ~826: Already correct (coupling regime vs propagation regime)
- Line ~1196: Check if needs update (may use spatial framing)

---

## Update Principles

### DO update:
- ✅ Change "Within field objects" → "Field propagation" or "coupling regime"
- ✅ Change "Between field objects" → "Field coupling" or "propagation regime"
- ✅ Emphasize functional distinction (move vs settle)
- ✅ Clarify that ALL field closure happens through Field Origin
- ✅ Use "coupling regime" and "propagation regime" consistently

### DON'T change:
- ❌ Don't add technical jargon (hyperbolic evolution, ADM constraints, etc.)
- ❌ Don't change places that already use correct framing ("coupling regime" vs "propagation regime")
- ❌ Don't increase length significantly (stay within ~1 line of current length)
- ❌ Don't change unrelated content

### Maintain:
- ✅ Undergraduate readability
- ✅ Clear physical intuition
- ✅ Consistency with bimetric gravity formalism (Hassan-Rosen)
- ✅ Consistency with tetrad gravity (MTW, Wald)

---

## Verification Steps

After making changes:

1. **LaTeX compiles:** PDF builds without errors
2. **Length check:** Total page count remains 94 pages (or ±0 pages)
3. **Consistency check:** All 4 locations use compatible framing
4. **Cross-reference check:** Definition table matches body text usage
5. **Technical accuracy:** Consistent with Hassan-Rosen bimetric gravity
6. **Readability:** Undergraduate-accessible language throughout

---

## Implementation Sequence

### Step 3: Find all instances
- Use Grep tool to search for key phrases
- Identify exact line numbers
- Read context around each instance (±10 lines)
- Categorize: needs update vs already correct

### Step 4: Design new prose
- For each instance needing update, draft new text
- Verify functional framing (propagation vs coupling)
- Check length against current text
- Ensure undergraduate readability

### Step 5: Make surgical changes
- Use Edit tool for each location
- Change one instance at a time
- Verify LaTeX compiles after each change
- Check PDF page count
- Verify no logical gaps introduced

---

## Key Messages to Preserve

1. **Two scales are both necessary**
   - Propagation ensures causal consistency
   - Coupling enables field closure

2. **Field Origin is universal**
   - Every field object has a Field Origin
   - Electron, asteroid, star, galaxy all maintain closure through their Field Origins
   - Nested hierarchies, each locally self-governing

3. **Distinction is functional, not spatial**
   - Propagation = how fields move (at speed c)
   - Coupling = how fields settle (through Field Origin)
   - Both aspects present everywhere

4. **Bimetric gravity foundation**
   - TetA and TetB couple nonlinearly
   - Coupling happens at Field Origin (r=0, τ_prop=0)
   - This is the mechanism for all field closure

---

## Success Criteria

- ✅ No spatial framing ("within" vs "between" removed)
- ✅ Functional framing consistent throughout ("propagation" vs "coupling")
- ✅ Definition table updated and clear
- ✅ All 3-4 body text instances consistent with new framing
- ✅ LaTeX compiles successfully
- ✅ Page count maintained (94 pages ±0)
- ✅ Undergraduate readable
- ✅ Technically accurate per Hassan-Rosen and MTW/Wald

---

**Plan created:** 2026-02-11
**Ready for:** Step 3 (Find all instances)
**Reference:** FIELD_CLOSURE_DEFINITIONS.md
