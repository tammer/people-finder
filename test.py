import json
from core_signal import search, collect, filter
from evaluate import evaluate
from pathlib import Path
from supa import write_score, get_score




# Load query from query1.json
with open("filter_queries/query1.json", "r") as file:
    query = json.load(file)

candidates = filter(query)

# print(len(candidates))
# print(candidates[0:10])
# exit()

for candidate in candidates[10:50]:
    profile = collect(candidate)
    if get_score(candidate):
        print(f"Skipping {candidate} because it has already been scored")
        continue
    evaluation = evaluate(profile)
    write_score(candidate, evaluation)

