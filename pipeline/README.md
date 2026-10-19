# Pipeline visuels iRead

Tout tourne **dans le cloud** depuis un clone du dépôt `iread-content` : le Mac n'est pas nécessaire. Les visuels sources sont dans `library/` (photos, couvertures du site, visuels vérifiés, fichiers d'échange des agents).

- `design.py` : fonctions de rendu (charte : crème, marine et or ; polices Playfair, Inter et Amiri).
  - Stories 1080×1920 : `story_photo`, `story_extract`, `story_ab`, `story_cover`, `story_visual`, `story_pack`.
  - Posts 1080×1350 : `post_photo`, `post_page`, `post_cover_card`, `post_pack`.
- `build.py` : plan JSON → images dans `stories/` et `posts/`, `schedule-fragment.json`, planche de contrôle. `--apply` ajoute aussi les items à `schedule.json`.
- `fonts/` : polices (Google Fonts, licence OFL).

Prérequis : Python 3 + Pillow, avec libraqm pour l'arabe (sinon `pip install arabic-reshaper python-bidi`).

## Semaine type (rythme validé par Amine le 19/10/2026)

**Stories (5 par jour) :**

| Heure (Maroc) | Fonction | Contenu |
|---|---|---|
| 09:00 | `story_photo` | Vraie photo d'ambiance |
| 12:30 | `story_extract` | Couverture du site + vraie page surlignée (recadrée avec `box`) |
| 15:30 | `story_ab` (jours impairs) / `story_cover` (jours pairs) | Duel A/B ou coup de cœur |
| 18:30 | `story_visual` | Visuel vérifié (PUNCTUATIONS, posts KIE) |
| 21:30 | `story_pack` | Pack du jour, avec la mention livraison |

**Posts :**

| Heure | Contenu |
|---|---|
| 12:00 | Carrousel livre : `post_photo` + `post_page` |
| 15:00 | Carrousel ou carte coup de cœur |
| 16:30 | `post_pack` |
| 21:00 | Carrousel livre |

## Photos KIE (livres rares)
`library/photos/<Titre>/<slug>-kie-aesthetic-N.jpg` : à utiliser en story 09:00 (`story_photo`) et en carrousel (`post_photo` + `post_cover_card`). Au moins 2 ou 3 par semaine quand il y en a. Jamais comme page.

## Packs dans le catalogue Meta (chaque lundi)
1. Exporter les packs depuis Neon : `select value::text from app_settings where key='bundles'` → `library/packs/bundles.json`.
2. `python3 -B packs_feed.py ../library/packs/bundles.json` → `library/packs/<slug>.jpg` + `library/packs/packs.csv`.
3. Commit et push. Meta recharge `packs.csv` chaque jour (flux « iread.ma – packs »), et un nouveau pack entre tout seul dans les pubs.

## Règles
- Uniquement des livres actifs sur iread.ma (Neon `products`), et la couverture doit être celle de l'édition du site (`library/couvertures/<slug>.jpg`, ou `https://iread.ma/media/covers/<slug>.jpg` pour un livre récent).
- Pas de prix. Arguments autorisés : livraison gratuite à Casablanca, paiement à la livraison, prix réduit en pack (footers déjà intégrés).
- Pas de logo ni de pseudo d'un autre compte, pas de citation tapée : les extraits sont de vraies photos de pages.
- Chiffres toujours occidentaux (3, 5, 2), jamais ٣ ٥ ٢ : `design.py` et `build.py` convertissent automatiquement.
- En arabe, éviter les « . » et « : » ASCII.
- Les légendes sont dans la langue du livre, avec 8 hashtags et le CTA FR/EN/AR (voir `claude/strategie-contenu.md`).
