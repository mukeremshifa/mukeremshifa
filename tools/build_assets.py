"""Render the profile README's section artwork as SVG.

GitHub strips <style> tags and style attributes from README HTML, so any real
layout control has to live inside an image. Every section below is therefore an
SVG committed to assets/, and this script is the only thing that writes them.

    python tools/build_assets.py

Data is read from data.json, refreshed by tools/fetch_data.py.
"""

from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
W = 880

# ---------------------------------------------------------------- design tokens

INK0 = "#121110"   # deepest ground
INK1 = "#191714"   # card ground
INK2 = "#221F1B"   # raised chip
LINE = "#302B24"
GOLD = "#EEBA2B"   # taken from the avatar, and already in ConverseKit's badge
GOLD_D = "#8B7128"
TEXT = "#F4F1E8"
MUTED = "#9C9483"
FAINT = "#6B6558"

MONO = ("ui-monospace,'SF Mono','Cascadia Mono','DejaVu Sans Mono',"
        "'Segoe UI Mono',Menlo,Consolas,monospace")


def esc(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def svg(width: int, height: int, body: str, css: str = "") -> str:
    style = f"<style>{css}</style>" if css else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" font-family="{MONO}" role="img">'
        f"{style}"
        f'<rect width="{width}" height="{height}" rx="10" fill="{INK1}"/>'
        f'<rect x=".5" y=".5" width="{width-1}" height="{height-1}" rx="9.5" '
        f'fill="none" stroke="{LINE}"/>'
        f"{body}</svg>"
    )


def write(name: str, markup: str) -> None:
    ASSETS.mkdir(exist_ok=True)
    (ASSETS / name).write_text(markup, encoding="utf-8")
    print(f"  assets/{name}  {len(markup):,} bytes")


def label(x, y, s, size=10.5, fill=FAINT, spacing=".18em", weight="400"):
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" '
            f'letter-spacing="{spacing}" font-weight="{weight}">{esc(s)}</text>')


# ---------------------------------------------------------------------- 1. hero

TONE = ["#7C6027", "#9A7A2B", "#B4902E", "#CDA231", "#E4B843", "#F8D473"]


def hero(portrait: str, tones: str) -> None:
    rows = portrait.split("\n")
    trows = tones.split("\n")
    cols = max(len(r) for r in rows)
    fs, lh = 10.1, 10.7
    art_w = 440.0
    art_x, art_y = 40, 56

    # colour is what carries tone here, so consecutive cells sharing a band
    # become one tspan rather than one per character
    art = []
    for i, r in enumerate(rows):
        r = r.ljust(cols)
        t = trows[i].ljust(cols) if i < len(trows) else " " * cols
        spans, run, band = [], "", None
        for ch, b in zip(r, t):
            b = b if ch != " " else band
            if b != band and run:
                spans.append((band, run)); run = ""
            band = b
            run += ch
        if run:
            spans.append((band, run))
        inner = "".join(
            f'<tspan fill="{TONE[int(b)] if b and b != " " else TONE[0]}" '
            f'xml:space="preserve">{esc(s)}</tspan>' for b, s in spans)
        art.append(
            f'<text x="{art_x}" y="{art_y + i*lh:.1f}" font-size="{fs}" '
            f'textLength="{art_w}" lengthAdjust="spacingAndGlyphs" '
            f'xml:space="preserve">{inner}</text>'
        )
    art_h = len(rows) * lh

    # terminal transcript, typed line by line
    cx = 524
    seq = [
        ("cmd", "whoami"),
        ("out", "Mukerem Shifa"),
        ("dim", "Full-stack developer, AI applications"),
        ("gap", ""),
        ("cmd", "cat now.txt"),
        ("out", "Building ConverseKit and SynapseDeck."),
        ("dim", "Learning how to evaluate retrieval"),
        ("dim", "instead of eyeballing it."),
    ]

    lines, css, t = [], [], 0.6
    y = 128
    for kind, txt in seq:
        if kind == "gap":
            y += 13
            continue
        i = len(lines)
        if kind == "cmd":
            body = (f'<tspan fill="{GOLD}">$</tspan> '
                    f'<tspan fill="{TEXT}">{esc(txt)}</tspan>')
            n = len(txt) + 2
        else:
            fill = TEXT if kind == "out" else MUTED
            body = f'<tspan fill="{fill}">{esc(txt)}</tspan>'
            n = len(txt)
        dur = round(n * 0.045, 2) if kind == "cmd" else 0.01
        lines.append(
            f'<g clip-path="url(#c{i})"><text x="{cx}" y="{y}" font-size="12" '
            f'xml:space="preserve">{body}</text></g>'
            f'<clipPath id="c{i}"><rect class="r{i}" x="{cx-2}" y="{y-12}" '
            f'width="0" height="17"/></clipPath>'
        )
        css.append(
            f"@keyframes k{i}{{to{{width:330px}}}}"
            f".r{i}{{animation:k{i} {dur}s steps({max(n,1)}) {t:.2f}s forwards}}"
        )
        t += dur + (0.28 if kind == "cmd" else 0.12)
        y += 21

    cursor = (f'<rect x="{cx}" y="{y-11}" width="7.5" height="14" fill="{GOLD}" '
              f'class="cur" opacity="0"/>')
    css.append(f".cur{{animation:blink 1.05s steps(1) {t:.2f}s infinite}}"
               "@keyframes blink{0%,50%{opacity:1}51%,100%{opacity:0}}")
    css.append("@media(prefers-reduced-motion:reduce){"
               "[class^='r']{width:330px!important;animation:none!important}"
               ".cur{opacity:1;animation:none}}")

    h = int(max(art_y + art_h, y) + 46)
    defs = (
        '<defs>'
        f'<linearGradient id="pg" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="#F3C956"/>'
        f'<stop offset=".55" stop-color="{GOLD}"/>'
        f'<stop offset="1" stop-color="#C08F27"/></linearGradient>'
        '</defs>'
    )
    body = (
        defs
        + label(cx, 74, "MUKEREM SHIFA", size=15, fill=TEXT, spacing=".26em", weight="600")
        + label(cx, 95, "ADDIS ABABA  /  BUILDING AI PRODUCTS END TO END", size=9.5)
        + f'<line x1="{cx}" y1="108" x2="{W-44}" y2="108" stroke="{LINE}"/>'
        + "".join(art) + "".join(lines) + cursor
    )
    write("hero.svg", svg(W, h, body, "".join(css)))


