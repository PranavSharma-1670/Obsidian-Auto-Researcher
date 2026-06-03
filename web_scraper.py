import trafilatura


def extract_web_text(url):
    """
    Downloads a webpage and extracts only the main article text,
    stripping out ads, navbars, and footers.
    """
    print(f"🌐 Fetching URL: {url}...")

    # 1. Download the raw HTML
    downloaded_html = trafilatura.fetch_url(url)

    # Check if the website blocked us (e.g., a 403 Forbidden error)
    if downloaded_html is None:
        return False, f"Failed to download {url}. The site might be blocking bots."

    # 2. Extract the clean text
    # We turn off links and comments to keep the LLM context as pure as possible
    clean_text = trafilatura.extract(
        downloaded_html,
        include_links=False,
        include_comments=False,
        include_tables=True
    )

    # 3. Final validation
    if clean_text:
        return True, clean_text
    else:
        return False, f"Downloaded {url}, but couldn't identify any main article text."


# --- QUICK TEST (Runs only if you execute this file directly) ---
if __name__ == "__main__":
    # Let's test it on a standard Wikipedia article
    test_url = "https://en.wikipedia.org/wiki/Retrieval-augmented_generation"
    success, result = extract_web_text(test_url)

    if success:
        print("\n✅ SUCCESS! Here is a preview of the clean text:\n")
        print(result[:500] + "...\n[TEXT TRUNCATED FOR PREVIEW]")
    else:
        print(f"\n❌ ERROR: {result}")