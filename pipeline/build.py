"""iRead — génère une semaine de contenu à partir d'un plan JSON.

Usage (dans le cloud, depuis un clone du dépôt iread-content) :
    cd iread-content/pipeline
    python3 -B build.py ../semaines/2026-11-01/plan.json

Le plan est une liste d'items :
{
  "id": "story-2026-11-01-1",            # unique ; "story-…" ou "post-…"
  "kind": "story" | "post" | "carousel",
  "publish_at": "2026-11-01T09:00:00+00:00",   # heure Maroc = UTC
  "title": "Titre court (suivi)",
  "caption": "Légende complète (posts uniquement)",
  "slides": [ {"fn": "story_photo", "args": {...}} , ... ]   # 1 slide = 1 image
}
Dans "args", tout chemin est RELATIF au dossier library/ du dépôt (ex. "photos/Deep Work/deep-work-aesthetic-1.jpg",
"couvertures/deep-work.jpg", "visuels-verifies/LA-1.jpg"). Les paramètres "out" sont générés automatiquement.

Sortie : images directement dans le dépôt (stories/…, posts/<date-id>/N.jpg)
         <dossier du plan>/schedule-fragment.json (items à ajouter à schedule.json — `--apply` le fait)
         <dossier du plan>/_planche.jpg (planche de contrôle à regarder AVANT de pousser)
"""
import json, os, sys
import design as D

REPO = os.environ.get("IREAD_REPO", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ROOT = os.environ.get("IREAD_ROOT", os.path.join(REPO, "library"))
PATH_KEYS = {"photo_path", "cover_path", "page_path", "cover_a", "cover_b", "src_path"}


def absify(args):
    out = {}
    for k, v in args.items():
        if k in PATH_KEYS:
            out[k] = os.path.join(ROOT, v)
        elif k == "cover_paths":
            out[k] = [os.path.join(ROOT, x) for x in v]
        else:
            out[k] = v
    return out


def main(plan_path):
    plan = json.load(open(plan_path))
    base = os.path.dirname(os.path.abspath(plan_path))
    repo = REPO
    frag, made, errors = [], [], []
    for it in plan:
        media = []
        for i, sl in enumerate(it["slides"], 1):
            if it["kind"] == "story":
                rel = f"stories/{it['id'].replace('story-', '')}.jpg"
            else:
                rel = f"posts/{it['id'].replace('post-', '')}/{i}.jpg"
            out = os.path.join(repo, rel)
            try:
                getattr(D, sl["fn"])(out=out, **absify(sl["args"]))
                media.append(rel); made.append(out)
            except Exception as e:  # keep going, report at the end
                errors.append(f"{it['id']} slide {i}: {e}")
        if len(media) == len(it["slides"]):
            row = {"id": it["id"], "kind": it["kind"], "media": media, "publish_at": it["publish_at"], "title": it["title"]}
            row["title"] = D.latin_digits(row["title"])
            if it.get("caption"):
                row["caption"] = D.latin_digits(it["caption"])
            frag.append(row)
    json.dump(frag, open(os.path.join(base, "schedule-fragment.json"), "w"), ensure_ascii=False, indent=1)
    if made:
        D.contact_sheet(made, os.path.join(base, "_planche.jpg"), cols=8, w=200)
    print(f"{len(frag)}/{len(plan)} items, {len(made)} images")
    for e in errors:
        print("ERREUR", e)
    return frag, errors


def apply(frag):
    """Ajoute les items à schedule.json (remplace un id existant)."""
    p = os.path.join(REPO, "schedule.json")
    d = json.load(open(p))
    ids = {x["id"] for x in frag}
    d["items"] = [x for x in d["items"] if x["id"] not in ids] + frag
    d["items"].sort(key=lambda x: x["publish_at"])
    json.dump(d, open(p, "w"), ensure_ascii=False, indent=1)
    print(f"schedule.json : {len(d['items'])} items")


if __name__ == "__main__":
    frag, errors = main(sys.argv[1])
    if "--apply" in sys.argv and not errors:
        apply(frag)
