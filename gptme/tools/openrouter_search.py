import asyncio
from . import _openrouter_search_werkend_inactive  # Import the renamed module


async def main():
    search_result = await _openrouter_search_werkend_inactive.openrouter_search(
        "melisearch"
    )
    print(search_result)


if __name__ == "__main__":
    asyncio.run(main())
