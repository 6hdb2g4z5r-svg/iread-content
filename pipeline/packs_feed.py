"""iRead — packs dans le catalogue Meta (2e flux, hébergé sur GitHub, sans redéployer le site).

    python3 -B packs_feed.py ../library/packs/bundles.json

- bundles.json = valeur de app_settings['bundles'] dans Neon (l'agent contenu la ré-exporte chaque lundi).
- Lit le flux livres https://iread.ma/catalogue-meta.csv (prix réels + couvertures).
- Génère library/packs/<slug>.jpg (1080x1080 : couvertures + titre + « X MAD au lieu de Y MAD ») et library/packs/packs.csv.
- Meta recharge packs.csv chaque jour (flux « iread.ma – packs » du catalogue « iRead – Livres »).
"""
import csv, io, json, os, sys, urllib.request
from PIL import Image, ImageDraw
import design as D

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "library", "packs")
RAW = "https://raw.githubusercontent.com/6hdb2g4z5r-svg/iread-content/main/library/packs/"
UA = {"User-Agent": "Mozilla/5.0 iRead-packs"}


def fetch(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40).read()


def money(s):
    return float((s or "0").split()[0] or 0)


def pack_image(title, covers, price, regular, out, sub=""):
    S = 1080
    img = Image.new("RGB", (S, S), D.CREAM)
    d = ImageDraw.Draw(img)
    D.pill(img, S // 2, 70, "PACK", bg=D.NAVY, fg=D.WHITE, size=24)
    y = D.draw_block(d, S // 2, 120, title, "serif", 62, 600, D.INK, 980, max_lines=1)
    if sub:
        y = D.draw_block(d, S // 2, y + 2, sub, "sans", 26, 400, D.MUTED, 980, max_lines=1)
    n = len(covers)
    cols = 3 if n in (3, 5, 6) else (2 if n in (2, 4) else 3)
    rows = (n + cols - 1) // cols
    top, bottom = y + 30, S - 190
    gap = 24
    ch = (bottom - top - gap * (rows - 1)) // rows
    cw = min(int(ch * 0.68), (S - 120 - gap * (cols - 1)) // cols)
    for i, c in enumerate(covers):
        r, k = divmod(i, cols)
        in_row = min(cols, n - r * cols)
        x0 = (S - (in_row * cw + (in_row - 1) * gap)) // 2
        cv = D.fit(c, cw, ch)
        D.shadow_paste(img, cv, (x0 + k * (cw + gap) + (cw - cv.width) // 2, top + r * (ch + gap) + (ch - cv.height) // 2),
                       radius=4, blur=16, offset=(0, 10), alpha=120)
    # prix : « 319 MAD » gros + « au lieu de 399 MAD » barré
    fp = D.font("serif", 64, 700); fr = D.font("sans", 30, 500)
    a = f"{price} MAD"; b = f"au lieu de {regular} MAD"
    wa, _ = D.text_w(d, a, fp); wb, hb = D.text_w(d, b, fr)
    x = (S - (wa + 24 + wb)) // 2; yy = S - 150
    d.text((x, yy), a, font=fp, fill=D.NAVY)
    bx = x + wa + 24; by = yy + 26
    d.text((bx, by), b, font=fr, fill=D.MUTED)
    tw = D.text_w(d, f"{regular} MAD", fr)[0]
    d.line([(bx + wb - tw, by + hb // 2 + 6), (bx + wb, by + hb // 2 + 6)], fill=D.MUTED, width=3)
    D.draw_center(d, S // 2, S - 60, "Livraison partout au Maroc · Paiement à la livraison", D.font("sans", 24, 500), D.INK)
    D.save(img, out)


def main(bundles_path):
    os.makedirs(OUT, exist_ok=True)
    data = json.load(open(bundles_path))
    defs = data["list"] if isinstance(data, dict) else data
    books = {r["id"]: r for r in csv.DictReader(io.StringIO(fetch("https://iread.ma/catalogue-meta.csv").decode("utf-8")))}
    rows = []
    for p in defs:
        if p.get("active") is False:
            continue
        items = [books.get(s) for s in p["items"]]
        if any(b is None for b in items) or len(items) < 2:
            print("pack ignoré (livre absent du site) :", p["slug"]); continue
        regular = int(round(sum(money(b["sale_price"]) or money(b["price"]) for b in items)))
        price = int(p["price"])
        if price >= regular:
            print("pack ignoré (pas de remise) :", p["slug"]); continue
        covers = [D.load_bytes(fetch(b["image_link"])) for b in items]
        img = os.path.join(OUT, f"{p['slug']}.jpg")
        pack_image(p["title"], covers, price, regular, img)
        stock = "out of stock" if any(b["availability"] != "in stock" for b in items) else "in stock"
        names = " · ".join(b["title"] for b in items)
        rows.append({
            "id": f"pack-{p['slug']}", "title": f"Pack {p['title']} ({len(items)} livres)"[:150],
            "description": f"{p.get('subtitle', '')} {len(items)} livres : {names}. Livraison partout au Maroc, paiement à la livraison."[:4900],
            "availability": stock, "condition": "new", "price": f"{regular:.2f} MAD", "sale_price": f"{price:.2f} MAD",
            "link": f"https://iread.ma/pack/{p['slug']}", "image_link": RAW + f"{p['slug']}.jpg?v={price}",
            "brand": "iRead", "google_product_category": "784", "product_type": "Packs",
            "custom_label_0": items[0]["custom_label_0"], "custom_label_1": "pack",
        })
    with open(os.path.join(OUT, "packs.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    print(len(rows), "packs →", os.path.join(OUT, "packs.csv"))


if __name__ == "__main__":
    main(sys.argv[1])
