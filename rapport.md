# Journal de projet

## 2025-10-28
- Création du journal de projet `rapport.md` pour tracer toutes les actions.
- Définition d'un plan de travail : sélection du dataset principal, enrichissement démographique, analyse et dataviz, rédaction du livrable.
- Recherche sur opendata.paris.fr des jeux de données relatifs aux fontaines et îlots de fraîcheur (requête "fontaine").
- Validation du sujet "résilience canicule" : fontaines à boire (couverture 24/7) croisée avec population senior par arrondissement.
- Choix d'un workflow Python (Pandas + visualisations dans un notebook) avec stockage local des extractions CSV.
- Création de l'arborescence locale `data/raw` pour stocker les fichiers téléchargés.
- Récupération de la métadonnée via l'API catalogue pour `fontaines-a-boire` (vérification des champs et fréquence).
- Consultation du catalogue (requête "structure de la population") ; résultats dominés par des couches PLU, aucun jeu arrondissement+tranche d'âge pertinent identifié.
- Consultation du catalogue (requête "population par tranche d'âge") ; mêmes constats, toujours pas de données seniors exploitables.
- Nouvelle interrogation du catalogue restreinte au thème `Population` (`refine.theme=Population`) : réponse réussie mais bruit élevé, essentiellement des couches électorales ou PLU.
- Nouvelle interrogation du catalogue ciblant les mots-clés `population` et `age` (`refine.keyword=population&refine.keyword=age`) : réponse sans dataset pertinent sur les seniors par arrondissement.
- Requête catalogue `search=seniors&arrondissement` (API v2.1) : toujours 482 jeux renvoyés, majorité de couches PLU; rien sur la population 65+ par arrondissement.
- Requête catalogue `search=population%20par%20groupe%20d%27age%20arrondissement` : même réponse, bruit dominé par données d'urbanisme.
- Requête catalogue `search="65%20ans%20et%20plus"%20population&refine.theme=Statistique` : total inchangé (482), trois premiers jeux = PLU/secteurs de vote.
- Requête catalogue `search=%22population%20+%2065%20ans%20%22` : aucun affinement, toujours pas de dataset seniors.
- Requête catalogue `search=seniors&offset=200` pour explorer la pagination : résultats à partir du rang 200 sans contenu démographique exploitable.
- Requête catalogue `search=d%C3%A9mographie` : réponse encore centrée sur couches PLU/électorales, absence de structure par âge.
- Requête catalogue (API v2) `search=population&limit=50` : 15 jeux listés, majoritairement environnement/élections, aucun indicateur seniors.
- Requête catalogue (API v2) `search=senior&limit=20` : premiers jeux orientés services sociaux (Pass Paris Seniors, CASVP) plutôt que démographie brute.
- Analyse du dataset `nombre-de-beneficiaires-pass-paris-seniors-ou-access` : repéré comme proxy seniors avec champs `arrondissement`, `exercice` et `personnes_agees`.
- Téléchargement JSON du jeu `nombre-de-beneficiaires-pass-paris-seniors-ou-access` (`data/raw/nombre_de_beneficiaires_pass_paris_seniors.json`) via `Invoke-WebRequest` (100 enregistrements couvrant 2013-2017).
- Tentative de téléchargement CSV via l'API `explore/v2.1/download` pour `fontaines-a-boire` (échec NotFoundURI, documentation à vérifier).
- Téléchargement CSV du jeu `fontaines-a-boire` via l'API records v1 (`data/raw/fontaines_a_boire.csv`, 1314 lignes).
- Création du script `scripts/compute_metrics.py` pour fusionner fontaines disponibles et bénéficiaires seniors et calculer un ratio par 1000.
- Installation de la dépendance Python `pandas` dans l'environnement virtuel du projet.
- Exécution du script `compute_metrics.py` : génération de `data/processed/fountains_vs_seniors.csv` (ratio de fontaines disponibles pour 1000 bénéficiaires seniors par arrondissement).
- Ajout du script `scripts/visualize_metrics.py` pour produire une visualisation des arrondissements les mieux couverts.
- Installation de la dépendance Python `matplotlib` pour la génération des graphes.
- Exécution du script `visualize_metrics.py` : production du graphique `data/processed/fountains_per_1000_seniors.png`.
- Rédaction du livrable synthétique `rapport_final.md` (méthodologie, résultats clés, limites).
- Création du script `scripts/load_to_sqlite.py` pour charger les données brutes, les agrégations et le résultat final dans une base SQLite.
- Exécution de `load_to_sqlite.py` : génération de `data/processed/paris_fountains.sqlite` avec les tables `fountains_raw`, `seniors_raw`, `fountains_available`, `seniors_latest` et `fountains_vs_seniors`.
- Vérification rapide de la structure de la base SQLite (liste des tables) pour confirmer l'installation des jeux de données dans le SGBD choisi.
- Création du script `scripts/export_sqlserver.py` pour répliquer la base SQLite vers SQL Server via SQLAlchemy/PyODBC.
- Installation des dépendances `sqlalchemy` et `pyodbc` dans l'environnement virtuel (`pip install`).
- Configuration de l'instance locale SQL Server (`SQLEXPRESS`) : activation du protocole TCP/IP, démarrage du service SQL Server Browser et ouverture du port pour accepter la connexion.
- Ajustement du script d'export pour gérer les chaînes de connexion (prise en charge de `TrustServerCertificate`, normalisation du nom de serveur) et lever les ambigüités SQLAlchemy.
- Exécution de `export_sqlserver.py --server "LAPTOP-4G8QP3G4\SQLEXPRESS" --database "ParcFountains" --trusted --trust-server-certificate` : transfert des tables (`fountains_raw`, `seniors_raw`, `fountains_available`, `seniors_latest`, `fountains_vs_seniors`) dans SQL Server pour exploitation sous SSMS.
- Création du script `scripts/download_data.py` pour télécharger automatiquement les jeux de données depuis l'API Paris Open Data.
- Installation de la dépendance HTTP `requests`.
- Intégration de ce téléchargement automatique dans `compute_metrics.py` et `load_to_sqlite.py`, puis rerun de `compute_metrics.py` pour vérifier fin à fin.
- Historique des commandes exécutées (PowerShell) :
	1. `Invoke-WebRequest -Uri "https://parisdata.opendatasoft.com/api/explore/v2.1/catalog/datasets/nombre-de-beneficiaires-pass-paris-seniors-ou-access/records?limit=100" -OutFile "d:\entretien\data\raw\nombre_de_beneficiaires_pass_paris_seniors.json"`
	2. `Invoke-WebRequest -Uri "https://parisdata.opendatasoft.com/api/explore/v2.1/catalog/datasets/fontaines-a-boire/download?format=csv&timezone=UTC&lang=fr&limit=-1" -OutFile "d:\entretien\data\raw\fontaines_a_boire.csv"`
	3. `Invoke-WebRequest -Uri "https://opendata.paris.fr/api/records/1.0/download/?dataset=fontaines-a-boire&format=csv" -OutFile "d:\entretien\data\raw\fontaines_a_boire.csv"`
	4. `D:/entretien/.venv/Scripts/python.exe d:/entretien/scripts/compute_metrics.py`
	5. `D:/entretien/.venv/Scripts/python.exe d:/entretien/scripts/visualize_metrics.py`
	6. `D:/entretien/.venv/Scripts/python.exe -c "import pandas as pd; df=pd.read_csv('d:/entretien/data/processed/fountains_vs_seniors.csv'); print(df.head(5)); print(); print(df.tail(5))"`
	7. `D:/entretien/.venv/Scripts/python.exe d:/entretien/scripts/load_to_sqlite.py`
	8. `D:/entretien/.venv/Scripts/python.exe -c "import sqlite3; conn=sqlite3.connect('d:/entretien/data/processed/paris_fountains.sqlite'); print(conn.execute('SELECT name FROM sqlite_master WHERE type=''table''').fetchall()); conn.close()"`
	9. `D:/entretien/.venv/Scripts/pip.exe install sqlalchemy pyodbc`
	10. `Get-OdbcDriver`
	11. `sqlcmd -S LAPTOP-4G8QP3G4\SQLEXPRESS -E -Q "SELECT 1"`
	12. `D:/entretien/.venv/Scripts/python.exe d:/entretien/scripts/export_sqlserver.py --server "LAPTOP-4G8QP3G4\SQLEXPRESS" --database "ParcFountains" --trusted`
	13. `D:/entretien/.venv/Scripts/python.exe d:/entretien/scripts/export_sqlserver.py --server "LAPTOP-4G8QP3G4\SQLEXPRESS" --database "ParcFountains" --trusted --trust-server-certificate`
	14. `D:/entretien/.venv/Scripts/python.exe -c "import pyodbc; conn=pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=LAPTOP-4G8QP3G4\SQLEXPRESS;DATABASE=ParcFountains;Trusted_Connection=Yes;TrustServerCertificate=Yes'); print('connected'); conn.close()"`
	15. `D:/entretien/.venv/Scripts/pip.exe install requests`
