"""The Great Pyramid of Khufu: a verified metrics dataset.

Every entry is a measurement *as published*, with the exact words of its source
in `quote`. `verify_metrics.py` checks that each quote occurs verbatim (after
whitespace normalisation) in the downloaded source and that the stated value
occurs in the quote; it then runs the cross-checks in `CROSS_CHECKS`.

Conventions
-----------
* Petrie's unit is the British inch (1 in = 0.0254 m exactly). His "±" is a
  *probable error* (≈ 0.6745 σ for a normal distribution), not a standard
  deviation. Ranges ("a to b") are the spread of his individual measures.
* Levels are above the pavement on which the casing stands (Petrie §23); negative
  levels are below it. Horizontal positions are from the Pyramid's centre or its
  N. base line, as Petrie gives them (§64).
* `tier`: "P" primary (Petrie's 1880–82 survey, published 1883); "S" secondary
  (Wikipedia revision 1384664775, used only for post-1883 results it cites:
  J. H. Cole's 1925 survey, the ScanPyramids muon results, Lehner); "D" derived
  in this folder from other entries (see CROSS_CHECKS).
* `status`: "measured", "estimate" (Petrie's reasoned estimate), "interpretation"
  (an author's reading, not a measurement).
"""

M = []


def m(id, group, name, value, unit, source, section, quote, *, err=None, rng=None,
      tier="P", status="measured", note="", match=None):
    """`match`: the token that must occur in the quote, when the value is not printed
    literally there (a word such as 'nine', a misprint, a sign convention)."""
    M.append(dict(id=id, group=group, name=name, value=value, err=err, range=rng, unit=unit,
                  tier=tier, status=status, source=source, section=section, quote=quote, note=note,
                  match=match))


# ---------------------------------------------------------------------------
# 1. Exterior (Petrie ch. 6 and ch. 21)
# ---------------------------------------------------------------------------
G = "exterior"
m("base_side_mean", G, "Base side, mean (casing on pavement)", 9068.8, "in", "petrie_c6", "§25",
  "The mean base being 9068.8 ± .5 inches", err=0.5)
m("height_original", G, "Original height to apex (from base and angle)", 5776.0, "in", "petrie_c6", "§25",
  "this yields a height of 5776.0 ± 7.0 inches", err=7.0, status="estimate")
m("face_angle", G, "Mean angle of the faces", "51º 52'", "deg-min", "petrie_c6", "§25",
  "take 51º 52' ± 2' as the nearest approximation to the mean angle of the Pyramid", err="2'",
  status="estimate")
m("base_N", G, "Base side N", 9069.4, "in", "petrie_c6", "§21", "N E S W 9069.4 9067.7 9069.5 9068.6")
m("base_E", G, "Base side E", 9067.7, "in", "petrie_c6", "§21", "N E S W 9069.4 9067.7 9069.5 9068.6")
m("base_S", G, "Base side S", 9069.5, "in", "petrie_c6", "§21", "N E S W 9069.4 9067.7 9069.5 9068.6")
m("base_W", G, "Base side W", 9068.6, "in", "petrie_c6", "§21", "N E S W 9069.4 9067.7 9069.5 9068.6")
m("base_azimuth_mean", G, "Mean azimuth of the sides (from true N; minus = anticlockwise)", "- 3' 43\"",
  "arc", "petrie_c6", "§21", "Mean 9068.8 .65 - 3' 43\" 12\"")
m("base_mean_error", G, "Mean error of the base (length, angle)", ".6", "in",
  "petrie_c6", "§21", "the mean errors of the base of the Great Pyramid were somewhat less than .6 inch, and 12\" of angle")
m("core_plane_side_mean", G, "Core-masonry plane, mean side", 9001.5, "in", "petrie_c6", "§20",
  "Mean Mean Difference 9001.5 1.0")
m("socket_side_mean", G, "Socket-to-socket side, mean", 9125.9, "in", "petrie_c6", "§20",
  "9125.9 4.4")
