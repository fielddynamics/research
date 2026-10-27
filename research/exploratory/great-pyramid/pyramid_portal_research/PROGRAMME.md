# The Giza Field-Resonator Programme

**Programme definition document — version 1.0 (October 2026)**
**Principal investigator:** Stephen Nelson, Field Dynamics Research
**Theoretical basis:** Gravity Field Dynamics (GFD), [`research/llms.txt`](../../../llms.txt) and [`docs/`](../../../../docs/README.md)

---

## 1. Thesis

The Great Pyramid of Khufu was designed as a **field-coupled resonant structure**. Its components are proposed to work as one system:

- **Gilded capstone:** a field concentrator at the apex, coupling the structure to the natural electric and magnetic fields of the Earth–atmosphere system.
- **Limestone body:** a dielectric that shapes and guides those fields.
- **King's Chamber:** a granite resonator at the structure's working core, lined entirely with quartz-bearing Aswan granite.
- **Coffer, relieving compartments, Grand Gallery, antechamber and shafts:** tuning, filtering and coupling elements, whose proportions encode the integer structure of the GFD framework (K = 4, the band integers 13, 17 and 21, and α).

GFD supplies the quantitative structure: which proportions should appear, which frequencies should dominate, and how strongly the structure should couple. The programme's purpose is to turn this thesis into measurements that can be made non-invasively, with predictions fixed in advance, so that each result either strengthens the foundation or redirects it.

The central argument, how the GFD Field Origin is realised at the King's Chamber from the measured architecture, is set out in [`FIELD_ORIGIN_KINGS_CHAMBER.md`](FIELD_ORIGIN_KINGS_CHAMBER.md).

## 2. Evidence base

The programme builds on the following established observations. Each entry is a documented fact about the monument; the interpretation in the right-hand column is the programme's.

| # | Observation | Source | Significance for the thesis |
|---|---|---|---|
| E1 | **Gilded capstones were part of royal pyramid practice.** Reliefs on Sahure's causeway, about two generations after Khufu, show a gilded pyramidion being brought to the pyramid. Gold traces are reported on Queen Udjebten's pyramidion. | Hawass & Verner, *MDAIK* 52 (1996); Verner (2001) | A conductive metal apex is historically grounded, not invented |
| E2 | **The King's Chamber is built entirely of granite.** It has 100 granite wall blocks, a granite floor and nine granite roof beams; everywhere else the builders used limestone. | Petrie (1883) §51–55 | The one all-granite room is a deliberate material choice. Granite is quartz-bearing, and quartz is piezoelectric |
| E3a | **The chamber sits on the pyramid's half-section plane.** Its floor (1691.4–1693.7 in above the base) is at the level where the horizontal section is exactly half the base area (1691.7 ± 1.8 in). | Petrie §148 | The structure's own equal-partition (μ = ½) plane, the defining property of the Field Origin |
| E3 | **The chamber has exact geometry.** Its proportions are 20 : 10 : 5√5 royal cubits, with end-wall diagonal 15 and space diagonal 25 (a 3-4-5 triangle). | Petrie §155; `04.2` | An integer diagonal requires the irrational height √5. The proportions are designed, not incidental |
| E4 | **The coffer-to-chamber volume ratio is 137.17,** within 0.1% of 1/α = 137.036 (±0.4% measurement uncertainty, floor-to-ceiling height). The coffer's interior is half its exterior. | Petrie §155–156; `04.3` | A dimensionless match to the fine-structure constant inside the resonator |
| E5 | **The pyramid is aligned to true north** to within an average of 3′38″ of arc. | Dash (2015 survey) | An alignment precision far beyond what a tomb requires; it sets a defined axis for field coupling |
| E6 | **The shafts have a paired architecture.** The King's Chamber shafts are open to the outside at both ends. The Queen's Chamber shafts are sealed at both ends, behind the chamber wall and by stone slabs fitted with **copper pins**. | Vyse (1837); Dixon (1872); Gantenbrink (1993); Djedi (2011) | Open signal channels against sealed reference channels, with metal fittings deep inside the structure |
| E7 | **The pyramid contains large unexplained voids.** These are the Big Void above the Grand Gallery (≥30 m) and the North Face Corridor. | ScanPyramids, *Nature* 552 (2017); *Nat. Commun.* (2023) | Internal volume whose function is unknown, and which any resonant model must include |
| E8 | **The structure is precision-built at scale.** The base is level to ~2 cm and squared to ~12″, and Petrie compared the casing joints to "opticians' work". | Petrie (1883); Dash (2015) | Engineering tolerances of the kind a functioning field device would need |
| E9 | **The GFD framework is quantitatively successful.** The same integer structure predicts G to 12 ppm and the galactic radial acceleration relation to 0.181 dex. | [`papers/`](../../../../papers/) | The framework applied to the pyramid has independent empirical support |

## 3. Prior work

The programme stands on a lineage of research that treated the Great Pyramid as more than a tomb, and on mainstream survey work that supplies its data.

