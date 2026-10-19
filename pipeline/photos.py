"""iRead — outil de l'agent photos (100 % cloud, sans Mac ni navigateur).

    python3 -B photos.py search <slug> "<Titre>" "<Auteur>"      # Pinterest → listes de candidats
    python3 -B photos.py cand <slug>                            # télécharge, OCR, 2 planches numérotées
    python3 -B photos.py pick <slug> "<Dossier = titre exact du catalogue>" --aes 3 7 12 --pages 0 4 9
    python3 -B photos.py kie <slug> "<Dossier>" [--inspi N] [--scene "..."]   # PLAN B livre rare : 1 photo générée

Travail dans /tmp/iread-photos/<slug>/ : planche_aes.jpg et planche_pages.jpg (à REGARDER avec Read avant de choisir).
Les numéros en jaune = candidats ; un cadre ROUGE = texte de type pseudo/site/filigrane détecté par OCR (à écarter sauf
vérification visuelle). Les photos choisies sont copiées dans library/photos/<Dossier>/<slug>-aesthetic-N.jpg / -page-N.jpg.
"""
import concurrent.futures as cf, io, json, os, re, shutil, subprocess, sys, urllib.parse, urllib.request
from PIL import Image, ImageDraw

REPO = os.environ.get("IREAD_REPO", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LIB = os.path.join(REPO, "library", "photos")
WORK = "/tmp/iread-photos"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Version/17.0 Safari/605.1.15"
MARK = re.compile(r"(@[\w.]{3,}|www\.\S+|\w+\.(?:com|net|pk|co|ma|fr)\b|[A-Z]{4,}/[A-Z]{3,}|\b\w*(?:BOOKS|STORE|SHOP)\w*\b)")


def pin_search(q, n=50):
    data = json.dumps({"options": {"query": q, "scope": "pins", "page_size": n, "rs": "typed"}, "context": {}})
    url = ("https://www.pinterest.com/resource/BaseSearchResource/get/?source_url="
           + urllib.parse.quote("/search/pins/?q=" + q) + "&data=" + urllib.parse.quote(data))
    req = urllib.request.Request(url, headers={"x-pinterest-pws-handler": "www/search/[scope].js",
                                               "x-requested-with": "XMLHttpRequest", "User-Agent": UA})
    for _ in range(3):
        try:
            j = json.load(urllib.request.urlopen(req, timeout=25))
            res = (j.get("resource_response", {}).get("data") or {}).get("results") or []
            return [x["images"]["orig"]["url"] for x in res if x.get("images", {}).get("orig")]
        except Exception:
            pass
    return []


def search(slug, title, author):
    d = os.path.join(WORK, slug); os.makedirs(d, exist_ok=True)
    pages, aes = [], []
    for q in (f"{title} {author} book page highlighted", f"{title} {author} annotated quotes page"):
        pages += pin_search(q)
    for q in (f"{title} book aesthetic bookstagram", f"{title} {author} book aesthetic"):
        aes += pin_search(q)
    pages, aes = list(dict.fromkeys(pages))[:48], [u for u in dict.fromkeys(aes) if u not in pages][:48]
    json.dump({"pages": pages, "aes": aes, "title": title, "author": author}, open(os.path.join(d, "urls.json"), "w"))
    print(slug, "pages", len(pages), "aes", len(aes))


def _dl(args):
    i, u, d = args
    try:
        raw = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA}), timeout=25).read()
        im = Image.open(io.BytesIO(raw)).convert("RGB")
        if min(im.size) < 500:
            return None
        f = f"{d}/{i:02d}.jpg"; im.save(f, quality=92); return f
    except Exception:
        return None


def _ocr(f):
    try:
        im = Image.open(f).convert("L"); im.thumbnail((1400, 1400)); t = f + ".png"; im.save(t)
        out = subprocess.run(["tesseract", t, "-", "--psm", "11"], capture_output=True, text=True,
                             env={**os.environ, "OMP_THREAD_LIMIT": "1"}, timeout=90).stdout
        os.remove(t)
        return f, len(re.findall(r"[A-Za-z']{3,}", out)), bool(MARK.search(out))
    except Exception:
        return f, -1, False


