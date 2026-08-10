#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rmt_psi_fix.py — Raw Materials Trade: PageSpeed Insights / Lighthouse 13.4 javítás

A 2026-08-10 08:45 CEST mobil audit alapján, a repo VALÓS markupjára írva.
Nem általános heurisztika: minden csere konkrét, ellenőrzött mintára illeszkedik.

  Teljesítmény 73 · Kisegítő lehetőségek 90 · Ügynöki böngészés 1/3

Futtatás a repo gyökeréből:
    python3 tools/rmt_psi_fix.py            # próba (semmit nem ír)
    python3 tools/rmt_psi_fix.py --write    # alkalmazás

Idempotens: másodszorra 0 fájlt módosít.
"""

import argparse
import glob
import re
import sys

CSS_LINK = '<link href="/assets/css/a11y-fixes.v1.css" rel="stylesheet"/>'
MAIN_CSS_RE = re.compile(r'<link href="/assets/css/site\.v[0-9a-z]+\.min\.css" rel="stylesheet"/>')


def fix_step_headings(html, rep):
    """<div class="step-num">1</div><h4>Enquiry</h4>  ->  <h3>
    A <h2 id="processHeading"> után <h4> következett: kihagyott szint."""
    new, n = re.subn(
        r'(<div class="step-num">[^<]*</div>\s*)<h4>(.*?)</h4>',
        r'\1<h3>\2</h3>',
        html, flags=re.S)
    if n:
        rep.append("h4->h3 folyamatlepes: %d" % n)
    return new


def fix_footer_headings(html, rep):
    """<div class="footer-col"><h4>Products</h4>  ->  <h3>"""
    new, n = re.subn(
        r'(<div class="footer-col">\s*)<h4>(.*?)</h4>',
        r'\1<h3>\2</h3>',
        html, flags=re.S)
    if n:
        rep.append("h4->h3 footer-col: %d" % n)
    return new


def fix_turnstile_role(html, rep):
    """role nelkuli <div> nem viselhet aria-label-t (implicit role=generic
    tiltja a nevadast) -> 'Elements must only use permitted ARIA attributes'."""
    def repl(m):
        tag = m.group(0)
        if 'role=' in tag:
            return tag
        rep.append('role="group" -> turnstileContainer')
        return tag[:-1].rstrip() + ' role="group">'

    return re.sub(r'<div[^>]*id="turnstileContainer"[^>]*>', repl, html)


def fix_generic_aria_divs(html, rep):
    """Ugyanaz a szabaly, mint a turnstile-nal: role nelkuli <div> nem
    viselhet aria-label-t. Ezek meg nem buktak el az auditon, de latens
    aria-prohibited-attr sertesek."""
    n = [0]

    def repl(m):
        tag = m.group(0)
        if 'role=' in tag or 'aria-label=' not in tag:
            return tag
        n[0] += 1
        return tag[:-1].rstrip() + ' role="group">'

    out = re.sub(r'<div[^>]*aria-label="[^"]*"[^>]*>', repl, html)
    if n[0]:
        rep.append('role="group" -> %d tovabbi div' % n[0])
    return out


def link_a11y_css(html, rep):
    """A javito stiluslap a fo stiluslap UTAN toltodjon be."""
    if 'a11y-fixes.v1.css' in html:
        return html
    m = MAIN_CSS_RE.search(html)
    if not m:
        return html
    rep.append("a11y-fixes.v1.css bekotve")
    return html[:m.end()] + CSS_LINK + html[m.end():]


FIXES = [fix_step_headings, fix_footer_headings, fix_turnstile_role,
         fix_generic_aria_divs, link_a11y_css]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    touched = 0
    for path in sorted(glob.glob("*.html")):
        src = open(path, encoding="utf-8").read()
        out, rep = src, []
        for fn in FIXES:
            out = fn(out, rep)
        if out != src:
            touched += 1
            print("%-58s %s" % (path, "; ".join(rep)))
            if args.write:
                open(path, "w", encoding="utf-8").write(out)

    print("\n%d fajl %s" % (touched, "irva" if args.write else "modosulna (proba)"))
    if not args.write:
        print("Alkalmazas: python3 tools/rmt_psi_fix.py --write")
    return 0


if __name__ == "__main__":
    sys.exit(main())
