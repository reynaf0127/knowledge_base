from book_summary import build_book_dataframe
from question_answer import build_answer_dataframe
from find_list import book_titles, topic_titles
import pandas as pd


def is_non_empty_list(x) -> bool:
    return isinstance(x, (list, tuple)) and len(x) > 0


if __name__ == "__main__":
    # Book summaries
    if is_non_empty_list(book_titles):
        df_books = build_book_dataframe(book_titles)
        df_books.to_csv("book_summaries.csv", index=False)
        print(f"✅ Saved book_summaries.csv ({len(df_books)} rows)")
    else:
        print("⏭️ Skipping book summaries: book_titles is empty or None")

    # Topic answers
    if is_non_empty_list(topic_titles):
        df_topics = build_answer_dataframe(topic_titles)
        df_topics.to_csv("topic_answers.csv", index=False)
        print(f"✅ Saved topic_answers.csv ({len(df_topics)} rows)")
    else:
        print("⏭️ Skipping topic answers: topic_titles is empty or None")