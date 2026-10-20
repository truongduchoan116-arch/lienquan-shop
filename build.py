#!/usr/bin/env python3
"""Sinh website shop từ config.py + templates/ + static/ vào dist/.

    python build.py            # build ra dist/
    python build.py --serve    # build rồi xem thử tại http://localhost:8000
"""

from __future__ import annotations

import argparse
import datetime as dt
import functools
import html
import http.server
import re
import shutil
import socketserver
import sys
from pathlib import Path
from urllib.parse import urlparse

from jinja2 import Environment, FileSystemLoader, select_autoescape
from markupsafe import Markup

import config

ROOT = Path(__file__).resolve().parent
DIST, STATIC, TEMPLATES = ROOT / "dist", ROOT / "static", ROOT / "templates"
warnings: list[str] = []

ICONS = {
    "facebook": '<path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>',
    "youtube": '<path d="M2.5 17a24.12 24.12 0 0 1 0-10 2 2 0 0 1 1.4-1.4 49.56 49.56 0 0 1 16.2 0A2 2 0 0 1 21.5 7a24.12 24.12 0 0 1 0 10 2 2 0 0 1-1.4 1.4 49.55 49.55 0 0 1-16.2 0A2 2 0 0 1 2.5 17"/><path d="m10 15 5-3-5-3z"/>',
    "tiktok": '<path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/>',
    "messenger": '<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/>',
    "mail": '<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
    "link": '<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>',
    "list": '<line x1="8" x2="21" y1="6" y2="6"/><line x1="8" x2="21" y1="12" y2="12"/><line x1="8" x2="21" y1="18" y2="18"/><line x1="3" x2="3.01" y1="6" y2="6"/><line x1="3" x2="3.01" y1="12" y2="12"/><line x1="3" x2="3.01" y1="18" y2="18"/>',
    "tag": '<path d="M12.586 2.586A2 2 0 0 0 11.172 2H4a2 2 0 0 0-2 2v7.172a2 2 0 0 0 .586 1.414l8.704 8.704a2.426 2.426 0 0 0 3.42 0l6.58-6.58a2.426 2.426 0 0 0 0-3.42z"/><circle cx="7.5" cy="7.5" r=".5" fill="currentColor"/>',
    "book": '<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>',
    "shield": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
    "search": '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
    "headset": '<path d="M3 14h3a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-7a9 9 0 0 1 18 0v7a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3"/>',
    "help": '<circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><path d="M12 17h.01"/>',
    "copy": '<rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/>',
    "share": '<circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" x2="15.42" y1="13.51" y2="17.49"/><line x1="15.41" x2="8.59" y1="6.51" y2="10.49"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/>',
    "moon": '<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>',
    "arrow-up": '<path d="m5 12 7-7 7 7"/><path d="M12 19V5"/>',
    "chevron": '<path d="m6 9 6 6 6-6"/>',
    "external": '<path d="M15 3h6v6"/><path d="M10 14 21 3"/><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>',
}


def icon(name: str, cls: str = "icon") -> Markup:
    body = ICONS.get(name, ICONS["link"])
    return Markup(
        f'<svg class="{html.escape(cls)}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
        f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{body}</svg>'
    )


def safe_url(url: str, label: str) -> str:
    url = (url or "").strip()
    if not url:
        return ""
    p = urlparse(url)
    if p.scheme in ("http", "https") and p.netloc:
        return url
    warnings.append(f"URL không hợp lệ, đã ẩn ({label}): {url!r}")
    return ""


def safe_email(v: str) -> str:
    v = (v or "").strip()
    if not v:
        return ""
    if re.fullmatch(r"[^@\s<>\"',;]+@[^@\s<>\"',;]+\.[^@\s<>\"',;]+", v):
        return v
    warnings.append(f"Email không hợp lệ, đã ẩn: {v!r}")
    return ""


def safe_asset(path: str, label: str) -> str:
    path = (path or "").strip().lstrip("/")
    if not path:
        return ""
    if ".." in Path(path).parts or not (STATIC / path).is_file():
        warnings.append(f"Không tìm thấy file '{path}' trong static/ ({label}); đã bỏ qua.")
        return ""
    return path


def safe_color(c: str, fallback: str, label: str) -> str:
    if re.fullmatch(r"#[0-9a-fA-F]{6}", c or ""):
        return c
    warnings.append(f"Màu không hợp lệ ({label}): {c!r}, dùng mặc định {fallback}")
    return fallback


