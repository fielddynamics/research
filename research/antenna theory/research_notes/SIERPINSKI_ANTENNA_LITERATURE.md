# Sierpiński antennas: what the engineering literature actually shows

This note records what measured and simulated Sierpiński antennas do, so GFD analogies rest on the real results and not on paraphrase. Full references are in `../SOURCES.md`.

## 1. The core measured result: a dyadic band ladder

- **Puente, Romeu, Pous, Garcia, Benitez (1996, *Electronics Letters*).** A printed Sierpiński gasket monopole built with five iterations was matched at five bands: 12.6, 6.4, 3.3, 1.62 and 0.64 GHz. The log-period was about a factor of two, the gasket's own scale factor.
- **Puente-Baliarda, Romeu, Pous, Cardama (1998, *IEEE TAP* 46(4) 517–524).** This is the standard reference. It compares the gasket with the single-band bow-tie of the same outline and shows that the geometry's self-similarity carries over into its electromagnetic behaviour. Computed current densities are also self-similar from band to band.
- **González-Arbesú, Puente, Romeu, Aguasca (1999).** Infrared thermograms measured the surface current directly and confirmed the self-similar distribution.
- **Puente et al. (1996, *Electronics Letters* 32(24)).** Perturbing the gasket (flare angle, scale factor) moves the log-period while keeping the multiband behaviour. The ratio is a design parameter, not a universal constant.
- **Puente, Borja, Navarro, Romeu (2000, *IEEE TAP* 48(5)).** A simple iterative network model reproduces the multiband behaviour and its change with flare angle.

**What GFD can use:** halving edges gives bands spaced by a factor of 2, and the active current at each band sits in a sub-gasket at the corresponding scale. Each band resonates on a self-similar copy of the whole.

## 2. Where the multiband behaviour really comes from

- **Best (2002, *IEEE AWPL*).** Most of the gasket's self-similar gap structure can be removed without much change to the multiband behaviour. What matters most is the periodic placement of the gaps **along the central axis through the feed**.
- **Hohlfeld and Cohen (1999, *Fractals*).** Working from symmetry arguments on Maxwell's equations, they showed that frequency independence needs **self-similarity *and* symmetry about the origin (the feed point)**. Self-similarity alone isn't enough, and self-complementarity gives only constant impedance.

**What GFD can use:** both results put the essential structure **at and around the feed**, the single point where the two arms meet. The gasket is self-similar about that point (tested in `antenna_engine.self_similar_about_feed`). In GFD terms the organising point is the Field Origin, not the bulk of the fractal. That is a genuine structural parallel, not a numerical coincidence.

## 3. The bow-tie and its two arms

A Sierpiński dipole is a bow-tie: two gasket arms meeting tip to tip at a feed gap. The arms have no conductive path between them; they are driven only at the feed. This is the clearest engineering image of two chambers coupled at one point. **The caution:** in a real antenna the arms also couple through the surrounding near field in space. GFD's claim is stronger (no spatial path at all), so the bow-tie is an analogy for the *feed-centred* structure, not a model of non-spatial coupling. The vertex model in `NONSPATIAL_RESONANCE_FIELD_ORIGIN.md` supplies the non-spatial part.

## 4. Complexity-tuned resonators (Marcelli)

Marcelli and colleagues (CNR-IMM) study equilateral triangular microwave resonators. They add Sierpiński internal complexity while keeping the edge length fixed, and the added complexity shifts and tunes the resonance frequency. Coupled triangles interact through their edges. The legacy tests drew on this work for the triangle mode labels (m+n+l=0) and the wavevector 4π/(3a). Those are properties of an equilateral triangular resonator's modes, not of the coupling polynomial (see `LEGACY_AUDIT.md`).

## 5. Three-dimensional versions

Sierpiński tetrahedron antennas exist and have been built. Jun, Sanz-Izquierdo, Parker and Franco (Kent, 2017) metal-3D-printed one, and later work added "dual" and "dual inverse" Sierpiński variants. FDTD and equivalent-circuit studies examine how the building-block shape changes the frequency response. **No measured stellated-octahedron (two interpenetrating Sierpiński tetrahedra) antenna was found.** That is the geometry GFD actually needs, and it would be a natural experimental target.

## 6. What the literature does *not* contain

- No measurement of 2/17 (11.76%) as a transmission or impedance of any Sierpiński antenna. GFD treats 2/17 as an estimate of the screening filter, and the antenna literature gives it no independent support.
- No broadband behaviour in the strict sense. Sierpiński antennas are **multiband** (discrete, log-periodic bands), not continuously broadband.
- No link from antenna measurements to gravity. The literature supplies structure (dyadic bands, feed-centred self-similarity), not evidence about TetB.
