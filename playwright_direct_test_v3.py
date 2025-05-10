import asyncio
from playwright.async_api import async_playwright


async def run():
    # Connect to the remote Playwright server using the Playwright WebSocket endpoint
    async with async_playwright() as playwright:
        # Connect to the browser through one of the browser types
        browser = await playwright.chromium.connect(ws_endpoint="ws://127.0.0.1:3432/")

        # Now proceed with your automation
        page = await browser.new_page()
        await page.goto("https://example.com")
        title = await page.title()
        print(f"Page title: {title}")

        # Close the browser when done
        await browser.close()


if __name__ == "__main__":
    asyncio.run(run())
