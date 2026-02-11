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
    f"1. INITIAL CHECK: If {who}'s profile already displays 'Pending' or 'Invitation sent', "
    "stop and return SUCCESS.\n"
    "2. FIND CONNECT: Locate the 'Connect' button. If it is not visible, click 'More' to find it. "
    "Click 'Connect'.\n"
    "3. SECURITY CHECK: If prompted to enter an email to 'verify this member knows you', "
    "stop and return FAIL.\n"
    "4. SENDING: If a 'Send without note' button is visible, click it. "
    "If 'Send without note' is NOT visible, stop and return FAIL.\n"
    "5. VERIFICATION: After clicking, confirm the profile now displays 'Pending' or 'Invitation sent'. "
    "If confirmed, return SUCCESS."
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
