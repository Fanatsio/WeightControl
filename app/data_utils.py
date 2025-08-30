import csv
import os
from datetime import datetime

FILENAME = "./data/weights.csv"

def load_data():
    if not os.path.exists(FILENAME):
        return [], []
    with open(FILENAME, "r", encoding="utf-8", newline="") as f:
        reader = list(csv.reader(f))
        if not reader:
            return [], []
        header = reader[0]
        rows = reader[1:]
        return header, rows

def save_data(header, rows):
    try:
        rows.sort(key=lambda r: datetime.strptime(r[0], "%Y-%m-%d"))
    except Exception:
        pass
    with open(FILENAME, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)