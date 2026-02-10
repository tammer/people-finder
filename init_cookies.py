"""
Open LinkedIn login page for manual cookie initialization.
Uses the same browser profile as linkedin_connect.py, so cookies saved here
will be used by the connection flow.
"""
import asyncio
import os

from browser_use import Browser

PROFILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "browser_profile")


async def main():
    browser = Browser(
        user_data_dir=PROFILE_DIR,
        profile_directory="Default",
        headless=False,
    )
    await browser.start()
    await browser.new_tab("https://www.linkedin.com/login")

    print()
    print("=" * 60)
    print("LinkedIn login page is open and ready.")
    print()
    print("Please log in manually in the browser window.")
    print("Complete any 2FA steps if prompted.")
    print()
    input("Press Enter after you've finished logging in to save cookies and close...")
    print()

    await browser.stop()
    print("Cookies saved. linkedin_connect will use this session.")


if __name__ == "__main__":
    asyncio.run(main())
