# -*- coding: utf-8 -*-
"""Nexora post renderer: the fixed Nexora header/footer + body helpers -> PNG (1080x1350) and MP4 (1080x1920).

Rana's standing rule (20 Nov 2026): EVERY Nexora post has
  - header: full-width gold band, Nexora hex logo as tall as the band, "NEXORA / DIGITAL SERVICES" big;
  - footer: gold band with  [globe] Website https://nexoradsa.org | [mail] Email info@nexoradsa.org |
            [phone] WhatsApp 0345 0383301   (labels in English, website always with https://).
Never change the header/footer per post; vary only the body.

Usage (python3, Playwright + /usr/bin/google-chrome, ffmpeg):
    import nexora_post as N
    html = N.page("ویب سائٹ", N.title("...") + N.bullets([...]), n=1, total=3)
    N.render({"1": html}, "/abs/out/dir")                 -> /abs/out/dir/1.png
    N.video(["/abs/out/dir/1.png", ...], "/abs/out/short.mp4", seconds=4, audio=None)
Fonts: Noto Nastaliq Urdu + Inter from @fontsource (installed into FONT_DIR by ensure_fonts()).
"""
import asyncio
import os
import subprocess

FONT_DIR = os.environ.get("NEXORA_FONT_DIR", "/home/claude/nexora-render/node_modules/@fontsource")
GOLD, NAVY = "#D4AF37", "#0B1E39"
URDU = "'Noto Nastaliq Urdu','Noto Naskh Arabic','Inter',sans-serif"
INTER = "'Inter','Helvetica Neue',Arial,sans-serif"
G = f"color:{GOLD}"
HDR_H = 150


def ensure_fonts() -> str:
    if not os.path.isdir(os.path.join(FONT_DIR, "noto-nastaliq-urdu")):
        root = os.path.dirname(os.path.dirname(FONT_DIR))
        os.makedirs(root, exist_ok=True)
        subprocess.run(["npm", "i", "--prefix", root, "@fontsource/noto-nastaliq-urdu", "@fontsource/inter"], check=True)
    css = ""
    for w in (400, 600, 700):
        css += f"@font-face{{font-family:'Noto Nastaliq Urdu';font-weight:{w};src:url('file://{FONT_DIR}/noto-nastaliq-urdu/files/noto-nastaliq-urdu-arabic-{w}-normal.woff2') format('woff2');}}\n"
    for w in (400, 500, 600, 700, 800):
        p = f"{FONT_DIR}/inter/files/inter-latin-{w}-normal.woff2"
        if os.path.exists(p):
            css += f"@font-face{{font-family:'Inter';font-weight:{w};src:url('file://{p}') format('woff2');}}\n"
    return css


LOGO_HDR = (f'<svg width="136" height="136" viewBox="0 0 100 100" style="flex:none"><polygon points="50,6 91,27 91,73 50,94 9,73 9,27" '
            f'fill="{NAVY}" stroke="{NAVY}" stroke-width="4"/><path d="M35,71 L35,29 M35,29 L65,71 M65,71 L65,29" fill="none" '
            f'stroke="{GOLD}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/></svg>')
GLOBE = (f'<svg width="38" height="38" viewBox="0 0 24 24" fill="none" stroke="{GOLD}" stroke-width="1.8" stroke-linecap="round">'
         f'<circle cx="12" cy="12" r="9.5"/><ellipse cx="12" cy="12" rx="4.2" ry="9.5"/><path d="M2.5 12h19M4 7h16M4 17h16"/></svg>')
MAIL = (f'<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="{GOLD}" stroke-width="1.9" stroke-linejoin="round">'
        f'<rect x="2.5" y="5" width="19" height="14" rx="2"/><path d="M3 6.5l9 6.5 9-6.5"/></svg>')
PHONE = (f'<svg width="36" height="36" viewBox="0 0 24 24" fill="{GOLD}"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 '
         f'11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 '
         f'3.57a1 1 0 0 1-.25 1z"/></svg>')
CHECK = (f'<svg width="40" height="40" viewBox="0 0 48 48" style="flex:none"><circle cx="24" cy="24" r="22" fill="none" stroke="{GOLD}" '
         f'stroke-width="3"/><path d="M14 25 l7 7 l13-15" fill="none" stroke="{GOLD}" stroke-width="4" stroke-linecap="round" '
         f'stroke-linejoin="round"/></svg>')


def _foot_item(icon, label, value, size):
    return (f'<div style="display:flex;align-items:center;gap:12px">'
            f'<div style="width:60px;height:60px;border-radius:50%;background:{NAVY};display:flex;align-items:center;justify-content:center;flex:none">{icon}</div>'
            f'<div style="display:flex;flex-direction:column;line-height:1.1">'
            f'<span style="font-size:22px;font-weight:700;letter-spacing:.02em;opacity:.85">{label}</span>'
            f'<span style="font-size:{size}px;font-weight:800;margin-top:2px">{value}</span></div></div>')