def initials(name: str) -> str:
    parts = [p for p in re.split(r"\s+", name.strip()) if p]
    if not parts:
        return "?"
    return parts[0][:2].upper() if len(parts) == 1 else (parts[0][0] + parts[-1][0]).upper()


def site_url() -> str:
    import os

    raw = os.environ.get("SITE_URL") or config.SITE.get("url") or ""
    return safe_url(raw, "SITE.url").rstrip("/")


def make_qr_svg(url: str) -> str:
    try:
        import segno
    except ImportError:
        warnings.append("Chưa cài segno nên không tạo được mã QR (pip install segno).")
        return ""
    import io

    buf = io.BytesIO()
    segno.make(url, error="m").save(buf, kind="svg", scale=6, border=2, dark="#000000", light="#ffffff", xmldecl=False,
                                    svgns=True, nl=False, title="QR", desc=None)
    svg = buf.getvalue().decode("utf-8")
    return svg.replace("<svg ", '<svg class="qr-svg" role="img" aria-label="QR code" ', 1)


def make_og_image(out: Path, name: str, tagline: str, colors: dict) -> bool:
    try:
        from PIL import Image, ImageDraw, ImageFilter, ImageFont
    except ImportError:
        warnings.append("Chưa cài Pillow nên không tạo được ảnh chia sẻ (pip install pillow).")
        return False
    w, h = 1200, 630
    base = Image.new("RGB", (w, h), "#0a0612")
    glow = Image.new("RGB", (w, h), "#0a0612")
    gd = ImageDraw.Draw(glow)
    gd.ellipse((-250, -250, 650, 450), fill=colors["primary"])
    gd.ellipse((650, 250, 1450, 900), fill=colors["secondary"])
    glow = glow.filter(ImageFilter.GaussianBlur(170))
    img = Image.blend(base, glow, 0.55)
    d = ImageDraw.Draw(img)

    def font(size, bold=False):
        for c in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                  "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
                  "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf"):
            if Path(c).exists():
                return ImageFont.truetype(c, size)
        return ImageFont.load_default()

    d.rounded_rectangle((90, 90, 190, 190), radius=26, fill=colors["primary"])
    ini = initials(name)
    f = font(44, True)
    bb = d.textbbox((0, 0), ini, font=f)
    d.text((140 - (bb[2] - bb[0]) / 2, 140 - (bb[3] - bb[1]) / 2 - bb[1]), ini, font=f, fill="white")
    size = 78 if len(name) <= 18 else 56
    d.text((90, 270), name, font=font(size, True), fill="#ffffff")
    d.text((90, 385), tagline, font=font(36), fill=colors["gold"])
    d.rectangle((90, 470, 250, 476), fill=colors["electric"])
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "PNG", optimize=True)
    return True


