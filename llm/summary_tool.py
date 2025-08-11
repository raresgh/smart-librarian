from data.loader import load_summaries

book_summaries = load_summaries()

def get_summary_by_title(title: str) -> str:
    return book_summaries.get(title, "Rezumatul nu este disponibil pentru această carte.")