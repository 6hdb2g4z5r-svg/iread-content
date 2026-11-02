# iRead — Stratégie contenu Instagram et pubs (validée par Amine le 19/10/2026, fil corrigé le 26/10, WhatsApp ajouté le 28/10)

**Objectif unique** : amener les gens sur **iread.ma** pour acheter. Chaque publication montre un livre ou un pack vendu sur le site et se termine par un appel à commander.

## 1. Formats et rythme
**Posts du fil (4:5, 1080×1350), jusqu'à 4 par jour — UNIQUEMENT DES PHOTOS (décision d'Amine du 26/10) :**

| Heure | Format |
|---|---|
| 12:00 | Carrousel livre (vraie photo d'ambiance + vraie page surlignée) |
| 15:00 | Carrousel livre en photos |
| 16:30 | Carrousel livre en photos |
| 21:00 | Carrousel livre en photos |

- **Interdit dans le fil** : carte couverture sur fond crème (`post_cover_card`), collage de pack (`post_pack`), toute carte texte ou graphique. Le 25/10, deux posts de ce type (pack Colleen Hoover, قواعد العشق الأربعون) sont partis et Amine les a refusés : « pas aligné avec ce qu'on a convenu ». Les 10 suivants (26–31/10) ont été retirés de `schedule.json`.
- Un post = livre réel dans une ambiance chaude, couverture lisible (photo réelle, vraie page, ou photo KIE validée). Pas assez de photos → moins de posts, jamais un visuel graphique.
- **Packs** : en stories uniquement (21:30). Une légende de post peut mentionner le pack qui contient le livre.

**Stories (9:16, 1080×1920), 5 par jour :**

| Heure | Format |
|---|---|
| 09:00 | Photo d'ambiance |
| 12:30 | Extrait (couverture du site + vraie page surlignée) |
| 15:30 | Duel A/B les jours impairs, carte coup de cœur les jours pairs |
| 18:30 | Visuel vérifié |
| 21:30 | Pack du jour |

- Mélange FR / EN / AR chaque jour.
- Stories avec lien : **on garde le rythme actuel**. L'agent publie sans sticker lien (limite de l'API) ; la story renvoie vers « iread.ma » en texte.
- **Passages (24/10)** : sur tout extrait ou page, le passage surligné doit être lisible en entier (aucune ligne coupée). Sinon, on ne l'utilise pas.

## 1 bis. Photos générées par KIE pour les livres rares (validé par Amine le 19/10)
Les fichiers `library/photos/<Titre>/<slug>-kie-aesthetic-N.jpg` sont des photos d'ambiance générées à partir de la couverture exacte du site (exemple validé : « جمرة »). Amine les veut **en posts ET en stories**, au même titre que les vraies photos :
- **Story 09:00** (`story_photo`) ;
- **Post** : `post_photo` seul. Un carrousel = photo du livre + **vraie page du livre** (`post_page`). **Deux photos de la couverture sont interdites, même différentes (Amine, 02/11)**. Sans page correcte : photo seule et demande de page dans `_demandes.txt`. **Plus de `post_cover_card` en slide 2** (règle du fil du 26/10).
- Ces photos servent à mettre en avant les livres rares du site : en programmer **au moins 2 ou 3 par semaine** quand il y en a de disponibles.
- Ne jamais les utiliser comme « page » ou « extrait ».