def _sheet(items, out):
    cols, tw, th = 6, 220, 290
    rows = max((len(items) + cols - 1) // cols, 1)
    S = Image.new("RGB", (cols * (tw + 8), rows * (th + 8)), (34, 34, 34))
    dr = ImageDraw.Draw(S)
    for i, (f, n, mark) in enumerate(items):
        im = Image.open(f); im.draft("RGB", (tw * 2, th * 2)); im = im.convert("RGB"); im.thumbnail((tw, th))
        x = (i % cols) * (tw + 8) + 4; y = (i // cols) * (th + 8) + 4
        S.paste(im, (x, y))
        if mark:
            dr.rectangle([x, y, x + im.width - 1, y + im.height - 1], outline=(255, 0, 0), width=5)
        dr.rectangle([x, y, x + 34, y + 18], fill=(0, 0, 0)); dr.text((x + 4, y + 3), str(i), fill=(255, 255, 0))
    S.save(out, quality=85)


def cand(slug):
    d = os.path.join(WORK, slug); u = json.load(open(os.path.join(d, "urls.json")))
    res = {}
    for kind in ("pages", "aes"):
        dd = os.path.join(d, kind); os.makedirs(dd, exist_ok=True)
        with cf.ThreadPoolExecutor(10) as ex:
            files = [f for f in ex.map(_dl, [(i, x, dd) for i, x in enumerate(u[kind])]) if f]
        with cf.ThreadPoolExecutor(6) as ex:
            oc = list(ex.map(_ocr, files))
        keep = [r for r in oc if (r[1] >= 40 if kind == "pages" else 0 <= r[1] <= 30)]
        keep.sort(key=lambda r: (r[2], -r[1] if kind == "pages" else r[1]))
        keep = keep[:36]
        json.dump([r[0] for r in keep], open(os.path.join(d, f"{kind}.json"), "w"))
        _sheet(keep, os.path.join(d, f"planche_{kind}.jpg"))
        res[kind] = (len(files), len(keep), sum(r[2] for r in keep))
    print(slug, {k: f"{a} téléchargées, {b} candidates, {c} suspectes" for k, (a, b, c) in res.items()})
    print("Planches :", os.path.join(d, "planche_aes.jpg"), os.path.join(d, "planche_pages.jpg"))


def pick(slug, folder, aes, pages):
    d = os.path.join(WORK, slug); dest = os.path.join(LIB, folder); os.makedirs(dest, exist_ok=True)
    for kind, labels, suffix in (("aes", aes, "aesthetic"), ("pages", pages, "page")):
        if not labels:
            continue
        lst = json.load(open(os.path.join(d, f"{kind}.json")))
        n = len([x for x in os.listdir(dest) if f"-{suffix}-" in x])
        for l in labels:
            n += 1
            shutil.copy(lst[int(l)], os.path.join(dest, f"{slug}-{suffix}-{n}.jpg"))
    print(folder, "→", sorted(os.listdir(dest)))


# ───────────── Plan B : livre rare sans bonne photo → photo générée avec KIE (nano-banana-pro) ─────────────
KIE_API = "https://api.kie.ai"
KIE_PROMPT = (
    "Photorealistic lifestyle 'bookstagram' photo for a bookshop's Instagram. "
    "The ONLY book in the picture must be EXACTLY the book shown in reference image 1: reproduce its front cover "
    "faithfully — identical title text, author name, colours, illustration, typography, layout and language "
    "(do not translate, rewrite, restyle or invent any text on the cover). "
    "Use reference image 2 ONLY as inspiration for the setting, props, colour palette and lighting; do not copy any "
    "text, logo, watermark, username, person or other book from it. "
    "Scene: {scene}. The book's front cover is fully visible, sharp and readable, facing the camera at a slight angle, "
    "occupying about 40% of the frame. Soft warm natural light, cozy elegant atmosphere, shallow depth of field, "
    "realistic paper texture and shadows. No text overlay, no logo, no watermark, no extra readable book titles, "
    "no distorted hands."
)


def _kie_key():
    k = os.environ.get("KIE_API_KEY")
    if k:
        return k
    import glob
    for p in glob.glob(os.path.expanduser("~/.claude/skills/**/kie-ai/SKILL.md"), recursive=True):
        m = re.search(r'KIE_API_KEY\s*=\s*"([0-9a-f]{20,})"', open(p).read())
        if m:
            return m.group(1)
    raise SystemExit("Clé KIE introuvable (variable KIE_API_KEY ou skill kie-ai).")


def _kie_req(method, path, **kw):
    import requests
    h = {"Authorization": f"Bearer {_kie_key()}"}
    return requests.request(method, path if path.startswith("http") else KIE_API + path, headers=h, timeout=120, **kw).json()


def _kie_upload(local):
    import requests
    r = requests.post("https://kieai.redpandaai.co/api/file-stream-upload",
                      headers={"Authorization": f"Bearer {_kie_key()}"},
                      files={"file": (os.path.basename(local), open(local, "rb"))},
                      data={"uploadPath": "iread/inputs", "fileName": os.path.basename(local)}, timeout=120).json()
    d = r.get("data") or {}
    return d.get("downloadUrl") or d.get("fileUrl")


def kie(slug, folder, inspi=None, scene=None, ratio="4:5"):
    """1 génération (≈ quelques dizaines de crédits). Couverture du site = référence 1, inspiration Pinterest = référence 2."""
    import time, requests
    credits = _kie_req("GET", "/api/v1/chat/credit").get("data")
    print("crédits KIE avant :", credits)
    if credits is not None and credits < 500:
        raise SystemExit("Moins de 500 crédits KIE : on n'en dépense pas, signaler à Amine.")
    cover = os.path.join(REPO, "library", "couvertures", f"{slug}.jpg")
    if not os.path.exists(cover):
        os.makedirs(os.path.join(WORK, slug), exist_ok=True)
        cover = os.path.join(WORK, slug, "cover.jpg")
        open(cover, "wb").write(urllib.request.urlopen(urllib.request.Request(
            f"https://iread.ma/media/covers/{slug}.jpg", headers={"User-Agent": UA}), timeout=30).read())
    refs = [_kie_upload(cover)]
    if inspi is not None:
        refs.append(_kie_upload(json.load(open(os.path.join(WORK, slug, "aes.json")))[int(inspi)]))
    prompt = KIE_PROMPT.format(scene=scene or "the book resting on a soft beige knitted blanket next to a cup of mint tea "
                               "and a lit candle, on a wooden table")
    if inspi is None:
        prompt = prompt.replace("Use reference image 2 ONLY as inspiration for the setting, props, colour palette and "
                                "lighting; do not copy any text, logo, watermark, username, person or other book from it. ", "")
    r = _kie_req("POST", "/api/v1/jobs/createTask", json={"model": "nano-banana-pro", "input": {
        "prompt": prompt, "image_input": refs, "aspect_ratio": ratio, "resolution": "2K", "output_format": "jpg"}})
    if r.get("code") != 200:
        raise SystemExit(f"KIE createTask : {r}")
    tid, t0, wait = r["data"]["taskId"], time.time(), 4
    while True:
        d = _kie_req("GET", "/api/v1/jobs/recordInfo", params={"taskId": tid})["data"]
        if d["state"] == "success":
            break
        if d["state"] == "fail" or time.time() - t0 > 600:
            raise SystemExit(f"KIE échec : {d.get('failMsg')}")
        time.sleep(wait); wait = min(wait * 1.5, 15)
    url = json.loads(d["resultJson"])["resultUrls"][0]
    dest = os.path.join(LIB, folder); os.makedirs(dest, exist_ok=True)
    n = len([x for x in os.listdir(dest) if "-kie-" in x]) + 1
    out = os.path.join(dest, f"{slug}-kie-aesthetic-{n}.jpg")
    Image.open(io.BytesIO(requests.get(url, timeout=120).content)).convert("RGB").save(out, quality=92)
    print("généré :", out, "| crédits restants :", _kie_req("GET", "/api/v1/chat/credit").get("data"))
    print("→ REGARDE l'image et compare-la à la couverture ; si le texte de la couverture est déformé, supprime-la "
          "(1 seule nouvelle tentative autorisée).")


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0] == "search":
        search(a[1], a[2], a[3] if len(a) > 3 else "")
    elif a[0] == "cand":
        cand(a[1])
    elif a[0] == "pick":
        sel, cur = {"--aes": [], "--pages": []}, None
        for x in a[3:]:
            if x in sel:
                cur = x
            elif cur and x.isdigit():
                sel[cur].append(x)
        pick(a[1], a[2], sel["--aes"], sel["--pages"])
    elif a[0] == "kie":
        opt = {k: a[a.index(k) + 1] for k in ("--inspi", "--scene", "--ratio") if k in a}
        kie(a[1], a[2], opt.get("--inspi"), opt.get("--scene"), opt.get("--ratio", "4:5"))
