from supa import get_highest_scored_response_without_invite, get_score, set_invite_sent
from linkedin_connect import connect_to
import json

response = get_highest_scored_response_without_invite()
if response is None:
    print("THere are no more responses to process")
    exit(1)

response = response.get("response")

url = response.get("linkedin_url") or response.get("websites_linkedin")

print(f"Connecting to {url}")

result = connect_to(url)

if result:
    set_invite_sent(response['id'])
    print("Invite sent")
else:
    print("Failed to connect to LinkedIn")
    exit(1)