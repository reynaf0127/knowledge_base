from pathlib import Path

vault_path = Path("/Users/reyna.feng/Documents/knowledge_obisidian")

books_folder = vault_path / "Stage_db/books"
book_titles = [file.stem for file in books_folder.glob("*.md")]

topics_folder = vault_path / "Stage_db/topics"
topic_titles = [file.stem for file in topics_folder.glob("*.md")]