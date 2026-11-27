#!/usr/bin/env python3
"""Download the primary and secondary sources the metrics are verified against.

    python fetch_sources.py          # downloads into sources_cache/ (git-ignored)

Every page is converted to plain text with the same normaliser the verifier
uses, and its SHA-256 is printed so a change in a source can be noticed.
Network hosts needed: www.ronaldbirdsall.com (Petrie 1883 transcription) and
en.wikipedia.org (secondary cross-checks).
"""
import hashlib
import html
import re
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
CACHE = HERE / "sources_cache"

PETRIE = "https://www.ronaldbirdsall.com/gizeh/petrie/{}.html"
SOURCES = {
    # Petrie, The Pyramids and Temples of Gizeh (1883), chapter pages
    "petrie_c6": PETRIE.format("c6"),     # Ch. 6, outside of Great Pyramid (sections 20-34)
    "petrie_c7": PETRIE.format("c7"),     # Ch. 7, inside of Great Pyramid (sections 35-64)
    "petrie_c19": PETRIE.format("c19"),   # Ch. 19, mechanical methods (sections 129-135)
    "petrie_c20": PETRIE.format("c20"),   # Ch. 20, values of the cubit (sections 136-141)
    "petrie_c21": PETRIE.format("c21"),   # Ch. 21, theories compared with facts (sections 142-163)
    "petrie_c22": PETRIE.format("c22"),   # Ch. 22, history of the Great Pyramid (sections 164-178)
    # Secondary: Wikipedia, used only for post-1883 results it cites (Cole 1925, ScanPyramids)
    "wikipedia_great_pyramid": "https://en.wikipedia.org/w/index.php?title=Great_Pyramid_of_Giza&oldid=1384664775",
}


def to_text(raw: bytes) -> str:
    try:
        t = raw.decode("utf-8")
    except UnicodeDecodeError:
        t = raw.decode("cp1252", errors="replace")
    t = re.sub(r"(?is)<(script|style).*?</\1>", "", t)
    t = re.sub(r"(?i)<br\s*/?>|</p>|</tr>|</h\d>|</li>|</td>", " ", t)
    t = re.sub(r"<[^>]+>", " ", t)
    return html.unescape(t)


def main() -> int:
    CACHE.mkdir(exist_ok=True)
    failed = []
    for key, url in SOURCES.items():
        req = urllib.request.Request(url, headers={"User-Agent": "gfd-metrics-verifier/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                raw = r.read()
        except Exception as e:  # noqa: BLE001
            print(f"[FAIL] {key}: {e}")
            failed.append(key)
            continue
        (CACHE / f"{key}.html").write_bytes(raw)
        (CACHE / f"{key}.txt").write_text(to_text(raw))
        print(f"[ OK ] {key}: {len(raw):>8d} bytes  sha256 {hashlib.sha256(raw).hexdigest()[:16]}…  {url}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
