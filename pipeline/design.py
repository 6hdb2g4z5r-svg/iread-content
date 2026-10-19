"""iRead — bibliothèque de visuels Instagram (stories 1080x1920, posts 1080x1350).

Charte (relevée sur les visuels publiés en oct. 2026) :
  crème #F3EDE1 · beige #E3D6C3 · marine #1B253E · or #C9A96E · texte #1E2533
  Titres : Playfair Display · Texte : Inter · Arabe : Amiri

Règles métier (voir claude/strategie-contenu.md) :
  - uniquement des livres vendus sur iread.ma, couverture = édition du site (05-Contenu-Instagram/couvertures-site)
  - jamais de prix ; arguments autorisés : livraison gratuite Casablanca, paiement à la livraison, prix réduit en pack
  - pas de logo/pseudo d'autres comptes, pas de citation tapée (extraits = vraies photos de pages)
"""
from __future__ import annotations
import os, re
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps, features

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")

CREAM = (243, 237, 225)
BEIGE = (227, 214, 195)
NAVY = (27, 37, 62)
GOLD = (201, 169, 110)
INK = (30, 37, 51)
MUTED = (110, 112, 120)
WHITE = (255, 255, 255)

SW, SH = 1080, 1920   # story
PW, PH = 1080, 1350   # post 4:5

FOOT_FR = "Livraison gratuite à Casablanca · Paiement à la livraison"
FOOT_EN = "Free delivery in Casablanca · Cash on delivery"
FOOT_AR = "توصيل مجاني في الدار البيضاء · الدفع عند الاستلام"
PACK_FR = "Prix réduit en pack · Livraison partout au Maroc"
PACK_EN = "Discounted as a pack · Delivery all over Morocco"
PACK_AR = "ثمن مخفض في الباقة · توصيل لجميع مدن المغرب"

RAQM = features.check("raqm")
_AR = re.compile(r"[؀-ۿ]")


def is_ar(s: str) -> bool:
    return bool(_AR.search(s or ""))


def font(kind: str, size: int, weight: int = 400) -> ImageFont.FreeTypeFont:
    path = {
        "serif": "PlayfairDisplay[wght].ttf",
        "serif-i": "PlayfairDisplay-Italic[wght].ttf",
        "sans": "Inter[opsz,wght].ttf",
        "ar": "Amiri-Bold.ttf" if weight >= 600 else "Amiri-Regular.ttf",
    }[kind]
    f = ImageFont.truetype(os.path.join(FONTS, path), size,
                           layout_engine=ImageFont.Layout.RAQM if RAQM else ImageFont.Layout.BASIC)
    if kind != "ar":
        try:
            axes = f.get_variation_axes()
            vals = []
            for a in axes:
                n = a.get("name", b"")
                n = n.decode() if isinstance(n, bytes) else str(n)
                if "eight" in n or n.lower().startswith("wght"):
                    vals.append(max(a["minimum"], min(a["maximum"], weight)))
                elif "ptical" in n or n.lower().startswith("opsz"):
                    vals.append(max(a["minimum"], min(a["maximum"], size / 2)))
                else:
                    vals.append(a["default"])
            f.set_variation_by_axes(vals)
        except Exception:
            pass
    return f


def _prep(text: str):
    """Arabic: Raqm shapes natively; otherwise fall back to arabic_reshaper + bidi."""
    if is_ar(text):
        if RAQM:
            return text, {"direction": "rtl", "language": "ar"}
        try:
            import arabic_reshaper
            from bidi.algorithm import get_display
            return get_display(arabic_reshaper.reshape(text)), {}
        except ImportError:
            return text, {}
    return text, {}


def tfont(text, kind, size, weight=400):
    """Pick Amiri automatically for Arabic strings. NB: avoid ASCII '.' and ':' in Arabic strings."""
    return font("ar", int(size * 1.1), weight) if is_ar(text) else font(kind, size, weight)


def text_w(d, text, f):
    t, kw = _prep(text)
    b = d.textbbox((0, 0), t, font=f, **kw)
    return b[2] - b[0], b[3] - b[1]


def draw_center(d, cx, y, text, f, fill):
    t, kw = _prep(text)
    b = d.textbbox((0, 0), t, font=f, **kw)
    d.text((cx - (b[2] - b[0]) / 2 - b[0], y - b[1]), t, font=f, fill=fill, **kw)
    return y + (b[3] - b[1])


