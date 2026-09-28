import os
import requests
from crewai.tools import tool

@tool("Web Search")
def web_search(query: str) -> str:
    """Search the web for relevant research and return titles, URLs, and snippets."""
    key = os.getenv("SERPER_API_KEY")
    if not key:
        return "Search unavailable: SERPER_API_KEY is not configured."
    try:
        response = requests.post(
            "https://google.serper.dev/search",
            headers={"X-API-KEY": key, "Content-Type": "application/json"},
            json={"q": query, "num": 8},
            timeout=25,
        )
        response.raise_for_status()
        data = response.json()
        results = data.get("organic", [])
        if not results:
            return "No search results found."
        return "\n\n".join(
            f"Title: {r.get('title','')}\nURL: {r.get('link','')}\nSnippet: {r.get('snippet','')}"
            for r in results
        )
    except Exception as e:
        return f"Search error: {e}"

@tool("Retrieve Webpage")
def retrieve_webpage(url: str) -> str:
    """Retrieve readable text from a public webpage URL. Use only http or https URLs."""
    from bs4 import BeautifulSoup
    if not url.startswith(("http://", "https://")):
        return "Invalid URL. Provide an http or https URL."
    try:
        response = requests.get(
            url, timeout=20,
            headers={"User-Agent": "Mozilla/5.0 (compatible; NexusResearchBot/1.0)"}
        )
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header", "noscript"]):
            tag.decompose()
        text = " ".join(soup.get_text(" ").split())
        return text[:12000] if text else "No readable text found."
    except Exception as e:
        return f"Could not retrieve page: {e}"

@tool("Verify Source URL")
def verify_source_url(url: str) -> str:
    """Check whether a source URL responds. This checks availability, not scientific validity."""
    if not url.startswith(("http://", "https://")):
        return "Invalid URL."
    try:
        response = requests.get(url, timeout=15, allow_redirects=True,
                                headers={"User-Agent": "Mozilla/5.0"})
        return f"HTTP status: {response.status_code}; final URL: {response.url}"
    except Exception as e:
        return f"URL check failed: {e}"
