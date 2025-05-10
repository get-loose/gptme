import asyncio
from playwright.async_api import async_playwright


async def run():
    # Connect to the remote Playwright server
    playwright = await async_playwright().start()
    try:
        browser = await playwright.chromium.connect_over_cdp("ws://127.0.0.1:3432/")
        page = await browser.new_page()
        await page.goto("https://example.com")
        title = await page.title()
        print(f"Page title: {title}")
        await browser.close()
    finally:
        await playwright.stop()


if __name__ == "__main__":
    asyncio.run(run())
