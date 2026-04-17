from books.models import Book
from rag.services.embedding_service import get_embedding
from rag.services.vector_store_service import add_document
from rag.services.retrieval_service import retrieve_context
from rag.services.llm_service import generate_answer


def index_books():
    books = Book.objects.all()

    for book in books:
        text = f"{book.title}. {book.description}"

        embedding = get_embedding(text)

        add_document(
            doc_id=book.id,
            text=text,
            embedding=embedding,
            metadata={"title": book.title}
        )


def answer_query(query: str):
    documents, metadatas = retrieve_context(query)

    # LLM step
    answer = generate_answer(query, documents, metadatas)

    return {
        "query": query,
        "answer": answer,
        "sources": [
            {
                "title": meta["title"],
                "text": doc
            }
            for doc, meta in zip(documents, metadatas)
        ]
    }