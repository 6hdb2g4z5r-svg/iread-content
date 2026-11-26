"""Black Friday 26-30/11/2026 : stories et posts « 3 livres au choix = 299 DH ».
Exception validée par Amine le 26/11 : prix affiché pour cette opération seulement.
Règle d'Amine (26/11) : aucun livre en série (tome 1, 2, 3…) dans la promo.
Stories : en-tête compact (250-520 px), livres ou photo sur >= 65 % de la hauteur, aucun texte dans les 250 px du bas.
Médias publiés dans library/black-friday/ (rangés par le workflow f-lot)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from design import *  # noqa
from design import _pack_boxes, _place
from PIL import Image, ImageDraw, ImageFilter

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COV = os.path.join(REPO, "library", "couvertures")
BLACK = (14, 16, 22)

TXT = {
    "fr": dict(kicker="BLACK FRIDAY · JUSQU'AU 30/11", title="3 livres au choix = 299 DH",
               sub="Livraison offerte partout au Maroc · Paiement à la livraison",
               was="Ces 3 livres : {old} DH → 299 DH", last="DERNIER JOUR · BLACK FRIDAY"),
    "en": dict(kicker="BLACK FRIDAY · UNTIL 30/11", title="Any 3 books for 299 DH",
               sub="Free delivery all over Morocco · Cash on delivery",
               was="These 3 books: {old} DH → 299 DH", last="LAST DAY · BLACK FRIDAY"),
    "ar": dict(kicker="بلاك فرايدي · حتى 30 نونبر", title="3 كتب من اختيارك بـ 299 درهم",
               sub="توصيل مجاني لجميع مدن المغرب · الدفع عند الاستلام",
               was="هذه الكتب الثلاثة بـ 299 درهم بدل {old} درهم", last="آخر يوم · بلاك فرايدي"),
}


def _header(img, lang, last=False, was=None):
    t = TXT[lang]
    d = ImageDraw.Draw(img)
    pill(img, SW // 2, 290, t["last"] if last else t["kicker"], bg=GOLD, fg=BLACK, size=28)
    y = draw_block(d, SW // 2, 345, t["title"], "serif", 74, 650, WHITE, 980, max_lines=1)
    line = was or t["sub"]
    draw_block(d, SW // 2, y + 8, line, "sans", 34, 500, (220, 200, 160) if was else (205, 210, 222), 980, max_lines=1)
    if was:
        draw_block(d, SW // 2, y + 56, t["sub"], "sans", 30, 400, (205, 210, 222), 980, max_lines=1)


def story_photo_bf(photo, lang, out, last=False):
    """Photo KIE du lot en grand (1000 x 1250 = 65 % de l'écran), fond = même photo floutée et assombrie."""
    ph = load(photo)
    img = blurred_bg(ph, SW, SH, dark=0.62)
    card = cover_crop(ph, 1000, 1250)
    shadow_paste(img, card, (40, 560), radius=28, alpha=150)
    # voile en haut pour le texte
    veil = Image.new("RGBA", (SW, 560), (*BLACK, 150)); img.paste(veil, (0, 0), veil)
    _header(img, lang, last)
    return save(img, out)


def story_covers_bf(slugs, lang, out, old, last=False):
    """3 vraies couvertures du site, toutes entières, en grand (560 -> 1790 px). slugs[0] = livre mis en avant."""
    img = Image.new("RGB", (SW, SH), BLACK)
    # halo doré discret derrière les livres
    halo = Image.new("L", (SW, SH), 0)
    ImageDraw.Draw(halo).ellipse([90, 700, SW - 90, 1700], fill=90)
    halo = halo.filter(ImageFilter.GaussianBlur(160))
    img.paste(GOLD, (0, 0), halo)
    covs = [load(os.path.join(COV, f"{s}.jpg")) for s in slugs]
    # « vedette » (validée le 19/11) : livre 1 en grand, les 2 autres entiers dessous ; 560 -> 1790 px
    for c, (x, y, w, h, r) in zip(covs, _pack_boxes(3, "vedette", 560, 1790)):
        _place(img, c, (x, y, w, h), r, alpha=200)
    t = TXT[lang]
    _header(img, lang, last, was=t["was"].format(old=old))
    return save(img, out)


def post_bf(photo, out):
    return post_photo(photo, out)
