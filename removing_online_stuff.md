# Removing ":online" Suffix Handling in gptme Models

## Initial Changes That Caused the Problem

- Added model entries with the ":online" suffix to the `OPENAI_MODELS` dictionary in `gptme/llm/llm_openai_models.py`:
  - `"gpt-4.1:online"`
  - `"gpt-4.1-mini:online"`
- This was done to suppress warnings about unknown models when specifying models with the ":online" suffix in the config or CLI.
- While this removed the warnings, it caused runtime issues because the rest of the code or API calls did not recognize models with the ":online" suffix.

## How We Fixed the Problem

- Removed the ":online" suffixed model entries from `OPENAI_MODELS` to avoid duplicates and runtime issues.
- Patched the `get_model` function in `gptme/llm/models.py` to strip the ":online" suffix from the model string before looking it up in the models dictionary.
  - This allows users to specify models with ":online" suffixes, but the lookup uses the base model name.
- Removed duplicate model entries to fix pre-commit linter errors.
- This approach maintains compatibility with ":online" suffix usage while ensuring model lookups succeed and runtime behavior is correct.

## Summary

- Avoid adding ":online" suffixed models to the models dictionary.
- Handle ":online" suffix stripping in the model lookup function.
- This keeps the code clean, avoids duplication, and supports the ":online" suffix transparently.
