"""iRead — flux catalogue Meta avec images CARRÉES (les couvertures 2:3 étaient rognées dans les pubs).

    python3 -B square_feed.py

- Lit https://iread.ma/catalogue-meta.csv (source de vérité : prix, stock, nouveaux livres).
- Pour chaque livre : library/carre/<slug>.jpg = couverture entière, centrée sur fond crème 1080x1080, ombre douce.
  Régénérée seulement si la couverture du site a changé (empreinte dans library/carre/_hash.json).
- Écrit library/carre/books.csv (mêmes colonnes, image_link → image carrée sur GitHub).
- Meta lit ce fichier chaque jour (flux « iread.ma – livres » du catalogue « iRead – Livres »).
- Tourne chaque jour via .github/workflows/feeds.yml.
"""
import csv, hashlib, io, json, os, urllib.request
from PIL import Image
import design as D

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "library", "carre")
RAW = "https://raw.githubusercontent.com/6hdb2g4z5r-svg/iread-content/main/library/carre/"
UA = {"User-Agent": "Mozilla/5.0 iRead-feed"}


def fetch(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40).read()


def square(cover_bytes, out):
    S = 1080
    img = Image.new("RGB", (S, S), D.CREAM)
    cv = D.fit(D.load_bytes(cover_bytes), 700, 900)
    D.shadow_paste(img, cv, ((S - cv.width) // 2, (S - cv.height) // 2 - 6), radius=6, blur=26, offset=(0, 16), alpha=110)
    D.save(img, out, q=88)


def main():
    os.makedirs(OUT, exist_ok=True)
    hpath = os.path.join(OUT, "_hash.json")
    hashes = json.load(open(hpath)) if os.path.exists(hpath) else {}
    rows = list(csv.DictReader(io.StringIO(fetch("https://iread.ma/catalogue-meta.csv").decode("utf-8"))))
    made = 0
    for r in rows:
        slug, src = r["id"], r["image_link"]
        p = os.path.join(OUT, f"{slug}.jpg")
        try:
            raw = fetch(src)
        except Exception as e:
            print("couverture introuvable:", slug, e); continue
        h = hashlib.md5(raw).hexdigest()[:10]
        if hashes.get(slug) != h or not os.path.exists(p):
            square(raw, p); hashes[slug] = h; made += 1
        r["image_link"] = RAW + f"{slug}.jpg?v={h}"
    json.dump(hashes, open(hpath, "w"), indent=0, sort_keys=True)
    with open(os.path.join(OUT, "books.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    print(len(rows), "livres,", made, "images (re)générées")


if __name__ == "__main__":
    main()
