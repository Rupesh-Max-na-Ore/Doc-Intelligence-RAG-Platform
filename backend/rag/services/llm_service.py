import requests


LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"


def generate_answer(query, context_docs, metadatas):
    context = format_context(context_docs, metadatas)

    prompt = f"""
    You are a strict question-answering system.

    You MUST follow these rules:

    1. Answer ONLY using the provided context.
    2. Do NOT use outside knowledge.
    3. If the answer is not in the context, say:
    "I could not find the answer in the provided data."
    4. Cite the book titles used in your answer.
    5. Be concise and factual.

    ---------------------
    CONTEXT:
    {context}
    ---------------------

    QUESTION:
    {query}

    ---------------------

    OUTPUT FORMAT:

    Answer:
    <your answer>

    Sources:
    - <book title 1>
    - <book title 2>
    """

    try:
        response = requests.post(
            LM_STUDIO_URL,
            json={
                "model": "local-model",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7
            },
            timeout=60
        )

        result = response.json()

        # 🔥 DEBUG (keep for now)
        print("LLM RAW RESPONSE:", result)

        # ✅ Safe extraction
        if "choices" in result:
            return result["choices"][0]["message"]["content"]

        # ❌ Handle error case
        elif "error" in result:
            return f"LLM Error: {result['error']}"

        else:
            return "LLM returned unexpected format"

    except Exception as e:
        return f"LLM request failed: {str(e)}"
    


def format_context(context_docs, metadatas):
    formatted = []

    for i, (doc, meta) in enumerate(zip(context_docs, metadatas)):
        formatted.append(
            f"[Document {i+1}]\nTitle: {meta['title']}\nContent: {doc}"
        )

    return "\n\n".join(formatted)