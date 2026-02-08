"""
Test script: calls connect_to() to send a LinkedIn connection request.
Uses browser-use + Groq under the hood (see linkedin_connect.py).

Setup:
  pip install browser-use
  uvx browser-use install   # installs Chromium (first time only)
  Set GROQ_API_KEY in .env or environment.
"""
from linkedin_connect import connect_to

if __name__ == "__main__":
    url = "https://www.linkedin.com/in/tanikamcleod/"
    ok = connect_to(url)
    print("Success" if ok else "Failed")
