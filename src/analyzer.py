from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest
from preprocess import load_data, build_features
from pymongo import MongoClient

df = load_data()
df, X = build_features(df)

# Clustering KMeans
kmeans = KMeans(n_clusters=3, random_state=42)
df["cluster"] = kmeans.fit_predict(X)

# Détection d’anomalies Isolation Forest
isf = IsolationForest(contamination=0.03, random_state=42)
df["anomaly"] = isf.fit_predict(X)
df["anomaly_score"] = isf.decision_function(X)

# Sauvegarde dans MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["logs_db"]
db.results.delete_many({})
db.results.insert_many(df.to_dict("records"))

print("✅ Clustering + Anomalies enregistrés dans MongoDB")
