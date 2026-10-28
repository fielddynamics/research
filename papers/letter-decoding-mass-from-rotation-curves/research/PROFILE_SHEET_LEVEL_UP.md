# Level-up plan: Milky Way profile sheet to SPARC-style galaxy card

## 1. Header (title bar)

- **What:** Single title bar at top: "Milky Way" in large text; subtitle with morphological type (SBbc), distance (e.g. 8.2 kpc), total baryonic mass, data source (McMillan 2017).
- **How:** Reserve space in `GridSpec` (e.g. reduce `top` and add a row or use `fig.suptitle` + subtitle). Example:
  - `fig.suptitle('Milky Way', fontsize=16, y=0.98)`
  - `fig.text(0.5, 0.94, 'SBbc  |  d = 8.2 kpc  |  $M_{\\rm bary} = 7.6 \\times 10^{10}\\,M_\\odot$  |  McMillan 2017', ha='center', fontsize=9)`
  - Shift panel grid down (e.g. `top=0.90` in GridSpec).

## 2. Panel (a) – RMS residual

- **What:** Show RMS between velocity decode and observations in a corner.
- **How:** Compute `rms_curve = np.sqrt(np.mean((mw_v_obs - np.interp(mw_r_obs, mw_r_decode, mw_v_dec))**2))`. Add:
  - `ax_a.text(0.98, 0.02, f'RMS = {rms_curve:.2f} km s$^{{-1}}$', transform=ax_a.transAxes, ha='right', va='bottom', fontsize=6)`

## 3. Panel (b) – Sigma below LambdaCDM at outermost r

- **What:** Annotation at right edge: "X.X sigma below LambdaCDM" (headline number from sensitivity).
- **How:** Reuse letter-script logic: at `r_outer = mw_r_decode[-1]`, get `M_dec_outer`, `M_lcdm_outer`, and `delta_M` from velocity error; `n_sigma = (M_lcdm_outer - M_dec_outer) / delta_M`. Add text in panel (b) at (0.95, 0.5) in axes coords or at data point (r_outer, M_dec_outer).

## 4. Panel (c) – "Interior nearly quiet" annotation

- **What:** Short line: "Interior nearly quiet: $M_{\\rm dec} \\approx M_{\\rm phot}$ to within ~10%."
- **How:** `ax_c.text(0.5, 0.95, 'Interior nearly quiet: $M_{\\rm dec} \\approx M_{\\rm phot}$ to within ~10%.', transform=ax_c.transAxes, ha='center', va='top', fontsize=7)`

## 5. Panel (d) – Blue shading consistent with (b)

- **What:** Use same alpha/color for Delta M_eff as in panel (b).
- **How:** In (d), change `fill_between(..., alpha=0.18, color='C0')` to `alpha=0.15` so it matches (b).

## 6. Panel (e) – Ratio line and error

- **What:** Keep 4.5% interior / 95.5% exterior clear; move ±10.8% error to summary strip so the main ratio line is clean. Fix any stray formatting (e.g. "\n\nRatio" if it appears).
- **How:** Option A: show only "4.5% interior | 95.5% exterior" on (e); put "ratio uncertainty ±X% from vortex RMS" in the summary strip. Option B: keep current ratio line but drop the "(±X% error)" part from the label.

## 7. Summary strip (footer or sidebar)

- **What:** One place with: $M_{\\rm dec}$ at outermost $r$, $M_{\\rm phot}$ at outermost $r$, $\\Delta M_{\\rm eff}$, interior/exterior split, $M_{\\Lambda{\\rm CDM}}$ at outermost $r$, separation in sigma.
- **How:** Add a thin horizontal strip at bottom of figure (new GridSpec row or `fig.text`/axes with `set_axis_off()`). Fill with a few lines of text, e.g.:
  - "At $r = 50$ kpc: $M_{\\rm dec} = ...$, $M_{\\rm phot} = ...$, $\\Delta M_{\\rm eff} = ...$, 95.5% exterior | 4.5% interior, $M_{\\Lambda{\\rm CDM}} = ...$, decoded X.X sigma below LambdaCDM."

## Implementation order

1. Add computations (RMS curve, n_sigma at outer r, outermost masses).
2. Header: suptitle + subtitle, adjust GridSpec top.
3. Panel (a): RMS text.
4. Panel (b): n_sigma annotation.
5. Panel (c): "Interior nearly quiet" text.
6. Panel (d): alpha=0.15 for Delta M fill.
7. Panel (e): simplify ratio line; move error to summary.
8. Summary strip: new row or fig.text block with key numbers.
