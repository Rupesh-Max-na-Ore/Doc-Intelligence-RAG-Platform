from ingestion.scrapers.book_scraper import get_book_links, fetch_page
from ingestion.parsers.book_parser import parse_book
from books.models import Book

import logging

logger = logging.getLogger(__name__)


def ingest_books(limit=10):
    links = get_book_links()

    results = []
    skipped = 0
    errors = 0

    for link in links[:limit]:
        try:

            # Retry mechanism (basic)
            for attempt in range(3):
                try:
                    html = fetch_page(link)
                    break
                except Exception as e:
                    if attempt == 2:
                        raise e

            data = parse_book(html, link)

            # Idempotent write (NO duplicates)
            book, created = Book.objects.get_or_create(
                title=data["title"],
                defaults={
                    "description": data["description"],
                    "rating": None,  # can refine later
                    "url": data["url"]
                }
            )

            if created:
                results.append(book.title)
            else:
                skipped += 1

        except Exception as e:
            logger.error(f"[INGESTION ERROR] {link}: {e}")
            errors += 1

    return {
        "created": results,
        "created_count": len(results),
        "skipped_count": skipped,
        "error_count": errors
    }