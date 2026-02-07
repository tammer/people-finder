# -- WARNING: This schema is for context only and is not meant to be run.
# -- Table order and constraints may not be valid for execution.

# CREATE TABLE public.responses (
#   id bigint NOT NULL,
#   response jsonb NOT NULL,
#   created_at timestamp with time zone DEFAULT now(),
#   CONSTRAINT responses_pkey PRIMARY KEY (id)
# );

import os

import dotenv
import requests

dotenv.load_dotenv()

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
