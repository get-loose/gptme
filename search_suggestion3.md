from gptme.tools.base import ToolSpec
import openai

async def execute_openrouter_search(query):
    client = openai.OpenAI(
        api_key="your-openrouter-api-key",
        base_url="https://openrouter.ai/api/v1"
    )

    # Use the simple ":online" suffix to enable web search
    response = client.chat.completions.create(
        model="openai/gpt-4o:online",  # Just add ":online" to any model
        messages=[
            {"role": "user", "content": query}
        ]
    )

    return response.choices[0].message.content

openrouter_search_tool = ToolSpec(
    name="web_search",
    desc="Search the web for the latest information",
    instructions="Use this tool to search for up-to-date information on the web",
    examples=["web_search: What happened in the world today?"],
    execute=execute_openrouter_search,
    parameters=[{"name": "query", "type": "string", "desc": "Search query"}]
)
