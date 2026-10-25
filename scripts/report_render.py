#!/usr/bin/env python3
"""
Visual reports: one renderer for every report the team emails Paul (built 24 Oct 2026 on
Paul's instruction: "change the output from just pure text to visual dashboards that
contain the text in them"). Spec and JSON shape: shared/visual-reports.md.

An agent writes its report as a small JSON file (headline, up to four number tiles,
sections of items with a tone each). This script turns it into:

  --html  an email-safe HTML page (tables and inline styles only, no scripts, no images,
          no web fonts), BTS navy and gold, readable on the phone and in Outlook.
  --text  the plain-text twin: the same content in the old plain layout. Gmail sends it
          as the text alternative, and its line structure is what the Morning Desk
          parses, so the HTML is built to strip down to the same lines.

The cloud routines run it with Bash in their cloned repo and pass the two files to
Gmail send_message (htmlBody and body). The Mac scripts import render_html and
render_text directly. Standard library only.

Run:  python3 shared/report_render.py report.json --html out.html --text out.txt
      python3 shared/report_render.py report.json --check     validate only, print warnings
Exit 0 on success (warnings go to stderr), 2 when the JSON is not usable.
"""

import argparse
import html
import json
import re
import sys

DESK_URL = "https://claude.ai/artifact/9Yg4BMV4cRjttrDxCpaPKy"
TONES = ("bad", "warn", "ok", "info", "none")
STYLES = ("list", "numbered", "text", "small")
MAX_TILES = 4

# Palette matches desk/morning-desk.html so the email and the page read as one system.
# Inline styles only. Gmail send_message, the cloud routines' sender, strips <style> blocks,
# class attributes, the background shorthand, list-style and opacity before the mail leaves
# Google (tested 25 Oct 2026 with a sent brief and a draft probe), so every rule sits on its
# element as longhand, with bgcolor attributes on the filled cells. The font is set once on the
# wrapper table and inherited.
INK, INK2, INK3, LINE, GOLD = "#0f1629", "#465069", "#737d97", "#d8dce6", "#C9A84C"
FONT = "font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
TONE_INK = {"bad": "#ad2a22", "warn": "#93570a", "ok": "#1c774c", "info": "#1d4f91", "none": INK3}
TONE_EDGE = {"bad": "#ad2a22", "warn": "#d08a1e", "ok": "#1c774c", "info": "#1d4f91", "none": LINE}
TONE_WASH = {"bad": "#fbe5e3", "warn": "#fbefd8", "ok": "#e2f2e9", "info": "#e3ecf8", "none": "#e6e9f0"}
TONE_PILL = dict(TONE_INK, none=INK2)
BAR_FILL = {"bad": "#ad2a22", "warn": "#d08a1e", "ok": "#1c774c", "info": "#1d4f91", "gold": GOLD}
ST = {
    "outer": "background-color:#eceef3",
    "wrap": f"max-width:640px;margin:0 auto;{FONT};color:{INK}",
    "hd": f"background-color:{INK};border-bottom:3px solid {GOLD};padding:20px 22px 18px",
    "eb": f"font-size:11px;font-weight:700;letter-spacing:.09em;text-transform:uppercase;color:{GOLD}",
    "ti": "font-size:26px;line-height:1.15;font-weight:700;color:#ffffff;margin-top:6px",
    "dt": "font-size:13px;color:#aab1c6;margin-top:4px",
    "hlc": "padding:16px 16px 4px",
    "hl": f"padding:14px 16px;background-color:#f7f0da;border-left:4px solid {GOLD};border-radius:6px;"
          f"font-size:16px;line-height:1.45;font-weight:600;color:{INK}",
    "tiles": "padding:12px 8px 4px",
    "tile": f"background-color:#ffffff;border:1px solid {LINE};border-radius:8px;padding:10px 10px 9px;vertical-align:top",
    "tv": "font-size:26px;line-height:1.05;font-weight:700",
    "tl": f"font-size:12px;line-height:1.3;color:{INK2};margin-top:4px",
    "sec": "padding:8px 16px",
    "card": f"background-color:#ffffff;border:1px solid {LINE};border-radius:10px",
    "sh": f"padding:14px 16px 4px;font-size:13px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:{INK2}",
    "n": "color:#b08d2c;font-weight:800",
    "sb": f"padding:4px 16px 14px;font-size:15px;line-height:1.5;color:{INK}",
    "sm": f"font-size:12.5px;line-height:1.5;color:{INK3}",
    "in": f"margin:0 0 10px;color:{INK2}",
    "gl": f"margin:12px 0 6px;font-size:12px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:{INK3}",
    "ul": "margin:0;padding:0",
    "li": "display:block;margin:0 0 8px;padding:9px 12px;background-color:#f6f7fa;border-radius:6px",
    "lism": "display:block;margin:0;padding:0 0 3px",
    "pl": "display:inline-block;padding:1px 7px;border-radius:999px;font-size:11px;font-weight:700;letter-spacing:.04em;text-transform:uppercase",
    "sub": f"margin-top:4px;font-size:13.5px;line-height:1.45;color:{INK2}",
    "lk": "margin-top:4px;font-size:13px",
    "a": "color:#1d4f91;text-decoration:underline",
    "ni": "margin:0 0 10px;padding:9px 12px;background-color:#f6f7fa;border-left:4px solid #1d4f91;border-radius:6px",
    "nt": "font-weight:600",
    "p": "margin:0 0 10px",
    "bar": "padding:3px 0",
    "bl": f"font-size:13.5px;line-height:1.3;color:{INK};padding:3px 10px 3px 0",
    "bv": "font-weight:700",
    "bk": "border-radius:5px;height:10px;line-height:10px;font-size:1px",
    "ft": "padding:14px 16px 28px;text-align:center",
    "btn": f"display:inline-block;background-color:{GOLD};color:{INK};text-decoration:none;font-weight:700;font-size:14px;"
           "padding:11px 18px;border-radius:8px",
    "fn": f"margin-top:12px;font-size:12px;line-height:1.5;color:{INK3}",
}


