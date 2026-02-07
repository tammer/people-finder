from groq import get_groq_response
import json
from pathlib import Path

SYSTEM_PROMPT_FILE = Path(__file__).resolve().parent / "system_prompt.md"

with open(SYSTEM_PROMPT_FILE, "r") as f:
    SYSTEM_PROMPT = f.read()

def evaluate(profile: object) -> str:
    """
    Evaluate the profile and return the evaluation.
    """
    response =  get_groq_response(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=json.dumps(profile)
    )
    return json.loads(response)