## 2. Règles non négociables
- Uniquement des livres actifs sur iread.ma, **édition et couverture exactes du site**. Une erreur de couverture est « inadmissible ».
- Aucun logo, pseudo ou filigrane d'un autre compte. Aucune citation tapée : les extraits sont de vraies photos de pages.
- **Pas de prix.** Arguments autorisés (validés) : « Livraison gratuite dès 3 livres » (offre d'Amine du 19/10, partout au Maroc), « Livraison gratuite à Casablanca », « Paiement à la livraison », « Prix réduit en pack ». Le pipeline les intègre en bas des stories et des packs.
- Ne jamais écrire « livres authentiques ».
- **WhatsApp autorisé depuis le 28/10 (décision d'Amine)** : numéro iRead **+212 675-214027** (lien `https://wa.me/212675214027`). Il apparaît dans le CTA des légendes (ci-dessous), sur le site (bouton flottant, fiche livre, pied de page) et l'agent DM peut le proposer. Avant le 28/10, la règle était « jamais WhatsApp » : elle est levée.
- **Chiffres toujours occidentaux (3, 5, 2), y compris en arabe** : jamais ٣ ٥ ٢ (demande d'Amine du 19/10). Le pipeline convertit automatiquement.

**Légendes** : dans la langue du livre, avec 8 hashtags. La légende se termine par (CTA du 28/10) :
- FR : « 👉 Commandez dès maintenant via DM, WhatsApp ou sur www.iread.ma ✅ »
- EN : « 👉 Order now via DM, WhatsApp or on www.iread.ma ✅ »
- AR : « 👉 اطلبه الآن عبر الرسائل الخاصة أو واتساب أو من موقعنا www.iread.ma ✅ » (« اطلبها » pour les listes et les packs)

## 3. Catalogue Meta (créé le 19/10/2026)
- Catalogue **« iRead – Livres »**, id `1141234108362386`, business IRead `29386217087735505`.
- Flux livres id `1884421093011996` : depuis le 19/10 il lit `library/carre/books.csv` du dépôt GitHub (copie de `iread.ma/catalogue-meta.csv` avec des **images carrées** : couverture entière sur fond crème, sinon Meta rognait les livres). Rechargé chaque jour à 04:13 (Maroc). Le fichier est régénéré chaque nuit à 02:15 UTC par l'action GitHub `.github/workflows/feeds.yml` (`pipeline/square_feed.py` + `pipeline/packs_feed.py`).
- Visuels packs : prix en Inter (les chiffres de Playfair rendaient « 189 » illisible).
- **Pixel** « iRead.ma » `1787289369151594` relié au catalogue. Le site envoie ViewContent, AddToCart, InitiateCheckout et Purchase (navigateur + API Conversions) avec `content_ids` = slug = id catalogue. Les pubs peuvent donc recibler chaque visiteur avec les livres qu'il a vus.
- **Ensembles de produits (centres d'intérêt)** :

| Ensemble | Livres | Id |
|---|---|---|
| Romans | 98 | 2657219814698849 |
| Développement personnel | 71 | 2220859398493518 |
| Business & Finance | 27 | 1167769189016762 |
| Classiques | 28 | 1416607700450603 |
| Thrillers | 17 | 1844921740276741 |
| Essais & Histoire | 17 | 1130293072909434 |
| Livres en arabe | 112 | 1679068457124719 |
| Livres en français | 89 | 1665617265132025 |
| Livres en anglais | 64 | 1768215361127040 |
| Best-sellers | 6 | 1150619220687676 |

- Un nouveau livre ajouté sur le site entre automatiquement dans le catalogue le lendemain, et dans le bon ensemble.

## 4. Pubs Meta : stratégie validée le 19/10 (modèle Books On Demand)
**Décisions d'Amine** : mêmes pubs que Books On Demand, **prix affichés dans les pubs** (exception à la règle sans prix, qui reste valable pour les posts et stories organiques), budget **environ 10 $/jour**. Amine ajoute la carte bancaire au compte pub IRead (`1816995082672132`).

**Catalogue** : 265 livres (flux du site) + **29 packs** (flux GitHub `library/packs/packs.csv`, id 1449409477395103 ; visuels avec « X MAD au lieu de Y MAD »). Ensemble « Packs » : 1469150558472505.

**Structure (une seule campagne, le budget ne se divise pas à 10 $/jour)** :
- Campagne Ventes (Advantage+), 10 $/jour, Maroc, ciblage large Advantage+, tous placements Instagram et Facebook.
- Optimisation : les 2 premières semaines sur « Ajout au panier » (assez de volume pour que Meta apprenne), puis sur « Achat » dès qu'il y a 15 à 20 commandes par semaine.
- Pubs dans la campagne :
  1. **Catalogue dynamique** (tous les livres et packs, carrousel) : Meta montre à chacun les livres qui l'intéressent, et reprend automatiquement les visiteurs qui ont vu un livre sans acheter.
  2. **Carrousel « par intérêt »** (format phare de BOD) : 1 carte par thème (Money Mindset, Mode Discipline ON, Romantasy, Nuits blanches, Racines marocaines, ابدأ من جديد…). Chaque carte renvoie vers la page du pack. Version 2 : les vraies photos de piles de livres prises par Amine.
  3. **Packs** : catalogue limité à l'ensemble Packs, avec le prix barré.
  4. (plus tard) vidéo : livres en main, façon BOD.
- Texte : offre en tête **« Livraison GRATUITE partout au Maroc dès 3 livres »** (validée par Amine le 19/10, aussi appliquée sur le site, au panier et par l'agent DM), puis paiement à la livraison.
- Campagne créée le 19/10 : 120250115355040473 (8,30 $/j CBO). Ensembles : catalogue 120250115364900473 (pubs catalogue dynamique + packs), carrousel par intérêt 120250115595530473.

**Attentes réalistes à 10 $/jour** (estimation, à vérifier sur 2 semaines) :
- environ 70 à 150 clics par jour ;
- 0,5 à 2 commandes par jour, soit environ 15 à 40 par mois ;
- coût par commande de 75 à 200 MAD, qui baisse avec les packs et quand Meta a appris ;
- juger sur les commandes **confirmées ou livrées** (paiement à la livraison), pas seulement passées.

## 5. Instagram Shopping (étiquettes produits sur les posts)
Nécessite une boutique Commerce Manager éligible. L'éligibilité du Maroc est à vérifier dans Commerce Manager. Si le pays n'est pas éligible, les pubs catalogue (§4) jouent le même rôle : carrousels cliquables qui mènent à la fiche produit.
