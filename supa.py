# -- WARNING: This schema is for context only and is not meant to be run.
# -- Table order and constraints may not be valid for execution.

# CREATE TABLE public.responses (
#   id bigint NOT NULL,
#   response jsonb NOT NULL,
#   created_at timestamp with time zone DEFAULT now(),
#   CONSTRAINT responses_pkey PRIMARY KEY (id)
# );

import os

import my_dotenv
import requests

my_dotenv.load_dotenv()

_BASE = None


def _base():
    global _BASE
    if _BASE is None:
        url = os.getenv("SUPABASE_URL", "").rstrip("/")
        _BASE = f"{url}/rest/v1"
    return _BASE


def _headers():
    return {
        "apikey": os.getenv("SUPABASE_KEY", ""),
        "Authorization": f"Bearer {os.getenv('SUPABASE_KEY', '')}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Prefer": "return=minimal",
    }


def write_response(id: int, response: object):
    """Insert or replace a response row by id (Supabase REST upsert)."""
    url = f"{_base()}/responses"
    headers = dict(_headers())
    headers["Prefer"] = "resolution=merge-duplicates"
    resp = requests.post(
        url,
        headers=headers,
        json={"id": id, "response": response},
    )
    resp.raise_for_status()


def read_response(id: int) -> object:
    """Return the response json for the given id, or None if not found."""
    url = f"{_base()}/responses"
    params = {"id": f"eq.{id}", "select": "response"}
    resp = requests.get(
        url,
        headers=_headers(),
        params=params,
    )
    resp.raise_for_status()
    data = resp.json()
    if data and len(data) > 0:
        return data[0]["response"]
    return None

def write_score(id: int, response: object, model_id: int = 0):
    """Insert or replace a score row by (id, model_id). Score is normalized to 0-100."""
    score_val = response["total_score"]
    max_score = response["max_score"]
    normalized_score = (score_val / max_score) * 100
    url = f"{_base()}/scores"
    headers = dict(_headers())
    headers["Prefer"] = "resolution=merge-duplicates"
    resp = requests.post(
        url,
        headers=headers,
        json={
            "id": id,
            "model_id": model_id,
            "score": normalized_score,
            "analysis": response,
        },
    )
    resp.raise_for_status()

def get_score(id: int, model_id: int = 0) -> object | None:
    """Return the score row for the given (id, model_id), or None if not found."""
    url = f"{_base()}/scores"
    params = {
        "id": f"eq.{id}",
        "model_id": f"eq.{model_id}",
        "select": "score,analysis,created_at",
    }
    resp = requests.get(
        url,
        headers=_headers(),
        params=params,
    )
    resp.raise_for_status()
    data = resp.json()
    if data and len(data) > 0:
        return data[0]
    return None
