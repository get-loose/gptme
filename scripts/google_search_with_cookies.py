import requests
import json
from pathlib import Path

COOKIE_FILE = Path(__file__).parent / "google_cookies.json"

def google_search_with_cookies(query: str, cookies: dict):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    }
    params = {
        "q": query,
        "hl": "en",
    }
    with requests.Session() as session:
        session.headers.update(headers)
        session.cookies.update(cookies)
        response = session.get("https://www.google.com/search", params=params)
        return response.text

def load_cookies():
    if COOKIE_FILE.exists():
        with COOKIE_FILE.open("r") as f:
            cookies_list = json.load(f)
        # Convert list of cookie dicts to dict of name:value
        cookies = {c["name"]: c["value"] for c in cookies_list}
        return cookies
    else:
        print(f"Cookie file {COOKIE_FILE} not found. Please run get_google_cookies.py first.")
        return {}

if __name__ == "__main__":
    cookies = load_cookies()
    query = "OpenAI GPT-4.1-mini context size"
    html = google_search_with_cookies(query, cookies)
    print(html[:2000])  # print first 2000 chars of the response
