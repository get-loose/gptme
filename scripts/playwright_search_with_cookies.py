import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright

COOKIE_FILE = Path(__file__).parent / "google_cookies.json"

async def search_with_cookies(query: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()

        # Load cookies if available
        if COOKIE_FILE.exists():
            cookies = json.loads(COOKIE_FILE.read_text())
            await context.add_cookies(cookies)
            print(f"Loaded {len(cookies)} cookies from {COOKIE_FILE}")

        page = await context.new_page()
        search_url = f"https://www.google.com/search?q={query}"
        await page.goto(search_url)
        await page.wait_for_load_state("networkidle")

        content = await page.content()
        await browser.close()
        return content

if __name__ == "__main__":
    query = "OpenAI GPT-4.1-mini context window size"
    html = asyncio.run(search_with_cookies(query))
    print(html[:2000])  # print first 2000 chars of the page content
