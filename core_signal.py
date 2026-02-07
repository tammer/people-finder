import os

import requests
from dotenv import load_dotenv

from supa import read_response

load_dotenv()


def collect(id: int) -> dict:
    """
    Return the profile for the given id from Supabase if present, otherwise fetch via raw_collect.
    """
    cached = read_response(id)
    if cached is not None:
        return cached
    return raw_collect(id)


def raw_collect(id: int) -> dict:
    """
    Collect the profile of a person by their  ID.
    """
    url = f"https://api.coresignal.com/cdapi/v2/employee_multi_source/collect/{id}"
    headers = {
        "apikey": os.getenv("CORESIGNAL_API_KEY"),
        "Accept": "application/json",
    }
    response = requests.get(url, headers=headers)
    return response.json()


def search(query: dict) -> list:
    """
    Search for employees using an Elasticsearch DSL query.
    """
    url = "https://api.coresignal.com/cdapi/v2/employee_multi_source/search/es_dsl"
    headers = {
        "apikey": os.environ["CORESIGNAL_API_KEY"],
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    response = requests.post(url, headers=headers, json=query)
    response = response.json()
    ids = []
    for i in response:
        ids.append(int(i))
    return ids