m("socket_NE", G, "NE socket floor level", -28.5, "in", "petrie_c6", "§22", "N.E. S.E. S.W. N.W. - 28.5 - 39.9 - 23.0 - 32.8")
m("socket_SE", G, "SE socket floor level", -39.9, "in", "petrie_c6", "§22", "N.E. S.E. S.W. N.W. - 28.5 - 39.9 - 23.0 - 32.8")
m("socket_SW", G, "SW socket floor level", -23.0, "in", "petrie_c6", "§22", "N.E. S.E. S.W. N.W. - 28.5 - 39.9 - 23.0 - 32.8")
m("socket_NW", G, "NW socket floor level", -32.8, "in", "petrie_c6", "§22", "N.E. S.E. S.W. N.W. - 28.5 - 39.9 - 23.0 - 32.8")
m("casing_base_level", G, "Top of first casing course (N side), mean level", 58.85, "in", "petrie_c6", "§26",
  "The average variation of the casing from a level plane of + 58.85 is but .02")
m("casing_joint_mean", G, "Mean thickness of casing-stone joints (N side)", 0.020, "in", "petrie_c6", "§26",
  "the mean thickness of the joints there is .020")
m("casing_thickness_top", G, "Casing thickness near the top (back to top edge)", 71, "in", "petrie_c6", "§26",
  "average about 71 ± 5 inches in thickness", err=5, status="estimate")
m("course_25_level", G, "Level of the 25th course", 885.0, "in", "petrie_c21", "§146",
  "The 25th course is at By theory equal to the Queen's Chamber level at The 50th course is at By theory equal to the King's Chamber floor level 885.0 858.4 1697.6")
m("course_50_level", G, "Level of the 50th course", 1697.6, "in", "petrie_c21", "§146",
  "885.0 858.4 1697.6 1691.4 to 1693.7")
m("basalt_pavement", G, "Basalt pavement east of the Pyramid", "a third of an acre", "area", "petrie_c6", "§28",
  "The basalt pavement is a magnificent work, which covered more than a third of an acre")
m("weight_petrie", G, "Weight of the Pyramid (Petrie's figure, from his dimensions)", 5923400, "English tons",
  "petrie_c21", "§145", "the weight of the Great Pyramid in English tons is 5,923,400", status="estimate",
  note="Petrie does not state the density he used; the implied density is a cross-check (X-volume).")

# ---------------------------------------------------------------------------
# 2. Passages (Petrie ch. 7, ch. 21)
# ---------------------------------------------------------------------------
G = "passages"
m("entrance_level", G, "Entrance passage, beginning (floor), level", 668.2, "in", "petrie_c7", "§64",
  "+ 668.2 ± .1", err=0.1)
m("entrance_east_offset", G, "Entrance passage axis, E of the Pyramid's mid-plane", 287, "in", "petrie_c21", "§149",
  "This would be 247, whereas it is really 287")
m("entrance_angle", G, "Entrance passage, mean angle of whole length", "26º 31' 23\"", "deg-min-sec",
  "petrie_c21", "§151", "the observed angle of the whole passage, which is 26º 31' 23\"")
m("entrance_floor_length", G, "Entrance passage floor, total original length", 4143, "in", "petrie_c21", "§149",
  "The total original length of the entrance passage floor being 4143")
m("entrance_height", G, "Entrance passage, perpendicular height", 47.24, "in", "petrie_c21", "§150",
  "the actual height being 47.24 ± .02", err=0.02)
m("passage_height_range", G, "Passage heights, range over all passages", "46.2 to 48.6", "in", "petrie_c21", "§150",
  "The passages vary from 46.2 to 48.6")
m("entrance_end_level", G, "Entrance passage, S end of floor, level", -1181, "in", "petrie_c7", "§64",
  "- 1181. ± 1.", err=1)
m("ascending_length", G, "Ascending passage, length", 1546.5, "in", "petrie_c21", "§149",
  "The length of the ascending passage is 1546.5 inches")
m("ascending_angle", G, "Ascending passage, altitude of mean axis", "26º 2' 30\"", "deg-min-sec", "petrie_c7", "§39",
  "From 26º 2' 30\" altitude")
m("ascending_begin_level", G, "Ascending passage, beginning, level", 179.9, "in", "petrie_c7", "§64",
  "+ 179.9 ± .2", err=0.2)
m("ascending_end_level", G, "Ascending passage, end, level", 852.6, "in", "petrie_c7", "§64",
  "+ 852.6 ± .3", err=0.3)
m("granite_plug_width", G, "Granite plug, width at lower (N) end vs upper end", 38.2, "in", "petrie_c7", "§38",
  "the plug is but 38.2 wide in place of 41.6 at the upper end")

