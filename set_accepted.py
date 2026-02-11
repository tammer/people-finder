# get linkedin url from the command line
import sys
from supa import read_response_by_li_url, set_invite_accepted
linkedin_url = sys.argv[1]

# strip trailing slash
linkedin_url = linkedin_url.rstrip('/')

# find the response id for the linkedin url
response = read_response_by_li_url(linkedin_url)
if response is None:
    print(f"No response found for LinkedIn URL: {linkedin_url}")
    exit(1)

id = response['id']
print(f"Setting invite accepted for response {id}")

print(set_invite_accepted(id))