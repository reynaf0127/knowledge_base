import os
import re
from generate_topic import generate_topics
from tag_list import tags
from pathlib import Path

OBSIDIAN_VAULT = Path("/Users/reyna.feng/Documents/knowledge_obisidian/Stage_db/topics")
results = generate_topics(tags)
os.makedirs(OBSIDIAN_VAULT, exist_ok=True)

def safe_filename(text: str) -> str:
    """
    Make topic safe for filename.
    """
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)   # remove special chars
    text = re.sub(r"\s+", "-", text)       # replace spaces with -
    return text[:80]                       # limit length

for item in results:
    tag = item["tag"]
    topic = item["topic"]

    filename = safe_filename(topic) + ".md"
    filepath = os.path.join(OBSIDIAN_VAULT, filename)

    content = f"""title = {topic}

---
tags:
category:
type:
progress: 0
rating:
started:
finished:
---
{tag}
"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
print(f"Created {len(results)} markdown files in '{OBSIDIAN_VAULT}' folder.")