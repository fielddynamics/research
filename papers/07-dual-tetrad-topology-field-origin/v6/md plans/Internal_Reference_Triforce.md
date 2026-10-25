# Internal Reference: Triforce Subdivision

**STATUS: INTERNAL RESEARCH DOCUMENT — NOT FOR PUBLICATION**

---

## Overview

This document describes the subdivision of each Merkaba face into 4 sampling regions. The naming convention ("Triforce") is excluded from publication due to its cultural associations.

---

## Face Subdivision Geometry

Each triangular face is subdivided by connecting edge midpoints, creating 4 smaller triangles:

```
        V1
        /\
       /  \
      /    \
     /  C1  \
    /________\
   /\   H   /\
  /  \     /  \
 / C3 \   / C2 \
/______\_/______\
V3              V2
```

Where:
- C1, C2, C3 = Corner regions (near vertices)
- H = Heart region (central triangle)

---

## Sampling Points

### Per Face
| Region | Location | Purpose |
|--------|----------|---------|
| C1 | Near V1 | Vertex gradient sample |
| C2 | Near V2 | Vertex gradient sample |
| C3 | Near V3 | Vertex gradient sample |
| HEART | Centroid | Face average sample |

### Total Structure
- 8 faces × 4 regions = **32 sampling points**
- Provides complete field gradient coverage
- Enables fine-grained closure tracking

---

## Coordinate Calculation

For a face with vertices (V1, V2, V3):

**Corner Centroids:**
- C1 centroid = (2V1 + V2 + V3) / 4
- C2 centroid = (V1 + 2V2 + V3) / 4
- C3 centroid = (V1 + V2 + 2V3) / 4

**Heart Centroid:**
- HEART = (V1 + V2 + V3) / 3

---

## Sampling Sequence

During field closure traversal:
1. Corner regions sample first (vertex activation)
2. Heart region samples last (face completion)
3. TIME faces complete before SPATIAL faces

---

## Information Content

Each sampling point can be addressed with:
- 3 bits for face (8 faces)
- 2 bits for region (4 regions)
- Total: 5 bits per sampling point
- 32 unique addresses

---

## Connection to Field Closure

The subdivision enables:
1. **Gradient Sampling**: Measure field changes across face
2. **Completion Detection**: Know when face fully traversed
3. **Phase Tracking**: Monitor relative phase between regions
4. **Resolution**: Finer granularity than vertex-only

---

## Why "Triforce" Name

The subdivision pattern visually resembles the Triforce symbol:
- 3 corner triangles
- 1 central triangle
- Self-similar recursive structure

This is purely geometric observation, not mystical connection.

---

## Why Excluded from Publication

1. Gaming/cultural associations
2. Distracts from physics content
3. Same information conveyed by "face subdivision"
4. Academic papers should avoid pop culture references

---

## Alternative Terminology for Publication

If subdivision is needed in paper, use:
- "Face quadrant sampling"
- "Corner-center subdivision"
- "Triangular face partitioning"

---

*Internal document — do not include in published paper*
