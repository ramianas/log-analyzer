from pymongo import MongoClient
import re
from datetime import datetime

# Connexion à MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["logs_db"]
logs = db["logs"]

# Expression régulière pour parser le format Apache
pattern = re.compile(
    r'(?P<ip>\S+) - - \[(?P<time>[^\]]+)\] "(?P<method>\S+) (?P<url>\S+) \S+" (?P<status>\d{3}) (?P<size>\S+)'
)

with open("data/access.log") as f:
    for line in f:
        m = pattern.match(line)
        if not m:
            continue
        d = m.groupdict()
        d["timestamp"] = datetime.strptime(d["time"], "%d/%b/%Y:%H:%M:%S %z")
        d["status"] = int(d["status"])
        d["size"] = 0 if d["size"] == '-' else int(d["size"])
        logs.insert_one(d)

print("✅ Logs Apache insérés dans MongoDB")