- **W. M. F. Petrie, *The Pyramids and Temples of Gizeh* (1883).** The primary metrological source for every interior dimension used here.
- **Christopher Dunn, *The Giza Power Plant* (1998).** The direct predecessor of this programme. Dunn argued that the pyramid was an acoustic and electromagnetic machine centred on a resonant granite King's Chamber. The present programme gives that idea a quantitative theoretical framework and a measurement plan. Graham Hancock has presented and discussed Dunn's thesis.
- **Joseph Davidovits; Barsoum, Ganguly & Hug, *J. Am. Ceram. Soc.* 89 (2006).** Evidence that some casing and upper blocks have microstructures consistent with reconstituted (cast) limestone. If confirmed, it shows the builders controlled their materials at the microstructural level.
- **Rudolf Gantenbrink, Upuaut Project (1992–93); Pyramid Rover (2002); Djedi (2010–11).** Robotic exploration of the shafts, the source of E6.
- **ScanPyramids (2015–present).** Muon radiography of the interior, the source of E7.
- **Glen Dash (2015 survey).** Modern base and orientation survey, the source of E5.

## 4. Hypotheses and pre-registered predictions

Each hypothesis states what the thesis predicts, how it will be measured, and the result that would count as confirmation or disconfirmation. The thresholds are fixed now, before any data are taken. That is what gives a positive result its force.

| ID | Hypothesis | Measurement | Confirms | Disconfirms | Detail |
|---|---|---|---|---|---|
| H1 | The coffer's exterior volume is α × the chamber's volume (floor to ceiling) | Laser survey of chamber and coffer, ≤0.05% volume uncertainty | ratio 137.04 ± 0.10 | ratio outside 137.04 ± 0.30 | `04.3`, `07.2` |
| H2 | The chamber's acoustic spectrum carries ℤ₂₁ = ℤ₃ × ℤ₇ structure | Swept-sine and impulse acoustic survey, 1 Hz–2 kHz, with the two shafts modelled | a 21-member comb with ℤ₃ and ℤ₇ sub-structure, at significance ≥ 5σ against a rectangular-cavity null model | the measured spectrum fits the null model | `07.1` |
| H3 | The chamber is a high-Q resonator | Ring-down of the principal modes | Q ≥ 10³ in at least one low mode | Q < 10² in all modes | `04.2`, `05.3` |
| H4 | The capstone was gilded | Non-destructive XRF surface analysis of the summit platform stones and of fallen apex-zone casing fragments | gold above the local background, in a distribution consistent with an apex fitting | no gold above background in any apex-zone sample | `05.2`, `07.6` |
| H5 | The structure couples to the geomagnetic field | Three-axis fluxgate magnetometers in the King's Chamber, the Queen's Chamber and outside, logged continuously for 12 months | a chamber/exterior transfer function that departs from the passive-limestone model, correlated with K-index | the transfer function matches the passive model | `05.1`, `07.5` |
| H6 | The granite resonator converts mechanical to electromagnetic energy | Broadband E-field and RF probes in the chamber, synchronised with seismometers and acoustic sensors | a coherent E-field response at the chamber's acoustic mode frequencies | no coherence above instrument noise | `05.2`, `05.5` |
| H7 | Local gravity in the chamber departs from the mass model | Relative gravimetry (and gradiometry) in the chamber against the 3D mass model | a residual above the mass-model uncertainty, at the sign and scale given in `05.4` | residual consistent with zero | `05.4` |
| H8 | The shafts define a 3D address frame | Robotic 3D survey of all four shafts | out-of-plane components sufficient to give a non-degenerate Gram matrix | shafts coplanar within survey error | `04.7` |
| H9 | Some blocks are cast, not cut | Independent blind petrography and microstructure of authorised samples from casing, core and upper blocks | reconstituted microstructure confirmed by at least two independent labs | all samples natural limestone | §3 |

H1, H3, H8 and H9 test the evidence base directly. H2, H5, H6 and H7 test the thesis as a working system. H4 tests the capstone.

## 5. Theory and simulation (Phase 0)

Phase 0 needs no site access and should precede fieldwork, so that every prediction in §4 is computed before it is measured.

1. **Acoustic finite-element model** of the King's Chamber with both shafts, the cracked roof beams and the relieving stack. Output: the null-model spectrum for H2 and expected Q values for H3.
2. **Electromagnetic model of the whole pyramid** with a gilded capstone, including:
   - **The static geomagnetic field.** Gold is only weakly diamagnetic, so a gilded cap barely perturbs a static magnetic field. The model must establish the coupling path quantitatively rather than assume concentration.
   - **The atmospheric electric field.** The fair-weather potential gradient is ~100–150 V/m near the ground, and far higher in dust storms. A conducting apex 146 m up concentrates this field strongly, which makes it the most promising channel for capstone coupling. The model must compute the field enhancement, the corona onset and the power available from the air–earth current, which is ~2 pA/m² in fair weather.
   - **The low-frequency geomagnetic and Schumann bands**, for H5.
