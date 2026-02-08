"""
Backfill li_url on responses from response.linkedin_url.
Iterates all rows in public.responses, extracts linkedin_url from the JSONB response,
and writes it to li_url.
"""

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


def main():
    url = f"{_base()}/responses"
    page_size = 500
    last_id = None
    updated = 0
    no_url = 0

    while True:
        params = {"select": "id,response", "order": "id.asc", "limit": page_size}
        if last_id is not None:
            params["id"] = f"gt.{last_id}"
        resp = requests.get(url, headers=_headers(), params=params)
        resp.raise_for_status()
        rows = resp.json()
        if not rows:
            break

        for row in rows:
            rid = row["id"]
            response = row.get("response") or {}
            li_url = response.get("linkedin_url")

            if li_url is None or li_url == "":
                no_url += 1
                continue

            patch_url = f"{_base()}/responses?id=eq.{rid}"
            patch_resp = requests.patch(
                patch_url,
                headers=_headers(),
                json={"li_url": li_url},
            )
            patch_resp.raise_for_status()
            updated += 1
            print(f"Updated id={rid} -> {li_url}")

        last_id = rows[-1]["id"]
        if len(rows) < page_size:
            break

    print(f"Done. Updated={updated}, no linkedin_url={no_url}")


if __name__ == "__main__":
    main()
