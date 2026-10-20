"""iRead — stories « À la une » (highlights) : 1 slide-couverture (icône centrée) + slides d'infos par thème.
Usage : python3 -B highlights.py  →  ../highlights/<theme>-<n>.jpg
Règles : pas de prix, jamais WhatsApp, jamais « authentiques », chiffres occidentaux.
"""
import os, math
from PIL import Image, ImageDraw
from design import (SW, SH, CREAM, BEIGE, NAVY, GOLD, INK, MUTED, WHITE, font, tfont, draw_center,
                    draw_block, pill, logo, save, wrap, text_w)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "highlights")
CX, CY, R = SW // 2, SH // 2, 300   # centre exact = zone recadrée par Instagram pour la couverture
LW = 16                              # épaisseur de trait des icônes


# ───────────── icônes (trait or sur rond marine) ─────────────
def ic_bag(d):
    d.rounded_rectangle([CX - 120, CY - 60, CX + 120, CY + 150], 22, outline=GOLD, width=LW)
    d.arc([CX - 70, CY - 160, CX + 70, CY + 10], 180, 360, fill=GOLD, width=LW)
    d.line([CX - 70, CY - 75, CX - 70, CY - 40], fill=GOLD, width=LW)
    d.line([CX + 70, CY - 75, CX + 70, CY - 40], fill=GOLD, width=LW)


def ic_truck(d):
    d.rounded_rectangle([CX - 190, CY - 110, CX + 40, CY + 70], 14, outline=GOLD, width=LW)
    d.polygon([(CX + 40, CY - 50), (CX + 130, CY - 50), (CX + 190, CY + 10), (CX + 190, CY + 70), (CX + 40, CY + 70)], outline=GOLD, width=LW)
    for x in (CX - 120, CX + 120):
        d.ellipse([x - 45, CY + 50, x + 45, CY + 140], fill=NAVY, outline=GOLD, width=LW)
    for i, y in enumerate((CY - 60, CY - 20, CY + 20)):
        d.line([CX - 280 + i * 20, y, CX - 215, y], fill=GOLD, width=10)


def ic_cash(d):
    d.rounded_rectangle([CX - 190, CY - 110, CX + 190, CY + 110], 22, outline=GOLD, width=LW)
    d.ellipse([CX - 60, CY - 60, CX + 60, CY + 60], outline=GOLD, width=LW)
    for x in (CX - 130, CX + 130):
        d.ellipse([x - 12, CY - 12, x + 12, CY + 12], fill=GOLD)


def ic_books(d):
    for i, (w, h) in enumerate(((300, 70), (260, 70), (320, 70))):
        y = CY + 110 - i * 85
        x0 = CX - w // 2 + (i - 1) * 18
        d.rounded_rectangle([x0, y - h, x0 + w, y], 12, outline=GOLD, width=LW)
        d.line([x0 + 30, y - h, x0 + 30, y], fill=GOLD, width=10)


def ic_tablet(d):
    d.rounded_rectangle([CX - 120, CY - 175, CX + 120, CY + 175], 30, outline=GOLD, width=LW)
    for i in range(4):
        y = CY - 100 + i * 50
        d.line([CX - 70, y, CX + (70 if i < 3 else 10), y], fill=GOLD, width=10)
    d.ellipse([CX - 12, CY + 125, CX + 12, CY + 149], fill=GOLD)


def ic_question(d):
    f = font("serif", 300, 700)
    draw_center(d, CX, CY - 150, "?", f, GOLD)


def ic_globe(d):
    d.ellipse([CX - 170, CY - 170, CX + 170, CY + 170], outline=GOLD, width=LW)
    d.ellipse([CX - 75, CY - 170, CX + 75, CY + 170], outline=GOLD, width=10)
    d.line([CX - 170, CY, CX + 170, CY], fill=GOLD, width=10)
    d.line([CX, CY - 170, CX, CY + 170], fill=GOLD, width=10)


ICONS = {"bag": ic_bag, "truck": ic_truck, "cash": ic_cash, "books": ic_books, "tablet": ic_tablet,
         "question": ic_question, "globe": ic_globe}


def cover(icon, title, sub, out):
    img = Image.new("RGB", (SW, SH), NAVY)
    d = ImageDraw.Draw(img)
    d.ellipse([CX - R - 40, CY - R - 40, CX + R + 40, CY + R + 40], outline=GOLD, width=4)
    d.ellipse([CX - R, CY - R, CX + R, CY + R], fill=(34, 46, 76))
    ICONS[icon](d)
    draw_center(d, CX, 330, "iRead", font("serif-i", 64, 500), CREAM)
    y = draw_block(d, CX, CY + R + 110, title, "serif", 88, 600, WHITE, 960, max_lines=1)
    draw_block(d, CX, y + 10, sub, "sans", 32, 400, (200, 205, 215), 900, max_lines=2)
    pill(img, CX, SH - 200, "iread.ma", bg=GOLD, fg=NAVY, size=30)
    return save(img, out)