HEADER = lambda chip, n, total: (  # noqa: E731
    f'<div dir="ltr" style="position:absolute;left:0;right:0;top:0;height:{HDR_H}px;background:{GOLD};color:{NAVY};display:flex;'
    f'align-items:center;justify-content:space-between;padding:0 44px 0 30px;font-family:{INTER};z-index:2">'
    f'<div style="display:flex;align-items:center;gap:20px">{LOGO_HDR}<div style="display:flex;flex-direction:column;line-height:1">'
    f'<span style="font-size:68px;font-weight:800;letter-spacing:.01em">NEXORA</span>'
    f'<span style="font-size:25px;font-weight:700;letter-spacing:.24em;margin-top:6px">DIGITAL SERVICES</span></div></div>'
    f'<div style="display:flex;align-items:center;gap:16px">'
    + (f'<div style="font-size:26px;font-weight:700;opacity:.75">{n} / {total}</div>' if total and total > 1 else "")
    + (f'<div dir="rtl" style="background:{NAVY};color:{GOLD};border-radius:999px;padding:2px 28px;font-family:{URDU};font-size:28px;'
       f'line-height:2.1;font-weight:700">{chip}</div>' if chip else "")
    + '</div></div>')

FOOTER = (f'<div dir="ltr" style="position:absolute;left:0;right:0;bottom:0;height:150px;background:{GOLD};color:{NAVY};display:flex;'
          f'align-items:center;justify-content:space-between;padding:0 30px;font-family:{INTER}">'
          + _foot_item(GLOBE, "Website", "https://nexoradsa.org", 25)
          + _foot_item(MAIL, "Email", "info@nexoradsa.org", 25)
          + _foot_item(PHONE, "WhatsApp", "0345 0383301", 29) + '</div>')


def page(chip, body, n=1, total=1, swipe=None, bg=NAVY, width=1080, height=1350):
    """One post image. body = HTML placed between header and footer (RTL Urdu by default).
    swipe: None => shown when n < total. Content area is roughly y=164..1190 at 1080x1350."""
    ff = ensure_fonts()
    if swipe is None:
        swipe = bool(total and n < total)
    swipe_html = (f'<div style="position:absolute;left:64px;bottom:178px;display:flex;align-items:center;gap:12px;color:{GOLD};'
                  f'font-size:30px;line-height:2"><span>اگلی سلائیڈ</span><span dir="ltr" style="font-family:{INTER};font-size:34px;'
                  f'font-weight:700">&larr;</span></div>') if swipe else ""
    return (f'<!doctype html><html lang="ur" dir="rtl"><head><meta charset="utf-8"><style>{ff}html,body{{margin:0;background:{bg}}}'
            f'*{{box-sizing:border-box}}</style></head><body>'
            f'<div style="position:relative;overflow:hidden;width:{width}px;height:{height}px;background:{bg};font-family:{URDU};direction:rtl;color:#fff">'
            f'<svg width="980" height="980" viewBox="0 0 100 100" style="position:absolute;left:-360px;top:420px;opacity:.08">'
            f'<polygon points="50,10 88,29 88,71 50,90 12,71 12,29" fill="none" stroke="{GOLD}" stroke-width="1.2"/></svg>'
            + HEADER(chip, n, total)
            + f'<div style="position:relative;height:{height - 150}px;padding:{HDR_H + 14}px 64px 0;display:flex;flex-direction:column">{body}</div>'
            + swipe_html + FOOTER + '</div></body></html>')


# ---------------- body helpers (all optional; write your own HTML when a style needs it) ----------------

def title(html, size=64, mt=18):
    return (f'<div style="margin-top:{mt}px;display:flex;flex-direction:column;gap:4px">'
            f'<h1 style="margin:0;font-size:{size}px;line-height:1.9;font-weight:700">{html}</h1>'
            f'<div style="width:120px;height:6px;background:{GOLD};border-radius:3px"></div></div>')


def gold(text, size=None):
    return f'<span style="{G}' + (f';font-size:{size}px' if size else '') + f'">{text}</span>'


def para(text, size=32, color="#dbe3f0", mt=8):
    return f'<div style="margin-top:{mt}px;font-size:{size}px;line-height:1.95;color:{color}">{text}</div>'


def bullets(items, size=34):
    rows = "".join(f'<div style="display:flex;align-items:center;gap:20px">{CHECK}<div style="font-size:{size}px;line-height:1.95">{t}</div></div>'
                   for t in items)
    return f'<div style="margin-top:10px;display:flex;flex-direction:column;gap:2px">{rows}</div>'


