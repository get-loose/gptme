from gptme.tools.base import ToolSpec
import asyncio
from playwright.async_api import async_playwright

async def execute_playwright_search(query, engine="google", num_results=5):
    """Perform a web search using Playwright and a search engine."""
    async with async_playwright() as playwright:
        browser = await playwright.chromium.connect(ws_endpoint="ws://127.0.0.1:3432/")
        try:
            page = await browser.new_page()

            # Different implementation based on search engine
            if engine.lower() == "google":
                # Navigate to Google
                await page.goto("https://www.google.com/")

                # Accept cookies if necessary (may vary by location)
                try:
                    await page.click('button:has-text("Accept all")', timeout=3000)
                except:
                    pass  # No cookie banner

                # Perform search
                await page.fill('input[name="q"]', query)
                await page.press('input[name="q"]', "Enter")
                await page.wait_for_load_state("networkidle")

                # Extract search results
                results = []
                elements = await page.query_selector_all("div.g")

                for i, element in enumerate(elements):
                    if i >= num_results:
                        break

                    # Get title, link and snippet
                    title_el = await element.query_selector("h3")
                    link_el = await element.query_selector("a")
                    snippet_el = await element.query_selector("div.VwiC3b")

                    if not title_el or not link_el:
                        continue

                    title = await title_el.inner_text() if title_el else "No title"
                    link = await link_el.get_attribute("href") if link_el else "No link"
                    snippet = await snippet_el.inner_text() if snippet_el else "No snippet"

                    results.append({"title": title, "link": link, "snippet": snippet})

            elif engine.lower() == "duckduckgo":
                # Navigate to DuckDuckGo
                await page.goto("https://duckduckgo.com/")

                # Perform search
                await page.fill('input[name="q"]', query)
                await page.press('input[name="q"]', "Enter")
                await page.wait_for_load_state("networkidle")

                # Extract search results
                results = []
                elements = await page.query_selector_all("article.result")

                for i, element in enumerate(elements):
                    if i >= num_results:
                        break

                    title_el = await element.query_selector("h2")
                    link_el = await element.query_selector("a.result__url")
                    snippet_el = await element.query_selector("div.result__snippet")

                    title = await title_el.inner_text() if title_el else "No title"
                    link = await link_el.get_attribute("href") if link_el else "No link"
                    snippet = await snippet_el.inner_text() if snippet_el else "No snippet"

                    results.append({"title": title, "link": link, "snippet": snippet})

            else:
                return {"error": f"Search engine {engine} not supported"}

            return {
                "engine": engine,
                "query": query,
                "results": results
            }

        finally:
            await browser.close()

# Create the tool specification
playwright_search_tool = ToolSpec(
    name="web_search",
    desc="Search the web using Google or DuckDuckGo",
    instructions="Use this tool to search for information on the web",
    examples=[
        "web_search: latest news about AI",
        "web_search: Python asyncio tutorial engine=google num_results=3"
    ],
    execute=execute_playwright_search,
    parameters=[
        {"name": "query", "type": "string", "desc": "Search query"},
        {"name": "engine", "type": "string", "desc": "Search engine (google or duckduckgo)", "default": "google"},
        {"name": "num_results", "type": "integer", "desc": "Number of results to return", "default": 5}
    ]
)

# To register this tool with gptme:
# from gptme.tools import register_tool
# register_tool(playwright_search_tool)
