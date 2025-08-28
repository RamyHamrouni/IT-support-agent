# app/utils/config_loader.py
import yaml
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def load_yaml(file_name: str):
    path = BASE_DIR / "config" / file_name
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)