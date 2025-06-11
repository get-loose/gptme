    +## Integrating Robust SearxNG Search in GPTME
    +
    +### Overview
    +
    +This document outlines the approach for integrating the SearxNG search engine in the GPTME project,
    using the JSON API endpoint for reliability and ease of parsing. It summarizes the migration from
    HTML/Playwright-based scraping to direct API calls, and provides tips for future
    maintenance/troubleshooting.
    
    +-
    +
    +### What We Di## Integrating Robust SearxNG Search in GPTME

### Overview

This document outlines the approach for integrating the SearxNG search engine in the GPTME project,
using the JSON API endpoint for reliability and ease of parsing. It summarizes the migration from
HTML/Playwright-based scraping to direct API calls, and provides tips for future
maintenance/troubleshooting.

---

### What We Did

1. **Replaced HTML scraping with direct JSON API calls**:
   - The \`_search_searxng\` function no longer relies on Playwright/browser scraping. Instead, it
makes a direct HTTP request to SearxNG's JSON API endpoint:
     - Example: \`http://10.0.0.12:8082/search?q=QUERY&format=json\`
   - The function extracts both \"instant answers\" (if present) and traditional search results from
the JSON payload, formats and returns them as before.

2. **Maintained output format compatibility**:
   - Results are fed into the existing \`titleurl_to_list\` function, reusing the \`SearchResult\`
dataclass for uniform output.

3. **Result: Faster, less fragile, and future-proof**:
   - No DOM scraping, much lower risk of breakage with SearxNG UI changes.

---

### When Updating Packages / Dependencies

- Ensure that the \`requests\` library is present and compatible (this is used for HTTP calls to
SearxNG).
- This function no longer depends on Playwright for SearxNG, but Playwright logic is still used for
other engines—do not remove Playwright unless you refactor or drop browser-based search for all
engines.
- If SearxNG changes its JSON schema, you may need to update the field extraction logic (see the
lines handling the JSON keys: \`results\`, \`answers\`, and how fields like \`title\`, \`content\` and
 \`url\` are accessed).

---

### Troubleshooting If SearxNG Search Breaks

1. **Check if the SearxNG instance is up and reachable**
   - Try opening your API endpoint URL (e.g., \`http://10.0.0.12:8082/search?q=test&format=json\`) in
 a browser or with \`curl\`. If you don't get JSON back, the problem is with SearxNG, not GPTME code.

2. **Check the structure of the JSON output**
   - SearxNG updates may change where instant answers or results live in the JSON (look for
\`results\`, \`answers\`, \`infoboxes\` etc). Update the extraction logic in \`_search_searxng\` if
needed.

3. **Check that the \`requests\` package is installed and at the right version**
   - Run \`pip3 show requests\` to confirm it's installed.

4. **Check the logs or error message**
   - Error messages will indicate if the problem is a network error, invalid JSON, or missing fields.

5. **Update or rollback as needed**
   - If the API changes unexpectedly, consult SearxNG docs or query open issues on their repo for
breaking changes.

---

### Additional Notes

- The HTML scraping logic (browser/Playwright selectors) remains as backup for other search engines
but is no longer needed for SearxNG after this patch.
- For further robustness, you may wish to handle additional keys like \`infoboxes\`, or add more
defensive code around JSON parsing in \`_search_searxng\`.

---

**Summary:**

SearxNG integration is now much more robust, parsing direct results from the API JSON. Only minor
changes are needed in the future if SearxNG's output format changes.
*** End Patchd
    +
    +1. **Replaced HTML scraping with direct JSON API calls**:
    +   - The \`_search_searxng\` function no longer relies on Playwright/browser scraping. Instead, it
    makes a direct HTTP request to SearxNG’s JSON API endpoint:
    +     - Example: \`http://10.0.0.12:8082/search?q=QUERY&format=json\`
    +   - The function extracts both \"instant answers\" (if present) and traditional search results from
    the JSON payload, formats and returns them as before.
    +
    +2. **Maintained output format compatibility**:
    +   - Results are fed into the existing \`titleurl_to_list\` function, reusing the \`SearchResult\`
    dataclass for uniform output.
    +
    +3. **Result: Faster, less fragile, and future-proof**:
    +   - No DOM scraping, much lower risk of breakage with SearxNG UI changes.
    +
    +---
    +
    +### When Updating Packages / Dependencies
    +
    +- Ensure that the \`requests\` library is present and compatible (this is used for HTTP calls to
    SearxNG).
    +- This function no longer depends on Playwright for SearxNG, but Playwright logic is still used for
    other engines—do not remove Playwright unless you refactor or drop browser-based search for all
    engines.
    +- If SearxNG changes its JSON schema, you may need to update the field extraction logic (see the
    lines handling the JSON keys: \`results\`, \`answers\`, and how fields like \`title\`, \`content\` and
     \`url\` are accessed).
    +
    +---
    +
    +### Troubleshooting If SearxNG Search Breaks
    +
    +1. **Check if the SearxNG instance is up and reachable**
    +   - Try opening your API endpoint URL (e.g., \`http://10.0.0.12:8082/search?q=test&format=json\`) in
     a browser or with \`curl\`. If you don’t get JSON back, the problem is with SearxNG, not GPTME code.
    +
    +2. **Check the structure of the JSON output**
    +   - SearxNG updates may change where instant answers or results live in the JSON (look for
    \`results\`, \`answers\`, \`infoboxes\` etc). Update the extraction logic in \`_search_searxng\` if
    needed.
    +
    +3. **Check that the \`requests\` package is installed and at the right version**
    +   - Run \`pip3 show requests\` to confirm it’s installed.
    +
    +4. **Check the logs or error message**
    +   - Error messages will indicate if the problem is a network error, invalid JSON, or missing fields.
    +
    +5. **Update or rollback as needed**
    +   - If the API changes unexpectedly, consult SearxNG docs or query open issues on their repo for
    breaking changes.
    +
    +---
    +
    +### Additional Notes
    +
    +- The HTML scraping logic (browser/Playwright selectors) remains as backup for other search engines
    but is no longer needed for SearxNG after this patch.
    +- For further robustness, you may wish to handle additional keys like \`infoboxes\`, or add more
    defensive code around JSON parsing in \`_search_searxng\`.
    +
    +---
    +
    +**Summary:**
    +
    +SearxNG integration is now much more robust, parsing direct results from the API JSON. Only minor
    changes are needed in the future if SearxNG’s output format changes.
    *** End Patch
