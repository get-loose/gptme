import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright

COOKIE_FILE = Path(__file__).parent / "google_cookies.json"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://www.google.com/search?q=OpenAI+GPT-4+context+window+size")
        print("Please interact with the page to accept cookies or login if needed.")
        print("Press Enter here when done...")
        input()
        cookies = await context.cookies()
        # Save cookies to file
        with COOKIE_FILE.open("w") as f:
            json.dump(cookies, f, indent=2)
        print(f"Cookies saved to {COOKIE_FILE}")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
