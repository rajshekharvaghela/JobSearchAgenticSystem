from ddgs import DDGS # The package was renamed, good catch!
from newspaper import Article

def get_full_page_content(url):
    """Clicks the link and extracts the main text."""
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        return f"Could not read page: {e}"

def search_and_read(query):
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=3))
        
        for r in results:
            print(f"\nFound: {r['title']}")
            # If snippet is short, we 'click' the link
            if len(r['body']) < 200:
                print("Snippet too short. Scraping full page...")
                full_text = get_full_page_content(r['href'])
                r['full_content'] = full_text
            else:
                r['full_content'] = r['body']
        return results

if __name__ == "__main__":
    query = "site:lever.co OR site:greenhouse.io 'Python' 'Backend' 'Remote'"
    listings = search_and_read(query)
    for l in listings:
        print(f"--- CONTENT PREVIEW ---\n{l['full_content'][:300]}...")