def sa(name, extra=""):
    """A style attribute: the named rule, then any per-element extras (later declarations win)."""
    return f' style="{ST[name]}{";" + extra if extra else ""}"'


def bg(colour):
    return f' bgcolor="{colour}"'


class ReportError(ValueError):
    pass


def esc(s):
    return html.escape(str(s if s is not None else ""), quote=True)


def safe_url(u):
    u = str(u or "").strip()
    return u if re.match(r"^https?://[^\s<>\"']+$", u) else ""


def tone_of(x):
    t = str((x or {}).get("tone") or "none").lower()
    return t if t in TONES else "none"


def ascii_warnings(rep):
    """House style is ASCII only (shared/house-style-summary.md); quoted sources are the exception, so warn, never rewrite."""
    found = sorted({c for c in json.dumps(rep, ensure_ascii=False) if ord(c) > 127})
    return [f"non-ASCII characters present: {' '.join(found)} (fine only inside a quoted source)"] if found else []


def validate(rep):
    if not isinstance(rep, dict):
        raise ReportError("top level must be an object")
    for k in ("title", "date", "headline", "sections"):
        if not rep.get(k):
            raise ReportError(f"missing '{k}'")
    if not isinstance(rep["sections"], list):
        raise ReportError("'sections' must be a list")
    warns = []
    tiles = rep.get("tiles") or []
    if len(tiles) > MAX_TILES:
        warns.append(f"{len(tiles)} tiles given, only the first {MAX_TILES} are shown")
    for i, s in enumerate(rep["sections"], 1):
        if not s.get("heading"):
            raise ReportError(f"section {i} has no 'heading'")
        st = s.get("style", "list")
        if st not in STYLES:
            raise ReportError(f"section {i} style '{st}' is not one of {', '.join(STYLES)}")
        for it in items_of(s):
            for ln in it.get("links") or []:
                if not safe_url(ln.get("url")):
                    warns.append(f"section {i}: dropped a link that is not http(s): {ln.get('url')!r}")
    return warns + ascii_warnings(rep)


def items_of(sec):
    out = list(sec.get("items") or [])
    for g in sec.get("groups") or []:
        out += list(g.get("items") or [])
    return out


# ---------- HTML ----------

def h_links(links):
    parts = [f'<a href="{esc(safe_url(l.get("url")))}"{sa("a")}>{esc(l.get("label") or "Open")}</a>'
             for l in links or [] if safe_url(l.get("url"))]
    return f'<div{sa("lk")}>{" &nbsp;|&nbsp; ".join(parts)}</div>' if parts else ""


def h_item(it, small=False):
    t = tone_of(it)
    pill = f"background-color:{TONE_WASH[t]};color:{TONE_PILL[t]}"
    tag = f'<span{sa("pl", pill)}>{esc(it["tag"])}</span> ' if it.get("tag") else ""
    src = f'<b>{esc(it["source"])}</b>: ' if it.get("source") else ""
    subs = "".join(f'<div{sa("sub")}>{esc(s)}</div>' for s in it.get("sub") or [] if s)
    style = sa("lism") if small else sa("li", f"border-left:4px solid {TONE_EDGE[t]}")
    return f'<li{style}>{tag}{src}{esc(it.get("text"))}{subs}{h_links(it.get("links"))}</li>'


def h_list(items, small=False):
    return f'<ul{sa("ul")}>{"".join(h_item(i, small) for i in items)}</ul>'


