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


async def main():
    groq_key = os.getenv("GROQ_API_KEY", "").strip().strip('"').strip("'")
    if not groq_key:
        raise SystemExit("Set GROQ_API_KEY in the environment or .env")

    llm = ChatGroq(model="meta-llama/llama-4-maverick-17b-128e-instruct")
    browser = Browser()  # local browser, no cloud

    agent = Agent(
        task='Go to https://google.com and search for "The Cars".',
        llm=llm,
        browser=browser,
    )
    await agent.run()


if __name__ == "__main__":
    asyncio.run(main())
