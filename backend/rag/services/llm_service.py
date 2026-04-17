import requests


LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"


def generate_answer(query, context_docs, metadatas):
    context = format_context(context_docs, metadatas)

    MAX_CONTEXT_CHARS = 2500

    context = context[:MAX_CONTEXT_CHARS]

    prompt = f"""
    You are a strict question-answering system.

    You MUST follow these rules:

    1. Answer ONLY using the provided context.
    2. Do NOT use outside knowledge.
    3. If the answer is not in the context, say:
    "I could not find the answer in the provided data."
    4. Cite the book titles used in your answer.
    5. Be concise and factual.
    6. Do NOT refer to documents as "Document 1", "Document 2". Instead, refer using book titles.
    7. Ignore any unrelated books completely.
    8. Do NOT mention irrelevant documents.
    9. Do NOT explain what is irrelevant.
    10. Do NOT suggest external knowledge.
    11. CRITICAL RULE:
    If the answer is not clearly supported by the context,
    you MUST say:
     "I could not find the answer in the provided data."
    Do NOT use prior knowledge.
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
                "temperature": 0.85
            },
            timeout=180
        )

        result = response.json()

        # DEBUG (keep for now)
        print("LLM RAW RESPONSE:", result)

        # Safe extraction
        if "choices" in result:
            answer = result["choices"][0]["message"]["content"]
            return clean_answer(answer)

        # Handle error case
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

def clean_answer(text):
    if "Answer:" in text:
        text = text.split("Answer:", 1)[1]

    if "Sources:" in text:
        text = text.split("Sources:", 1)[0]

    # 🔥 remove Document references
    text = text.replace("[Document 1]", "")
    text = text.replace("[Document 2]", "")
    text = text.replace("[Document 3]", "")

    return text.strip()