def h_numbered(items, start=1):
    out = []
    for n, it in enumerate(items, start):
        meta = "".join(f'<div{sa("sub")}>{esc(s)}</div>' for s in it.get("sub") or [] if s)
        out.append(f'<div{sa("ni")}><div{sa("nt")}>{n}. {esc(it.get("text"))}</div>{meta}{h_links(it.get("links"))}</div>')
    return "".join(out)


def h_bars(bars):
    vals = [float(b.get("value") or 0) for b in bars]
    top = max(vals + [1.0])
    rows = []
    for b, v in zip(bars, vals):
        pct = max(2, round(100 * v / top)) if v > 0 else 0
        fc = BAR_FILL.get(str(b.get("tone") or ""), INK)
        fill = f'<td width="{pct}%"{bg(fc)}{sa("bk", "background-color:" + fc)}>&nbsp;</td>' if pct else ""
        rest = f'<td width="{100 - pct}%"{bg("#e6e9f0")}{sa("bk", "background-color:#e6e9f0")}>&nbsp;</td>' if pct < 100 else ""
        shown = b.get("display", b.get("value"))
        rows.append(
            f'<tr><td width="42%"{sa("bl")}>{esc(b.get("label"))} <span{sa("bv")}>{esc(shown)}</span></td>'
            f'<td{sa("bar")}><table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr>{fill}{rest}</tr></table></td></tr>')
    return f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0">{"".join(rows)}</table>'


def h_body(sec, small=False):
    st = sec.get("style", "list")
    out = [f'<div{sa("in")}>{esc(sec["intro"])}</div>'] if sec.get("intro") else []
    if sec.get("bars"):
        out.append(h_bars(sec["bars"]))
    if st == "text":
        out += [f'<div><div{sa("p")}>{esc(p)}</div></div>' for p in sec.get("paras") or [] if p]
    elif st == "numbered":
        out.append(h_numbered(sec.get("items") or []))
    else:
        if sec.get("items"):
            out.append(h_list(sec["items"], small))
        for g in sec.get("groups") or []:
            out.append(f'<div{sa("gl")}>{esc(g.get("label"))}</div>')
            if g.get("text"):
                out.append(f'<div{sa("p")}>{esc(g["text"])}</div>')
            if g.get("items"):
                out.append(f'<div{sa("sm")}>{h_list(g["items"], True)}</div>' if g.get("small") else h_list(g["items"], small))
            elif g.get("empty"):
                out.append(f'<div{sa("p")}>{esc(g["empty"])}</div>')
        if not items_of(sec) and sec.get("empty"):
            out.append(f'<div{sa("p")}>{esc(sec["empty"])}</div>')
    if st != "text" and sec.get("paras"):
        out += [f'<div><div{sa("p")}>{esc(p)}</div></div>' for p in sec["paras"] if p]
    if sec.get("note"):
        out.append(f'<div{sa("sub")}>{esc(sec["note"])}</div>')
    return "".join(out)


def h_heading(text):
    m = re.match(r"^(\d{1,2}\.)\s+(.*)$", text)
    return f'<span{sa("n")}>{esc(m.group(1))}</span> {esc(m.group(2))}' if m else esc(text)


def render_html(rep):
    validate(rep)
    tiles = (rep.get("tiles") or [])[:MAX_TILES]
    w = f"{100 // len(tiles)}%" if tiles else "25%"
    # One row of cells (not nested tables) so every tile takes the height of the tallest.
    tile_cells = "".join(
        f'<td width="{w}"{bg("#ffffff")}{sa("tile", "border-top:3px solid " + TONE_INK[tone_of(t)])}>'
        f'<div{sa("tv", "color:" + (TONE_INK[tone_of(t)] if tone_of(t) != "none" else INK))}>{esc(t.get("value"))}</div>'
        f'<div{sa("tl")}>{esc(t.get("label"))}</div></td>' for t in tiles)
    secs = []
    for sec in rep["sections"]:
        small = sec.get("style") == "small"
        body = h_body(dict(sec, style="list") if small else sec, small)
        secs.append(
            f'<tr><td{sa("sec")}><table role="presentation" width="100%" cellpadding="0" cellspacing="0"{bg("#ffffff")}{sa("card")}>'
            f'<tr><td{sa("sh")}>{h_heading(sec["heading"])}</td></tr>'
            f'<tr><td{sa("sb", ST["sm"] if small else "")}>{body}</td></tr></table></td></tr>')
    eyebrow = "BTS Exec Team / " + str(rep.get("agent") or "")
    foot = esc(rep.get("footer") or "")
    desk = "" if rep.get("desk") is False else f'<a href="{DESK_URL}"{sa("btn")}>Open the Morning Desk</a>'
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>{esc(rep["title"])} - {esc(rep["date"])}</title></head>'
        '<body style="margin:0;padding:0;background-color:#eceef3">'
        f'<div style="display:none;max-height:0;overflow:hidden">{esc(rep["headline"])}</div>'
        f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0"{bg("#eceef3")}{sa("outer")}><tr><td>'
        f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" align="center"{sa("wrap")}>'
        f'<tr><td{bg(INK)}{sa("hd")}>'
        f'<div{sa("eb")}>{esc(eyebrow)}</div><div{sa("ti")}>{esc(rep["title"])}</div><div{sa("dt")}>{esc(rep["date"])}</div></td></tr>'
        f'<tr><td{sa("hlc")}><div{sa("hl")}>{esc(rep["headline"])}</div></td></tr>'
        + (f'<tr><td{sa("tiles")}><table role="presentation" width="100%" cellpadding="0" cellspacing="0" '
           f'style="border-collapse:separate;border-spacing:8px 0"><tr>{tile_cells}</tr></table></td></tr>' if tiles else "")
        + "".join(secs)
        + f'<tr><td{sa("ft")}>{desk}<div{sa("fn")}>{foot}</div></td></tr>'
        '</table></td></tr></table></body></html>')


