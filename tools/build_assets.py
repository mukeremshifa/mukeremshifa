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
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from brand import SIGNATURE_ASPECT, SIGNATURE_PATHS, SIGNATURE_VIEWBOX  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
W = 880

# ---------------------------------------------------------------- design tokens

# Every value below is the portfolio's dark-theme token of the same role, from
# app/globals.css. The README is a dark document, so it takes the dark palette.

INK0 = "#161109"   # deepest ground   -- dark --canvas
INK1 = "#1b1813"   # card ground      -- dark --surface
INK2 = "#2a2722"   # raised chip      -- dark --surface-alt
LINE = "#34312c"   #                  -- dark --border-subtle
TEXT = "#f3ece2"   #                  -- dark --text
MUTED = "#a3988c"  #                  -- dark --text-muted
FAINT = "#7a7168"  #                  -- dark --border-strong

BRAND = "#52b788"   # portfolio dark --brand. NOT #184e38: that is the
                    # light-theme value and is invisible on this ground.
BRAND_D = "#317453" # dimmed brand, for eyebrows and hairline strokes. Derived,
                    # not quoted: the site has no dimmed-emerald token because it
                    # never needs one. Sits between --brand-soft and --brand,
                    # and clears 3:1 on INK1 (3.16:1).
BRAND_SOFT = "#172a21"  # dark --brand-soft

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

