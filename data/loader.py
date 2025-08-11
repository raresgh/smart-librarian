import json
from config import SUMMARY_FILE

def load_summaries(path=SUMMARY_FILE):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)