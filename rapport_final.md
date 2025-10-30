# Analyse croisée fontaines vs seniors

## Contexte et objectif
L'étude vise à évaluer la couverture des fontaines à boire publiques à Paris, en la rapportant aux bénéficiaires du dispositif Pass Paris Seniors (proxy de la population âgée) par arrondissement. L'objectif est d'identifier les zones où l'accès à l'eau potable est susceptible d'être insuffisant pour les seniors, population particulièrement exposée aux vagues de chaleur.

## Jeux de données
- **Fontaines à boire** (`data/raw/fontaines_a_boire.csv`) : inventaire des fontaines publiques parisiennes avec leur statut de disponibilité.
- **Pass Paris Seniors ou Access** (`data/raw/nombre_de_beneficiaires_pass_paris_seniors.json`) : nombre annuel de bénéficiaires âgés par arrondissement (2013-2017).

Les deux jeux ont été croisés via le numéro d'arrondissement (code INSEE `750XX`).
Ils sont récupérés automatiquement via l'API Paris Open Data (`scripts/download_data.py`), chargés avec les agrégations intermédiaires dans une base SQLite (`data/processed/paris_fountains.sqlite`) pour répondre à l'étape d/ du plan initial, puis répliqués dans une base SQL Server (`ParcFountains`) pour exploitation sous SSMS.

## Méthodologie
1. Filtrage des fontaines disponibles (`dispo = "OUI"`).
2. Comptage du nombre de fontaines par arrondissement.
3. Sélection, pour chaque arrondissement, du millésime le plus récent (2017) de bénéficiaires seniors.
4. Calcul du ratio `fontaines pour 1000 bénéficiaires seniors`.
5. Téléchargement automatisé des données brutes via `scripts/download_data.py` (API Paris Open Data).
6. Ingestion des jeux de données bruts, des agrégations et du résultat final dans la base SQLite `data/processed/paris_fountains.sqlite` (tables `fountains_raw`, `seniors_raw`, `fountains_available`, `seniors_latest`, `fountains_vs_seniors`).
7. Classement des arrondissements selon ce ratio et production d'une visualisation bar chart (`data/processed/fountains_per_1000_seniors.png`).
8. Export des tables SQLite vers SQL Server (`ParcFountains`) via `scripts/export_sqlserver.py` pour faciliter les requêtes dans SSMS.

Toutes les étapes de traitement sont automatisées dans `scripts/compute_metrics.py` et `scripts/visualize_metrics.py`.

## Résultats clés (2017)
| Arrondissement | Seniors bénéficiaires | Fontaines disponibles | Fontaines / 1000 seniors |
|----------------|-----------------------|-----------------------|---------------------------|
| 75008 | 767 | 32 | 41.72 |
| 75004 | 1041 | 30 | 28.82 |
| 75016 | 4538 | 107 | 23.58 |
| 75007 | 1284 | 29 | 22.59 |
| 75012 | 6175 | 103 | 16.68 |
| ... | ... | ... | ... |
| 75019 | 9800 | 89 | 9.08 |
| 75011 | 6395 | 57 | 8.91 |
| 75009 | 1803 | 14 | 7.76 |
| 75015 | 8945 | 68 | 7.60 |
| 75001 | 553 | 0 | 0.00 |

## Visualisation
La figure `data/processed/fountains_per_1000_seniors.png` présente les 10 arrondissements les mieux pourvus en fontaines rapportées aux seniors. Elle met en évidence la surreprésentation des arrondissements centraux et de l'ouest parisien.

- Les 1er et 15e arrondissements ressortent comme les moins bien couverts : absence totale de fontaines disponibles dans le 1er, densité inférieure à 8 pour 1000 seniors dans le 15e.
- Les arrondissements 8e, 4e et 16e offrent la meilleure densité de fontaines pour 1000 seniors, possiblement en raison d'un maillage plus dense d'espaces publics et de parcs.
- Les arrondissements 19e et 20e, bien que disposant de nombreuses fontaines en valeur absolue, restent dans la moyenne basse une fois rapportés au nombre élevé de seniors.

## Limites et pistes
- Le fichier Pass Paris Seniors mesure des bénéficiaires, pas l'ensemble des seniors résidents ; la couverture réelle des personnes âgées pourrait différer.
- Les fontaines temporaires ou privatisées ne sont pas couvertes par la base.
- Pour aller plus loin : intégrer des données climatiques (îlots de chaleur) ou croiser avec les établissements médico-sociaux pour prioriser les nouvelles implantations.
