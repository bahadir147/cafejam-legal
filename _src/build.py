#!/usr/bin/env python3
"""Generates the static Café Jam legal site from _src/lang_*.py.

Run from anywhere:  python3 legal-site/_src/build.py
Edit texts in _src/lang_<code>.py, constants (email, dates, links) here, then rebuild.
All links are relative so the site works under a GitHub Pages subpath (/cafejam-legal/).
"""
import html
import importlib.util
import os
import re
import sys

sys.dont_write_bytecode = True

# ---- single source of truth ------------------------------------------------
# Placeholder until the user picks the support address. build.py warns while it is still set.
CONTACT_EMAIL = "bahadirdemirbusiness@gmail.com"
GAME = "Café Jam"
STORE_TITLE = "Café Jam"  # the brand; per-language store titles (e.g. "Café Jam: Coffee Sort Puzzle") live in docs/store/STORE_LISTING.md
PUBLISHER = "Synverse"
PACKAGE_ID = "com.synverse.cafejam"
LINKS = {
    "%U_PRIV%": "https://unity.com/legal/game-player-and-app-user-privacy-policy",
    "%U_LEGAL%": "https://unity.com/legal/privacy-policy",
    "%G_PRIV%": "https://policies.google.com/privacy",
    "%G_PARTNER%": "https://policies.google.com/technologies/partner-sites",
    "%G_ADS%": "https://myadcenter.google.com/",
    "%APPLE_EULA%": "https://www.apple.com/legal/internet-services/itunes/dev/stdeula/",
    "%KVKK%": "https://www.kvkk.gov.tr/",
    "%EDPB%": "https://edpb.europa.eu/about-edpb/about-edpb/members_en",
}
LANGS = ["en", "tr", "es", "pt-BR", "fr", "de", "id"]  # en is the default (index.html)
PAGES = ["privacy", "terms", "delete"]
DIRS = {"home": "", "privacy": "privacy", "terms": "terms", "delete": "delete-data"}

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "_src")


