"""
Use browser-use to send a LinkedIn connection request to a profile URL.
Returns True if the flow succeeds, False otherwise.
"""
import asyncio
import os

try:
    from my_dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from browser_use import Agent, Browser
from browser_use.llm import ChatGroq

PROFILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "browser_profile")


async def _connect_async(who: str) -> bool:
    groq_key = os.getenv("GROQ_API_KEY", "").strip().strip('"').strip("'")
    if not groq_key:
        raise RuntimeError("Set GROQ_API_KEY in the environment or .env")

    llm = ChatGroq(model="meta-llama/llama-4-maverick-17b-128e-instruct")
    browser = Browser(
        user_data_dir=PROFILE_DIR,
        profile_directory="Default",
    )
    task = (
        f'Go to {who} and press the connect button. Then press send without note. '
        'If the connect button is not visible, then look for it under the "more" button. '
        "Then press connect and send without a note."
        "VERIFICATION: Look for the text 'Pending' or 'Invitation sent' on the profile."
        "If you see that text, the task is a SUCCESS, even if the buttons disappear."
    )
    agent = Agent(task=task, llm=llm, browser=browser)
    history = await agent.run()
    return history.is_successful()


def connect_to(who: str) -> bool:
    """
    Send a LinkedIn connection request to the profile at the given URL.

    :param who: LinkedIn profile URL (e.g. https://www.linkedin.com/in/username/)
    :return: True if the connection request was sent successfully, False otherwise.
    """
    return asyncio.run(_connect_async(who))
