def chunk_text(text, chunk_size=300, overlap=50):
    words = text.split()
    chunks = []

    start = 0
    n = len(words)

    while start < n:
        end = start + chunk_size
        chunk = words[start:end]
        chunks.append(" ".join(chunk))

        start += chunk_size - overlap

    return chunks