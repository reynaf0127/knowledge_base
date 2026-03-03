from pathlib import Path

vault_path = Path("/Users/reyna.feng/Documents/knowledge_obisidian")

meta_folder = vault_path / "Meta"
tag_list_file = f"{meta_folder}/Tag inventory.md"


with open(tag_list_file, "r", encoding="utf-8") as file:
    tags = [line.strip() for line in file if line.strip()]

tags = [item.replace('- #', '') for item in tags]
remove_items = ['philosophy', 'reflection', 'idea', 'action', 'fiction', 'habits']
tags = [item for item in tags if item not in remove_items]