# Readable Prose Framework

**Goal:** Prose that reads like a human wrote it: easy to follow, strong at transferring knowledge, not robotic or procedural, and not verbose. Use this when drafting or revising so the reader finishes with "this read so nicely."

---

## 1. Why Prose Sounds Robotic (and How to Fix It)

| Red flag | Why it feels off | Fix |
|----------|------------------|-----|
| **"We add X" / "We apply Y"** | Sounds like a methods checklist, not a narrative. No reason or lead-in. | Give a motive or pivot: "To test the framework further, we turn to NGC 3198..." or "NGC 3198 offers a canonical test case..." |
| **Repeated "the same"** | Feels like a form: "the same A and the same B and the same C." | Use once, then list: "the same equation, G, and a0" or "unchanged G and a0." |
| **Back-to-back short declarations** | "No parameters are fitted. Three galaxies, one formula." Reads like bullets. | Weave into one sentence: "No parameters are fitted: three galaxies, one formula, zero free parameters." |
| **No connective before a figure** | "Figure 2 shows that..." drops in without linking. | Add a light bridge: "As Figure 2 shows," or "In Figure 2, the same equation..." |
| **Subject–verb–object only** | Every sentence = "We do X. We do Y." Monotone. | Vary: lead with purpose ("To ..."), with the object ("NGC 3198, the canonical case, ..."), or with the result ("As Fig. 2 shows, ..."). |
| **Jargon stacks** | Many technical terms in one phrase. | Unpack in order: one concept per clause; use the known–new pattern (see below). |

---

## 2. Core Principles (Evidence-Based)

### 2.1 Flow: Two Levels

- **Global (coherence):** Ideas in a clear order (e.g. result → example → implication). Use signposting so the reader knows where they are.
- **Sentence-level (cohesion):** Each sentence links to the last. Known/given information first, new information second (given–new contract).

### 2.2 Given–New Contract

- **Rule:** Start the sentence with what the reader already has in mind; put the new point at the end.
- **Why:** New info at the end is easier to attach to working memory; the start anchors it to what they already know.
- **Pattern:** The "new" at the end of sentence N often becomes the "given" at the start of sentence N+1 (chain).

### 2.3 Rhythm

- **Mix length:** Short and long sentences. Avoid long runs of similar length.
- **Strong verbs:** Prefer concrete verbs over nominalizations ("we measured" vs "we performed a measurement of" when the former is enough).
- **Active voice (where natural):** "We turn to NGC 3198" reads more clearly than "NGC 3198 is now considered" unless you have a reason for passive.

### 2.4 Clarity Without Bloat

- **Concrete subjects:** "The same equation yields" not "It can be seen that the application of the same equation yields."
- **One main idea per sentence:** If a sentence does two things, consider splitting or tightening.
- **No false depth:** Adding words does not add rigor; clarity does.

---

## 3. Practical Checklist (Use When Editing)

**Before publishing or sending a draft, scan for:**

- [ ] **Openings:** Does the paragraph or section start with a clear purpose or pivot (why we do this, why this object), not just "We add/apply/consider X"?
- [ ] **Repetition:** Same phrase repeated ("the same ... the same ...")? Reduce to one clear statement.
- [ ] **Figure/equation links:** Is the figure or equation introduced with a small bridge ("As Fig. 2 shows," "From Eq. 5,") so it feels connected?
- [ ] **Staccato:** Three or more short, declarative sentences in a row? Weave one into the next or add a colon/semicolon so it reads as one thought.
- [ ] **Slogan-like lines:** "Three galaxies, one formula." Standalone? Either make it the punchline of a full sentence or fold it into the previous sentence.
- [ ] **Given–new:** Does each sentence start with something the previous sentence set up (or the section title)? If not, add a word or reorder.
- [ ] **Rhythm:** Read aloud. Does it sound like a person explaining, or like a list? Vary sentence length and structure where it feels flat.

---

## 4. Example: Before and After (NGC 3198 Paragraph)

**Before (robotic):**  
"We add a third galaxy: NGC 3198, the canonical rotation-curve test case in dark matter studies, with well-measured HI kinematics and independently inferred baryonic mass. Figure 2 shows that the same equation and the same G and a0 yield a velocity-decoded mass (solid green) consistent with the known baryonic content and well below the LambdaCDM enclosed mass (red dotted). No gravitational parameters are fitted. Three galaxies, one formula, zero free parameters."