def hero() -> None:
    # left column: the portfolio's signature mark, as outlines rather than text
    sig_x, sig_w = 40, 440
    sig_h = sig_w / SIGNATURE_ASPECT

    # terminal transcript, typed line by line
    cx = 524
    seq = [
        ("cmd", "whoami"),
        ("out", "Mukerem Shifa"),
        ("dim", "AI Engineer and Full-stack Developer"),
        ("gap", ""),
        ("cmd", "cat now.txt"),
        ("out", "Building ConverseKit and SynapseDeck."),
        ("dim", "Learning how to evaluate retrieval"),
        ("dim", "instead of eyeballing it."),
        ("gap", ""),
        ("dim", "// powered by coffee"),
    ]

    lines, css, t = [], [], 0.6
    y = 128
    for kind, txt in seq:
        if kind == "gap":
            y += 13
            continue
        i = len(lines)
        if kind == "cmd":
            body = (f'<tspan fill="{BRAND}">$</tspan> '
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

    cursor = (f'<rect x="{cx}" y="{y-11}" width="7.5" height="14" fill="{BRAND}" '
              f'class="cur" opacity="0"/>')
    css.append(f".cur{{animation:blink 1.05s steps(1) {t:.2f}s infinite}}"
               "@keyframes blink{0%,50%{opacity:1}51%,100%{opacity:0}}")
    css.append("@media(prefers-reduced-motion:reduce){"
               "[class^='r']{width:330px!important;animation:none!important}"
               ".cur{opacity:1;animation:none}}")

    # the transcript is now the tallest element: the composition rebalances from
    # side-by-side to a short banner, and the signature centres against it
    h = int(y + 46)
    sig_y = (h - sig_h) / 2
    sig = (
        f'<svg x="{sig_x}" y="{sig_y:.1f}" width="{sig_w}" height="{sig_h:.0f}" '
        f'viewBox="{SIGNATURE_VIEWBOX}" preserveAspectRatio="xMinYMid meet">'
        f'<g fill="{TEXT}">'
        + "".join(f'<path d="{d}"/>' for d in SIGNATURE_PATHS)
        + '</g></svg>'
    )
    body = (
        sig
        + label(cx, 74, "MUKEREM SHIFA", size=15, fill=TEXT, spacing=".26em", weight="600")
        + label(cx, 95, "RAS AL-KHAIMAH, UAE  /  BUILDING AI PRODUCTS END TO END", size=9.5)
        + f'<line x1="{cx}" y1="108" x2="{W-44}" y2="108" stroke="{LINE}"/>'
        + "".join(lines) + cursor
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
        ("txt",  "I learn by shipping whole systems rather than tutorials."),
        ("txt",  "The three projects below"),
        ("key",  "are deployed, tested and documented."),
        ("gap",  ""),
        ("dim",  "// open to engineering roles and selected contract work"),
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
        fill = {"txt": TEXT, "dim": FAINT, "key": BRAND}[kind]
        out.append(f'<text x="{x}" y="{y}" font-size="13.5" fill="{fill}">'
                   f'{esc(txt)}</text>')
        y += lh
    h = int(y + 24)
    body = (
        f'<rect x="70" y="20" width="1" height="{h-40}" fill="{LINE}"/>'
        + label(96, 36, "ABOUT", size=10, fill=BRAND_D)
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
    out = [label(x0, 34, "STACK", size=10, fill=BRAND_D)]
    for gi, (name, items) in enumerate(groups):
        out.append(f'<text x="{x0}" y="{y+13}" font-size="10" fill="{FAINT}" '
                   f'letter-spacing=".16em">{esc(name)}</text>')
        cx = x0 + 150
        for it in items:
            w = len(it) * 7.0 + 22
            if cx + w > W - 44:
                cx = x0 + 150
                y += 30
            tint = BRAND if gi in (0, 4) else MUTED
            fill = BRAND_SOFT if gi in (0, 4) else INK2
            out.append(
                f'<rect x="{cx}" y="{y}" width="{w:.0f}" height="24" rx="4" '
                f'fill="{fill}" stroke="{BRAND_D if gi in (0,4) else LINE}" '
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
        label(lx, 34, "LANGUAGES", size=10, fill=BRAND_D),
        label(rx, 34, "TRAJECTORY", size=10, fill=BRAND_D),
        f'<line x1="{rx-28}" y1="20" x2="{rx-28}" y2="290" stroke="{LINE}"/>',
    ]

    # left: one thin bar per language
    y = 62
    ramp = [BRAND, "#47a077", "#3d8a66", "#337457",
            "#2a5f47", "#224b38", "#1a3829", "#13261c"]
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
    kc = {"TypeScript": BRAND,     "JavaScript": "#3d8a66",
          "Python":     "#2f6f52", "PLpgSQL":    "#24543e",
          "Java":       "#1a3c2c"}
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
    body = label(44, 30, text, size=10, fill=BRAND_D)
    if note:
        body += (f'<text x="{W-44}" y="30" font-size="10" fill="{FAINT}" '
                 f'letter-spacing=".1em" text-anchor="end">{esc(note)}</text>')
    write(f"label-{slug}.svg", svg(W, 46, body))


def contact() -> None:
    for slug, text in [("email", "EMAIL"), ("github", "GITHUB"),
                       ("linkedin", "LINKEDIN"), ("site", "WEBSITE")]:
        w, h = len(text) * 8.4 + 46, 38
        body = (
            f'<circle cx="20" cy="{h/2}" r="3.5" fill="{BRAND}"/>'
            f'<text x="34" y="{h/2+4}" font-size="11" fill="{TEXT}" '
            f'letter-spacing=".16em">{esc(text)}</text>'
        )
        markup = (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.0f}" height="{h}" '
            f'viewBox="0 0 {w:.0f} {h}" font-family="{MONO}" role="img">'
            f'<rect width="{w:.0f}" height="{h}" rx="6" fill="{INK1}"/>'
            f'<rect x=".5" y=".5" width="{w-1:.0f}" height="{h-1}" rx="5.5" '
            f'fill="none" stroke="{BRAND_D}" stroke-opacity=".5"/>{body}</svg>'
        )
        write(f"contact-{slug}.svg", markup)


# ------------------------------------------------------------------------ build

def main() -> None:
    data = json.loads((ROOT / "data.json").read_text(encoding="utf-8"))

    print("building assets:")
    hero()
    about()
    section("work", "SELECTED WORK", "THREE PROJECTS, TWO LIVE")
    section("contact", "CONTACT")
    stack()
    languages([(k, v) for k, v in data["languages"]], data["trajectory"])

    # The set is the portfolio's three featured projects, in the site's order.
    # Anything shown here must exist in the portfolio's content/projects/.
    card("conversekit", "ConverseKit",
         ["Multi-tenant AI chat that installs with one script tag. Answers from each",
          "client's own documents, eleven LLM vendors behind one interface, tenants",
          "isolated by row-level security rather than by application code."],
         ["TypeScript", "Cloudflare Workers", "Supabase", "pgvector", "Hono"],
         BRAND, "LIVE")

    card("synapsedeck", "SynapseDeck",
         ["Notes in, flashcards out, reviewed on a real FSRS scheduler. Cards stream",
          "in as the model writes them and pass a review gate before entering a deck.",
          "Every figure on the progress page is counted from an append-only log."],
         ["React 19", "TypeScript", "Supabase", "Edge Functions", "ts-fsrs"],
         BRAND, "LIVE")

    card("surveyquest", "Survey Quest",
         ["A React prototype that turns a questionnaire into a light game loop:",
          "XP, levels, badges and a confetti finish. Progress is awarded for",
          "participation only, so the survey data stays honest."],
         ["React", "TypeScript", "Vite"],
         BRAND, "PROTOTYPE")

    contact()
    print("done.")


if __name__ == "__main__":
    main()
