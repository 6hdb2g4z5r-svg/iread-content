#!/usr/bin/env python3
"""Agent F : télécharge et range les photos listées dans library/_f_lot.json.
Lancé par .github/workflows/f-lot.yml. Format :
{"items":[{"url":"https://...","dest":"library/photos/<Titre>/<slug>-page-1.jpg",
           "rotate":0,"crop":[g,h,d,b],"autocontrast":false}]}
rotate, crop et autocontrast sont facultatifs. N'écrase jamais un fichier :
si dest existe, prend le premier numéro libre. Écrit le résultat dans
library/_f_lot.log, puis supprime le lot s'il n'y a eu aucun échec."""
import io, json, os, re, sys, time, urllib.request
from PIL import Image, ImageOps

LOT = "library/_f_lot.json"
LOG = "library/_f_lot.log"


def libre(dest):
    if not dest.startswith("library/") or ".." in dest:
        raise ValueError("chemin refusé")
    if "PUNCTUATIONS" in dest:
        raise ValueError("dossier interdit")
    if not os.path.exists(dest):
        return dest
    base = re.sub(r"-\d+\.jpg$", "", dest)
    n = 1
    while os.path.exists(f"{base}-{n}.jpg"):
        n += 1
    return f"{base}-{n}.jpg"


def traite(it):
    req = urllib.request.Request(it["url"], headers={"User-Agent": "Mozilla/5.0"})
    data = urllib.request.urlopen(req, timeout=60).read()
    im = Image.open(io.BytesIO(data)).convert("RGB")
    if it.get("rotate"):
        im = im.rotate(it["rotate"], resample=Image.BICUBIC)
    if it.get("crop"):
        im = im.crop(tuple(it["crop"]))
    if it.get("autocontrast"):
        im = ImageOps.autocontrast(im, cutoff=1)
    if im.width > 1440:
        im = im.resize((1440, im.height * 1440 // im.width), Image.LANCZOS)
    dest = libre(it["dest"])
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    im.save(dest, quality=92)
    return dest


def main():
    if not os.path.exists(LOT):
        return 0
    items = json.load(open(LOT, encoding="utf8"))["items"]
    date = time.strftime("%Y-%m-%d %H:%M")
    lignes, echecs = [], 0
    for it in items:
        try:
            lignes.append(f"{date} | ok | {traite(it)}")
        except Exception as e:
            echecs += 1
            lignes.append(f"{date} | ECHEC | {it.get('dest')} | {type(e).__name__}: {str(e)[:120]}")
    with open(LOG, "a", encoding="utf8") as f:
        f.write("\n".join(lignes) + "\n")
    print("\n".join(lignes))
    if not echecs:
        os.remove(LOT)
    return 1 if echecs else 0


if __name__ == "__main__":
    sys.exit(main())
