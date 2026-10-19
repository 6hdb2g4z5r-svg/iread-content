"""iRead — génère une semaine de contenu à partir d'un plan JSON.

Usage (sur le Mac via device_bash) :
    cd ~/mnt/Desktop/iRead/05-Contenu-Instagram/_pipeline
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
Dans "args", tout chemin est RELATIF au dossier iRead (ex. "04-Photos-Livres/Deep Work/deep-work-aesthetic-1.jpg",
"05-Contenu-Instagram/couvertures-site/deep-work.jpg"). Les paramètres "out" sont générés automatiquement.

Sortie : <dossier du plan>/repo/{stories,posts}/… (même arborescence que le dépôt GitHub iread-content)
         <dossier du plan>/schedule-fragment.json (items à ajouter à schedule.json)
         <dossier du plan>/_planche.jpg (planche de contrôle à regarder AVANT de pousser)
"""
import json, os, sys
import design as D

ROOT = os.environ.get("IREAD_ROOT", os.path.expanduser("~/mnt/Desktop/iRead"))
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
    repo = os.path.join(base, "repo")
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


if __name__ == "__main__":
    main(sys.argv[1])
