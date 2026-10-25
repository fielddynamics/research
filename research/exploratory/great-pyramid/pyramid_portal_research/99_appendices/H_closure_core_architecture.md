# Closure Core 256 Architecture

**Purpose.** This document describes a buildable architecture for the proposed closure algebra primitive:

\[
\textbf{cube outside, hexagon inside, Sierpinski by tensor lift.}
\]

The implementation is provided in `closure_core256.py`.

---

## 1. The primitive: an 8-state hypercube node

The base node is a 3-cube:

\[
\{-1,+1\}^3.
\]

It has 8 vertices:

\[
2^3=8.
\]

Those same 8 vertices are also the outer vertices of the **stella octangula**, the compound of two parity-conjugate tetrahedra.

Define the parity character:

\[
\chi_{123}(x)=x_1x_2x_3.
\]

Then:

\[
\chi_{123}=+1
\]

selects one tetrahedron, and:

\[
\chi_{123}=-1
\]

selects the other.

So the node begins as:

\[
8=4+4.
\]

This is the geometric carrier.

---

## 2. Walsh/Clifford basis

The 3-cube has 8 Walsh basis functions:

\[
1,\quad x_1,\quad x_2,\quad x_1x_2,\quad x_3,\quad x_1x_3,\quad x_2x_3,\quad x_1x_2x_3.
\]

These are identified with the Clifford basis of \(\mathrm{Cl}(3,0)\):

\[
1,\quad e_1,\quad e_2,\quad e_{12},\quad e_3,\quad e_{13},\quad e_{23},\quad I=e_{123}.
\]

The grade split is:

\[
1+3+3+1.
\]

Meaning:

| Grade | Basis | Count |
|---|---|---:|
| 0 | scalar \(1\) | 1 |
| 1 | vectors \(e_1,e_2,e_3\) | 3 |
| 2 | bivectors \(e_{12},e_{13},e_{23}\) | 3 |
| 3 | pseudoscalar \(I\) | 1 |

---

## 3. Hexagon/Eisenstein interior

Project the cube along the body diagonal \((1,1,1)\).

Two vertices collapse onto the axial line:

\[
(+,+,+),\quad (-,-,-).
\]

The other six vertices form a regular hexagon.

So the same 8-state node has an internal split:

\[
8=2+6.
\]

The two axial states correspond to:

\[
\langle 1,I\rangle.
\]

The six middle states form three Hodge-paired vector/bivector channels:

\[
(e_1,e_{23}),\quad(e_2,e_{31}),\quad(e_3,e_{12}).
\]

Each pair is treated as an Eisenstein coordinate:

\[
z_k=x_k+y_k\omega,\qquad \omega^2+\omega+1=0.
\]

Therefore the node is:

\[
\boxed{
A_3=\langle1,I\rangle\oplus\mathbb Z[\omega]^3.
}
\]

This is the key architectural statement.

---

## 4. What a node computes

A node takes three sign bits:

\[
x_1,x_2,x_3\in\{-1,+1\}.
\]

It computes the Walsh feature vector:

\[
[1,x_1,x_2,x_1x_2,x_3,x_1x_3,x_2x_3,x_1x_2x_3].
\]

Given 8 coefficients \(c_0,\ldots,c_7\), its raw score is:

\[
y=c_0+c_1x_1+c_2x_2+c_3x_1x_2+c_4x_3+c_5x_1x_3+c_6x_2x_3+c_7x_1x_2x_3.
\]

Boolean readout is:

\[
\operatorname{sign}(y).
\]

So externally:

\[
3\text{ bits in}\rightarrow 1\text{ bit out}.
\]

Internally:

\[
8\text{ coefficients}=2\text{ axial}+3\text{ Eisenstein pairs}.
\]

---

## 5. Closure phase

The closure operator \(\Omega\) fixes the axial pair and multiplies each Eisenstein channel by \(\omega\).

For a channel:

\[
z=x+y\omega,
\]

multiplication by \(\omega\) is:

\[
\omega z=-y+(x-y)\omega.
\]

So the pair update is:

\[
(x,y)\mapsto(-y,x-y).
\]

This gives:

\[
\Omega^3=1,
\]

and on the middle six-dimensional sector:

\[
\Omega^2+\Omega+1=0.
\]

The closure projection is:

\[
P_\Omega=\frac13(1+\Omega+\Omega^2).
\]

The sweep product is:

\[
a\star b=P_\Omega(ab),
\]

where \(ab\) is the Clifford product.

Interpretation:

\[
\boxed{
\text{Clifford product followed by Eisenstein closure projection.}
}
\]

---

## 6. SierpinskiTile64: two nodes tensored

The next object is:

\[
\boxed{
\text{SierpinskiTile}_{64}=A_3\otimes A_3.
}
\]

Dimension:

\[
8\times8=64.
\]

This is the same scale as a 6-cube or LUT-6:

\[
2^6=64.
\]

At the channel-family level, one node is:

\[
1+3,
\]

where:

- \(1\) = axial family,
- \(3\) = three Eisenstein families.

Therefore:

\[
(1+3)^2=16.
\]

The two-node tile has 16 channel families:

\[
1+3+3+9.
\]

Since each family has \(2\times2=4\) real dimensions:

\[
16\times4=64.
\]

The code reports this as:

\[
64=4+12+12+36.
\]

Meaning:

| Family type | Dimension |
|---|---:|
| axial ⊗ axial | 4 |
| axial ⊗ hex | 12 |
| hex ⊗ axial | 12 |
| hex ⊗ hex | 36 |
| total | 64 |

---

## 7. Face/rank-2 decomposition: the 40/24 split

For \(K=4\), each face has a rank-2 interaction space:

\[
K^2=16.
\]

This splits into symmetric and exterior parts:

\[
\dim \mathrm{Sym}^2 W=\frac{K^2+K}{2}=10,
\]

\[
\dim \Lambda^2 W=\frac{K^2-K}{2}=6.
\]

Therefore, per face:

\[
16=10+6.
\]

With \(K=4\) faces:

\[
4\times16=64.
\]

So one 64-state Sierpinski tile has:

\[
64=40+24.
\]

Specifically:

\[
4\times10=40,
\]

\[
4\times6=24.
\]

Architecturally:

\[
\boxed{
\text{one 64-tile}=
\text{four faces}\times
(\text{10 symmetric}+\text{6 exterior}).
}
\]

---

## 8. Coupling polynomial

The coupling polynomial is:

\[
f(K,s)=K^2+sK+1.
\]

At \(K=4\):

\[
f(4,+1)=21,
\]

\[
f(4,0)=17,
\]

\[
f(4,-1)=13.
\]

The symmetric and exterior tangent shadows are:

\[
\frac{21-1}{2}=10,
\]

\[
\frac{13-1}{2}=6.
\]

This exactly matches the per-face rank-2 split:

\[
10+6=16.
\]

The product is:

\[
21\cdot13=273.
\]

And:

\[
273=4^4+4^2+1=|\mathbb P^2(\mathbb F_{16})|.
\]

So the same structure appears three ways:

| Layer | Symmetric/base | Exterior/quotient |
|---|---:|---:|
| coupling polynomial | \(21\) | \(13\) |
| tangent shadow | \(10\) | \(6\) |
| four-face tile | \(40\) | \(24\) |

---

## 9. ClosureCore256: four Sierpinski tiles

The architecture then lifts one 64-tile into a four-tile core:

\[
\boxed{
\text{ClosureCore}_{256}=4\times \text{SierpinskiTile}_{64}.
}
\]

Dimension:

\[
4\times64=256.
\]

This matches the number of all Boolean truth tables on three inputs:

\[
2^{2^3}=256.
\]

So the architecture is:

\[
\boxed{
4\times(A_3\otimes A_3)=256.
}
\]

Each tile has:

\[
40+24=64.
\]

Four tiles have:

\[
4\times40=160,
\]

\[
4\times24=96.
\]

Therefore:

\[
256=160+96.
\]

---

## 10. Full architecture diagram

```text
ClosureCore256
│
├── Tile64 #1 = A3 ⊗ A3
│   ├── 4 faces
│   ├── 40 symmetric channels
│   └── 24 exterior channels
│
├── Tile64 #2 = A3 ⊗ A3
│   ├── 4 faces
│   ├── 40 symmetric channels
│   └── 24 exterior channels
│
├── Tile64 #3 = A3 ⊗ A3
│   ├── 4 faces
│   ├── 40 symmetric channels
│   └── 24 exterior channels
│
└── Tile64 #4 = A3 ⊗ A3
    ├── 4 faces
    ├── 40 symmetric channels
    └── 24 exterior channels

Total:
    4 × 64 = 256
    160 symmetric
    96 exterior
```

---

## 11. How hypercube, stella octangula, hexagon, and Sierpinski fit together

| Object | Role |
|---|---|
| 3-cube | external 8-state carrier |
| stella octangula | parity split \(8=4+4\) |
| Walsh basis | executable coefficient basis |
| Clifford algebra | orientation/twisted multiplication |
| hexagon | body-diagonal projection of the six middle states |
| Eisenstein pairs | internal closure phase channels |
| \(A_3\) node | \(2\) axial \(+\;3\) Eisenstein pairs |
| \(A_3\otimes A_3\) | 64-state Sierpinski/LUT-6 tile |
| four faces | \(4\times16=64\) rank-2 channels |
| coupling polynomial | \(21/17/13\) closure shells |
| \(40/24\) | four-face symmetric/exterior split |
| four tiles | 256-state closure core |
| Sierpinski recursion | \(S(D+1,K)=K^2S(D,K)+1\) |
| projective plane | \(S(3,4)=273=|\mathbb P^2(\mathbb F_{16})|\) |

---

## 12. Best one-line summary

\[
\boxed{
\text{Build it as four }64\text{-state Sierpinski tiles, each tile being }A_3\otimes A_3,
\text{ where }A_3\text{ is an 8-state cube node with a hexagonal Eisenstein interior.}
}
\]

Even shorter:

\[
\boxed{
\textbf{cube node} \rightarrow \textbf{tensor tile} \rightarrow \textbf{four-face Sierpinski core}.
}
\]