**After (readable):**  
"To test the framework further, we turn to NGC 3198, the canonical rotation-curve case in dark matter studies, with well-measured HI kinematics and independently inferred baryonic mass. As Fig. 2 shows, the same equation, G, and a0 yield a velocity-decoded mass (solid green) that tracks the known baryonic content and stays well below the LambdaCDM enclosed mass (red dotted). No gravitational parameters are fitted: three galaxies, one formula, zero free parameters."

**Changes applied:** motive in the first sentence; "As Fig. 2 shows" for linkage; one "same" + list; closing merged with a colon; "tracks" and "stays" for a slightly more natural verb choice.

---

## 5. Tone: Teach from Authority, Not from Defence

**Principle:** When you argue for something that is already established (textbook, cited literature), you accidentally signal that it needs defending. The reader's brain flips into adversarial mode. In a pedagogical document, state the physics, cite it, and move on. Do not try to convince.

### 5.1 Textbook and Protected Physics

- **If it is textbook:** Before claiming something is textbook or "already in the literature," do a quick check (e.g. search) to confirm it. Then state it and use it. Do not try to convince the reader it is true.
- **Textbook tone:** A textbook does not say "we will now demonstrate that triangles have three sides." It says "a triangle has three sides" and moves on. The reader who does not know that is not the audience; the reader who does absorbs it and keeps reading.
- **No pincer, no invitation to doubt:** Avoid "from above, from below," "why X and not Y?," or "this is the only way to satisfy..." when the point is standard. Those framings acknowledge that doubt is reasonable and invite it.

### 5.2 Phrases That Invite Doubt (Cut in Pedagogical Prose)

Every time you say "this is not fitted," "this is not a model," "this is not an assumption," or "not chosen," you are telling the reader that someone might think it is. In a letter or response to referees, such phrases can be strategic. In a teaching document aimed at readers who have the background, they are counterproductive.

| Defensive pattern | Why it backfires | Fix |
|------------------|------------------|-----|
| "That decomposition is not optional" | Arguing. | State: "The metric decomposes as ...; the tetrad is the unique local Minkowski frame satisfying the equivalence principle." |
| "You already know that ..." | Slightly condescending and defensive ("please don't argue"). | State the fact: "The metric must remain non-degenerate, det(g) ne 0." |
| "X you already accept" / "one more fact you already accept" | Pre-empting disagreement rather than stating a fact. | Drop the framing: "LIGO adds one more fact. Gravitational waves propagate at c, so ..." |
| "this is not a model / not fitted / not an assumption" | Signals you expect the reader to suspect otherwise. | Omit. If the walk-through is clean, the reader sees there are no extra assumptions. |
| "with no extra assumptions" | Same. | Cut. |
| "There is no gap between X and Y" | Closing argument. | Let the chain of steps speak; end on the last step. |
| "Everything from Step 1 through ... is either textbook GR or cited literature" | Courtroom closing. A textbook does not end by saying "everything I just taught you is real physics." | End on the final step or result. The chain speaks for itself. |
| Repeating "zero-parameter" (or similar) many times | In a letter it can be deliberate; in a pedagogical doc it starts to sound like a sales pitch. | Use once or twice where it matters; then let the content carry it. |

### 5.3 Checklist (Pedagogical or Essentials Documents)

- [ ] **Textbook claims:** If you say something is textbook or standard, have you verified it (e.g. quick search)? Then state it; do not try to convince.
- [ ] **Defensive openings:** "We do not introduce ...," "This is not optional," "You already know ..."? Replace with a direct statement.
- [ ] **Defensive closings:** Does the section or document end with a "so everything I said is valid" sentence? Cut it; end on the last substantive step or result.
- [ ] **Doubt-inviting phrases:** Scan for "not a model," "not fitted," "not an assumption," "not chosen," "no extra assumptions." Remove unless strategically needed (e.g. for referees).
- [ ] **Repetition of a selling point:** "Zero-parameter," "no free parameters," etc. If it appears more than once or twice, trim so the document teaches rather than sells.

---

## 6. One-Sentence Summary

**Readable = one clear idea per sentence, given–new order, varied rhythm, and a reason or link (not just "we add X") so the reader feels guided, not processed. In pedagogical work, add: state textbook and protected physics, cite it, use it; verify when in doubt; do not defend or convince.**

Use this framework when drafting or revising; it pairs with the main Writing Framework (Understand → Plan → Write → Format) as the "readable prose" lens in the Write stage.