# --------------------------------------------------------------------- 2. about

def about() -> None:
    para = [
        ("dim",  "// about.md"),
        ("gap",  ""),
        ("txt",  "I like the problems that hide behind the demo."),
        ("gap",  ""),
        ("txt",  "Anyone can call an LLM API. The work is everything"),
        ("txt",  "around it: deciding which passage is worth retrieving,"),
        ("txt",  "keeping one client's documents out of another client's"),
        ("txt",  "answers, and holding a conversation together when the"),
        ("txt",  "stream drops halfway through a sentence."),
        ("gap",  ""),
        ("txt",  "I am early in my career and I learn by shipping whole"),
        ("txt",  "systems rather than tutorials. The four projects below"),
        ("key",  "are deployed, tested and documented."),
        ("gap",  ""),
        ("dim",  "// open to junior and entry-level roles"),
    ]
    x, y, lh = 96, 62, 21.5
    out, n = [], 0
    for kind, txt in para:
        n += 1
        out.append(f'<text x="{54}" y="{y}" font-size="11" fill="{LINE}" '
                   f'text-anchor="end">{n:02d}</text>')
        if kind == "gap":
            y += 11
            continue
        fill = {"txt": TEXT, "dim": FAINT, "key": GOLD}[kind]
        out.append(f'<text x="{x}" y="{y}" font-size="13.5" fill="{fill}">'
                   f'{esc(txt)}</text>')
        y += lh
    h = int(y + 24)
    body = (
        f'<rect x="70" y="20" width="1" height="{h-40}" fill="{LINE}"/>'
        + label(96, 36, "ABOUT", size=10, fill=GOLD_D)
        + "".join(out)
    )
    write("about.svg", svg(W, h, body))


# --------------------------------------------------------------------- 3. stack

def stack() -> None:
    groups = [
        ("LANGUAGES", ["TypeScript", "Python", "JavaScript", "SQL", "Java"]),
        ("FRONTEND",  ["React 19", "Vite", "Tailwind", "TanStack Query", "Zod"]),
        ("BACKEND",   ["Node", "Hono", "Django REST", "Cloudflare Workers"]),
        ("DATA",      ["PostgreSQL", "Supabase", "pgvector", "Row-level security"]),
        ("AI",        ["LangChain", "OpenAI", "Anthropic", "Gemini", "Groq", "RAG"]),
        ("TOOLING",   ["Vitest", "GitHub Actions", "Git", "Linux", "Docker"]),
    ]
    x0, y = 44, 56
    out = [label(x0, 34, "STACK", size=10, fill=GOLD_D)]
    for gi, (name, items) in enumerate(groups):
        out.append(f'<text x="{x0}" y="{y+13}" font-size="10" fill="{FAINT}" '
                   f'letter-spacing=".16em">{esc(name)}</text>')
        cx = x0 + 150
        for it in items:
            w = len(it) * 7.0 + 22
            if cx + w > W - 44:
                cx = x0 + 150
                y += 30
            tint = GOLD if gi in (0, 4) else MUTED
            fill = "#241F14" if gi in (0, 4) else INK2
            out.append(
                f'<rect x="{cx}" y="{y}" width="{w:.0f}" height="24" rx="4" '
                f'fill="{fill}" stroke="{GOLD_D if gi in (0,4) else LINE}" '
                f'stroke-opacity="{".55" if gi in (0,4) else "1"}"/>'
                f'<text x="{cx + w/2:.0f}" y="{y+16}" font-size="11.5" '
                f'fill="{tint}" text-anchor="middle">{esc(it)}</text>'
            )
            cx += w + 8
        y += 38
    write("stack.svg", svg(W, int(y + 12), "".join(out)))


