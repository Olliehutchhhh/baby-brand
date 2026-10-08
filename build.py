#!/usr/bin/env python3
"""Generates pages/bottle-warmer-bundle-pdp.html from pages/bottle-warmer-pdp.html (the source of truth).
Run after every edit to the warmer page:  python3 build.py"""
import pathlib
d = pathlib.Path(__file__).parent / "pages"
s = (d / "bottle-warmer-pdp.html").read_text()
assert s.count("var PAGE = 'single';") == 1
s = s.replace("var PAGE = 'single';", "var PAGE = 'bundle';")
s = s.replace("<title>Superfast Portable Bottle Warmer for Travel</title>", "<title>Portable Bottle Warmer &amp; Cooler Set</title>")
(d / "bottle-warmer-bundle-pdp.html").write_text(s)
print("built bottle-warmer-bundle-pdp.html")
