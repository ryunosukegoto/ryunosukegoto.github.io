#!/usr/bin/env python3
"""
Turn BibTeX into an entry for _data/publications.yml.

    # paste BibTeX, then press Ctrl-D
    python3 bin/bib2yml.py --area compbio

    # or from a file / clipboard
    python3 bin/bib2yml.py --area epi paper.bib
    pbpaste | python3 bin/bib2yml.py --area epi

    # append straight into the data file (newest first, at the top of that area)
    python3 bin/bib2yml.py --area epi --append paper.bib

Most publisher "Export citation -> BibTeX" output works as-is. The script:
  * reorders authors from "Goto, Ryunosuke and Naito, Tatsuhiko" to
    "Ryunosuke Goto, Tatsuhiko Naito"
  * converts LaTeX escapes ({\\"o}, \\'e, ---, \\&) to real characters
  * strips the {brace protection} publishers add around titles
  * builds the url from the DOI
  * flags preprints from the venue or an arXiv/bioRxiv/medRxiv eprint field

Standard library only. Review the output before committing — BibTeX from publishers is
frequently wrong about capitalisation and occasionally about the author list.
"""

import argparse
import re
import sys

# --- LaTeX -> Unicode ------------------------------------------------------------------

ACCENTS = {
    ("`", "a"): "à", ("'", "a"): "á", ('"', "a"): "ä", ("^", "a"): "â", ("~", "a"): "ã",
    ("`", "e"): "è", ("'", "e"): "é", ('"', "e"): "ë", ("^", "e"): "ê",
    ("`", "i"): "ì", ("'", "i"): "í", ('"', "i"): "ï", ("^", "i"): "î",
    ("`", "o"): "ò", ("'", "o"): "ó", ('"', "o"): "ö", ("^", "o"): "ô", ("~", "o"): "õ",
    ("`", "u"): "ù", ("'", "u"): "ú", ('"', "u"): "ü", ("^", "u"): "û",
    ("'", "c"): "ć", ("v", "c"): "č", ("'", "n"): "ń", ("~", "n"): "ñ",
    ("'", "s"): "ś", ("v", "s"): "š", ("v", "z"): "ž", ("'", "z"): "ź",
    ("'", "y"): "ý", ("c", "c"): "ç",
}
# Uppercase forms: {\'E} -> É, {\"O} -> Ö, and so on.
ACCENTS.update({(a, ch.upper()): v.upper() for (a, ch), v in list(ACCENTS.items())})
SYMBOLS = {
    r"\ss": "ß", r"\ae": "æ", r"\oe": "œ", r"\o": "ø", r"\aa": "å",
    r"\l": "ł", r"\&": "&", r"\%": "%", r"\$": "$", r"\#": "#", r"\_": "_",
    r"\textendash": "–", r"\textemdash": "—", r"\textquotesingle": "'",
}


def delatex(s: str) -> str:
    """Best-effort LaTeX -> plain Unicode."""
    # {\"o} / \"{o} / \"o  and  {\v c} etc.
    def accent(m):
        return ACCENTS.get((m.group(1), m.group(2)), m.group(2))

    s = re.sub(r'\{?\\([`\'"^~vc])\{?([A-Za-z])\}?\}?', accent, s)
    for tex, ch in sorted(SYMBOLS.items(), key=lambda kv: -len(kv[0])):
        s = s.replace(tex + "{}", ch).replace(tex + " ", ch + " ").replace(tex, ch)
    s = s.replace("---", "—").replace("--", "–")
    s = s.replace("``", "\u201c").replace("''", "\u201d")
    s = re.sub(r"\\[a-zA-Z]+\s*", "", s)   # drop any remaining commands
    s = s.replace("{", "").replace("}", "")
    s = s.replace("\\", "")
    return re.sub(r"\s+", " ", s).strip()


# --- BibTeX parsing --------------------------------------------------------------------

def parse_entries(text: str):
    """Yield {field: value} dicts, one per @entry. Handles nested braces."""
    for m in re.finditer(r"@(\w+)\s*\{", text):
        start = m.end()
        depth, i = 1, start
        while i < len(text) and depth:
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
            i += 1
        body = text[start:i - 1]
        entry = {"__type__": m.group(1).lower()}
        # split top-level commas only
        parts, depth, buf = [], 0, ""
        for ch in body:
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
            if ch == "," and depth == 0:
                parts.append(buf); buf = ""
            else:
                buf += ch
        parts.append(buf)
        for part in parts[1:]:                     # parts[0] is the cite key
            if "=" not in part:
                continue
            k, v = part.split("=", 1)
            v = v.strip().rstrip(",").strip()
            if v[:1] in "{\"" and v[-1:] in "}\"":
                v = v[1:-1]
            entry[k.strip().lower()] = v.strip()
        yield entry