# ----------------------------------------------------------------- 4. languages

def languages(langs: list[tuple[str, int]], traj: dict) -> None:
    total = sum(v for _, v in langs)
    colw = (W - 44*2 - 56) / 2
    lx, rx = 44, 44 + colw + 56
    out = [
        label(lx, 34, "LANGUAGES", size=10, fill=GOLD_D),
        label(rx, 34, "TRAJECTORY", size=10, fill=GOLD_D),
        f'<line x1="{rx-28}" y1="20" x2="{rx-28}" y2="290" stroke="{LINE}"/>',
    ]

    # left: one thin bar per language
    y = 62
    ramp = [GOLD, "#D5A62D", "#B98F2C", "#9C7829", "#7F6226", "#654E22", "#4E3D1F", "#3B2F1B"]
    for i, (name, v) in enumerate(langs[:8]):
        pct = 100 * v / total
        out.append(f'<text x="{lx}" y="{y}" font-size="11.5" fill="{TEXT if i<2 else MUTED}">'
                   f'{esc(name)}</text>')
        out.append(f'<text x="{lx+colw}" y="{y}" font-size="11" fill="{FAINT}" '
                   f'text-anchor="end">{pct:.1f}%</text>')
        out.append(f'<rect x="{lx}" y="{y+6}" width="{colw:.0f}" height="3" rx="1.5" '
                   f'fill="{INK2}"/>')
        out.append(f'<rect x="{lx}" y="{y+6}" width="{max(colw*pct/100, 2):.1f}" '
                   f'height="3" rx="1.5" fill="{ramp[i]}"/>')
        y += 27
    out.append(f'<text x="{lx}" y="{y+12}" font-size="10.5" fill="{FAINT}">'
               f'{total:,} bytes across public repositories</text>')

    # right: composition by repository creation year
    years = sorted(traj)
    bw, gap = 46, 34
    base, top = 262, 66
    bx = rx + 14
    keys = ["TypeScript", "JavaScript", "Python", "PLpgSQL", "Java"]
    kc = {"TypeScript": GOLD, "JavaScript": "#C29430", "Python": "#987231",
          "PLpgSQL": "#7A5C2E", "Java": "#5E4A2A"}
    for yr in years:
        d = traj[yr]
        tot = sum(d.values())
        cy = base
        for k in keys:
            if not d.get(k):
                continue
            hgt = (base - top) * d[k] / tot
            cy -= hgt
            out.append(f'<rect x="{bx}" y="{cy:.1f}" width="{bw}" height="{hgt:.1f}" '
                       f'fill="{kc[k]}"/>')
        out.append(f'<text x="{bx + bw/2}" y="{base+18}" font-size="11" fill="{MUTED}" '
                   f'text-anchor="middle">{yr}</text>')
        kb = f"{tot/1000:.0f} KB" if tot < 1_000_000 else f"{tot/1_000_000:.1f} MB"
        out.append(f'<text x="{bx + bw/2}" y="{base+33}" font-size="9" fill="{FAINT}" '
                   f'text-anchor="middle">{kb}</text>')
        bx += bw + gap
    leg = rx + 14
    for k in keys:
        out.append(f'<rect x="{leg}" y="{top-26}" width="8" height="8" rx="2" fill="{kc[k]}"/>')
        out.append(f'<text x="{leg+13}" y="{top-19}" font-size="9.5" fill="{FAINT}">'
                   f'{esc(k)}</text>')
        leg += len(k) * 5.6 + 26
    write("languages.svg", svg(W, 320, "".join(out)))


# --------------------------------------------------------------------- 5. cards