def info(kicker, title, items, out, cta="Commande sur iread.ma ou en DM", note=None, dark=False):
    """items = [(numéro/puce, titre, détail)]"""
    bg, fg, sub, card = (NAVY, WHITE, (200, 205, 215), (34, 46, 76)) if dark else (CREAM, INK, MUTED, WHITE)
    img = Image.new("RGB", (SW, SH), bg)
    d = ImageDraw.Draw(img)
    pill(img, CX, 230, kicker, bg=GOLD, fg=NAVY)
    y = draw_block(d, CX, 310, title, "serif", 72, 600, fg, 940, max_lines=2)
    y += 50
    n = len(items)
    gap = 30
    avail = 1500 - y - (130 if note else 0)
    h = min(270, (avail - gap * (n - 1)) // n)
    y += max(0, (avail - (n * h + (n - 1) * gap)) // 3)
    for i, (num, head, det) in enumerate(items):
        y0 = y + i * (h + gap)
        d.rounded_rectangle([70, y0, SW - 70, y0 + h], 28, fill=card)
        d.ellipse([110, y0 + h // 2 - 46, 202, y0 + h // 2 + 46], fill=GOLD)
        draw_center(d, 156, y0 + h // 2 - 26, num, font("serif", 52, 700), NAVY)
        fh = tfont(head, "sans", 42, 700)
        fd = tfont(det, "sans", 33, 400)
        lines = wrap(d, det, fd, SW - 70 - 240 - 40)[:3]
        th = 52 + len(lines) * 44
        ty = y0 + (h - th) // 2
        t_head = head
        d.text((240, ty), t_head, font=fh, fill=fg)
        for j, ln in enumerate(lines):
            d.text((240, ty + 62 + j * 44), ln, font=fd, fill=sub)
    yb = y + n * (h + gap) - gap
    if note:
        draw_block(d, CX, yb + 50, note, "serif-i", 34, 400, fg, 920, max_lines=2)
    by = pill(img, CX, SH - 260, cta, bg=NAVY if not dark else GOLD, fg=WHITE if not dark else NAVY, size=30)
    logo(img, CX, SH - 140, r=40, dark_bg=dark)
    return save(img, out)


def build():
    o = lambda n: os.path.join(OUT, n)
    files = []
    # 1. Commander
    files += [cover("bag", "Commander", "Comment passer commande en 1 minute", o("1-commander-1.jpg")),
              info("Commander", "Commander sur iread.ma", [
                  ("1", "Choisis ton livre", "Cherche par titre, auteur ou langue sur iread.ma"),
                  ("2", "Ajoute au panier", "Un livre, plusieurs, ou un pack à prix réduit"),
                  ("3", "Remplis le formulaire", "Nom, téléphone, ville et adresse. Pas de carte bancaire"),
                  ("4", "On te livre", "Livraison en 24 à 72 h, tu paies à la réception")],
                  o("1-commander-2.jpg"), cta="Lien dans la bio · iread.ma"),
              info("Commander", "Ou directement en DM", [
                  ("1", "Envoie-nous le titre", "Ou une photo de la couverture du livre que tu cherches"),
                  ("2", "On vérifie pour toi", "Disponibilité, langue et édition"),
                  ("3", "Donne tes infos", "Nom, téléphone et ville, et c'est réglé")],
                  o("1-commander-3.jpg"), cta="Écris-nous en DM", note="On te répond en français, en anglais et en arabe")]
    # 2. Livraison
    files += [cover("truck", "Livraison", "Partout au Maroc en 24 à 72 h", o("2-livraison-1.jpg")),
              info("Livraison", "Livraison partout au Maroc", [
                  ("1", "Gratuite à Casablanca", "Quel que soit le nombre de livres"),
                  ("2", "Gratuite partout dès 3 livres", "Dans toutes les villes du Maroc"),
                  ("3", "En 24 à 72 h", "Selon ta ville. Sinon, les frais sont affichés au panier")],
                  o("2-livraison-2.jpg"), note="Astuce : un pack = livraison offerte partout")]
    # 3. Paiement
    files += [cover("cash", "Paiement", "Tu paies à la livraison", o("3-paiement-1.jpg")),
              info("Paiement", "Paiement à la livraison", [
                  ("1", "Le livreur arrive", "Tu ouvres le colis devant lui"),
                  ("2", "Tu vérifies", "Titre, langue, édition et état des livres"),
                  ("3", "Tu paies en espèces", "Seulement si tout est conforme. Sinon, tu refuses et tu ne paies rien")],
                  o("3-paiement-2.jpg"),
                  note="Une fois le colis accepté et payé, pas de retour ni d'échange")]
    # 4. Packs
    files += [cover("books", "Packs", "Plusieurs livres, prix réduit", o("4-packs-1.jpg")),
              info("Packs", "Les packs iRead", [
                  ("1", "Prix réduit", "Les livres d'un même thème ou d'une saga, moins chers ensemble"),
                  ("2", "Livraison offerte", "Dès 3 livres, partout au Maroc"),
                  ("3", "Pour tous les goûts", "Thrillers, romance, développement perso, classiques, livres en arabe…")],
                  o("4-packs-2.jpg"), cta="Tous les packs sur iread.ma", dark=True)]
    # 5. ePub
    files += [cover("tablet", "ePub", "Nos livres aussi en numérique", o("5-epub-1.jpg")),
              info("ePub", "Livres numériques", [
                  ("1", "Tout de suite", "Téléchargement immédiat après le paiement par carte"),
                  ("2", "Sur tous tes écrans", "Apple Livres, Google Play Livres, Kobo, liseuses"),
                  ("3", "Sans DRM", "Ton fichier, pour un usage personnel")],
                  o("5-epub-2.jpg"), cta="Livres ePub sur iread.ma")]
    # 6. FAQ
    files += [cover("question", "FAQ", "Vos questions, nos réponses", o("6-faq-1.jpg")),
              info("FAQ", "Questions fréquentes", [
                  ("?", "Quelles langues ?", "Français, anglais et arabe"),
                  ("?", "Je vérifie avant de payer ?", "Oui, toujours, devant le livreur"),
                  ("?", "Retour ou échange ?", "Non après réception : vérifie bien ton colis avant de payer"),
                  ("?", "Une autre question ?", "Écris-nous en DM, on te répond rapidement")],
                  o("6-faq-2.jpg"), cta="Contact : DM ou iread.ma@hotmail.com")]
    return files


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for f in build():
        print(f)
