from groq_client import get_groq_response
import json
from pathlib import Path

SYSTEM_PROMPT_FILE = Path(__file__).resolve().parent / "system_prompt.md"

with open(SYSTEM_PROMPT_FILE, "r") as f:
    SYSTEM_PROMPT = f.read()


def check_for_problems(profile: object) -> dict:
    if profile.get("location_country") != "Canada":
        return {
            "problem": "Not in Canada",
            "id": profile.get("id"),
            "total_score": 0,
            "max_score": 11,
        }
    return None

def evaluate(profile: object) -> dict:
    """
    Evaluate the profile and return the evaluation.
    """

    problems = check_for_problems(profile)

    if problems is None:
        response =  get_groq_response(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=json.dumps(profile)
        )
        return json.loads(response)
    
    return problems