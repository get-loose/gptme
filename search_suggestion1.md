from gptme.tools.base import ToolSpec

async def execute_playwright_search(query):
    # Your Playwright code from the successful test, modified to do a search
    # ...
    return search_results

playwright_search_tool = ToolSpec(
    name="playwright_search",
    desc="Search the web using Playwright",
    instructions="Use this tool to perform web searches",
    examples=["playwright_search: What is the weather in New York?"],
    execute=execute_playwright_search,
    parameters=[{"name": "query", "type": "string", "desc": "Search query"}]
)

# Register the tool
