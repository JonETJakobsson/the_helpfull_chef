#!/usr/bin/env python3
"""Extract grocery offers from a saved Matpriskollen "Erbjudanden" page.

Matpriskollen renders each offer as a server-rendered card. Save the offers
page from the browser as **"Webpage, Single File" (.mhtml)** or **.html** and
feed it to this script. It parses every card and prints a neat table you can
hand to The Helpful Chef (store-offers skill) to build the weekly offers file.

Usage:
    python scripts/parse-matpriskollen.py "Erbjudanden - Matpriskollen.mhtml"
    python scripts/parse-matpriskollen.py page.mhtml --format csv  > offers.csv
    python scripts/parse-matpriskollen.py page.mhtml --format md   > offers.md

Formats: table (default, aligned text), md (Markdown table), csv, json.
Only stdlib is used, so no extra install is needed.
"""
from __future__ import annotations

import argparse
import csv
import email
import io
import json
import re
import sys
from html import unescape

# --- HTML extraction -------------------------------------------------------

CARD_MARKER = "border-(--deal-color)"  # each offer card starts with this class


def load_html(path: str) -> str:
    """Return the page HTML from an .mhtml (multipart) or plain .html file."""
    raw = open(path, "rb").read()
    head = raw[:400].lstrip().lower()
    if head.startswith(b"from:") or b"multipart/related" in head or b"mime-version" in head:
        msg = email.message_from_bytes(raw)
        for part in msg.walk():
            if part.get_content_type() == "text/html":
                return part.get_payload(decode=True).decode("utf-8", "replace")
        raise SystemExit("No text/html part found in the MHTML file.")
    return raw.decode("utf-8", "replace")


# --- Card parsing ----------------------------------------------------------

TAG_RE = re.compile(r"<[^>]+>")
NAME_RE = re.compile(r'<h3\b[^>]*font-black[^>]*>(.*?)</h3>', re.S)
SUBTITLE_RE = re.compile(r'<div class="text-\[12px\]"[^>]*>(.*?)</div>', re.S)
PRICE_RE = re.compile(
    r'font-black text-\(--color-primary\)[^>]*>(.*?)</div>', re.S
)
STORE_RE = re.compile(
    r'text-\(--text-secondary-color\)[^>]*>(.*?)</div>', re.S
)


def clean(text: str) -> str:
    text = TAG_RE.sub(" ", text)
    text = unescape(text).replace("\xa0", " ")
    return re.sub(r"\s+", " ", text).strip()


def split_cards(html: str) -> list[str]:
    parts = html.split(CARD_MARKER)
    # first chunk is the page shell before the first card
    return parts[1:]


def parse_card(chunk: str) -> dict | None:
    name_m = NAME_RE.search(chunk)
    price_m = PRICE_RE.search(chunk)
    if not name_m or not price_m:
        return None
    name = clean(name_m.group(1))
    price = clean(price_m.group(1))
    if not name or not price:
        return None
    subtitles = [clean(s) for s in SUBTITLE_RE.findall(chunk)]
    subtitles = [s for s in subtitles if s]
    brand = subtitles[0] if subtitles else ""
    note = subtitles[1] if len(subtitles) > 1 else ""
    store_m = STORE_RE.search(chunk)
    store = clean(store_m.group(1)) if store_m else ""
    # jämförpris, if present in the note text
    jmf_m = re.search(r"jmf[r]?\s*pris\s*([\d.,]+\s*/\s*\w+)", note, re.I)
    jmf = clean(jmf_m.group(1)) if jmf_m else ""
    return {
        "vara": name,
        "marke": brand,
        "pris": price,
        "jmfpris": jmf,
        "butik": store,
        "notering": note,
    }


def parse(html: str) -> list[dict]:
    rows = []
    for chunk in split_cards(html):
        row = parse_card(chunk)
        if row:
            rows.append(row)
    return rows


# --- Output ----------------------------------------------------------------

COLS = ["vara", "marke", "pris", "jmfpris", "butik"]
HEAD = {"vara": "Vara", "marke": "Märke/förp.", "pris": "Pris",
        "jmfpris": "Jmf-pris", "butik": "Butik"}


def out_table(rows: list[dict]) -> str:
    widths = {c: len(HEAD[c]) for c in COLS}
    for r in rows:
        for c in COLS:
            widths[c] = max(widths[c], len(r[c]))
    line = "  ".join(HEAD[c].ljust(widths[c]) for c in COLS)
    sep = "  ".join("-" * widths[c] for c in COLS)
    body = "\n".join(
        "  ".join(r[c].ljust(widths[c]) for c in COLS) for r in rows
    )
    return f"{line}\n{sep}\n{body}"


def out_md(rows: list[dict]) -> str:
    head = "| " + " | ".join(HEAD[c] for c in COLS) + " |"
    sep = "| " + " | ".join("---" for _ in COLS) + " |"
    body = "\n".join(
        "| " + " | ".join(r[c] for c in COLS) + " |" for r in rows
    )
    return f"{head}\n{sep}\n{body}"


def out_csv(rows: list[dict]) -> str:
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=COLS + ["notering"], extrasaction="ignore")
    w.writeheader()
    w.writerows(rows)
    return buf.getvalue().rstrip("\n")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", help="Saved Matpriskollen offers page (.mhtml or .html)")
    ap.add_argument("--format", choices=["table", "md", "csv", "json"],
                    default="table")
    ap.add_argument("--out", help="Write UTF-8 output to this file instead of stdout "
                                  "(recommended on Windows, where '>' writes UTF-16).")
    args = ap.parse_args()

    rows = parse(load_html(args.file))
    if not rows:
        print("No offers found — is this a Matpriskollen 'Erbjudanden' page?",
              file=sys.stderr)
        sys.exit(1)

    if args.format == "json":
        text = json.dumps(rows, ensure_ascii=False, indent=2)
    elif args.format == "csv":
        text = out_csv(rows)
    elif args.format == "md":
        text = out_md(rows)
    else:
        text = out_table(rows)

    if args.out:
        with open(args.out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text + "\n")
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        print(text)
    print(f"\n{len(rows)} erbjudanden.", file=sys.stderr)


if __name__ == "__main__":
    main()
