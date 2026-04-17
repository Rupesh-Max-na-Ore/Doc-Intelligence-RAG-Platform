from rag.services.embedding_service import get_embedding
from rag.services.vector_store_service import query_similar


def retrieve_context(query: str):
    query_embedding = get_embedding(query)

    results = query_similar(query_embedding)

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    return documents, metadatas