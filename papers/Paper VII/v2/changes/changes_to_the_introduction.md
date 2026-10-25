# Changes to the Introduction

## Writing Framework Stage 1: UNDERSTAND

### Reader State Entering

- **Knows:** Constants are measured but unexplained. This paper explores topology as the source.
- **Expects:** "Show me. What topology? What does it predict?"

### Reader State Exiting

- **Knows:** G was derived from the stellated octahedron. The chain d=3 -> (3+1) -> 21 -> G. The polynomial f(k) = 1 + k + k^2 formalizes this chain. f(4) = 21.
- **Ready for:** "The Deeper Why" (why does this geometry exist?) and the rest of the paper.

### Connects To

- **Previous:** Abstract (reader knows the headline results).
- **Next:** "The Deeper Why" subsection asks why the geometry exists. Later, the Field Origin section (Plan C) will recall f(k) and show that the same polynomial evaluated at three vortex positions gives 21, 17, and 13.

---

## Writing Framework Stage 2: PLAN (Internal Only)

**PURPOSE:** Plant the polynomial f(k) = 1 + k + k^2 in the reader's mind, right next to the G equation, so it is available for recall later.

**CORE CONCEPTS:**
1. Every integer in G traces to d = 3 (the chain)
2. The chain is a polynomial: f(k) = 1 + k + k^2

**EXIT CRITERIA:**
- Reader has f(k) in mind
- Reader connects f(4) = 21 to the exponent in G
- Reader is ready for "This derivation raises a question..."

**TENSION ARC:** "The equation works. But where do the integers come from?"

---

## Writing Framework Stage 3: WRITE

### Location

After line 116 ("The prediction agrees with measurement to 0.12%, with zero adjustable parameters.") and before line 118 ("This result raises a question...") in [Published/Paper VII/v2/Dual_Tetrad_Gravity_And_The_Field_Origin.tex](../Dual_Tetrad_Gravity_And_The_Field_Origin.tex).

### What to Add

Two to three sentences using the Equation Sandwich (motivation -> equation -> interpretation):

**MOTIVATION:** "Every integer in Eq.~\eqref{eq:G} traces to one source: the dimensionality of space. The companion paper established the chain: $d = 3$ requires $(3+1)$ coupling faces, which generates the hierarchy $1 + (3+1) + (3+1)^2 = 21$~\cite{paper6}."

Note: Do NOT start with "The companion paper established..." as line 111 already opens with "The companion paper." Instead, lead with the claim ("Every integer traces to one source") and let the cite come at the end of the chain.

**EQUATION:** "This hierarchy is a polynomial. Defining $k = (3+1) = 4$:
$$f(k) = 1 + k + k^2$$"

**INTERPRETATION:** "The exponent in $G$ is $f(4) = 1 + 4 + 16 = 21$."

That's it. No time states, no 17/13, no vortex. The polynomial is planted. The reader carries it forward.

### What to Change on Existing Text

**Line 118:** Change "This result raises a question" to "This derivation raises a question."

**Why:** Before the plan, "This result" clearly referred to "The prediction agrees with measurement to 0.12%." With the polynomial now inserted between line 116 and line 118, "This result" becomes ambiguous (does it mean the 0.12% prediction or the polynomial?). Changing to "This derivation" makes the referent unambiguously the entire G derivation, not just the polynomial.

### What NOT to Include

- No middle coefficient variation (that comes in the Field Origin section, Plan C)
- No time states, no vortex language
- No derivation of 17/13
- Keep it to 2-3 sentences maximum -- just the chain and the polynomial

---

## Writing Framework Stage 4: FORMAT

- Equation uses \begin{equation} environment with \label{eq:polynomial} for later cross-reference
- No em dashes
- No defensive language
- Academic register throughout
- "We" voice if needed, but these sentences are declarative and may not need it

---

## Summary of Changes

1. **Insert after line 116:** 2-3 sentences (chain + polynomial + f(4)=21)
2. **Line 118:** "This result" -> "This derivation"

## Files to Edit

- [Published/Paper VII/v2/Dual_Tetrad_Gravity_And_The_Field_Origin.tex](../Dual_Tetrad_Gravity_And_The_Field_Origin.tex) lines 116-118