def cards(items, cols=2, size=29, light=True):
    """items: [(heading, text)]. light=True => white cards with navy text (readable lists)."""
    bg, fg, sub = ("#FFFFFF", NAVY, "#3b4a63") if light else ("rgba(255,255,255,.05)", GOLD, "#dbe3f0")
    cells = "".join(f'<div style="border:3px solid {GOLD};background:{bg};border-radius:18px;padding:0 20px 4px">'
                    f'<div style="font-size:{size}px;line-height:1.7;font-weight:700;color:{fg}">{h}</div>'
                    + (f'<div style="font-size:{size - 5}px;line-height:1.7;color:{sub}">{t}</div>' if t else "") + '</div>'
                    for h, t in items)
    return f'<div style="margin-top:12px;display:grid;grid-template-columns:repeat({cols},1fr);gap:10px 16px">{cells}</div>'


def pill(text, filled=True, size=38):
    st = f"background:{GOLD};color:{NAVY}" if filled else f"border:3px solid {GOLD};color:{GOLD}"
    return f'<div style="align-self:center;margin-top:24px;{st};border-radius:999px;padding:4px 44px;font-size:{size}px;line-height:2;font-weight:700">{text}</div>'


def ltr(text, size=40, color=GOLD, weight=800):
    return f'<span dir="ltr" style="font-family:{INTER};font-size:{size}px;font-weight:{weight};color:{color}">{text}</span>'


def shot(src, h=None, pad=10, mt=24):
    """A screenshot/photo card. src = file:// or https URL."""
    inner = (f'<img src="{src}" style="width:100%;height:auto;border-radius:12px;display:block">' if h is None else
             f'<img src="{src}" style="max-width:100%;max-height:100%;object-fit:contain;border-radius:12px;display:block">')
    hs = f"height:{h}px;display:flex;align-items:center;justify-content:center;" if h else ""
    return (f'<div style="margin-top:{mt}px;{hs}border-radius:24px;background:#fff;padding:{pad}px;border:3px solid rgba(212,175,55,.85);'
            f'box-shadow:0 24px 60px rgba(0,0,0,.45);overflow:hidden">{inner}</div>')


# ---------------- output ----------------

async def _render(pages: dict, out_dir: str, width: int, height: int) -> list:
    from playwright.async_api import async_playwright
    os.makedirs(out_dir, exist_ok=True)
    out = []
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox", "--allow-file-access-from-files"])
        pg = await b.new_page(viewport={"width": width, "height": height}, device_scale_factor=1)
        for name, html in pages.items():
            path = os.path.abspath(os.path.join(out_dir, f"{name}.html"))
            open(path, "w", encoding="utf-8").write(html)
            await pg.goto("file://" + path)
            await pg.wait_for_load_state("networkidle")
            await pg.evaluate("document.fonts.ready")
            await asyncio.sleep(0.4)
            png = path[:-5] + ".png"
            await pg.screenshot(path=png, clip={"x": 0, "y": 0, "width": width, "height": height})
            os.remove(path)
            out.append(png)
        await b.close()
    return out


def render(pages: dict, out_dir: str, width=1080, height=1350) -> list:
    """pages: {"1": html, "2": html}. Returns PNG paths (absolute out_dir required)."""
    return asyncio.run(_render(pages, os.path.abspath(out_dir), width, height))


def video(images: list, out_mp4: str, seconds: float = 4.0, audio: str | None = None) -> str:
    """1080x1920 MP4 (H.264 + AAC) for TikTok / YouTube Shorts / Facebook Reel: each 1080x1350 image centred on navy,
    no zoom (zoom cropped the footer phone number), cross-fade. audio = optional mp3/wav voice-over (video length follows the images). Under 16 MB."""
    n = len(images)
    inputs, filters = [], []
    for i, img in enumerate(images):
        inputs += ["-loop", "1", "-t", str(seconds + 0.6), "-i", img]
        filters.append(f"[{i}:v]scale=1080:1350,fps=30,"
                       f"pad=1080:1920:0:285:color=0x0B1E39,setsar=1,format=yuv420p[v{i}]")
    chain, last = "", "[v0]"
    for i in range(1, n):
        chain += f";{last}[v{i}]xfade=transition=fade:duration=0.6:offset={i * seconds:.2f}[x{i}]"
        last = f"[x{i}]"
    total = seconds * n + 0.6
    cmd = ["ffmpeg", "-y", *inputs]
    if audio:
        cmd += ["-i", audio]
        amap = [f"{n}:a"]
    else:
        cmd += ["-f", "lavfi", "-t", str(total), "-i", "anullsrc=channel_layout=stereo:sample_rate=44100"]
        amap = [f"{n}:a"]
    cmd += ["-filter_complex", ";".join(filters) + chain, "-map", last, "-map", amap[0], "-t", f"{total:.2f}",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "26", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "96k",
            "-movflags", "+faststart", out_mp4]
    subprocess.run(cmd, check=True, capture_output=True)
    return out_mp4
