"""
Sample: BrowserUse (local) + Groq — go to google.com and search for "The Cars".
Runs a local browser controlled by Groq; no Browser Use cloud server.

Setup:
  pip install browser-use
  uvx browser-use install   # installs Chromium (first time only)
  Set GROQ_API_KEY in .env or environment.
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

# Persistent profile: cookies and logins are reused across runs (no fresh login each time)
PROFILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "browser_profile")


async def main():
    groq_key = os.getenv("GROQ_API_KEY", "").strip().strip('"').strip("'")
    if not groq_key:
        raise SystemExit("Set GROQ_API_KEY in the environment or .env")

    llm = ChatGroq(model="meta-llama/llama-4-maverick-17b-128e-instruct")
    browser = Browser(
        user_data_dir=PROFILE_DIR,
        profile_directory="Default",
    )

    agent = Agent(
        task='Go to https://www.linkedin.com/in/kimmedgar/ and press the connect button. Then press send without note. If the connect button is not visible, then look for it under the "more" button. Then press connect and send without a note.',
        llm=llm,
        browser=browser,
    )
    await agent.run()


if __name__ == "__main__":
    asyncio.run(main())
