Based on the information you've provided, you have several options for implementing web search in gptme, with some being significantly easier than others. Let me outline your options from easiest to most complex:

## 1. Easiest: Use OpenRouter with the `:online` suffix (Recommended)

This is by far the simplest approach:

```python
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
```

This approach:
- Requires only OpenRouter API key
- Is a one-line change to your model name (just add `:online`)
- Costs ~$0.02 per search (based on OpenRouter's pricing)
- Works with any model on OpenRouter
- Provides standardized citation formatting

## 2. Easy: Use OpenAI's Web Search Tool

If you prefer using OpenAI directly:

```python
from gptme.tools.base import ToolSpec
from openai import OpenAI

async def execute_openai_search(query):
    client = OpenAI()  # Uses OPENAI_API_KEY from environment

    response = client.responses.create(
        model="gpt-4.1",  # Requires gpt-4.1 or similar with search support
        tools=[{"type": "web_search_preview"}],
        input=query
    )

    return response.output_text

openai_search_tool = ToolSpec(
    name="web_search",
    desc="Search the web for the latest information",
    instructions="Use this tool to search for up-to-date information on the web",
    examples=["web_search: What happened in the world today?"],
    execute=execute_openai_search,
    parameters=[{"name": "query", "type": "string", "desc": "Search query"}]
)
```

This approach:
- Uses OpenAI's native search capability
- Works with gpt-4.1 and similar models
- Has tiered pricing based on search context size

## 3. Moderately Easy: Use Perplexity API

The script you shared has a functioning Perplexity API implementation:

```python
from gptme.tools.base import ToolSpec
from openai import OpenAI

async def execute_perplexity_search(query, mode="concise"):
    client = OpenAI(
        api_key="your-perplexity-api-key",  # From PERPLEXITY_API_KEY
        base_url="https://api.perplexity.ai"
    )

    response = client.chat.completions.create(
        model="llama-3.1-sonar-large-128k-online",
        messages=[
            {
                "role": "system",
                "content": "You are an artificial intelligence assistant and you need to engage in a helpful, detailed, polite conversation with a user."
            },
            {
                "role": "user",
                "content": query
            }
        ]
    )

    return response.choices[0].message.content

perplexity_search_tool = ToolSpec(
    name="perplexity_search",
    desc="Search the web using Perplexity AI",
    instructions="Use this tool to search for up-to-date information",
    examples=["perplexity_search: What are the latest developments in AI?"],
    execute=execute_perplexity_search,
    parameters=[
        {"name": "query", "type": "string", "desc": "Search query"},
        {"name": "mode", "type": "string", "desc": "Search mode (concise or copilot)", "default": "concise"}
    ]
)
```

This approach:
- Leverages Perplexity's specialized search capabilities
- Requires a Perplexity API key
- Has competitive pricing

## Recommendation

I recommend the **OpenRouter with `:online`** approach (Option 1) because:

1. It's by far the simplest implementation
2. It works with any model on their platform
3. The pricing is transparent (~$0.02 per search)
4. You mentioned you already have an OpenRouter API key
5. It provides standardized citation formatting

To implement this in gptme, you would:

1. Create the custom tool as shown in Option 1
2. Register it with gptme using `register_tool(openrouter_search_tool)`
3. Configure your OpenRouter API key in the environment or gptme config

This would give you a replacement for the currently broken search in gptme with minimal effort and high reliability.
