# Active Exploitation Seeker (V1)
This Python script scans RSS feeds from cybersecurity news sources to identify articles describing active exploits and vulnerabilities. Keywords are highlighted in the terminal for easy identification.

## Features
- Feed Parsing: Fetches and processes RSS feeds from predefined sources.
- Keyword Search: Highlights articles containing specific keywords related to active exploitation.
- Customizable: Easily configure keywords, exclusion phrases, and feed limits.

## Usage
- Edit the script to configure the following
- RSS Feeds: Add or remove feeds from the RSS_FEEDS list.
- Keywords: Customize the KEYWORDS list to match your desired search terms.
- Exclusion Phrases: Update the EXCLUSION_PHRASES list to filter irrelevant entries.
- Feed Limits: Modify LIMIT_PER_FEED in the main() function to control the number of entries processed per feed.

To tailor the script to your needs:
- Add New Feeds: Update the RSS_FEEDS list with new RSS feed URLs.
- Change Keywords: Modify the KEYWORDS list to focus on specific exploitation terms.
- Adjust Exclusions: Use the EXCLUSION_PHRASES list to ignore irrelevant articles.

## Installation
```
git clone https://github.com/your-username/rss-vulnerability-scanner.git
   cd rss-vulnerability-scanner
```

```
pip install feedparser requests
```
## Screenshot(s)
![image](https://github.com/user-attachments/assets/1e2d6a31-47d4-4c38-8ec2-dc16c7bbf69c)