def card(slug: str, name: str, blurb: list[str], stack_items: list[str],
         accent: str, meta: str) -> None:
    h = 30 + 17 * len(blurb) + 52
    out = [
        f'<rect width="6" height="{h}" fill="{accent}"/>',
        f'<rect x="6" width="2" height="{h}" fill="{accent}" opacity=".25"/>',
        f'<text x="34" y="38" font-size="17" font-weight="600" fill="{TEXT}" '
        f'letter-spacing=".01em">{esc(name)}</text>',
        f'<text x="{W-34}" y="38" font-size="10" fill="{accent}" '
        f'letter-spacing=".14em" text-anchor="end">{esc(meta)}</text>',
    ]
    y = 60
    for ln in blurb:
        out.append(f'<text x="34" y="{y}" font-size="12" fill="{MUTED}">{esc(ln)}</text>')
        y += 17
    cx = 34
    for it in stack_items:
        w = len(it) * 6.4 + 18
        out.append(
            f'<rect x="{cx}" y="{h-30}" width="{w:.0f}" height="20" rx="3" '
            f'fill="{INK2}" stroke="{LINE}"/>'
            f'<text x="{cx + w/2:.0f}" y="{h-16}" font-size="10.5" fill="{MUTED}" '
            f'text-anchor="middle">{esc(it)}</text>'
        )
        cx += w + 7
    write(f"card-{slug}.svg", svg(W, h, "".join(out)))


# -------------------------------------------------------------------- 6. contact

def section(slug: str, text: str, note: str = "") -> None:
    body = label(44, 30, text, size=10, fill=GOLD_D)
    if note:
        body += (f'<text x="{W-44}" y="30" font-size="10" fill="{FAINT}" '
                 f'letter-spacing=".1em" text-anchor="end">{esc(note)}</text>')
    write(f"label-{slug}.svg", svg(W, 46, body))


def contact() -> None:
    for slug, text in [("email", "EMAIL"), ("github", "GITHUB"),
                       ("linkedin", "LINKEDIN"), ("site", "WEBSITE")]:
        w, h = len(text) * 8.4 + 46, 38
        body = (
            f'<circle cx="20" cy="{h/2}" r="3.5" fill="{GOLD}"/>'
            f'<text x="34" y="{h/2+4}" font-size="11" fill="{TEXT}" '
            f'letter-spacing=".16em">{esc(text)}</text>'
        )
        markup = (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.0f}" height="{h}" '
            f'viewBox="0 0 {w:.0f} {h}" font-family="{MONO}" role="img">'
            f'<rect width="{w:.0f}" height="{h}" rx="6" fill="{INK1}"/>'
            f'<rect x=".5" y=".5" width="{w-1:.0f}" height="{h-1}" rx="5.5" '
            f'fill="none" stroke="{GOLD_D}" stroke-opacity=".5"/>{body}</svg>'
        )
        write(f"contact-{slug}.svg", markup)


# ------------------------------------------------------------------------ build

def main() -> None:
    data = json.loads((ROOT / "data.json").read_text(encoding="utf-8"))
    portrait = (ROOT / "assets" / "portrait.txt").read_text(encoding="utf-8").rstrip("\n")
    tones = (ROOT / "assets" / "portrait-tone.txt").read_text(encoding="utf-8").rstrip("\n")

    print("building assets:")
    hero(portrait, tones)
    about()
    section("work", "SELECTED WORK", "FOUR PROJECTS, ALL DEPLOYED OR TESTED")
    section("contact", "CONTACT")
    stack()
    languages([(k, v) for k, v in data["languages"]], data["trajectory"])

    card("conversekit", "ConverseKit",
         ["Multi-tenant AI chat that installs with one script tag. Answers from each",
          "client's own documents, eleven LLM vendors behind one interface, tenants",
          "isolated by row-level security rather than by application code."],
         ["TypeScript", "Cloudflare Workers", "Supabase", "pgvector", "Hono"],
         "#EEBA2B", "LIVE")

    card("synapsedeck", "SynapseDeck",
         ["Notes in, flashcards out, reviewed on a real FSRS scheduler. Cards stream",
          "in as the model writes them and pass a review gate before entering a deck.",
          "Every figure on the progress page is counted from an append-only log."],
         ["React 19", "TypeScript", "Supabase", "Edge Functions", "ts-fsrs"],
         "#C8F14D", "LIVE")

    card("ragbot", "Document RAG QA Bot",
         ["Question answering grounded in uploaded PDFs: chunking, embedding, vector",
          "retrieval and generation that cites what it read. Built as the capstone",
          "for IBM's AI engineering coursework."],
         ["Python", "LangChain", "Gemini", "ChromaDB"],
         "#4589FF", "CAPSTONE")

    card("littlelemon", "Little Lemon API",
         ["Restaurant back end covering all 21 acceptance criteria of the Meta",
          "capstone: role-based permissions across four user groups, cart and order",
          "flows, throttling, and 24 acceptance tests."],
         ["Python", "Django", "Django REST Framework"],
         "#44B78B", "CAPSTONE")

    contact()
    print("done.")


if __name__ == "__main__":
    main()
