import chromadb

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(name="books")


def add_document(doc_id, text, embedding, metadata):
    collection.add(
        ids=[str(doc_id)],
        documents=[text],
        embeddings=[embedding],
        metadatas=[metadata]
    )


def query_similar(query_embedding, top_k=5):
    return collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )