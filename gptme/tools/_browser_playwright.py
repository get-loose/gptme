import atexit
import logging
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, ElementHandle

COOKIE_FILE = Path(__file__).parent.parent.parent / "scripts" / "google_cookies.json"

from ._browser_thread import BrowserThread

_browser: BrowserThread | None = None
logger = logging.getLogger(__name__)


def get_browser() -> BrowserThread:
    global _browser
    if _browser is None:
        _browser = BrowserThread()
        atexit.register(_browser.stop)
    return _browser


def read_url(url: str) -> str:
    """Read the text of a webpage and return the text in Markdown format."""
    browser = get_browser()
    body_html = browser.execute(_load_page, url)
    return html_to_markdown(body_html)


def search_google(query: str) -> str:
    raise NotImplementedError("Google search disabled temporarily.")


def search_duckduckgo(query: str) -> str:
    raise NotImplementedError("DuckDuckGo search disabled temporarily.")


def search_searxng(query: str) -> list[dict]:
    from urllib.parse import quote_plus

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        base_url = f"http://10.0.0.12:8082/search?q={quote_plus(query)}"
        page.goto(base_url)
        page.wait_for_selector("div#urls article.result")
        content = page.content()
        browser.close()

    soup = BeautifulSoup(content, "html.parser")
    results = []
    for article in soup.select("div#urls article.result"):
        title_tag = article.select_one("h3 a")
        link_tag = article.select_one("a.url_header")
        snippet_tag = article.select_one("p.content")
        if title_tag and link_tag:
            results.append(
                {
                    "title": title_tag.get_text(strip=True),
                    "url": link_tag["href"],
                    "snippet": snippet_tag.get_text(strip=True) if snippet_tag else "",
                }
            )
    return results


@dataclass
class Element:
    type: str
    text: str
    name: str
    href: str | None
    element: ElementHandle
    selector: str

    @classmethod
    def from_element(cls, element: ElementHandle):
        return cls(
            type=element.evaluate("el => el.type"),
            text=element.evaluate("el => el.innerText"),
            name=element.evaluate("el => el.name"),
            href=element.evaluate("el => el.href"),
            element=element,
            selector=element.evaluate("el => el.selector"),
        )


@dataclass
class SearchResult:
    title: str
    url: str
    description: str | None = None


def titleurl_to_list(results: list[SearchResult]) -> str:
    s = ""
    for i, r in enumerate(results):
        s += f"\n{i + 1}. {r.title} ({r.url})"
        if r.description:
            s += f"\n   {r.description}"
    return s.strip()


def screenshot_url(url: str, path: Path | str | None = None) -> Path:
    logger.info(f"Taking screenshot of '{url}' and saving to '{path}'")
    browser = get_browser()
    path = browser.execute(_take_screenshot, url, path)
    print(f"Screenshot saved to {path}")
    return path


def html_to_markdown(html):
    if not shutil.which("pandoc"):
        raise Exception("Pandoc is not installed. Needed for browsing.")

    p = subprocess.Popen(
        ["pandoc", "-f", "html", "-t", "markdown"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = p.communicate(input=html.encode())

    if p.returncode != 0:
        raise Exception(f"Pandoc returned error code {p.returncode}: {stderr.decode()}")

    markdown = stdout.decode()
    markdown = "\n".join(
        line for line in markdown.split("\n") if not line.strip().startswith(":::")
    )
    markdown = markdown.replace("<div>", "").replace("</div>", "")
    markdown = re.sub(r"[\n]{3,}", "\n\n", markdown)
    markdown = re.sub(r"\{(#|style|target|\.)[^}]*\}", "", markdown)

    re_strip_data = re.compile(r"!\[[^\]]*\]\(data:image[^)]*\)")
    markdown = re_strip_data.sub("", markdown)

    return markdown
