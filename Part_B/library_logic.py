"""Data and storage functions for Kuromi's Little Library."""
import json
from pathlib import Path

DATA_FILE = Path(__file__).with_name("library_data.json")


def load_data():
    if DATA_FILE.exists():
        try:
            data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
            return {"books": data.get("books", []), "students": data.get("students", []), "loans": data.get("loans", [])}
        except (json.JSONDecodeError, OSError):
            pass
    return {"books": [], "students": [], "loans": []}


def save_data(data):
    DATA_FILE.write_text(json.dumps(data, indent=4), encoding="utf-8")


def next_id(records, key):
    numbers = [int(item.get(key, 0)) for item in records if str(item.get(key, "")).isdigit()]
    return str(max(numbers, default=0) + 1)
