# Lightweight lazy loader for heavy solver data
import json
import os

_data = None

def get_hand_tables():
    """
    Return precomputed hand tables. Prefer a JSON data file if present.
    If not present, raise a clear error so you can generate or wire in the
    existing heavy data source.
    """
    global _data
    if _data is not None:
        return _data

    data_path = os.path.join(os.path.dirname(__file__), "hand_tables.json")
    if os.path.exists(data_path):
        with open(data_path, "r") as f:
            _data = json.load(f)
        return _data

    raise RuntimeError("No hand_tables.json found. Generate it or wire heavy data into _heavy_loader.get_hand_tables().")
