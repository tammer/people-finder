# get all unscored responses
# score them
# write the scores to the scores table

from supa import get_unscored_responses, write_score
from evaluate import evaluate

responses = get_unscored_responses()
print(f"Found {len(responses)} unscored responses")
for response in responses:
    print(f"Scoring {response['id']}")
    score = evaluate(response['response'])
    write_score(response['id'], score)
    print(f"Scored {response['id']} with score {score['total_score']}")