from rag.services.embedding_service import get_embedding
from rag.services.vector_store_service import query_similar


def retrieve_context(query: str):
    query_embedding = get_embedding(query)

    results = query_similar(query_embedding)

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    # -----------------------------
    # STEP 1: Keyword Boosting
    # -----------------------------
    query_lower = query.lower()
    query_words = query_lower.split()

    boosted = []

    for doc, meta, dist in zip(documents, metadatas, distances):
        score = dist

        # 🔥 keyword boost (light heuristic)
        if any(word in doc.lower() for word in query_words):
            score -= 0.1  # lower distance = higher relevance

        boosted.append((score, doc, meta))

    # sort by boosted score
    boosted.sort(key=lambda x: x[0])

    # take top-k after boost
    TOP_K = 5
    boosted = boosted[:TOP_K]

    # unpack
    documents = [x[1] for x in boosted]
    metadatas = [x[2] for x in boosted]
    distances = [x[0] for x in boosted]

    # -----------------------------
    # STEP 2: Similarity Filtering
    # -----------------------------
    THRESHOLD = 0.85  # more permissive for semantic queries

    filtered_docs = []
    filtered_meta = []

    for doc, meta, dist in zip(documents, metadatas, distances):
        if dist < THRESHOLD:
            filtered_docs.append(doc)
            filtered_meta.append(meta)

    # -----------------------------
    # STEP 3: Balanced Fallback
    # -----------------------------
    if filtered_docs:
        return filtered_docs, filtered_meta

    # fallback: return best match only (avoid empty context collapse)
    return documents[:1], metadatas[:1]