# ---------------------------------------------------------------------------
# 3. Subterranean chamber
# ---------------------------------------------------------------------------
G = "subterranean"
m("subt_length", G, "Subterranean chamber, length", "553.5 to 554.1", "in", "petrie_c21", "§152", "Length 553.5 to 554.1")
m("subt_width", G, "Subterranean chamber, width", "325.9 to 329.6", "in", "petrie_c21", "§152", "Width 325.9 to 329.6 ?",
  note="Petrie marks the width with '?'.")
m("subt_roof_level", G, "Subterranean chamber, roof level", -1056, "in", "petrie_c21", "§148",
  "1056 ± 2 level of subterranean Chamber roof", err=2)
m("subt_unfinished", G, "Subterranean chamber: state", "unfinished", "—", "petrie_c7", "§37",
  "The large chamber is most clearly unfinished", status="interpretation")

# ---------------------------------------------------------------------------
# 4. Queen's Chamber
# ---------------------------------------------------------------------------
G = "queens_chamber"
QC = "The size of the chamber (after allowing suitably in each part for the incrustation of salt) is on an average 205.85 wide, and 226.47 long, 184.47 high on N. and S. walls, and 245.1 high to the top of the roof ridge on E. and W. walls"
m("qc_width", G, "Queen's Chamber, width (E–W of N/S walls)", 205.85, "in", "petrie_c7", "§41", QC)
m("qc_length", G, "Queen's Chamber, length", 226.47, "in", "petrie_c7", "§41", QC)
m("qc_wall_height", G, "Queen's Chamber, N and S wall height", 184.47, "in", "petrie_c7", "§41", QC)
m("qc_ridge_height", G, "Queen's Chamber, height to roof ridge", 245.1, "in", "petrie_c7", "§41", QC)
m("qc_floor_level", G, "Queen's Chamber, NE corner (floor), level", 834.4, "in", "petrie_c7", "§64", "+ 834.4 ± .4", err=0.4)
m("qc_roof_level", G, "Queen's Chamber, mid W roof, level", 1078.7, "in", "petrie_c7", "§64", "+ 1078.7 ± .6 roof", err=0.6)
m("qc_niche_height", G, "Queen's Chamber niche, height", 183.80, "in", "petrie_c21", "§153", "the niche being 183.80")

# ---------------------------------------------------------------------------
# 5. Grand Gallery
# ---------------------------------------------------------------------------
G = "grand_gallery"
m("gg_floor_end_level", G, "Gallery floor at the S wall (virtual end), level", 1689.0, "in", "petrie_c7", "§45",
  "the floor of the gallery intersects the S. wall at 1689.0 ± .5 above the pavement", err=0.5)
m("gg_floor_horizontal", G, "Gallery floor, horizontal length", 1688.9, "in", "petrie_c21", "§148",
  "1689.0 ± .5 1688.9 ± .2", err=0.2)
m("gg_roof_length", G, "Gallery roof length (horizontal / sloping)", 1648.4, "in", "petrie_c7", "§46",
  "the length of the roof of the gallery is 1688.9 - 40.45 = 1648.4 horizontal, or 1838.6 sloping")
m("gg_angle", G, "Gallery, altitude of mean axis", "26º16'40\"", "deg-min-sec", "petrie_c7", "§45",
  "of 26º16'40\" altitude")
m("gg_top_width", G, "Gallery, width at top (N / S end)", 40.9, "in", "petrie_c7", "§46",
  "The width of the top of the gallery is 40.9 at N., and 41.3 at S. end")
m("gg_lower_width", G, "Gallery, width of lower part (between walls)", 82.42, "in", "petrie_c21", "§150",
  "Wide 206.13 82.42")
m("gg_laps_overhang", G, "Gallery, total overhang of the seven laps", 20.55, "in", "petrie_c7", "§46",
  "mean of all, 20.55, for the sum of the seven projections of the laps, or one cubit")

# ---------------------------------------------------------------------------
# 6. Antechamber
# ---------------------------------------------------------------------------
G = "antechamber"
AC = "The mean length is thus 116.30 (by the two series from top to base), breadth 65.00, and height 149.35"
m("ac_length", G, "Antechamber, length", 116.30, "in", "petrie_c7", "§48", AC)
m("ac_breadth", G, "Antechamber, breadth above wainscot", 65.00, "in", "petrie_c7", "§48", AC)
m("ac_height", G, "Antechamber, height", 149.35, "in", "petrie_c7", "§48", AC)
m("ac_granite_floor", G, "Antechamber, granite part of floor (E side)", 103.20, "in", "petrie_c21", "§154",
  "as accurately measured by steel tape along the E. side the granite floor is 103.20")
