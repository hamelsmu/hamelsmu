"""Fetch latest blog posts from RSS and update README.md."""
import re
import subprocess
import feedparser

FEED_URL = "https://hamel.dev/index.xml"
MAX_POSTS = 6
IGNORE = [
    "Why I Stopped Using nbdev",
    "Selecting The Right AI Evals Tool",
    "Inspect AI, An OSS Python Library For LLM Evals",
]

# Fetch feed (use curl as fallback for SSL issues)
try:
    feed = feedparser.parse(FEED_URL)
    if feed.bozo and not feed.entries:
        raise Exception(feed.bozo_exception)
except Exception:
    xml = subprocess.check_output(["curl", "-s", FEED_URL], text=True)
    feed = feedparser.parse(xml)

lines = []
for entry in feed.entries:
    if any(t in entry.title for t in IGNORE):
        continue
    lines.append(f"- [{entry.title}]({entry.link})")
    if len(lines) >= MAX_POSTS:
        break

block = "\n".join(lines)
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
print(f"Updated README with {len(lines)} posts")
