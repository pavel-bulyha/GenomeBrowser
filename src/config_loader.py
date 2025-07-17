import json
import os

def load_config(path="config.json"):
    """
    Читает JSON-конфиг и возвращает словарь с настройками.
    """
    here = os.path.dirname(__file__)
    full = os.path.join(here, path)
    with open(full, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    return cfg
