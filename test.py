import supa
import json

from groq_client import get_groq_response
id = 834324515

# get the response from the responses table
response = supa.read_response(id)

# load the contents of example_messages.md
with open('example_messages.md', 'r') as file:
    example_messages = file.read()

user_prompt = {
    "Guideline A": """
    reference their current startup.
    """,
    "Guideline B": """
    ask if they plan to do another startup in future. Tell them that I'm an inception stage VC and that we can fund at the idea stage if they are interested. do not mention how much we invest.
    """,
    "Guideline C": """
    ask them if they ever plan to do a startup in future. Tell them that I'm an inception stage VC and that we can fund at the idea stage if they are interested. Try to reference sometihg about thier profile that would indicate that they would be successful at it. don't be too specific in what you reference. but make sure it is something they would reccognize.
    You may not write long sentences. Keep it short and concise. no em dashes.
    do not mention how much we invest.
    """,
    "examples": example_messages,
    "target": response
}


def compose_intro_message(user_prompt: object) -> str:
    system_prompt = """
    You will compose an introductory message from me to the person in the prompt.
    First you will determine if this person is currently a founder of a startup.
    If so, then use Guideline A.
    If they were a fonder in the past but are not now, use Guideline B.
    If they have never been a founder, use Guideline C
    The tone of the message is a short brief hello from me where you communicate that I am an inception stage VC and am happy to tell them more about how we support startups at the idea stage with upto $500,000 in funding.
    """
    user_prompt = f"""
    {json.dumps(user_prompt)}
    """
    return get_groq_response(system_prompt, user_prompt)

print(compose_intro_message(user_prompt))