# ---------- plain text ----------

def t_item(it, numbered_n=None):
    lead = f"{numbered_n}. " if numbered_n else "- "
    tag = f"[{it['tag']}] " if it.get("tag") and not numbered_n else ""
    src = f"{it['source']}: " if it.get("source") else ""
    lines = [f"{lead}{tag}{src}{it.get('text', '')}"]
    pad = "   " if numbered_n else "  "
    lines += [f"{pad}{s}" for s in it.get("sub") or [] if s]
    lines += [f"{pad}{l.get('label')}: {safe_url(l.get('url'))}" if numbered_n is None else f"{pad}{safe_url(l.get('url'))}"
              for l in it.get("links") or [] if safe_url(l.get("url"))]
    return lines


def render_text(rep):
    validate(rep)
    out = [f"{rep['title']} - {rep['date']}", rep["headline"], ""]
    tiles = (rep.get("tiles") or [])[:MAX_TILES]
    if tiles:
        out += [" | ".join(f"{t.get('value')} {t.get('label')}" for t in tiles), ""]
    for sec in rep["sections"]:
        st = sec.get("style", "list")
        out.append(sec["heading"])
        if sec.get("intro"):
            out.append(sec["intro"])
        out += [f"{b.get('label')}: {b.get('display', b.get('value'))}" for b in sec.get("bars") or []]
        if st == "text":
            for p in sec.get("paras") or []:
                out += [p, ""]
            out.pop() if out and out[-1] == "" else None
        elif st == "numbered":
            for n, it in enumerate(sec.get("items") or [], 1):
                out += t_item(it, n) + [""]
            out.pop() if out and out[-1] == "" else None
        else:
            for it in sec.get("items") or []:
                out += t_item(it)
            for g in sec.get("groups") or []:
                out.append(g.get("label", ""))
                if g.get("text"):
                    out.append(g["text"])
                for it in g.get("items") or []:
                    out += t_item(it)
                if not g.get("items") and g.get("empty"):
                    out.append(g["empty"])
            if not items_of(sec) and sec.get("empty"):
                out.append(sec["empty"])
        if st != "text":
            out += [p for p in sec.get("paras") or [] if p]
        if sec.get("note"):
            out.append(sec["note"])
        out.append("")
    if rep.get("desk") is not False:
        out.append(f"Open the Morning Desk: {DESK_URL}")
    if rep.get("footer"):
        out.append(rep["footer"])
    return "\n".join(out).rstrip() + "\n"


def main():
    ap = argparse.ArgumentParser(description="Render a visual report (shared/visual-reports.md).")
    ap.add_argument("report", help="path to the report JSON")
    ap.add_argument("--html", help="write the email HTML here")
    ap.add_argument("--text", help="write the plain-text twin here")
    ap.add_argument("--check", action="store_true", help="validate only")
    a = ap.parse_args()
    try:
        with open(a.report, encoding="utf-8") as f:
            rep = json.load(f)
        for w in validate(rep):
            print(f"warning: {w}", file=sys.stderr)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if a.check:
        print("ok")
        return 0
    if a.html:
        with open(a.html, "w", encoding="utf-8") as f:
            f.write(render_html(rep))
    if a.text:
        with open(a.text, "w", encoding="utf-8") as f:
            f.write(render_text(rep))
    if not (a.html or a.text):
        sys.stdout.write(render_text(rep))
    return 0


if __name__ == "__main__":
    sys.exit(main())
