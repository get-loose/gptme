# Adding OpenRouter Search Tool to gptme

## Overview

This document describes the approach taken to integrate the OpenRouter web search tool into the gptme project.

## Approach

1. **Tool Definition:**
   - Created a new tool module `gptme/tools/openrouter_search.py`.
   - Defined the `openrouter_search_tool` using the `ToolSpec` dataclass.
   - The tool uses the OpenRouter API with the `openai/gpt-4o:online` model to perform web searches.
   - The API key is expected to be provided via the environment variable `OPENROUTER_API_KEY`.

2. **Tool Discovery and Registration:**
   - gptme dynamically discovers tools by importing modules listed in the `TOOL_MODULES` environment variable or configuration.
   - To include the new tool, the module `gptme.tools.openrouter_search` must be added to the `TOOL_MODULES` list.
   - This allows the tool to be loaded and available without modifying core code imports.

3. **Configuration Update:**
   - The environment variable or configuration file should be updated to include `gptme.tools.openrouter_search` in the list of tool modules.
   - This ensures the tool is discovered and registered on startup.

## Benefits of This Approach

- **Modularity:** The new tool is self-contained in its own module.
- **Dynamic Loading:** No need to modify core imports; tools can be added or removed by changing configuration.
- **Scalability:** Easy to add more tools in the future following the same pattern.
- **Security:** API keys are managed via environment variables, avoiding hardcoding secrets.

## Next Steps

- Update the environment variable `TOOL_MODULES` or the relevant configuration to include `gptme.tools.openrouter_search`.
- Restart or reload gptme to pick up the new tool.
- Test the tool by invoking it with a search query.

---

Document created to track the integration of the OpenRouter search tool in gptme.
