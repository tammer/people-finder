import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

CACHE_FILE = Path(__file__).resolve().parent / "cache.json"


def _load_cache() -> dict:
    if not CACHE_FILE.exists():
        return {}
    with open(CACHE_FILE, "r") as f:
        return json.load(f)


def _save_cache(cache: dict) -> None:
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)


def collect(employee_id: str) -> dict:
    """
    Collect the profile of a person by their employee ID.
    Uses cache.json to avoid repeated API calls for the same employee_id.
    """
    cache = _load_cache()
    if employee_id in cache:
        return cache[employee_id]

    print(f"Collecting profile for employee {employee_id}...")
    url = f"https://api.coresignal.com/cdapi/v2/employee_multi_source/collect/{employee_id}"
    headers = {
        "apikey": os.getenv("CORESIGNAL_API_KEY"),
        "Accept": "application/json",
    }
    response = requests.get(url, headers=headers)
    data = response.json()

    cache[employee_id] = data
    _save_cache(cache)
    return data