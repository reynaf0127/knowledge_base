from pathlib import Path
import os

vault_path = Path("/Users/reyna.feng/Documents/knowledge_obisidian")

books_folder = vault_path / "Stage_db/books"
book_list_file = f"{books_folder}/book list.md"

topics_folder = vault_path / "Stage_db/topics"
topic_list_file = f"{topics_folder}/topic list.md"

topics_filename = [
    os.path.splitext(f)[0].replace("-", " ").capitalize()
    for f in os.listdir(topics_folder)
    if f.endswith(".md") and not f.startswith(".")
]
remove_items = ['Topic list']
topics_filename = [item for item in topics_filename if item not in remove_items]

with open(book_list_file, "r", encoding="utf-8") as file:
    books = [line.strip() for line in file if line.strip()]
with open(topic_list_file, "r", encoding="utf-8") as file:
    topics = [line.strip() for line in file if line.strip()]