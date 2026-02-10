from supa import get_first_scored_response_without_invite, get_score, write_score
from evaluate import evaluate

response = get_first_scored_response_without_invite()
print(response['id'])

score = get_score(response['id'])
if score is None:
    score = evaluate(response['response'])
    write_score(response['id'], score)

print(score)