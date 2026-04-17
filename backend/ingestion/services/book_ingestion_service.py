from ingestion.scrapers.book_scraper import get_book_links, fetch_page
from ingestion.parsers.book_parser import parse_book
from books.models import Book


def ingest_books(limit=10):
    links = get_book_links()

    results = []

    for link in links[:limit]:
        try:
            html = fetch_page(link)
            data = parse_book(html, link)

            book = Book.objects.create(
                title=data["title"],
                description=data["description"],
                rating=None,  # simplify for now
                url=data["url"]
            )

            results.append(book.title)

        except Exception as e:
            print(f"Error processing {link}: {e}")

    return results