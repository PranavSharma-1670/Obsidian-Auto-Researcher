import requests
from bs4 import BeautifulSoup
import trafilatura


def extract_web_text(url):
    """Downloads a webpage and extracts clean text."""
    try:
        downloaded_html = trafilatura.fetch_url(url)
        if downloaded_html is None:
            return False, f"Failed to download {url}. (Site might block bots)"

        clean_text = trafilatura.extract(
            downloaded_html,
            include_links=False,
            include_comments=False,
            include_tables=True
        )

        if clean_text:
            return True, clean_text
        return False, "No readable text found."
    except Exception as e:
        return False, str(e)


def autonomous_web_search(query, max_results=3):
    """
    Guerrilla Scraper: Hits DuckDuckGo Lite to bypass JS challenges and bot-blockers.
    It manually parses the raw HTML to extract the top external links.
    """
    print(f"🔍 Searching the wild web for: '{query}'...")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }

    try:
        # DDG Lite requires a POST request to search
        response = requests.post("https://lite.duckduckgo.com/lite/", headers=headers, data={"q": query})
        response.raise_for_status()
    except Exception as e:
        return False, f"Search engine blocked us: {str(e)}"

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    results = []

    # Find all links on the page
    for a in soup.find_all('a'):
        url = a.get('href', '')

        # Filter out DuckDuckGo's internal links to only get the actual search results
        if url.startswith('http') and 'duckduckgo.com' not in url:
            title = a.text.strip()

            # Ignore UI elements like "Next Page"
            if title and len(title) > 5:
                # Prevent duplicate links
                if not any(r['url'] == url for r in results):
                    results.append({"title": title, "url": url})

        if len(results) >= max_results:
            break

    if not results:
        return False, "DuckDuckGo returned a page, but we couldn't parse any links."

    compiled_web_context = ""

    # 3. Iterate through our successfully scraped links and extract the article text
    for idx, result in enumerate(results):
        url = result["url"]
        title = result["title"]
        print(f"  [{idx + 1}/{len(results)}] Scraping: {title}...")

        success, text = extract_web_text(url)

        if success:
            compiled_web_context += f"--- SOURCE: {title} ({url}) ---\n{text}\n\n"

    if not compiled_web_context:
        return False, "Found links, but the websites actively blocked our text scraper."

    return True, compiled_web_context


# --- QUICK TEST ---
# if __name__ == "__main__":
#     test_query = "What are the latest breakthroughs in Edge AI in 2026"
#     success, result = autonomous_web_search(test_query, max_results=5)
#
#     if success:
#         print("\n✅ AUTONOMOUS SEARCH SUCCESS!\n")
#         print(result[:1000] + "...\n[TEXT TRUNCATED]")
#         print("*"*50)
#         # print(result + "...\n[TEXT TRUNCATED]")
#     else:
#         print(f"\n❌ ERROR: {result}")

# --- QUICK TEST ---
if __name__ == "__main__":
    test_query = "What are the latest breakthroughs in Edge AI in 2026"
    success, result = autonomous_web_search(test_query, max_results=5)

    if success:
        print("\n✅ AUTONOMOUS SEARCH SUCCESS!\n")
        print(f"📊 Total Characters Scraped: {len(result)}")
        print("--------------------------------------------------")
        # Print the first 5,000 characters instead of 1,000
        print(result[:5000] + "\n... [TRUNCATED FOR TERMINAL VIEW]")
    else:
        print(f"\n❌ ERROR: {result}")