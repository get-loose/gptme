# Dealing with Cookies for Google Search in gptme

## Overview

When using the integrated search tool powered by SearxNG or similar JSON API-based searches, Google often presents a consent page that blocks direct access to search results. To bypass this, we use a real browser to accept the consent and extract the necessary cookies. These cookies are then used in HTTP requests to fetch Google search results without hitting the consent page.

## What We Did

1. **Opened a real browser with Playwright**  
   We created and ran the script `scripts/get_google_cookies.py` which launches a Chromium browser window.  
   - You interact with the page to accept cookies or login if needed.  
   - After accepting, the script prints out the cookies from the browser session.

2. **Used the cookies to perform Google searches**  
   We created the script `scripts/google_search_with_cookies.py` which:  
   - Takes the cookies obtained from the browser session.  
   - Sends HTTP requests to Google Search with these cookies to bypass the consent page.  
   - Prints the HTML content of the search results.

## How to Use the Scripts

### Getting Cookies

1. Run the script to open the browser and accept consent:

   ```bash
   python scripts/get_google_cookies.py
   ```

2. Interact with the browser window to accept cookies or login if necessary.  
3. Press Enter in the terminal when done. The cookies will be printed.

4. Copy the printed cookies and save them in the `scripts/google_search_with_cookies.py` script in the `cookies` dictionary.

### Performing Searches

1. Run the search script with the saved cookies:

   ```bash
   python scripts/google_search_with_cookies.py
   ```

2. The script will print the HTML of the search results page, bypassing the consent screen.

## Saving and Reusing Cookies

Currently, cookies are manually copied from the browser script output and pasted into the search script. For convenience and persistence, you can:

- Save cookies to a JSON file after obtaining them.
- Load cookies from the JSON file in the search script.
- This avoids repeating the browser consent step every time.

## Updating Cookies

Google cookies expire or become invalid over time. If you notice:

- The search script returns a consent page again.
- Search results are missing or incomplete.

Then you need to update the cookies by:

1. Running `scripts/get_google_cookies.py` again to open the browser and accept consent.  
2. Copying the new cookies output.  
3. Updating the `cookies` dictionary in `scripts/google_search_with_cookies.py` with the new values.

## Summary

- Use `get_google_cookies.py` to interactively get valid Google cookies.  
- Use `google_search_with_cookies.py` to perform searches with those cookies.  
- Save and reuse cookies to avoid repeated consent acceptance.  
- Update cookies periodically as they expire or become invalid.

This approach enables bypassing Google's consent page for automated search queries in gptme.
## Saving and Loading Cookies Automatically

We improved the workflow by adding automatic saving and loading of cookies:

- The script `scripts/get_google_cookies.py` now saves the cookies to a JSON file named `google_cookies.json` inside the `scripts` folder after you accept the consent in the browser.
- The script `scripts/google_search_with_cookies.py` loads cookies from this JSON file automatically and uses them in the HTTP requests to Google Search.
- This eliminates the need to manually copy and paste cookies between scripts.
- To update cookies, simply rerun `get_google_cookies.py` to refresh and save new cookies.

This makes the process more convenient and persistent across sessions.
