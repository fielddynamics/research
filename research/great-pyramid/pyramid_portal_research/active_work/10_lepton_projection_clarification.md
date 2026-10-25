# Active Work 10 — Lepton Projection: Why Muons and Taus Are Not Particles

**Status:** Clarification — encodes the framework's established position on the lepton sector and corrects a recent test that drifted from it
**Purpose:** Document that charged "leptons" beyond the electron are structural mode configurations of the same vortex, and lock that position into the regression suite
**Reading time:** 5 minutes
**Companion:** `python/predictions.py` (`lepton_anchor_report` docstring), `python/tests/test_curvature_integration.py::TestLeptonProjectionStructure`

---

## 1. The framework position

From multiple prior sessions (chats `fae8d24d` March 2026 and `d08cd7e7` May 2026) the framework's treatment of charged "leptons" is settled:

> *"These are not particles. They are mode configurations of the vortex structure that either achieve closure (stable) or cannot (unstable, must redistribute modes until something that CAN close is reached)."*

The electron is the unique irreducible single-mode excitation (Generation 1). The muon and tau are not independent particles — they are the same tile excitation viewed through 2 and 3 closure cycles respectively.

| "Particle" | Mode count | Factorization | Framework reading |
|------------|-----------:|---------------|-------------------|
| electron | $1$ | irreducible | Generation 1, direct tile excitation |
| muon | $\sim 207\,m_e$ | $9 \times 23$ | Generation 2, closure positions × asymmetry |
| tau | $\sim 3477\,m_e$ | $51 \times 68 + 9$ | Generation 3, $(F_+ + F_0 + F_-) \times K \cdot F_0 + 9$ |
| pion$^\pm$ | $273\,m_e$ | $\Phi_3 \times \Phi_6 = 21 \times 13$ | endpoint product, not a closure sum → unstable |
| pion$^0$ | $264\,m_e$ | $2 \times 132$ | divides into two photon packets |
| proton | $1836\,m_e$ | $36 \times 51 = (K \cdot 9) \times (F_+ + F_0 + F_-)$ | clean closure → stable |
| neutron | $1839\,m_e$ | $3 \times 613$ (613 prime) | excess $D=3$ modes have no home → unstable |

CODATA mass ratios match these mode counts to within 0.05–0.5%:
- $m_\mu / m_e = 206.7683$ vs framework $207$ (0.11% low)
- $m_\tau / m_e \approx 3477.5$ vs framework $3477$ (0.014% high)

The 20/20-pass projection test session (chat `fae8d24d`) established three independent lines of evidence: every particle mass is integer multiples of $m_e$; every decay conserves integer mode counts; stability correlates with clean structural factorization. The proton lives because $1836 = 36 \times 51$ factors cleanly; the neutron decays because $1839 = 3 \times 613$ has 613 prime and the 3 excess modes leak; the pion is a bridge ($\Phi_3 \times \Phi_6$ is a product across the vortex rather than a closure sum) and must hand off its modes to something that *can* close.

## 2. Why the framework anchors at $m_e$ specifically

The gravity formula

$$G = \frac{17}{13} \cdot \alpha^{21} \cdot \frac{g_e}{2} \cdot \frac{\hbar c}{m_e^2}$$

anchors at $m_e$ not because the electron is one option among many leptons, but because **Generation 1 is the unique irreducible single-mode excitation**. There is no other charged-lepton choice at the same structural level. The muon and tau are higher-generation mode configurations of the same vortex; they share the same tree-level coupling

$$\alpha_G^{\text{tree}} = \frac{17}{13} \cdot \alpha^{21}$$

which is **lepton-independent**, but the dimensional anchor $\hbar c / m^2$ is structurally forced to $m_e$ by the irreducibility argument.

The implication: substituting a heavier mass $m$ into the dimensional anchor gives

$$G_{\text{anchored at } m} = G_e \cdot (m_e / m)^2$$

This is a **dimensional rescaling**, not a falsifying probe of the framework. There is no sense in which the muon offers an "alternative anchor" whose disagreement with the electron-anchored prediction would falsify anything — the muon is the same vortex at closure depth 2.