def format_authors(raw: str) -> str:
    """'Goto, Ryunosuke and Naito, T.' -> 'Ryunosuke Goto, T. Naito'"""
    out = []
    for name in re.split(r"\s+and\s+", raw.replace("\n", " ")):
        name = delatex(name).strip().rstrip(",")
        if not name:
            continue
        if name.lower() in ("others", "et al", "et al."):
            out.append("et al.")
            continue
        if "," in name:
            last, first = [p.strip() for p in name.split(",", 1)]
            name = f"{first} {last}".strip()
        out.append(re.sub(r"\s+", " ", name))
    return ", ".join(out)


PREPRINT_VENUES = ("arxiv", "biorxiv", "medrxiv", "chemrxiv", "ssrn", "research square", "preprint")


def to_record(e: dict, area: str) -> dict:
    venue = ""
    for key in ("journal", "journaltitle", "booktitle", "publisher", "archiveprefix", "eprinttype"):
        if e.get(key):
            venue = delatex(e[key]); break

    doi = (e.get("doi") or "").strip()
    doi = re.sub(r"^https?://(dx\.)?doi\.org/", "", doi)
    url = f"https://doi.org/{doi}" if doi else (e.get("url") or "").strip()

    eprint_kind = (e.get("archiveprefix") or e.get("eprinttype") or "").lower()
    # arXiv entries usually have an eprint id instead of a DOI.
    if not url and e.get("eprint"):
        eid = e["eprint"].strip()
        if "arxiv" in eprint_kind or re.fullmatch(r"\d{4}\.\d{4,5}(v\d+)?", eid):
            url = f"https://arxiv.org/abs/{eid}"
    is_preprint = (
        any(v in venue.lower() for v in PREPRINT_VENUES)
        or any(v in eprint_kind for v in PREPRINT_VENUES)
        or e["__type__"] in ("misc", "unpublished")
        and bool(e.get("eprint"))
    )
    if eprint_kind == "arxiv" and not venue:
        venue = "arXiv"

    year = (e.get("year") or "").strip()
    if not year and e.get("date"):
        year = e["date"][:4]

    return {
        "area": area,
        "year": year or "????",
        "authors": format_authors(e.get("author", "")),
        "title": delatex(e.get("title", "")).rstrip("."),
        "venue": venue,
        "url": url,
        "preprint": is_preprint,
    }


# --- YAML emission ---------------------------------------------------------------------

def yaml_scalar(v: str) -> str:
    """Quote only when YAML would otherwise misread the value."""
    if v == "":
        return "''"
    risky = v[0] in "&*?|>%@`!,[]{}#'\"" or ": " in v or v.endswith(":") or " #" in v
    if risky:
        return "'" + v.replace("'", "''") + "'"
    return v


def render(rec: dict) -> str:
    # Never emit a bare `url:` — that parses as null and would render href="".
    url = rec["url"] if rec["url"] else "''  # TODO: add a DOI or URL"
    lines = [
        f"- area: {rec['area']}",
        f"  year: {rec['year']}",
        f"  authors: {yaml_scalar(rec['authors'])}",
        f"  title: {yaml_scalar(rec['title'])}",
        f"  venue: {yaml_scalar(rec['venue'])}",
        f"  url: {url}",
    ]
    if rec["preprint"]:
        lines.append("  preprint: true")
    if rec.get("notes"):
        lines.append("  notes:")
        lines.append(f"    en: {yaml_scalar(rec['notes'])}")
    return "\n".join(lines)


def append_to_data(blocks, area, path="_data/publications.yml"):
    """Insert new entries above the first existing entry of the same area."""
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    marker = f"- area: {area}\n"
    at = text.find(marker)
    if at == -1:
        text = text.rstrip("\n") + "\n\n" + "\n\n".join(blocks) + "\n"
    else:
        text = text[:at] + "\n\n".join(blocks) + "\n\n" + text[at:]
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return path


def main():
    ap = argparse.ArgumentParser(description="BibTeX -> publications.yml entry")
    ap.add_argument("file", nargs="?", help="BibTeX file (default: stdin)")
    ap.add_argument("--area", required=True, choices=["compbio", "epi"],
                    help="which tab the paper belongs on")
    ap.add_argument("--append", action="store_true",
                    help="write into _data/publications.yml instead of printing")
    ap.add_argument("--notes", metavar="TEXT",
                    help="footnote legend, e.g. '* Joint first authors'. BibTeX carries no "
                         "joint-authorship data, so add the * markers to the author list by hand.")
    args = ap.parse_args()

    text = open(args.file, encoding="utf-8").read() if args.file else sys.stdin.read()
    records = [to_record(e, args.area) for e in parse_entries(text)]
    for r in records:
        r['notes'] = args.notes
    if not records:
        sys.exit("No BibTeX entries found.")

    blocks = [render(r) for r in records]

    for r in records:
        missing = [k for k in ("authors", "title", "venue", "url") if not r[k]]
        if missing:
            print(f"# WARNING: '{r['title'][:50] or '(untitled)'}' is missing: "
                  f"{', '.join(missing)}", file=sys.stderr)

    if args.append:
        path = append_to_data(blocks, args.area)
        print(f"Added {len(blocks)} entr{'y' if len(blocks) == 1 else 'ies'} to {path}",
              file=sys.stderr)
    else:
        print("\n\n".join(blocks))


if __name__ == "__main__":
    main()
