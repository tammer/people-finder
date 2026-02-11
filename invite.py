from supa import get_highest_scored_response_without_invite, get_score, set_invite_sent
from linkedin_connect import connect_to
import json

response = get_highest_scored_response_without_invite()
if response is None:
    print("THere are no more responses to process")
    exit(1)

response = response.get("response")

print("ID", response.get("id"))
score = get_score(response.get("id")).get("score")
print("score", round(score))

location_country = response.get("location_country")

if location_country is None:
    print("No location country found")
    exit(1)

if location_country != "Canada":
    print("Not in Canada")
    exit(1)

url = response.get("linkedin_url") or response.get("websites_linkedin")

print(f"Connecting to {url}")

result = connect_to(url)

if result:
    set_invite_sent(response['id'])
    print("Invite sent")
else:
    print("Failed to connect to LinkedIn")
    exit(1)