m("ac_floor_level", G, "Antechamber, N end floor, level", 1692.6, "in", "petrie_c7", "§64", "+ 1692.6 ± .6", err=0.6)

# ---------------------------------------------------------------------------
# 7. King's Chamber
# ---------------------------------------------------------------------------
G = "kings_chamber"
KC = "Width 206.12 ± .12 squared, is 100 cubits of 20.612 ± .012 Length 412.24 ± .12 squared, is 400 cubits of 20.612 ± .006 Height 230.09 ± .15 squared, is 125 cubits of 20.580 ± .014"
m("kc_width", G, "King's Chamber, width", 206.12, "in", "petrie_c21", "§155", KC, err=0.12)
m("kc_length", G, "King's Chamber, length", 412.24, "in", "petrie_c21", "§155", KC, err=0.12)
m("kc_height_floor", G, "King's Chamber, height above the floor", 230.09, "in", "petrie_c21", "§155", KC, err=0.15)
m("kc_wall_height", G, "King's Chamber, wall height (above wall base)", 235.20, "in", "petrie_c21", "§150",
  "the actual height differs half an inch from this, being 235.20 ± .06", err=0.06)
m("kc_N_wall_mean", G, "King's Chamber, N wall length (mean of top/base)", 412.40, "in", "petrie_c7", "§52",
  "Top Mean Base 412.14 412.40 412.78")
m("kc_floor_level", G, "King's Chamber floor, level", 1692.8, "in", "petrie_c7", "§64", "+ 1692.8 ± .6", err=0.6)
m("kc_floor_range", G, "King's Chamber floor, range of level", "1691.4 to 1693.7", "in", "petrie_c21", "§148",
  "1691.4 to 1693.7 ± .6", err=0.6)
m("kc_wall_base_level", G, "King's Chamber, N.E. wall base, level", 1688.5, "in", "petrie_c7", "§64", "+ 1688.5 ± .6", err=0.6)
m("kc_roof_level", G, "King's Chamber roof, level", "1921.6 to 1923.7", "in", "petrie_c7", "§64",
  "+ 1921.6 ± .6 to + 1923.7 ± .6")
m("kc_floor_raise", G, "Floor raised above wall base", 5.11, "in", "petrie_c21", "§155",
  "it is raised 5.11 ± .12 inches", err=0.12)
m("kc_course_height", G, "Mean course height of the walls", 47.040, "in", "petrie_c21", "§150",
  "the mean course height is 47.040 ± .013", err=0.013)
m("kc_first_course", G, "Height of the first (lowest) course", 41.91, "in", "petrie_c21", "§155",
  "whereas it is but 41.91 ± .12", err=0.12)
m("kc_roof_beams", G, "Roof: number of granite beams", 9, "count", "petrie_c7", "§53",
  "The roof of the chamber is formed of nine granite beams", match="nine")
m("kc_cubit", G, "Cubit from the chamber base (four sides)", 20.632, "in", "petrie_c7", "§52",
  "The four sides there yield a mean value of 20.632 ± .004", err=0.004)
m("kc_cubic_diagonal", G, "Cubic (space) diagonal of the chamber", 515.17, "in", "petrie_c21", "§156",
  "This cubic diagonal actually is 515.I7", match="515.I7",
  note="The transcription prints '515.I7' (a letter I for the digit 1); the value is 515.17.")
m("kc_channel_N_angle", G, "N air channel, mean floor angle (measured part)", "31º 33'", "deg-min", "petrie_c7", "§56",
  "30º 43' 15\" 31º 33'")
m("kc_channel_S_angle", G, "S air channel, mean floor angle (measured part)", "45º 13' 40\"", "deg-min-sec", "petrie_c7", "§56",
  "44º 26' 18\" 45º 13' 40\"")
m("kc_channel_N_section", G, "N channel, original width × height", "9.0 × 8.72–8.74", "in", "petrie_c7", "§56",
  "(mean 9.0) in width, and to have been 8.72 and 8.74 in height")

