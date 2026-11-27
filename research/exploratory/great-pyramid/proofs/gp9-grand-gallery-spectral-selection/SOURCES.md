# GP-9 · Sources and input provenance

- W. M. F. Petrie, *The Pyramids and Temples of Gizeh* (1883), ch. VII §§44–48 and ch. XXI–XXII: [survey transcription](https://www.ronaldbirdsall.com/gizeh/petrie/c7.html), [design discussion](https://www.touregypt.net/petrie/c22.htm), [Petrie Project](https://petrieproject.com/book/the-pyramids-and-temples-of-gizeh). The virtual horizontal run 1688.9 in and roof horizontal run 1648.4 in are different. GP-1 adopts 5776 in height and 1692.55 in floor elevation. No precision interval for the run is invented here.
- L. Miatello, [Examining the Grand Gallery in the Pyramid of Khufu and its Features](https://giza.fas.harvard.edu/pubdocs/972/full/), *PalArch's Journal of Archaeology of Egypt/Egyptology* 7(6), 2010, pp. 1–36. [Text consulted](https://www.academia.edu/1915431/_Examining_the_Grand_Gallery_in_the_Pyramid_of_Khufu_and_its_Features_Palarch_archaeology_of_Egypt_Egyptology_7_6_2010_1_36), pp. 2–6. Supports normal-height ideal dimensions, alternating slot means, the terminal pair, and alternative archaeological interpretations. Does not establish acoustical intent. Detailed individual tier heights and centres are not transcribed from survey plates here. Model uses equal tiers and regular illustrative spacing. Sawtooth longitudinal roof and local niches are omitted.
- [Re-expansion method for circular waveguide discontinuities](https://pmc.ncbi.nlm.nih.gov/articles/PMC3292601/), modal matching and limits of plane-wave approximation; [finite 1D expansion-chamber structures](https://www.nature.com/articles/s41598-024-85002-x), transfer matrices and periodic filters. The mathematical derivations here are self-contained, not copied.
- [Resonant Chambers: Comparative impulse-response study inside the Great Pyramid of Khufu](https://doi.org/10.14236/ewic/EVA2026.35), EVA 2026. Identified as relevant measurement literature; no raw impulse responses used or claimed to validate the gallery model.
- GFD repository: [Grand Gallery kernel](../../pyramid_portal_research/04_apparatus_engineering/04.5_grand_gallery_kernel.md), [Antechamber filter](../../pyramid_portal_research/04_apparatus_engineering/04.6_antechamber_Z3_filter.md), [acoustic prediction](../../pyramid_portal_research/07_predictions_and_tests/07.1_acoustic_Z21_spectrum.md), [proofs](../). Original 21-mode cutoff assertion withdrawn elsewhere; no reuse. GP-6–8 supply methodological foundations, not acoustic/gravitational equivalence.

## Model input register

| Input | Value | Status |
|---|---:|---|
| cubit | 20.632 in | adopted from existing programme |
| floor to roof normal height | 15 cubits | approximate architectural ideal |
| bench height, central width | 1, 2 cubits | simplified model |
| widest section, roof width | 4, 2 cubits | ideal from survey summaries |
| upper tier height sum | 11 cubits | approximate; split equally for computation |
| gallery model length | 88 cubits | physical north-wall to Great Step ideal |
| virtual horizontal run | 1688.9 in | separate Petrie datum |
| ramp slot pairs | 27 (+1 terminal) | archaeological count |
| alternating mean lengths | 0.521 / 0.592 m | Miatello summary |
| width, depth | 0.14 / 0.18 m | approximate means |
| spacing | 1.67 m | illustrative, not surveyed centre list |
| air speed | 343 m/s | nominal, not measured onsite |
| end leads | 1 m² each | illustrative, not surveyed |

All simulations use stationary, linear, homogeneous air and perfectly rigid walls. No hidden coupling constants, fitted frequencies, GFD-specific transduction or alleged historical devices.
