# TetB packing and the Walsh closure read

## Source and scope

Read the GFD [valence-shell walk](https://github.com/fielddynamics/research/blob/1d73ef8ad10000861a25e1c67e58ddcfc4f563ad/research/matter/research/gfd_valence_shells_synthesis.md) and [Paper XIII](https://github.com/fielddynamics/research/blob/1d73ef8ad10000861a25e1c67e58ddcfc4f563ad/papers/13-nuclear-binding-bidirectional-sst/letter.tex). The former describes a 64-address nested walk and a 21-node landmark score; the latter uses a bound coupling sum. Here we prove an address-space identity, not a physical Hamiltonian or a new nuclear prediction. The explicit test uses contiguous base-four prefix filling (corners then gate in each digit); the earlier note also mentions a global gate-depth threshold at 27, which is not the same ordering. The exact prefix-block theorem holds independently of the order of visiting whole blocks.

## Fixed address space

Let $b(w)$ be occupancy on $w\in\mathbb F_2^6$, grouped into three two-bit digits, and $H=H_4^{\otimes 3}$. The raw Walsh register is $c=Hb$ and reconstruction is $b=Hc/64$. Each digit sweep is the same fixed four-way transform. For a prefix of length $d$, a completely filled subtree has indicator $b_p(w)=\mathbf1[w_{<d}=p]$. The character sum over each free suffix digit vanishes unless its Walsh index is zero. Consequently $c(a)=0$ when any suffix index is nonzero. Completed four-cell channels have no finest-grade detail; completed sixteen-cell faces have only coarse detail; full 64-cell occupancy has only the common mode. Partial fills need not be invariant under the simultaneous rotation; a rotation average preserves total occupancy but loses anisotropic detail.

![Packing and read](figures/packing_walsh_bridge.svg)

## Exact accounting and conservation

With normalized $W=H/8$, $\|Wb\|^2=\|b\|^2$. For binary occupancy with count $A$, $c_0=A$, and $\sum_{a\ne0}c_a^2=64A-A^2$. The three grade energies are differences of squared norms of conditional-mean projections: $\|P_db\|^2=\sum_{p:|p|=d}(\sum_{w\succeq p}b_w)^2/4^{3-d}$ and $\|(P_d-P_{d-1})b\|^2=\|P_db\|^2-\|P_{d-1}b\|^2$. Grades have dimensions 3,12,48. The C3-invariant detail sector has dimensions 1,4,16 (plus one common coordinate), not one raw scalar per arbitrary local tree node. The 21 internal tree nodes each have three local contrasts. Invariant Walsh coordinates can be related by a change of basis, not identified with arbitrary raw counts.

At a single binary four-child node, occupancy 0 or 4 gives zero local contrast, occupancy 2 gives one nonzero Walsh contrast, occupancy 1 or 3 gives three. This is a spectral interpretation of the older 0/2/4 landmarks *for binary complete children only*, not a derivation of the full old closure score.

## Repeated closure

Represent full cycles by $b=k\mathbf1+r$, with residual register $r$. Then $c_0=64k+\sum r$ and $c_{a\ne0}=(Hr)_a$. If completed cycles are held in pointers instead, the same total count can be restored by adding their registered counts. Uniform inventory is invisible to the contrast read but not to the common read. A contrast-only gravitational source would vanish at a full cycle, so a viable mass register must also retain common inventory, binding energy or equivalent independent information. For binary occupancy the normalized total detail energy $A(64-A)/64$ peaks halfway and vanishes at both endpoints. This rules out identifying that energy alone with monotonically accumulated mass. Physical mass need not equal occupancy because binding energy matters.

## Implication

The same fixed address geometry supports TetB writing, spectral accounting and inverse reconstruction. A candidate vortex map is $\psi_* = \arg\min E(\psi,Wb,j)$, with $j$ the neighboring read and the geometry held fixed. The input register changes, not the geometry. Neither the address identity nor the inverse transform proves a physical Walsh implementation, an atomic shell law, $|t|^2=\alpha$, a collective determinant source, or G. A source-conserving bridge must preserve the common inventory or carry its equivalent pointer and independently justify the contrast-dependent response. The prior $17/13$ construction is unchanged and conditional.

[Offline explorer](interactive/packing_walsh.html) · [Exact verifier](verify_packing_walsh.py) · [Log](packing_walsh_verification_output.txt).
