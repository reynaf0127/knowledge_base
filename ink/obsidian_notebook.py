from question_template import QUESTION_TEMPLATE
from pathlib import Path
import pandas as pd
import re


OBSIDIAN_VAULT = Path("/Users/reyna.feng/Documents/knowledge_obisidian")


def safe_filename(name: str) -> str:
    """Remove illegal filename characters."""
    return re.sub(r'[\\/:"*?<>|]+', "", name).strip()


def generate_obsidian_notes_from_df(df: pd.DataFrame, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)

    # Ensure correct order
    df = df.sort_values(["title", "section_index"])

    grouped = df.groupby("title")

    for title, group in grouped:
        paragraphs = group["response"].tolist()

        # Join paragraphs with blank line separation
        content = "\n\n".join(paragraphs)

        note_text = QUESTION_TEMPLATE.format(
            title=title,
            content=content
        )

        filename = safe_filename(title) + ".md"
        file_path = output_dir / filename

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(note_text)

        print(f"✅ Created: {file_path}")


# Example usage:
if __name__ == "__main__":
    df = pd.read_csv("topic_answers.csv")
    generate_obsidian_notes_from_df(df, OBSIDIAN_VAULT)