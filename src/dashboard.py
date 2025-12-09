import streamlit as st
import pandas as pd
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["logs_db"]
df = pd.DataFrame(list(db.results.find()))

st.title("📊 Analyse intelligente des logs serveurs Apache")

col1, col2, col3 = st.columns(3)
col1.metric("Total logs", len(df))
col2.metric("Anomalies", len(df[df["anomaly"] == -1]))
col3.metric("Clusters", df["cluster"].nunique())

st.subheader("📈 Répartition des clusters")
st.bar_chart(df["cluster"].value_counts())

st.subheader("🚨 Logs anormaux")
st.dataframe(df[df["anomaly"] == -1][["timestamp", "ip", "url", "status", "cluster", "anomaly_score"]])

st.subheader("🕒 Volume par heure")
st.bar_chart(df.groupby("hour")["status"].count())
