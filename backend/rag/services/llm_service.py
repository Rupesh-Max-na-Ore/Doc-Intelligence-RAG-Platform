import requests


LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"


def generate_answer(query, context_docs):
    context = "\n\n".join(context_docs)

    prompt = f"""
You are an intelligent assistant.

Answer the question based ONLY on the context below.

Context:
{context}

Question:
{query}

Answer clearly and concisely.
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