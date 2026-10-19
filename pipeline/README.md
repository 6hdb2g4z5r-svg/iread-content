# Pipeline visuels iRead

Copie de référence dans le dépôt GitHub `iread-content/pipeline/`. Copie de travail sur le Mac dans `~/Desktop/iRead/05-Contenu-Instagram/_pipeline/`.

- `design.py` : fonctions de rendu (charte : crème, marine et or ; polices Playfair, Inter et Amiri).
  - Stories 1080×1920 : `story_photo`, `story_extract`, `story_ab`, `story_cover`, `story_visual`, `story_pack`.
  - Posts 1080×1350 : `post_photo`, `post_page`, `post_cover_card`, `post_pack`.
- `build.py` : plan JSON → images + `schedule-fragment.json` + planche de contrôle.
- `fonts/` : polices (Google Fonts, licence OFL).

Prérequis : Python 3 + Pillow, avec libraqm pour l'arabe (sinon `pip install arabic-reshaper python-bidi`). Le Mac (VM `device_bash`) a tout.

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

## Règles
- Uniquement des livres actifs sur iread.ma (Neon `products`), et la couverture doit être celle de l'édition du site (`couvertures-site/<slug>.jpg`).
- Pas de prix. Arguments autorisés : livraison gratuite à Casablanca, paiement à la livraison, prix réduit en pack (footers déjà intégrés).
- Pas de logo ni de pseudo d'un autre compte, pas de citation tapée : les extraits sont de vraies photos de pages.
- En arabe, éviter les « . » et « : » ASCII.
- Les légendes sont dans la langue du livre, avec 8 hashtags et le CTA FR/EN/AR (voir `claude/strategie-contenu.md`).