# ---------------------------------------------------------------------------
# 8. Coffer
# ---------------------------------------------------------------------------
G = "coffer"
m("coffer_material", G, "Coffer material", "red granite", "—", "petrie_c7", "§57",
  "an approximately flat-sided box of red granite")
m("coffer_contents", G, "Coffer contents (by offsets from planes)", 72030, "in^3", "petrie_c7", "§61",
  "Contents- 72,030; solid bulk = 70,500; volume over all, 142,530 cubic inches", err=60)
m("coffer_bulk", G, "Coffer solid bulk (by offsets)", 70500, "in^3", "petrie_c7", "§61",
  "Contents- 72,030; solid bulk = 70,500; volume over all, 142,530 cubic inches", err=100)
m("coffer_volume_overall", G, "Coffer volume over all (by offsets)", 142530, "in^3", "petrie_c7", "§61",
  "Contents- 72,030; solid bulk = 70,500; volume over all, 142,530 cubic inches", err=60)
m("coffer_volume_calipers", G, "Coffer volume over all (by calipers)", 142590, "in^3", "petrie_c7", "§61",
  "Contents = 71,960; solid bulk = 70,630; volume over all, 142,590")
m("coffer_outer_height", G, "Coffer outer height", 41.31, "in", "petrie_c21", "§156",
  "41.31 (var 41.14 to 41.50 ) outer height", rng=[41.14, 41.50])
m("coffer_outer_length", G, "Coffer outer length (mean)", 89.62, "in", "petrie_c21", "§156",
  "Outer length mean 89.62", rng=[89.18, 90.6],
  note="§156 gives the mean as 89.62 in one table and 89.63 (var 89.18 to 90.6?) in another.")
m("coffer_outer_width", G, "Coffer outer width", 38.50, "in", "petrie_c21", "§156", "38.50 (var 38.35 to 38.87 ) outer width")
m("coffer_inner_length", G, "Coffer inner length", 78.06, "in", "petrie_c21", "§156", "78.06 (var 77.64 to 78.23 ) inner length")
m("coffer_inner_width", G, "Coffer inner width (mean)", 26.81, "in", "petrie_c21", "§156", "26.81 actual mean")
m("coffer_inner_height", G, "Coffer inner height", 34.42, "in", "petrie_c21", "§156", "34.42 (var 34.36 to 34.54 ) inner height")

# ---------------------------------------------------------------------------
# 9. Relieving ("construction") chambers
# ---------------------------------------------------------------------------
G = "relieving_chambers"
m("rc_count", G, "Chambers of construction above the King's Chamber", 5, "count", "petrie_c7", "§62",
  "Top 4th 3rd 2nd 1st (Kings", match="1st", note="Rows of Petrie's table: Top, 4th, 3rd, 2nd, 1st (and the King's Chamber).")
m("rc_first_S", G, "1st chamber, S side length (rough masonry)", 464.6, "in", "petrie_c7", "§62", "468.4 467 472 471.8 464.6 412.5")
m("rc_top_S", G, "Top chamber, S side length (rough masonry)", 468.4, "in", "petrie_c7", "§62", "468.4 467 472 471.8 464.6 412.5")
m("rc_apex_level", G, "Apex of the construction chambers, level (after Vyse)", 2525, "in", "petrie_c21", "§148",
  "The level of the apex of the construction chambers (according to Vyse's measure above the King's Chamber) is about 2,525",
  status="estimate")
m("rc_materials", G, "Floors granite; upper side blocks limestone", "granite / limestone", "—", "petrie_c7", "§63",
  "In the fourth chamber the supporting blocks along the N. and S. sides are all of limestone", match="limestone")

# ---------------------------------------------------------------------------
# 10. Units, materials and methods
# ---------------------------------------------------------------------------
G = "units_materials_methods"
m("cubit_from_height", G, "Height in cubits (theory: 280 cubits)", 20.632, "in", "petrie_c21", "§144",
  "By theory, 280 cubits of 20.632 ± .004 (Egyptian cubit)", err=0.004, status="interpretation")
m("saw_thickness", G, "Thickness of straight saw cuts", ".03 to .2", "in", "petrie_c19", "§130",
  "The straight saws varied from .03 to .2 inch thick")
