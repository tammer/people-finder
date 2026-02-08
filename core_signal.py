import os

import requests
from my_dotenv import load_dotenv

from supa import read_response, write_response

load_dotenv()


def collect(id: int) -> dict:
    """
    Return the profile for the given id from Supabase if present, otherwise fetch via raw_collect.
    """
    cached = read_response(id)
    if cached is not None:
        return cached
    profile = raw_collect(id)
    write_response(id, profile)
    return profile


def raw_collect(id: int) -> dict:
    """
    Collect the profile of a person by their  ID.
    """
    print("Warning: Calling Core Signal API to collect profile for id:", id)
    url = f"https://api.coresignal.com/cdapi/v2/employee_clean/collect/{id}"
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

def filter(query: dict) -> list[int]:
    """
    Search for employees using Coresignal's filter endpoint.
    Pass a dict of filter fields (e.g. full_name, headline, location, keyword,
    experience_company_name, skill, ...). Returns a list of employee IDs.
    See: https://docs.coresignal.com/employee-api/base-employee-api/endpoints/search-filters
    """
    url = "https://api.coresignal.com/cdapi/v2/employee_base/search/filter"
    headers = {
        "apikey": os.environ["CORESIGNAL_API_KEY"],
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    response = requests.post(url, headers=headers, json=query)
    response.raise_for_status()
    data = response.json()
    if isinstance(data, list):
        return [int(i) for i in data]
    if isinstance(data, dict) and "ids" in data:
        return [int(i) for i in data["ids"]]
    return [int(i) for i in data]