def load(code):
    path = os.path.join(SRC, "lang_%s.py" % code.replace("-", "_"))
    spec = importlib.util.spec_from_file_location("lang_" + code, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.L


def filename(code):
    return "index.html" if code == "en" else code + ".html"


def href(from_page, to_page, code):
    """Relative link between two generated pages."""
    up = "../" if DIRS[from_page] else ""
    d = DIRS[to_page]
    return up + (d + "/" if d else "") + filename(code)


CSS = """
:root{color-scheme:light dark;--bg:#fff8ee;--fg:#2b1d14;--muted:#6e5a4c;--line:#ecdcc8;--card:#fff;--accent:#c8733a;--link:#9a4a1c}
@media (prefers-color-scheme:dark){:root{--bg:#1a130e;--fg:#f3e8dc;--muted:#b09c8a;--line:#3a2c22;--card:#231a13;--accent:#e89a5c;--link:#f2b27a}}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.6 system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif}
a{color:var(--link)}
.wrap{max-width:760px;margin:0 auto;padding:0 16px}
header{border-bottom:1px solid var(--line);background:var(--card)}
.top{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:8px 16px;padding:14px 0}
.brand{font-weight:700;font-size:18px;text-decoration:none;color:var(--fg)}
.brand span{color:var(--accent)}
nav.pages{display:flex;flex-wrap:wrap;gap:4px 14px;font-size:15px}
nav.pages a{text-decoration:none}
nav.pages a[aria-current]{font-weight:700;color:var(--fg)}
nav.langs{display:flex;flex-wrap:wrap;gap:4px 10px;font-size:13px;padding:0 0 12px;color:var(--muted)}
nav.langs a{text-decoration:none}
nav.langs a[aria-current]{color:var(--fg);font-weight:700}
main{padding:24px 0 40px}
h1{font-size:28px;line-height:1.25;margin:0 0 6px}
h2{font-size:20px;margin:32px 0 8px;padding-top:8px;border-top:1px solid var(--line)}
h3{font-size:16px;margin:20px 0 4px}
.meta{color:var(--muted);font-size:14px;margin:0 0 20px}
.box{background:var(--card);border:1px solid var(--line);border-left:4px solid var(--accent);border-radius:8px;padding:12px 16px;margin:16px 0}
.box ul{margin:6px 0;padding-left:20px}
.toc{font-size:15px}
.toc ol{padding-left:22px;margin:6px 0}
table{border-collapse:collapse;width:100%;font-size:14px;margin:8px 0}
th,td{border:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top}
.cards{display:grid;gap:12px;margin:20px 0}
.cards a{display:block;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px;text-decoration:none;color:var(--fg)}
.cards a b{display:block;color:var(--link)}
.cards a small{color:var(--muted)}
footer{border-top:1px solid var(--line);color:var(--muted);font-size:13px;padding:16px 0 32px}
code{font-size:14px;background:var(--card);border:1px solid var(--line);border-radius:4px;padding:0 4px}
"""


def fill(text, page, code):
    e = html.escape(CONTACT_EMAIL)
    email = '<a href="mailto:%s">%s</a>' % (e, e) if "@" in CONTACT_EMAIL else "<b>%s</b>" % e
    rep = {
        "%EMAIL%": email,
        "%EMAIL_RAW%": html.escape(CONTACT_EMAIL),
        "%GAME%": GAME,
        "%STORE%": STORE_TITLE,
        "%PUB%": PUBLISHER,
        "%PKG%": PACKAGE_ID,
        "%PRIVACY_LINK%": href(page, "privacy", code),
        "%TERMS_LINK%": href(page, "terms", code),
        "%DELETE_LINK%": href(page, "delete", code),
    }
    rep.update(LINKS)
    for k, v in rep.items():
        text = text.replace(k, v)
    return text


def page_html(L, page, all_langs):
    code, ui = L["code"], L["ui"]
    if page == "home":
        title = "%s — %s" % (GAME, ui["legal"])
        body = home_body(L)
        desc = ui["tagline"]
    else:
        P = L[page]
        title = "%s — %s" % (P["title"], GAME)
        body = doc_body(L, P)
        desc = P["title"] + " — " + STORE_TITLE
    nav = []
    for p, label in (("home", ui["home"]), ("privacy", ui["privacy"]), ("terms", ui["terms"]), ("delete", ui["delete"])):
        cur = ' aria-current="page"' if p == page else ""
        nav.append('<a href="%s"%s>%s</a>' % (href(page, p, code), cur, html.escape(label)))
    langs = []
    for o in all_langs:
        cur = ' aria-current="true"' if o["code"] == code else ""
        langs.append('<a href="%s" hreflang="%s" lang="%s"%s>%s</a>' % (
            href(page, page, o["code"]), o["code"], o["code"], cur, html.escape(o["name"])))
    alternates = "\n".join('<link rel="alternate" hreflang="%s" href="%s">' % (o["code"], filename(o["code"])) for o in all_langs)
    doc = """<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="light dark">
<meta name="description" content="{desc}">
<meta name="referrer" content="no-referrer">
<title>{title}</title>
{alternates}
<style>{css}</style>
</head>
<body>
<header><div class="wrap">
<div class="top"><a class="brand" href="{home}">Café <span>Jam</span></a>
<nav class="pages" aria-label="{navlabel}">{nav}</nav></div>
<nav class="langs" aria-label="{langlabel}">{langs}</nav>
</div></header>
<main class="wrap">
{body}
</main>
<footer><div class="wrap">© 2026 {pub} · {game} ({pkg}) · {contact}: {email}</div></footer>
</body>
</html>
""".format(lang=L["htmllang"], desc=html.escape(desc), title=html.escape(title), alternates=alternates,
           css=CSS.strip(), home=href(page, "home", code), navlabel=html.escape(ui["menu"]), nav=" ".join(nav),
           langlabel=html.escape(ui["language"]), langs=" · ".join(langs), body=body, pub=PUBLISHER,
           game=GAME, pkg=PACKAGE_ID, contact=html.escape(ui["contact"]), email="%EMAIL%")
    return fill(doc, page, code)


def home_body(L):
    ui = L["ui"]
    cards = []
    for p in PAGES:
        cards.append('<a href="%s"><b>%s</b><small>%s</small></a>' % (
            "%" + {"privacy": "PRIVACY", "terms": "TERMS", "delete": "DELETE"}[p] + "_LINK%",
            html.escape(L[p]["title"]), html.escape(L[p]["blurb"])))
    return """<h1>%s</h1>
<p class="meta">%s · %s</p>
<p>%s</p>
<div class="cards">%s</div>
<p>%s: %%EMAIL%%</p>""" % (html.escape(STORE_TITLE), html.escape(ui["by"]), PACKAGE_ID, ui["landing"],
                           "".join(cards), html.escape(ui["contact"]))


def doc_body(L, P):
    ui = L["ui"]
    out = ["<h1>%s</h1>" % html.escape(P["title"]),
           '<p class="meta">%s · %s: %s</p>' % (html.escape(STORE_TITLE), html.escape(ui["effective"]), html.escape(L["date"]))]
    out.append(P["intro"])
    if P.get("summary"):
        out.append('<div class="box"><b>%s</b><ul>%s</ul></div>' % (
            html.escape(ui["summary"]), "".join("<li>%s</li>" % s for s in P["summary"])))
    secs = P["sections"]
    if len(secs) > 5:
        out.append('<div class="toc"><b>%s</b><ol>%s</ol></div>' % (html.escape(ui["toc"]), "".join(
            '<li><a href="#s%d">%s</a></li>' % (i + 1, html.escape(h)) for i, (h, _) in enumerate(secs))))
    for i, (h, body) in enumerate(secs):
        out.append('<h2 id="s%d">%d. %s</h2>\n%s' % (i + 1, i + 1, html.escape(h), body))
    return "\n".join(out)


def main():
    all_langs = [load(c) for c in LANGS]
    count = 0
    for L in all_langs:
        for page in ["home"] + PAGES:
            d = os.path.join(ROOT, DIRS[page])
            os.makedirs(d, exist_ok=True)
            with open(os.path.join(d, filename(L["code"])), "w", encoding="utf-8") as f:
                out = page_html(L, page, all_langs)
                assert not re.search(r"%[A-Z_]+%", out) and "{{" not in out, (L["code"], page, re.findall(r"%[A-Z_]+%", out))
                f.write(out)
            count += 1
    print("wrote %d pages" % count)
    if "@" not in CONTACT_EMAIL:
        print("WARNING: CONTACT_EMAIL is still the placeholder %r. Set it in _src/build.py and rebuild before publishing." % CONTACT_EMAIL)


if __name__ == "__main__":
    main()
