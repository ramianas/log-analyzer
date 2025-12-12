# 🔎 Log Analyzer – Analyse intelligente des logs Apache avec Machine Learning

Ce projet analyse automatiquement les logs Apache afin de détecter des comportements suspects, des erreurs et des anomalies grâce à des algorithmes de **Machine Learning non supervisé** (KMeans + Isolation Forest).  
Il inclut un pipeline complet : collecte → preprocessing → analyse IA → visualisation dans un tableau de bord.

---

## 🚀 Fonctionnalités

- 📥 Collecte automatique des logs Apache (`access_log`)
- 🗄 Stockage structuré dans **MongoDB** (Docker)
- 🧹 Préprocessing et extraction de features
- 🤖 Détection d’anomalies (Isolation Forest)
- 🔎 Clustering de comportements (KMeans)
- 📊 Dashboard interactif avec **Streamlit**
- ✔ Architecture claire, modulaire et extensible

---

## 🧩 Architecture du projet

log-analyzer/
│
├── data/
│ └── access.log # Logs Apache bruts
│
├── src/
│ ├── collector.py # Extraction & insertion dans MongoDB
│ ├── preprocess.py # Mise en forme & ajout de features
│ ├── analyzer.py # Analyse IA : clustering + anomalies
│ └── dashboard.py # Tableau de bord Streamlit
│
├── docker-compose.yml # Service MongoDB
├── requirements.txt # Dépendances Python
└── README.md # Documentation


---

## 🧠 Pipeline d’analyse (explication claire)

### 1️⃣ **Collector – extraction des logs**
`collector.py` lit le fichier systeme :

/var/log/apache2/access_log


Il parse chaque ligne (IP, timestamp, URL, code HTTP, taille) et l’insère dans MongoDB.

---

### 2️⃣ **Preprocess – transformation des données**
`preprocess.py` :

- convertit le timestamp en format datetime
- extrait l’heure (`hour`)
- ajoute un flag erreur (`is_error = 1 si status >= 400`)
- renvoie un DataFrame propre pour le ML

---

### 3️⃣ **Analyzer – Machine Learning**
`analyzer.py` applique deux modèles non supervisés :

#### 🔹 **KMeans (clustering)**
→ regroupe les comportements similaires du serveur  
(ex : cluster de 200, cluster de 404, cluster de pages sensibles…)

#### 🔹 **Isolation Forest (anomalies)**
→ détecte les requêtes rares ou atypiques

Résultat ajouté pour chaque log :

- `cluster`
- `anomaly` (1 = normal, -1 = anomalie)
- `anomaly_score` (plus négatif = plus suspect)

Les résultats sont sauvegardés dans la collection :

logs_db.results


---

### 4️⃣ **Dashboard – visualisation**
`dashboard.py` affiche :

- nombre total de logs
- nombre d’erreurs
- anomalies détectées
- graphiques d’activité
- table complète filtrable

Accessible via :

👉 http://localhost:8501

---

## 🛠 Installation

### 1. Cloner le projet

git clone https://github.com/<username>/log-analyzer.git
cd log-analyzer
2. Activer un environnement virtuel
bash
Copier le code
python3 -m venv .venv
source .venv/bin/activate
3. Installer les dépendances Python
bash
Copier le code
pip install -r requirements.txt
4. Lancer MongoDB avec Docker
bash
Copier le code
docker-compose up -d
▶️ Exécution du pipeline complet
✔ 1. Collecter les logs Apache
bash
Copier le code
python src/collector.py
✔ 2. Lancer le modèle IA

python src/analyzer.py
✔ 3. Lancer le dashboard
streamlit run src/dashboard.py
Dashboard → http://localhost:8501

📌 Exemples d’anomalies détectées
Accès répétés à /admin ou /login

Burst de requêtes en quelques millisecondes

Séries anormales de 404

Trafic inhabituel à des heures rares

Pages inexistantes (scan d’attaque)

📦 Technologies utilisées
Python 3

MongoDB (Docker)

Pandas

scikit-learn

Streamlit

Regex / parsing logs Apache
