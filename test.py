import json
from core_signal import search, collect
from evaluate import evaluate
from pathlib import Path


ELIMINATED_FILE = Path(__file__).resolve().parent / "eliminated.json"

def _load_eliminated():
    if not ELIMINATED_FILE.exists():
        return set()
    with open(ELIMINATED_FILE, "r") as f:
        try:
            data = json.load(f)
            return set(data)
        except Exception:
            return set()

def _save_eliminated(eliminated_set):
    with open(ELIMINATED_FILE, "w") as f:
        json.dump(list(eliminated_set), f, indent=2)

def elinate(id):
    eliminated = _load_eliminated()
    eliminated.add(id)
    _save_eliminated(eliminated)

def check_if_eliminated(id):
    eliminated = _load_eliminated()
    return id in eliminated



# Load query from query1.json
with open("query1.json", "r") as file:
    query = json.load(file)

candidates = search(query)

print(len(candidates))
print(candidates[0:10])

for candidate in candidates:
    if check_if_eliminated(candidate):
        print(f"Skipping {candidate} because it has been eliminated")
        continue
    profile = collect(candidate)

    evaluation = evaluate(profile)
    if evaluation["total_score"] < 7:
        print(f"Eliminating {candidate} because it has a total score of {evaluation['total_score']}")
        elinate(candidate)
    else:
        print(f"Keeping {candidate} because it has a total score of {evaluation['total_score']}")
        print(evaluation)







# # Collect single employee by ID (from first search result)
# # Iterate through the search results, collect profiles, evaluate each, and print the evaluation
# for result in search_results:
#     employee_id = str(result)
#     if check_if_eliminated(employee_id):
#         print(f"Skipping {employee_id} because it has been eliminated")
#         continue
#     profile = collect(employee_id)
#     evaluation = evaluate(profile)
#     evaluation = json.loads(evaluation)
#     if evaluation["total_score"] < 7:
#         print(f"Eliminating {employee_id} because it has a total score of {evaluation['total_score']}")
#         elinate(employee_id)
#         continue

#     print(evaluation)

