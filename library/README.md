# Photothèque iRead (source de vérité des agents)

| Dossier / fichier | Contenu | Écrit par |
|---|---|---|
| `photos/<Titre exact du catalogue>/` | Vraies photos : `*-aesthetic-N.jpg` (ambiance) et `*-page-N.jpg` (pages surlignées). `PUNCTUATIONS/` = ne pas modifier. `_inspiration-pinterest/` = non vérifié, ne pas publier tel quel. | agent photos |
| `couvertures/<slug>.jpg` | Couvertures exactes du site (slug = id produit = id catalogue Meta). Livre récent absent : `https://iread.ma/media/covers/<slug>.jpg` | agent contenu |
| `visuels-verifies/` | Visuels déjà vérifiés (posts KIE nettoyés) utilisables en story 18:30 | agent contenu |
| `_done.txt` | Titres traités par l'agent photos (`Titre \| ok/partiel/skip`) | agent photos |
| `_demandes.txt` | Titres demandés par l'agent contenu, à traiter en premier | agent contenu → agent photos |
| `_utilise.txt` | Photos déjà publiées (pas de réutilisation avant 60 jours) | agent contenu |
| `_ecartees/` | Photos retirées (filigrane, mauvaise édition…), avec la raison dans le nom | tous |

Les photos viennent de tiers (Pinterest). Avant de publier, vérifier : bon titre, **même édition que `couvertures/`**, aucun pseudo, logo ou filigrane d'un autre compte.
