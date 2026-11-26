#!/usr/bin/env python3
"""Ajoute au planning les éléments de library/_schedule_add.json (même format que schedule.json : {"items": [...]}).
Appelé par pipeline/f_lot.py (workflow f-lot, déclenché par un push de library/_f_lot.json, même vide : {"items": []}). Sert aux sessions qui ne peuvent pas pousser un gros schedule.json
(connecteur GitHub limité au texte court). N'écrase jamais un id existant ; vérifie que chaque média existe ;
trie par publish_at ; supprime le fichier d'ajout si tout est passé. Journal : library/_schedule_add.log"""
import json, os, subprocess, sys, time

ADD, LOG, SCH = "library/_schedule_add.json", "library/_schedule_add.log", "schedule.json"


def main():
    if not os.path.exists(ADD):
        return 0
    sch = json.load(open(SCH, encoding="utf8"))
    ids = {i["id"] for i in sch["items"]}
    date = time.strftime("%Y-%m-%d %H:%M")
    lignes, echecs = [], 0
    for it in json.load(open(ADD, encoding="utf8"))["items"]:
        manque = [m for m in it.get("media", []) if not os.path.exists(m)]
        if it["id"] in ids:
            lignes.append(f"{date} | deja | {it['id']}")
        elif manque or not it.get("media"):
            echecs += 1
            lignes.append(f"{date} | ECHEC media absent | {it['id']} | {manque}")
        else:
            sch["items"].append(it); ids.add(it["id"])
            lignes.append(f"{date} | ok | {it['id']} | {it['publish_at']}")
    sch["items"].sort(key=lambda x: x["publish_at"])
    json.dump(sch, open(SCH, "w", encoding="utf8"), ensure_ascii=False, indent=1)
    with open(LOG, "a", encoding="utf8") as f:
        f.write("\n".join(lignes) + "\n")
    print("\n".join(lignes))
    if not echecs:
        os.remove(ADD)
    # le workflow f-lot ne fait « git add » que sur library/ : on indexe schedule.json ici
    subprocess.run(["git", "add", SCH], check=False)
    return 1 if echecs else 0


if __name__ == "__main__":
    sys.exit(main())
