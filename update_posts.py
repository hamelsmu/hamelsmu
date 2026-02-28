"""Fetch latest blog posts from RSS and update README.md."""
import re
import subprocess
import time
import feedparser

FEED_URL = "https://hamel.dev/index.xml"
MAX_POSTS = 10
IGNORE = [
    "Why I Stopped Using nbdev",
    "Selecting The Right AI Evals Tool",
    "Inspect AI, An OSS Python Library For LLM Evals",
    "Thoughts On A Month With Devin",
]

# Fetch feed (use curl as fallback for SSL issues)
try:
    feed = feedparser.parse(FEED_URL)
    if feed.bozo and not feed.entries:
        raise Exception(feed.bozo_exception)
except Exception:
    xml = subprocess.check_output(["curl", "-s", FEED_URL], text=True)
    feed = feedparser.parse(xml)

rows = []
for entry in feed.entries:
    if any(t in entry.title for t in IGNORE):
        continue
    date = time.strftime("%b %Y", entry.published_parsed)
    rows.append(f"| {date} | {entry.title} | [->]({entry.link}) |")
    if len(rows) >= MAX_POSTS:
        break

block = "| Date | Post | |\n| --- | --- | --- |\n" + "\n".join(rows)
with open("README.md") as f:
    readme = f.read()
readme = re.sub(
    r"(<!-- BLOG-POST-LIST:START -->\n).*?(\n<!-- BLOG-POST-LIST:END -->)",
    rf"\1{block}\2",
    readme,
    flags=re.DOTALL,
)
with open("README.md", "w") as f:
    f.write(readme)
print(f"Updated README with {len(rows)} posts")
