import supa
import json
import sys

# get the id from the command line
id = int(sys.argv[1])

# get the response from the responses table
response = supa.read_response(id)


print(json.dumps(response, indent=4))