def wrap(d, text, f, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if text_w(d, t, f)[0] <= maxw or not cur:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_block(d, cx, y, text, kind, size, weight, fill, maxw, gap=1.25, max_lines=3):
    f = tfont(text, kind, size, weight)
    lines = wrap(d, text, f, maxw)
    while len(lines) > max_lines and size > 20:
        size -= 4; f = tfont(text, kind, size, weight); lines = wrap(d, text, f, maxw)
    for ln in lines:
        draw_center(d, cx, y, ln, f, fill)
        y += int(size * gap)
    return y


def pill(img, cx, cy, text, bg=NAVY, fg=WHITE, size=26, padx=30, pady=14):
    d = ImageDraw.Draw(img)
    f = tfont(text, "sans", size, 600)
    w, h = text_w(d, text, f)
    h = max(h, int(size * 0.8))
    x0, y0, x1, y1 = cx - w / 2 - padx, cy - h / 2 - pady, cx + w / 2 + padx, cy + h / 2 + pady
    d.rounded_rectangle([x0, y0, x1, y1], radius=(y1 - y0) / 2, fill=bg)
    t, kw = _prep(text)
    b = d.textbbox((0, 0), t, font=f, **kw)
    d.text((cx - (b[2] - b[0]) / 2 - b[0], cy - (b[3] - b[1]) / 2 - b[1]), t, font=f, fill=fg, **kw)
    return y1


def shadow_paste(base, im, xy, radius=0, blur=28, offset=(0, 18), alpha=110):
    x, y = xy
    w, h = im.size
    sh = Image.new("L", (w + blur * 4, h + blur * 4), 0)
    ImageDraw.Draw(sh).rounded_rectangle([blur * 2, blur * 2, blur * 2 + w, blur * 2 + h], radius=radius, fill=alpha)
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    base.paste((0, 0, 0), (x - blur * 2 + offset[0], y - blur * 2 + offset[1]), sh)
    if radius:
        m = Image.new("L", (w, h), 0)
        ImageDraw.Draw(m).rounded_rectangle([0, 0, w, h], radius=radius, fill=255)
        base.paste(im, (x, y), m)
    else:
        base.paste(im, (x, y))


def load(path):
    return ImageOps.exif_transpose(Image.open(path)).convert("RGB")


def fit(im, w, h):
    """Scale to fit inside w x h (no crop)."""
    im = im.copy(); im.thumbnail((w, h), Image.LANCZOS)
    if im.width < w and im.height < h:
        s = min(w / im.width, h / im.height); im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    return im


def cover_crop(im, w, h, cy=0.5):
    return ImageOps.fit(im, (w, h), Image.LANCZOS, centering=(0.5, cy))


def blurred_bg(photo, w, h, dark=0.35):
    bg = cover_crop(photo, w, h).filter(ImageFilter.GaussianBlur(40))
    return Image.blend(bg, Image.new("RGB", (w, h), (0, 0, 0)), dark)


def logo(img, cx, cy, r=34, dark_bg=False):
    d = ImageDraw.Draw(img)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=NAVY if not dark_bg else CREAM)
    f = font("serif-i", int(r * 0.62), 500)
    draw_center(d, cx, cy - r * 0.32, "iRead", f, CREAM if not dark_bg else NAVY)


def save(img, out, q=90):
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    img.convert("RGB").save(out, quality=q, optimize=True)
    return out


def foot_for(lang):
    return {"ar": FOOT_AR, "en": FOOT_EN}.get(lang, FOOT_FR)


def pack_line(lang):
    return {"ar": PACK_AR, "en": PACK_EN}.get(lang, PACK_FR)


# ───────────────────────────── STORIES 1080x1920 ─────────────────────────────

