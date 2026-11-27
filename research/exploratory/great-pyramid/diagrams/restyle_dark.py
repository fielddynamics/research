#!/usr/bin/env python3
"""Recolour the light-theme Great Pyramid diagrams into the repository's dark
diagram style (the palette of closure-hinge.svg). Idempotent: run from this folder.
"""
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
GRAD = ('<linearGradient id="gpbg" x2="1" y2="1"><stop stop-color="#102237"/>'
        '<stop offset="1" stop-color="#162f43"/></linearGradient>')

# light value -> dark value (case-insensitive hex, quoted names)
MAP = {
    # surfaces and frames
    "#f6f8fa": "url(#gpbg)", "#c8d5df": "#496075", "#cbd5e1": "#496075",
    '"white"': '"#1b3a52"',
    # inks
    "#142d43": "#eef5fb", "#52677a": "#b7c9d7", "#607f90": "#91a9bc",
    "#71859a": "#91a9bc",
    # graph nodes
    "#e5eff3": "#1b3a52", "#7492a4": "#78bdf0", "#d5eee6": "#173f45",
    "#e7eef7": "#1b3a52", "#d0e9e3": "#173f45",
    # accents
    "#067d6c": "#59d4b5", "#078a83": "#59d4b5",
    "#3277a9": "#78bdf0", "#356a9b": "#78bdf0",
    "#b57c36": "#d6a15e", "#b77539": "#d6a15e", "#a87b43": "#d6a15e",
    # light panels, rules and gridlines
    "#d7e1e8": "#2c3f4f", "#d0dce4": "#6f8699", "#d8e7f0": "#1b3a52",
    "#d4dfe8": "#496075", "#c6d5de": "#496075", "#d4e8f2": "#2f5470",
}

def restyle(text):
    if 'id="gpbg"' in text or '#102237' in text:
        return text
    pat = re.compile("|".join(re.escape(k) for k in MAP), re.I)
    text = pat.sub(lambda m: MAP[m.group(0).lower()], text)
    if "<defs>" in text:
        text = text.replace("<defs>", "<defs>" + GRAD, 1)
    else:
        text = re.sub(r"(<svg\b[^>]*>)", r"\1<defs>" + GRAD + "</defs>", text, count=1)
    # graphviz background polygon: transparent stroke -> repo border
    text = re.sub(r'(<polygon fill="url\(#gpbg\)") stroke="transparent"', r'\1 stroke="#496075"', text, count=1)
    return text

if __name__ == "__main__":
    for f in sorted(HERE.glob("*.svg")):
        old = f.read_text()
        new = restyle(old)
        if new != old:
            f.write_text(new)
            print("restyled", f.name)
