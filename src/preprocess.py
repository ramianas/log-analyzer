import pandas as pd
from pymongo import MongoClient

def load_data():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["logs_db"]
    df = pd.DataFrame(list(db.logs.find()))
    df["hour"] = df["timestamp"].dt.hour
    df["is_error"] = (df["status"] >= 400).astype(int)
    return df

def build_features(df):
    features = df[["status", "hour", "size", "is_error"]]
    features = features.fillna(0)
    return df, features
