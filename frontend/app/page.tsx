"use client";

import { useState } from "react";

export default function Home() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  const sendQuery = async () => {
    if (!query.trim()) return;

    const userMessage = { role: "user", content: query };

    setMessages((prev) => [...prev, userMessage]);
    setLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:8000/api/rag/query/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query }),
      });

      const data = await res.json();

      const botMessage = {
        role: "assistant",
        content: data.answer,
        sources: data.sources,
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      console.error(err);
    }

    setQuery("");
    setLoading(false);
  };

  return (
    <main className="flex flex-col h-screen bg-gray-100">
      {/* Header */}
      <div className="p-4 text-xl font-bold bg-black text-white">
        📚 Doc Intelligence RAG
      </div>

      {/* Chat Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`p-3 rounded-lg max-w-xl ${
              msg.role === "user"
                ? "bg-blue-500 text-white ml-auto"
                : "bg-white text-black"
            }`}
          >
            <p>{msg.content}</p>

            {/* Sources */}
            {msg.sources && msg.sources.length > 0 && (
              <div className="mt-2 text-sm text-gray-600">
                <strong>Sources:</strong>
                <ul className="list-disc ml-5">
                  {msg.sources.map((s: string, idx: number) => (
                    <li key={idx}>{s}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ))}

        {loading && <p className="text-gray-500">Thinking...</p>}
      </div>

      {/* Input */}
      <div className="p-4 bg-white flex gap-2">
        <input
          className="flex-1 border rounded p-2"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask about books..."
        />
        <button
          onClick={sendQuery}
          className="bg-black text-white px-4 py-2 rounded"
        >
          Send
        </button>
      </div>
    </main>
  );
}