def build_context(base_url: str) -> dict:
    s = config.SHOP
    colors = {
        "primary": safe_color(s["colors"].get("primary"), "#d6203f", "primary"),
        "secondary": safe_color(s["colors"].get("secondary"), "#7c3aed", "secondary"),
        "electric": safe_color(s["colors"].get("electric"), "#38bdf8", "electric"),
        "gold": safe_color(s["colors"].get("gold"), "#f5c542", "gold"),
    }

    def contact_item(key: str, platform: str, ic: str, desc: str) -> dict | None:
        item = config.CONTACT.get(key, {})
        if not item.get("enabled", True):
            return None
        if key == "email":
            v = safe_email(item.get("url", ""))
            href = f"mailto:{v}" if v else ""
        else:
            href = safe_url(item.get("url", ""), key)
        return {"key": key, "platform": platform, "icon": ic, "description": desc, "href": href} if href else None

    contact_all = [
        contact_item("messenger_url", "Messenger", "messenger", "Nhắn tin trực tiếp với shop"),
        contact_item("facebook_url", "Facebook", "facebook", "Trang Facebook của shop"),
        contact_item("youtube_url", "YouTube", "youtube", "Video và nội dung của shop"),
        contact_item("tiktok_url", "TikTok", "tiktok", "Video ngắn của shop"),
        contact_item("email", "Email", "mail", "Gửi email cho shop"),
    ]
    contact_all = [c for c in contact_all if c]
    for c in contact_all:
        c["external"] = not c["href"].startswith("mailto:")
    socials = contact_all
    primary_contact = next((c for c in contact_all if c["key"] in ("messenger_url", "facebook_url", "email")), None)

    featured = []
    furl: dict[str, str] = {}
    for f in config.FEATURED_LINKS:
        url = safe_url(f.get("url", ""), f"FEATURED_LINKS[{f.get('id')}]") if f.get("enabled", True) else ""
        furl[f["id"]] = url
        if url:
            featured.append({**f, "url": url})

    services = []
    for sv in config.SERVICES:
        t = sv.get("target", "contact")
        action = None
        if t == "contact":
            action = {"href": "#contact", "external": False}
        elif t == "faq":
            action = {"href": "#faq", "external": False}
        else:
            url = furl.get(t, "")
            if url:
                action = {"href": url, "external": True}
            elif primary_contact:  # chưa có URL riêng -> mở kênh liên hệ chính
                action = {"href": primary_contact["href"], "external": primary_contact["external"]}
        services.append({**sv, "action_info": action})

    footer_policy = safe_url(config.FOOTER.get("policy_url", ""), "FOOTER.policy_url")
    logo = safe_asset(s.get("logo", ""), "SHOP.logo")
    bg = safe_asset(s.get("background_image", ""), "SHOP.background_image")

    qr_svg = ""
    if base_url:
        qr_svg = make_qr_svg(base_url + "/")
    return {
        "lang": config.SITE.get("lang", "vi"),
        "theme": config.SITE.get("default_theme", "dark") if config.SITE.get("default_theme") in ("dark", "light") else "dark",
        "base_url": base_url,
        "canonical": f"{base_url}/" if base_url else "",
        "og_image": f"{base_url}/assets/og-image.png" if base_url and (DIST / "assets" / "og-image.png").exists() else "",
        "shop": {**s, "colors": colors, "logo": logo, "bg": bg, "initials": initials(s["name"])},
        "contact_all": contact_all,
        "socials": socials,
        "primary_contact": primary_contact,
        "featured": featured,
        "services": services,
        "faq": config.FAQ,
        "footer": {**config.FOOTER, "policy_url": footer_policy},
        "qr_svg": Markup(qr_svg),
        "year": dt.date.today().year,
        "updated": dt.date.today().isoformat(),
    }


def build() -> int:
    base_url = site_url()
    if not base_url:
        warnings.append("Chưa có SITE.url / SITE_URL: không tạo mã QR, canonical, sitemap và ảnh chia sẻ tuyệt đối.")
    if DIST.exists():
        shutil.rmtree(DIST)
    shutil.copytree(STATIC, DIST)

    s = config.SHOP
    colors = {k: safe_color(v, "#888888", k) for k, v in s["colors"].items()}
    make_og_image(DIST / "assets" / "og-image.png", s["name"], s["tagline"], colors)

    env = Environment(loader=FileSystemLoader(str(TEMPLATES)), autoescape=select_autoescape(["html", "j2"]),
                      trim_blocks=True, lstrip_blocks=True)
    env.globals["icon"] = icon
    ctx = build_context(base_url)
    (DIST / "index.html").write_text(env.get_template("index.html.j2").render(**ctx), encoding="utf-8")

    prefix = urlparse(base_url).path.rstrip("/") if base_url else ""
    ctx["root"] = prefix + "/"
    (DIST / "404.html").write_text(env.get_template("404.html.j2").render(**ctx), encoding="utf-8")

    robots = "User-agent: *\nAllow: /\n"
    if base_url:
        robots += f"Sitemap: {base_url}/sitemap.xml\n"
        (DIST / "sitemap.xml").write_text(
            '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            f"  <url><loc>{html.escape(base_url)}/</loc><lastmod>{dt.date.today().isoformat()}</lastmod></url>\n</urlset>\n",
            encoding="utf-8")
    (DIST / "robots.txt").write_text(robots, encoding="utf-8")
    import json

    (DIST / "manifest.webmanifest").write_text(json.dumps({
        "name": s["name"], "short_name": s["name"][:12], "start_url": "./", "display": "standalone",
        "background_color": "#0a0612", "theme_color": colors["primary"],
        "icons": [{"src": "favicon.svg", "sizes": "any", "type": "image/svg+xml"}]}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8")
    (DIST / ".nojekyll").write_text("")
    return 0


def serve(port: int) -> None:
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(DIST))
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Xem thử tại http://localhost:{port}  (Ctrl+C để dừng)")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nĐã dừng.")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--serve", action="store_true")
    ap.add_argument("--port", type=int, default=8000)
    args = ap.parse_args()
    code = build()
    if code:
        return code
    print(f"Đã build xong -> {DIST}")
    if warnings:
        print("\nCẢNH BÁO:")
        for w in dict.fromkeys(warnings):
            print(f"  - {w}")
    if args.serve:
        serve(args.port)
    return 0


if __name__ == "__main__":
    sys.exit(main())
