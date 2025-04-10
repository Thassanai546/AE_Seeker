import feedparser
import requests
import re

"""
This script will (attempt) to find articles describing active exploitation.
Keyword matches are highlighted in the terminal.
Edit "LIMIT_PER_FEED" in MAIN to configure this script.
"""

# RSS feed URLs
RSS_FEEDS = [
    {"name": "Hacker News", "url": "https://feeds.feedburner.com/TheHackersNews"},
    {"name": "Bleeping Computer", "url": "https://www.bleepingcomputer.com/feed/"},
]

# Keywords to search for
KEYWORDS = ["exploit", "active"]

# Exclusion phrases to skip entries
EXCLUSION_PHRASES = ["if successfully exploited"]

# Custom User-Agent to mimic a browser
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"


def fetch_feed(url):
    """
    Fetch RSS feed content using a custom User-Agent.
    """
    headers = {"User-Agent": USER_AGENT}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise exception for HTTP errors
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching feed from {url}: {e}")
        return None


def matches_keywords(text, keywords):
    """
    Check if the text contains any keyword or its variations.
    """
    keyword_patterns = [rf"\b{keyword}(ed|ing|ly)?\b" for keyword in keywords]
    return any(re.search(pattern, text, re.IGNORECASE) for pattern in keyword_patterns)


def contains_exclusions(text, exclusions):
    """
    Check if the text contains any exclusion phrase.
    """
    return any(exclusion.lower() in text.lower() for exclusion in exclusions)


def process_feed(feed_url, keywords, exclusions, limit=None):
    """
    Process an RSS feed, filter entries based on keywords and exclusions.
    Returns a list of matching entries, limited by the specified count.
    """
    raw_feed = fetch_feed(feed_url)
    if not raw_feed:
        return []

    feed = feedparser.parse(raw_feed)
    if not feed.entries:
        print(f"No valid entries found in the feed: {feed_url}")
        return []

    matches = []

    for entry in feed.entries:
        # Stop processing if the limit is reached
        if limit and len(matches) >= limit:
            break

        # Combine title and summary for searching
        title = entry.get("title", "")
        summary = entry.get("summary", "")
        link = entry.get("link", "")
        combined_text = f"{title} {summary}"

        # Skip entry if it contains exclusion phrases
        if contains_exclusions(combined_text, exclusions):
            print(f"Excluding entry due to exclusion phrase: {title}")
            continue

        # Add entry if it matches keywords
        if matches_keywords(combined_text, keywords):
            matches.append(
                {
                    "title": title,  # No need for highlighting in the text file
                    "summary": summary,
                    "link": link,
                }
            )

    return matches


def highlight_keywords(text, keywords):
    """
    Highlight keywords and their variations in the text using ANSI escape codes for colors.
    """
    for keyword in keywords:
        text = re.sub(
            rf"\b({keyword}(ed|ing|ly)?)\b",
            r"\033[91m\1\033[0m",
            text,
            flags=re.IGNORECASE,
        )
    return text


def main():
    print(
        r"""    ___    ______   _____           __            
   /   |  / ____/  / ___/___  ___  / /_____  _____
  / /| | / __/     \__ \/ _ \/ _ \/ //_/ _ \/ ___/
 / ___ |/ /___    ___/ /  __/  __/ ,< /  __/ /    
/_/  |_/_____/   /____/\___/\___/_/|_|\___/_/     
                                                  """
    )
    """
    Main function to search vulnerabilities across all RSS feeds.
    """
    LIMIT_PER_FEED = 5  # Set the limit for how many headlines to pull per feed
    all_matches = []  # Collect all matches for saving to a file

    for feed in RSS_FEEDS:
        print(f"\nSearching in {feed['name']}...")
        matches = process_feed(
            feed["url"], KEYWORDS, EXCLUSION_PHRASES, limit=LIMIT_PER_FEED
        )

        if matches:
            print(f"Found {len(matches)} matches.\n")
            for match in matches:
                print(f"Title: {highlight_keywords(match['title'], KEYWORDS)}")
                print(f"Summary: {highlight_keywords(match['summary'], KEYWORDS)}")
                print(f"Link: {match['link']}")
                print("-" * 80)
            all_matches.extend(matches)  # Add matches to the overall list
        else:
            print("No matches found.")


if __name__ == "__main__":
    main()
