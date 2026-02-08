import supa
import json

id = 3313308

# get the response from the responses table
response = supa.read_response(id)

print(json.dumps(response, indent=4))