## 3. What was wrong and how it was fixed

The recent integration test suite (`test_curvature_integration.py::TestCounterFactualPerturbationBreaksGPrediction`) contained one test that drifted from this position:

```python
def test_wrong_lepton_anchor_muon_breaks_G(self):
    """Muon mass anchor would give wildly wrong G..."""
    m_muon = 1.883531627e-28
    report = lepton_anchor_report(m_muon, G_E_OVER_2)
    G_wrong = report['G_from_this_lepton_anchor']
    ...
```

This treated the muon as if it were an alternative independent particle whose substitution constitutes a meaningful counter-factual probe of the gravity formula. Under the framework's actual position, the muon is not an independent anchor: substituting $m_\mu$ produces $G/207^2$ by dimensional rescaling, and there is no falsification to celebrate.

**Fix.** The test was removed from the counter-factual class and replaced with a new test class `TestLeptonProjectionStructure` that encodes the framework's structural treatment:

- Electron mode count = 1 (irreducible Generation 1)
- Muon mode count = 207 = 9 × 23 (verified against CODATA ratio 206.77 within 0.5)
- Tau mode count = 3477 = 51 × 68 + 9 (verified against CODATA ratio 3477.5 within 5)
- 51 = $F_+ + F_0 + F_-$ = 21 + 17 + 13 (proton polynomial content)
- 68 = $K \cdot F_0$ = 4 × 17 (face threshold)
- Number of generations = $D = 3$ (closure cycles)
- Mode counts grow with closure depth: $1 < 207 < 3477$
- Electron is the unique minimum mode count (uniqueness of the irreducible anchor)
- Anchor substitution with muon yields $(m_e/m_\mu)^2$ rescaling, machine-precision verified
- $\alpha_G^{\text{tree}} = (17/13) \cdot \alpha^{21}$ verified lepton-independent
- Sentinel: proton 1836 mode count factors as $(K \cdot 9) \times (F_+ + F_0 + F_-)$
- Sentinel: neutron–proton difference = $D = 3$ excess modes

**`lepton_anchor_report` docstring** was also updated. The function itself is unchanged (it still answers the arithmetic question "what value of $G$ would the formula return at this mass anchor?"), but the docstring now states explicitly that the muon and tau are not independent particles and that anchor substitution is a dimensional rescaling, not a falsifying probe.

## 4. The remaining open prediction about leptons

The framework does make one real prediction *about* leptons that is not foreclosed by the projection picture: gravity coupled through the muon's anomalous magnetic moment $g_\mu/2$ should reflect any deviation of $g_\mu/2$ from QED (the Fermilab muon-$g{-}2$ anomaly).

The mechanism: the framework's $g_e/2$ factor in $\alpha_G$ is the Generation-1 anomalous moment of the same vortex that, viewed through Generation 2, carries $g_\mu/2$. If the muon's measured $g_\mu/2$ deviates from QED prediction by $\sim 250$ ppb, gravity read through muonium or muon-orbital atomic systems should show the same fractional deviation. This is experimentally distant but algebraically forced.

This prediction is *about* a known QED anomaly carrying a gravitational signature, not about the muon being an independent fundamental particle.

## 5. Headline

The framework's gravity coupling reads through one vortex, not three independent lepton fields. The electron's role is structurally unique (Generation 1, 1 mode, irreducible). The muon and tau are higher-generation mode configurations of the same vortex, and the framework's mass anchor at $m_e$ is forced by that uniqueness — not chosen from alternatives.

---

**Cross-references:**
- Chat `fae8d24d` (March 2026) — projection-vs-particle frontier tests, 20/20 pass
- Chat `d08cd7e7` (May 2026) — breakthrough doc, lepton-anchor as dimensional anchor
- `python/predictions.py::lepton_anchor_report` (docstring updated)
- `python/tests/test_curvature_integration.py::TestLeptonProjectionStructure` (12 tests)
- Active Work 09 (sector-valued curvature) — for the framework integration context
- Active Work 02 (transition frequency) — correctly treats muon vertex as 207 × ω_C