m("coffer_length_feet", G, "Coffer length, in feet", "7 feet 6 in.", "—", "petrie_c19", "§130",
  "the Great Pyramid coffer, which is 7 feet 6 in. long")
m("drill_load", G, "Load on 4-inch tubular drills in granite (Petrie's estimate)", "a ton or two", "—", "petrie_c19", "§133",
  "probably a load of at least a ton or two was placed on the 4 inch drills cutting in granite", status="interpretation")
m("jewel_points", G, "Tool hypothesis: bronze set with hard cutting points", "bronze + jewel points", "—", "petrie_c19", "§129",
  "by means of bronze tools; these were set with cutting points", status="interpretation", match="bronze",
  note="Petrie's 1883 hypothesis; modern work favours copper/bronze with quartz-sand abrasive.")

# ---------------------------------------------------------------------------
# 11. Secondary (post-1883) results, via Wikipedia rev. 1384664775
# ---------------------------------------------------------------------------
G = "modern"
W = "wikipedia_great_pyramid"
m("cole_sides", G, "Cole (1925) side lengths", "230.252 / 230.454 / 230.391 / 230.357", "m", W, "note 1031",
  "Based on side lengths 230.252 m, 230.454 m, 230.391 m, 230.357 m.", tier="S")
m("base_infobox", G, "Base (infobox)", 230.33, "m", W, "infobox", "Base 230.33 m (756 ft) or 440 cubits", tier="S")
m("height_original_m", G, "Original height (infobox)", 146.6, "m", W, "infobox", "Original: 146.6 m (481 ft) or 280 cubits", tier="S")
m("height_current_m", G, "Current height", 138.5, "m", W, "infobox", "Current: 138.5 m (454 ft)", tier="S")
m("slope_seked", G, "Slope (seked 5½ palms)", "51°50'40\"", "deg", W, "infobox", "Slope 51°50'40\" or seked of", tier="S")
m("volume_m3", G, "Volume", 2.6e6, "m^3", W, "infobox", "Volume 2.6 million m 3", tier="S", status="estimate")
m("blocks", G, "Number of blocks", 2.3e6, "count", W, "Materials",
  "The Great Pyramid consists of an estimated 2.3 million blocks", tier="S", status="estimate")
m("material_masses", G, "Limestone / granite / mortar masses", "5.5 Mt / 8,000 t / 500,000 t", "t", W, "Materials",
  "Approximately 5.5 million tonnes of limestone, 8,000 tonnes of granite, and 500,000 tonnes of mortar were used",
  tier="S", status="estimate")
m("granite_source", G, "Granite source", "Aswan", "—", W, "Materials",
  "The granite stones in the pyramid were transported from Aswan, more than 900 km (560 mi) south.", tier="S")
m("granite_beams", G, "Largest granite blocks (KC ceiling, relieving chambers)", "25 to 80", "t", W, "Materials",
  "The largest, weighing 25 to 80 tonnes, form the ceilings", tier="S", status="estimate")
m("casing_source", G, "White casing limestone source (Diary of Merer)", "Tura", "—", W, "History",
  "It documents the transportation of white limestone blocks from Tura to the Great Pyramid", tier="S")
m("big_void", G, "ScanPyramids Big Void (2017, muography): length", "at least 30", "m", W, "The Big Void",
  "Its length is at least 30 metres (98 ft) and its cross-section is similar to that of the Grand Gallery", tier="S")
m("nf_corridor", G, "North Face Corridor (2023 endoscopy): length and section", "9 m; ~2 × 2 m", "m", W, "North Face Corridor",
  "revealing a horizontal tunnel with a length of 9 metres (30 ft) and a transverse section of about 2 by 2 metres", tier="S")
m("entrance_course", G, "Original entrance: course and height", "19th layer, ~17 m", "m", W, "Entrance",
  "the pyramid was entered through a hole in the 19th layer of masonry, approximately 17 metres (56 ft) above the pyramid's base level",
  tier="S")
m("summit_loss", G, "Summit: height lost and material missing", "~8 m; ~1,000 t", "—", W, "Casing",
  "nowadays the pyramid is about 8 metres (26 ft) shorter than it was when intact, with about 1,000 tonnes", tier="S", status="estimate")
m("coordinates", G, "Coordinates", "29°58′45″N 31°08′03″E", "—", W, "infobox", "29°58′45″N 31°08′03″E", tier="S")
