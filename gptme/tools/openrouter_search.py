"""
Tool to search the web using OpenRouter's :online suffix functionality.
This provides realtime web search results through any LLM.

Installation:
  1. Set up an OpenRouter API key at https://openrouter.ai
  2. Add the key to your environment as OPENROUTER_API_KEY
  3. Or add it to ~/.config/gptme/config.toml under [env] section
"""

import os
import logging
import openai
from pathlib import Path
import tomllib

from ..util import console
from .base import ToolSpec

logger = logging.getLogger(__name__)


def get_openrouter_api_key() -> str | None:
    """Get API key from environment or config file"""
    # Try environment variable first
    if api_key := os.getenv("OPENROUTER_API_KEY"):
        return api_key

    # Try config file
    config_path = Path.home() / ".config" / "gptme" / "config.toml"
    if config_path.exists():
        with open(config_path, "rb") as f:
            config = tomllib.load(f)
            if api_key := config.get("env", {}).get("OPENROUTER_API_KEY"):
                return api_key

    return None


def has_openrouter_key() -> bool:
    """Check if OpenRouter API key is available"""
    key = get_openrouter_api_key()
    if key:
        console.log("OpenRouter search tool available")
        return True
    console.log("OpenRouter search tool not available (API key not found)")
    return False


# Make sure this function is defined at module level and properly exported
async def openrouter_search(query: str) -> str:
    """Search the web using OpenRouter's :online suffix functionality."""
    api_key = get_openrouter_api_key()
    if not api_key:
        return "Error: OpenRouter API key not found. Please set OPENROUTER_API_KEY environment variable."

    try:
        # Create the OpenAI AsyncClient with OpenRouter base URL
        client = openai.AsyncOpenAI(
            api_key=api_key, base_url="https://openrouter.ai/api/v1"
        )

        # Perform the search using a model with :online suffix
        response = await client.chat.completions.create(
            model="openai/gpt-4.1-mini:online",  # Use :online suffix for web search
            messages=[{"role": "user", "content": query}],
        )

        # Return the response content
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error in OpenRouter search: {e}")
        return f"Error performing search: {str(e)}"


# Create the tool
tool = ToolSpec(
    name="openrouter_search",
    desc="Search the web using OpenRouter's real-time search",
    functions=[openrouter_search],
    available=has_openrouter_key(),
)

# Make sure to expose the function at module level
__all__ = ["openrouter_search", "tool"]

__doc__ = tool.get_doc(__doc__)