def story_photo(photo_path, title, out, kicker="Lecture du jour", cta="Disponible sur iread.ma", lang="fr"):
    """Vraie photo d'ambiance sur fond flouté + titre + CTA."""
    ph = load(photo_path)
    img = blurred_bg(ph, SW, SH)
    card = cover_crop(ph, 880, 1180)
    shadow_paste(img, card, (100, 300), radius=28)
    pill(img, SW // 2, 250, kicker, bg=CREAM, fg=INK)
    d = ImageDraw.Draw(img)
    y = draw_block(d, SW // 2, 1540, title, "serif", 64, 600, WHITE, 900, max_lines=2)
    y = pill(img, SW // 2, y + 70, cta)
    draw_center(d, SW // 2, y + 40, foot_for(lang), tfont(foot_for(lang), "sans", 24, 500), (235, 235, 235))
    return save(img, out)


def story_extract(cover_path, page_path, title, author, out, box=None, kicker="Extrait", cta="Commande en DM", lang="fr"):
    """Couverture du site + VRAIE photo de page recadrée (box=(l,t,r,b) en fraction 0-1)."""
    img = Image.new("RGB", (SW, SH), CREAM)
    d = ImageDraw.Draw(img)
    pill(img, SW // 2, 200, kicker)
    cov = fit(load(cover_path), 300, 430)
    shadow_paste(img, cov, ((SW - cov.width) // 2, 270), radius=6)
    y = 270 + cov.height + 40
    y = draw_block(d, SW // 2, y, title, "serif", 50, 600, INK, 900, max_lines=2)
    y = draw_block(d, SW // 2, y + 4, author, "sans", 28, 400, MUTED, 900, max_lines=1)
    page = load(page_path)
    if box:
        W, H = page.size; page = page.crop((int(box[0] * W), int(box[1] * H), int(box[2] * W), int(box[3] * H)))
    page = fit(page, 960, 1700 - y - 60 - 120)
    py = y + 50
    shadow_paste(img, page, ((SW - page.width) // 2, py), radius=14)
    by = pill(img, SW // 2, min(SH - 150, py + page.height + 80), cta)
    draw_center(d, SW // 2, by + 34, foot_for(lang), tfont(foot_for(lang), "sans", 23, 500), MUTED)
    return save(img, out)


def story_ab(cover_a, cover_b, question, sub, out, cta="Réponds en message"):
    img = Image.new("RGB", (SW, SH), CREAM)
    d = ImageDraw.Draw(img)
    y = draw_block(d, SW // 2, 330, question, "serif", 76, 600, INK, 940, max_lines=2)
    draw_block(d, SW // 2, y + 10, sub, "sans", 30, 400, MUTED, 940, max_lines=2)
    for i, c in enumerate((cover_a, cover_b)):
        cv = fit(load(c), 430, 640)
        x = (60 + 440 * i) + (440 - cv.width) // 2 + (10 if i else 0)
        shadow_paste(img, cv, (x, 640 + (640 - cv.height) // 2), radius=6)
        cx = 60 + 440 * i + 220 + (10 if i else 0)
        d.ellipse([cx - 44, 1330, cx + 44, 1418], fill=NAVY)
        draw_center(d, cx, 1352, "AB"[i], font("serif", 50, 700), WHITE)
    draw_center(d, SW // 2, 1500, cta, font("sans", 30, 600), INK)
    logo(img, SW // 2, 1680)
    return save(img, out)


def story_cover(cover_path, title, author, tagline, out, kicker="Coup de cœur", cta="Commande en DM", lang="fr"):
    img = Image.new("RGB", (SW, SH), BEIGE)
    d = ImageDraw.Draw(img)
    pill(img, SW // 2, 240, kicker)
    cv = fit(load(cover_path), 640, 900)
    shadow_paste(img, cv, ((SW - cv.width) // 2, 320), radius=6)
    y = 320 + cv.height + 60
    y = draw_block(d, SW // 2, y, title, "serif", 60, 600, INK, 920, max_lines=2)
    y = draw_block(d, SW // 2, y + 6, author, "sans", 30, 400, MUTED, 920, max_lines=1)
    if tagline:
        y = draw_block(d, SW // 2, y + 30, tagline, "serif-i", 34, 400, INK, 900, max_lines=2)
    by = pill(img, SW // 2, min(SH - 170, y + 90), cta)
    draw_center(d, SW // 2, by + 34, foot_for(lang), tfont(foot_for(lang), "sans", 23, 500), MUTED)
    return save(img, out)


def story_visual(src_path, out, kicker="Notre sélection", cta="Commande en DM"):
    """Visuel déjà vérifié (PUNCTUATIONS nettoyé, posts KIE) sur fond flouté."""
    src = load(src_path)
    img = blurred_bg(src, SW, SH, dark=0.15)
    card = fit(src, 940, 1460)
    shadow_paste(img, card, ((SW - card.width) // 2, 230 + (1460 - card.height) // 2), radius=22)
    pill(img, SW // 2, 180, kicker)
    pill(img, SW // 2, 1790, cta)
    return save(img, out)


def story_pack(cover_paths, title, sub, out, dark=True, kicker="Pack", lang="fr", cta="Commande en DM ou sur iread.ma"):
    bg, fg, sub_c = (NAVY, WHITE, (200, 205, 215)) if dark else (BEIGE, INK, MUTED)
    img = Image.new("RGB", (SW, SH), bg)
    d = ImageDraw.Draw(img)
    pill(img, SW // 2, 230, kicker, bg=GOLD, fg=NAVY)
    y = draw_block(d, SW // 2, 300, title, "serif", 74, 600, fg, 960, max_lines=2)
    draw_block(d, SW // 2, y + 6, sub, "sans", 30, 400, sub_c, 960, max_lines=2)
    covs = [load(c) for c in cover_paths[:4]]
    n = len(covs)
    # bigger covers: 3 in one big row, 4 in a 2x2 grid
    if n == 4:
        cw, ch = 370, 520; xs = [145, 565]; ys = [530, 1080]
        pos = [(xs[i % 2], ys[i // 2]) for i in range(4)]
    else:
        cw, ch = (300, 450) if n == 3 else (420, 620); gap = 30
        tot = n * cw + (n - 1) * gap; x0 = (SW - tot) // 2
        pos = [(x0 + i * (cw + gap), 780) for i in range(n)]
    for c, (x, yy) in zip(covs, pos):
        cv = fit(c, cw, ch)
        shadow_paste(img, cv, (x + (cw - cv.width) // 2, yy + (ch - cv.height) // 2), radius=6, alpha=150)
    line = pack_line(lang)
    draw_center(d, SW // 2, 1660, line, tfont(line, "sans", 26, 500), sub_c)
    pill(img, SW // 2, 1750, cta, bg=GOLD, fg=NAVY)
    return save(img, out)


# ───────────────────────────── POSTS 1080x1350 ─────────────────────────────

def post_photo(photo_path, out, cy=0.5):
    """Vraie photo plein cadre 4:5 (slide 1 des carrousels livre)."""
    return save(cover_crop(load(photo_path), PW, PH, cy), out)


def post_page(page_path, out, box=None):
    """Vraie page surlignée sur fond crème (slide 2)."""
    img = Image.new("RGB", (PW, PH), CREAM)
    page = load(page_path)
    if box:
        W, H = page.size; page = page.crop((int(box[0] * W), int(box[1] * H), int(box[2] * W), int(box[3] * H)))
    page = fit(page, 900, 1180)
    shadow_paste(img, page, ((PW - page.width) // 2, (PH - page.height) // 2), radius=12)
    return save(img, out)


def post_cover_card(cover_path, title, author, tagline, out, kicker="Coup de cœur"):
    img = Image.new("RGB", (PW, PH), CREAM)
    d = ImageDraw.Draw(img)
    pill(img, PW // 2, 90, kicker)
    cv = fit(load(cover_path), 520, 760)
    shadow_paste(img, cv, ((PW - cv.width) // 2, 150), radius=6)
    y = 150 + cv.height + 50
    y = draw_block(d, PW // 2, y, title, "serif", 52, 600, INK, 900, max_lines=2)
    y = draw_block(d, PW // 2, y + 4, author, "sans", 28, 400, MUTED, 900, max_lines=1)
    if tagline:
        draw_block(d, PW // 2, y + 20, tagline, "serif-i", 30, 400, INK, 880, max_lines=2)
    logo(img, PW - 90, PH - 80, r=30)
    return save(img, out)


def post_pack(cover_paths, title, sub, out, foot="Disponible en pack sur iread.ma", kicker="PACK"):
    img = Image.new("RGB", (PW, PH), CREAM)
    d = ImageDraw.Draw(img)
    pill(img, PW // 2, 90, kicker)
    y = draw_block(d, PW // 2, 150, title, "serif", 66, 600, INK, 960, max_lines=2)
    y = draw_block(d, PW // 2, y + 4, sub, "sans", 28, 400, MUTED, 960, max_lines=2)
    covs = [load(c) for c in cover_paths[:4]]
    n = len(covs)
    top = y + 40
    avail = PH - top - 170
    if n == 4:
        cw, ch = 330, (avail - 30) // 2; xs = [PW // 2 - cw - 15, PW // 2 + 15]
        pos = [(xs[i % 2], top + (i // 2) * (ch + 30)) for i in range(4)]
    else:
        cw, ch = (300, avail) if n == 3 else (420, avail); gap = 30
        tot = n * cw + (n - 1) * gap; x0 = (PW - tot) // 2
        pos = [(x0 + i * (cw + gap), top) for i in range(n)]
    for c, (x, yy) in zip(covs, pos):
        cv = fit(c, cw, ch)
        shadow_paste(img, cv, (x + (cw - cv.width) // 2, yy + (ch - cv.height) // 2), radius=6)
    draw_center(d, PW // 2, PH - 120, foot, tfont(foot, "sans", 28, 600), INK)
    logo(img, PW - 90, PH - 80, r=30)
    return save(img, out)


def contact_sheet(paths, out, cols=5, w=270):
    ims = [Image.open(p).convert("RGB") for p in paths]
    hs = [int(w * im.height / im.width) for im in ims]
    h = max(hs) if hs else w
    rows = (len(ims) + cols - 1) // cols
    S = Image.new("RGB", (cols * w, rows * h), WHITE)
    for i, im in enumerate(ims):
        S.paste(im.resize((w, int(w * im.height / im.width))), ((i % cols) * w, (i // cols) * h))
    return save(S, out, q=80)
