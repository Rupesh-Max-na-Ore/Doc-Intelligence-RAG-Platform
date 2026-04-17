from books.models import Book
from rag.services.embedding_service import get_embedding
from rag.services.vector_store_service import add_document
from rag.services.retrieval_service import retrieve_context
from rag.services.llm_service import generate_answer
from rag.utils.chunking import chunk_text


def index_books():
    books = Book.objects.all()

    for book in books:
        full_text = f"{book.title}. {book.description}"

        chunks = chunk_text(full_text)

        for i, chunk in enumerate(chunks):
            embedding = get_embedding(chunk)

            add_document(
                doc_id=f"{book.id}_{i}",   # 🔥 unique per chunk
                text=chunk,
                embedding=embedding,
                metadata={
                    "title": book.title,
                    "chunk_index": i
                }
            )

def answer_query(query: str):
    documents, metadatas = retrieve_context(query)

    # LLM step
    answer = generate_answer(query, documents, metadatas)


    unique_titles = list({meta["title"] for meta in metadatas})

    return {
        "query": query,
        "answer": answer,
        "sources": unique_titles
    }