# Proposed Changes - Field Closure Framing Update

## Summary of Findings

**Three locations need updating:**

1. **Lines 470-476** (Definition box) - PRIMARY TARGET
   - Uses spatial framing: "Within field objects" vs "Between field objects"
   - Status: NEEDS COMPLETE REWRITE

2. **Line 826** (Section 4.4 body text)
   - Uses correct "coupling regime" vs "propagation regime" ✓
   - BUT also uses spatial language: "within quantum mass bodies" vs "between separated field regions"
   - Status: NEEDS MINOR EDITS to remove spatial framing

3. **Line 1196** (Section 9.1 body text)
   - Uses correct "coupling regime" vs "propagation regime" ✓
   - BUT ends with: "within field object configurations" vs "between configurations"
   - Status: NEEDS MINOR EDIT at end of sentence

---

## CHANGE 1: Definition Box (Lines 470-476)

### Current Text (INCORRECT - spatial framing):
```latex
\noindent\textbf{Two Propagation Scales:}
\begin{itemize}[leftmargin=1.5em,itemsep=1pt,topsep=2pt]
\item \textbf{Within field objects} ($s = 0$): Field Origin at $r = 0$ where $\tau_{\text{prop}} = 0$. Propagation is instantaneous (no time delay). Enables Full State Snapshot of the unified configuration.
\item \textbf{Between field objects} ($s = \pm 1$): FC$_{\Sigma}$ propagates causally at speed $c$ through $k = 4$ face channels. Information travels at light speed between separated objects.
\end{itemize}

\noindent Both scales necessary: propagation at speed $c$ ensures causal consistency between separated objects; Field Origin ($\tau_{\text{prop}} = 0$) enables atomic coupling within each unified configuration.
```

### Proposed Text (CORRECT - functional framing):
```latex
\noindent\textbf{Two Propagation Scales:}
\begin{itemize}[leftmargin=1.5em,itemsep=1pt,topsep=2pt]
\item \textbf{Field coupling} ($s = 0$): Field closure settles through Field Origin at $r = 0$ where $\tau_{\text{prop}} = 0$. TetA-TetB coupling provides nonlinear boundary enabling Full State Snapshot. All field objects maintain closure through Field Origin.
\item \textbf{Field propagation} ($s = \pm 1$): Fields propagate causally at speed $c$ through $k = 4$ face channels. Information about field changes travels at light speed through spacetime.
\end{itemize}

\noindent Both scales necessary: propagation governs how fields move through spacetime; coupling governs how fields settle into closed configurations. Every field object couples through its Field Origin.
```

### Character count:
- Current: ~475 characters
- Proposed: ~485 characters
- Difference: +10 characters (acceptable - within tolerance)

### Key changes:
- ✅ Removed "Within" and "Between" spatial framing
- ✅ Changed to functional framing: "Field coupling" vs "Field propagation"
- ✅ Emphasized that ALL field objects use Field Origin (not just some)
- ✅ Clarified: coupling = how fields settle, propagation = how fields move
- ✅ Maintained undergraduate readability
- ✅ Kept technical accuracy (TetA-TetB, nonlinear boundary)

---

## CHANGE 2: Line 826 Context (Section 4.4)

### Current Text (mixed framing):
```latex
This structural distinction has a physical consequence. As established in Section~\ref{subsec:origin}, the Field Origin enables coherent field configurations within quantum mass bodies by providing a coupling point where $\tau_{\text{prop}} = 0$. But between separated field regions, FC$_{\Sigma}$ propagates causally at speed $c$ through the $k = 4$ face channels.
```

### Proposed Text (functional framing):
```latex
This structural distinction has a physical consequence. As established in Section~\ref{subsec:origin}, the Field Origin enables coherent field configurations by providing a coupling point where $\tau_{\text{prop}} = 0$. Meanwhile, FC$_{\Sigma}$ propagates causally at speed $c$ through the $k = 4$ face channels.
```

