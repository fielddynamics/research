# Field Closure Fix Plan

## Reference
**Correct definitions:** `FIELD_CLOSURE_CORRECT_DEFINITIONS.md`

## Problem Statement

The paper currently uses problematic framing in some places that suggests:
1. Field Origin only works at tile scale (WRONG - works at all scales)
2. Settlement happens "within" field objects (WRONG - happens between configuration and ambient field)
3. Spatial distinction: "within" vs "between" field objects (WRONG - should be functional: coupling vs propagation)

## Correct Understanding (Summary)

**TetA → Field Origin → TetB** is ONE unified structure

**Two aspects (always both present):**
1. **Field propagation** (s = ±1): FC_Σ propagates at speed c through spacetime
2. **Field coupling** (s = 0): Settlement through Field Origin between configuration and ambient field

**Key points:**
- Field Origin works at ALL scales (electron to galaxy cluster)
- Multi-tile configurations use Field Origin for settlement
- Settlement is relational: configuration ↔ ambient field (not internal)
- Both aspects necessary everywhere

---

## Step 1: Search Strategy

Search the main paper for problematic phrases:

### A. Scale Restriction Phrases
These would incorrectly limit Field Origin to small scales:
- "at the tile scale"
- "tile scale"
- "quantum mass bodies at" (when followed by scale restriction)
- "for quantum mass bodies" (when implying only QMB, not all field objects)

### B. Spatial Framing Phrases
These create within/between spatial dichotomy:
- "within field objects"
- "within field object"
- "within quantum mass"
- "between field objects"
- "between separated"
- "between field regions"

### C. Internal vs Relational Language
These might suggest internal coupling rather than relational:
- "all field components of a field object couple" (sounds internal)
- "components couple simultaneously" (without mentioning ambient field)

### D. Good Phrases (Keep These)
These are CORRECT framing to preserve:
- "coupling regime" and "propagation regime"
- "at all scales"
- "regardless of scale"
- "field objects of any size"

---

## Step 2: Expected Scope

**Files to search:**
- `Dual_Tetrad_Gravity_And_The_Field_Origin.tex` (main paper, ~2700 lines)

**Sections most likely to have issues:**
- Early definitions (Section 1-2)
- Field Origin introduction (Section 4)
- Two Propagation Scales discussions
- Mass-energy conversion section (Section 9)

**Already changed (may need reverting or fixing):**
- Line 466: Field Origin definition
- Lines 470-476: Two Propagation Scales definition box
- Line 826: Section 4.4 discussion
- Line 1194: Mass-energy conversion discussion
- Line 1196: Both scales necessary statement

---

## Step 3: Proposed Approach

### Option A: Systematic Search First (Recommended)
1. Search for all problematic phrases
2. Generate report showing every instance with context
3. Categorize: CRITICAL vs MINOR vs ACCEPTABLE
4. Review findings with user
5. Make targeted fixes only where needed
6. Verify PDF compiles and page count maintained

### Option B: Section-by-Section Review
1. Review Section 1 (Introduction)
2. Review Section 4 (Field Origin)
3. Review Section 9 (Mass)
4. Review definitions boxes
5. Make fixes section by section
6. More time-consuming, but thorough

### Option C: Revert and Restart
1. Revert all changes made
2. Start fresh with correct understanding
3. Make only essential changes
4. Cleaner but loses some work already done

**Recommendation: Option A** - Most efficient, allows user to see full scope before committing to changes

---

## Step 4: Search Queries to Run

If we proceed with Option A, run these Grep searches:

1. `"at the tile scale"` - find scale restrictions
2. `"tile scale"` - broader search
3. `"within field object"` - spatial framing (singular)
4. `"within field objects"` - spatial framing (plural)
5. `"within quantum mass"` - spatial framing (QMB variant)
6. `"between field object"` - spatial framing (singular)
7. `"between field objects"` - spatial framing (plural)
8. `"between separated"` - spatial framing (separated variant)
9. `"coupling regime"` - verify CORRECT usage preserved
10. `"propagation regime"` - verify CORRECT usage preserved

**Output:** Create comprehensive report showing:
- Line number
- Context (±3 lines)
- Classification: CRITICAL / HIGH / MEDIUM / LOW / OK
- Suggested fix (if needed)

---

## Step 5: Decision Criteria

**CRITICAL (must fix):**
- Statements that directly contradict correct physics
- "Field Origin only at tile scale" type statements
- Scale restrictions that are factually wrong

**HIGH (should fix):**
- Spatial framing that obscures relational nature
- Missing clarification about scale independence
- Ambiguous language that could mislead

**MEDIUM (nice to fix):**
- Suboptimal wording that's not wrong but could be clearer
- Missing emphasis on key points

**LOW (leave as is):**
- Context-appropriate language (e.g., discussing electron specifically)
- Correct statements that happen to use similar words
- Places where change would disrupt flow without adding clarity

---

## Step 6: Verification After Changes

After any changes:
1. ✅ LaTeX compiles without errors
2. ✅ Page count = 94 pages (no change)
3. ✅ All equations render correctly
4. ✅ Cross-references still work
5. ✅ No new inconsistencies introduced
6. ✅ Definitions consistent with body text
7. ✅ PDF looks correct when opened

---

## Questions for User Before Proceeding

1. **Scope:** Should we search entire paper or focus on known problem sections?

2. **Approach:** Option A (systematic search), B (section-by-section), or C (revert and restart)?

3. **Threshold:** What level of issues should we fix? (Only CRITICAL, or also HIGH/MEDIUM?)

4. **Already-changed text:** Should we review what I already changed for correctness, or start fresh?

5. **Priority:** Are there specific sections you're most concerned about?

---

## Current Status

**Definitions file:** ✅ Created (FIELD_CLOSURE_CORRECT_DEFINITIONS.md)

**Changes already made:**
- Line 466: Field Origin definition (changed to mention ambient field)
- Lines 470-476: Two Propagation Scales (removed within/between, added functional framing)
- Line 826: Removed some spatial framing
- Line 1194: Changed "at the tile scale" to "at all scales" (FIXED CRITICAL ERROR)
- Line 1196: Changed ending to functional framing

**Concerns:**
- Changes were made reactively without full scope assessment
- May have missed other instances
- Don't know full extent of the problem yet

---

## Recommended Next Step

**Run systematic search** (Step 4) to assess full scope, then present findings to user before making any additional changes.

This will show:
- How many instances exist
- Where they are
- How serious each one is
- What the full scope of work would be

Then we can make informed decision about how to proceed.

---

**Awaiting user approval to proceed with searches.**