3. **Piezoelectric response of the granite lining.** This means the net electromechanical coupling of the chamber's granite under acoustic excitation, given the measured quartz content and grain-orientation statistics. It is needed to set the sensitivity required for H6.
4. **GFD predictions in final form.** These are the ℤ₂₁ mode assignment (`07.1`), the gravity residual (`05.4`) and the K=4→5 transition frequency (`08.1`), each fixed as a number with an uncertainty before Phase 1.

## 6. Work packages

| WP | Title | Scope | Hypotheses |
|---|---|---|---|
| WP1 | Metrology and survey | Laser scanning and photogrammetry of the King's Chamber, coffer, antechamber, Grand Gallery and relieving compartments; robotic shaft survey | H1, H8 |
| WP2 | Acoustics | Excitation and recording, mode identification, ring-down Q | H2, H3 |
| WP3 | Electromagnetics and geomagnetics | Magnetometer network, E-field and RF probes, atmospheric-field monitoring at the summit | H5, H6 |
| WP4 | Gravimetry | Relative gravimetry and gradiometry; 3D mass model with the ScanPyramids voids | H7 |
| WP5 | Materials | Summit XRF survey; petrography and microstructure of authorised samples | H4, H9 |
| WP6 | Theory and simulation | Phase 0 models; GFD prediction set; blind-analysis framework | all |
| WP7 | Data and open science | Pre-registration, public data release, independent replication | all |

## 7. Phasing

| Phase | Duration | Access | Content | Exit criterion |
|---|---|---|---|---|
| 0 | 6–12 months | none | WP6 complete; predictions fixed and published; instrument specifications set | pre-registration document published |
| 1 | 3–6 months | non-invasive, short campaigns | WP1 survey, WP2 acoustics, WP5 summit XRF | H1, H2, H3, H4 evaluated |
| 2 | 12 months | non-invasive, long-term logging | WP3 network, WP4 gravimetry | H5, H6, H7 evaluated |
| 3 | as authorised | robotic and sampling | shaft survey (H8); petrography (H9) | H8, H9 evaluated |

## 8. Methods standards

The programme adopts the practices that give large-collaboration results their credibility:

- **Pre-registration.** The Phase 0 prediction set, with thresholds, is published with a timestamp before any measurement.
- **Blind analysis.** Where possible, analysts fit spectra and residuals without knowing the predicted values, and unblind only after the analysis is frozen.
- **Null models.** Every claimed signal is tested against an explicit conventional model: a rectangular granite cavity, a passive limestone body, or a mass-only gravity model.
- **Significance.** Claims of a new effect require ≥ 5σ against the null model; 3σ results are reported as evidence, not discovery.
- **Open data.** Raw data, code and models are released under open licences alongside every result.
- **Independent replication.** H1, H2 and H9 are designed so that a second team with its own instruments can repeat them.

## 9. Access, ethics and conservation

All fieldwork is non-invasive except H9, which uses only samples authorised and supplied by the antiquities authorities. Work in Egypt requires permits from the Ministry of Tourism and Antiquities and is best undertaken in partnership with Egyptian institutions and an established mission. Instruments are free-standing or reversibly mounted, and no measurement alters the monument.

## 10. Deliverables

1. Pre-registered prediction set (end of Phase 0).
2. Survey dataset of the chamber, coffer and shafts, with the H1 result (Phase 1).
3. Acoustic dataset and mode analysis, with the H2 and H3 results (Phase 1).
4. Summit material survey, with the H4 result (Phase 1).
5. Twelve-month field-monitoring dataset, with the H5, H6 and H7 results (Phase 2).
6. Programme report and peer-reviewed publications for each work package, with all data released.

## 11. How this document relates to the compendium

The rest of this compendium is the programme's technical basis:

- the GFD algebra, in sections `01`–`03` and `06`;
- the chamber-by-chamber analysis, in `04`;
- the field-coupling physics, in `05`;
- the detailed test protocols, in `07`;
- the open theoretical questions, in `08`;
- the measured data and sources, in `99_appendices/`, especially Appendix E.

Where a component has been tested already against existing data, the result is recorded in its file. The coffer ratio matches. The relieving-compartment volume formula does not, and needs a new formulation before WP1 measures the volumes.

---

*Sources for the evidence base:*

- W. M. F. Petrie (1883), [online text](https://www.ronaldbirdsall.com/gizeh/petrie/).
- Sahure reliefs: [Pyramid of Sahure (Wikipedia)](https://en.wikipedia.org/wiki/Pyramid_of_Sahure).
- Pyramidia: [List of Egyptian pyramidia (Wikipedia)](https://en.wikipedia.org/wiki/List_of_Egyptian_pyramidia).
- Shafts: [Star shaft (Wikipedia)](https://en.wikipedia.org/wiki/Star_shaft).
- Orientation, base and ScanPyramids: [Great Pyramid of Giza (Wikipedia)](https://en.wikipedia.org/wiki/Great_Pyramid_of_Giza).
- Cast-limestone evidence: [Barsoum et al. (2006)](https://ceramics.onlinelibrary.wiley.com/doi/abs/10.1111/j.1551-2916.2006.01308.x).