### Key changes:
- ✅ Removed "within quantum mass bodies" (spatial framing)
- ✅ Removed "between separated field regions" (spatial framing)
- ✅ Changed "But between" → "Meanwhile" (removes spatial contrast)
- ✅ Maintains same meaning: Field Origin provides coupling, FC_Σ propagates at c
- ✅ Shorter by ~15 characters

### Note:
The rest of line 826 is already CORRECT - it uses "propagation regime" and "coupling regime" which is the functional framing we want. Only the beginning of the sentence needs this small fix.

---

## CHANGE 3: Line 1196 Context (Section 9.1)

### Current Text (mixed framing):
```latex
Both scales are necessary: the Field Origin (coupling regime, $s = 0$) enables Full State Snapshot within field object configurations, while causal propagation (propagation regime, $s = \pm 1$) governs interactions between configurations.
```

### Proposed Text (functional framing):
```latex
Both scales are necessary: the Field Origin (coupling regime, $s = 0$) enables Full State Snapshot for all field objects, while causal propagation (propagation regime, $s = \pm 1$) governs how fields move through spacetime.
```

### Key changes:
- ✅ Changed "within field object configurations" → "for all field objects"
- ✅ Changed "interactions between configurations" → "how fields move through spacetime"
- ✅ Removes spatial framing (within/between)
- ✅ Emphasizes functional distinction (coupling vs movement)
- ✅ Similar character count (±5 characters)

### Note:
Most of line 1196 is already CORRECT - it uses "coupling regime" and "propagation regime". Only the final phrase needs updating to remove the "within"/"between" spatial language.

---

## Additional Context Check

### Line 1194 (just before 1196):
Current text mentions:
```
FC$_{\Sigma}$ propagates causally at speed $c$ between separated field regions. But within a quantum mass body (a field object configuration at the tile scale), the Field Origin enables the Full State Snapshot read at $\tau_{\text{prop}} = 0$.
```

This ALSO uses spatial framing ("between" and "within"). Should we update this too?

### Proposed fix for line 1194:
```
FC$_{\Sigma}$ propagates causally at speed $c$ through spacetime. Meanwhile, the Field Origin enables the Full State Snapshot read at $\tau_{\text{prop}} = 0$ for field objects at the tile scale.
```

**Decision:** YES, update line 1194 as well since it's in the same paragraph and uses the same problematic framing.

---

## Summary of All Changes

### Total changes: 4 locations

1. **Lines 470-476** (Definition box): Complete rewrite to functional framing
2. **Line 826** (Section 4.4): Remove "within"/"between" from opening sentence
3. **Line 1194** (Section 9.1): Remove "between"/"within" spatial framing
4. **Line 1196** (Section 9.1): Change ending to functional framing

### Consistency achieved:
- ✅ All locations use "coupling regime" vs "propagation regime"
- ✅ No spatial framing ("within"/"between") anywhere
- ✅ Functional framing throughout: coupling = settle, propagation = move
- ✅ Clear message: ALL field objects use Field Origin for coupling
- ✅ Undergraduate readable
- ✅ Technically accurate per Hassan-Rosen and MTW/Wald

---

## Implementation Order

Execute changes in this order:

1. **First:** Update definition box (lines 470-476)
   - Most visible location
   - Sets the standard for rest of paper
   - User will see this change immediately

2. **Second:** Update line 826 (Section 4.4)
   - Remove spatial framing from opening sentence
   - Rest of paragraph already correct

3. **Third:** Update line 1194 (Section 9.1)
   - Remove "between"/"within" from this sentence

4. **Fourth:** Update line 1196 (Section 9.1)
   - Update ending phrase
   - Completes the paragraph update

After each change:
- ✅ Verify LaTeX compiles
- ✅ Check page count (should stay at 94)
- ✅ Read context to ensure no logical gaps

---

**Ready for:** Step 5 (Surgical implementation)
**Verification:** All changes preserve meaning, update framing, maintain readability
**Risk:** Low - changes are localized and well-defined
