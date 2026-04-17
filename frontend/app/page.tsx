"use client";

import { useState, useRef, useEffect } from "react";

type Message = {
  role: "user" | "assistant";
  content: string;
  sources?: string[];
};

export default function Home() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);

  const bottomRef = useRef<HTMLDivElement | null>(null);

  // 🔥 auto scroll
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const sendQuery = async () => {
    if (!query.trim()) return;

    const userMessage: Message = {
      role: "user",
      content: query,
    };

    setMessages((prev) => [...prev, userMessage]);
    setQuery("");
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

      const botMessage: Message = {
        role: "assistant",
        content: data.answer,
        sources: data.sources,
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Error connecting to server.",
        },
      ]);
    }

    setLoading(false);
  };

  return (
    <div className="flex flex-col h-screen bg-neutral-950 text-white">
      {/* HEADER */}
      <div className="p-4 border-b border-neutral-800 font-semibold text-lg">
        📚 Doc Intelligence RAG
      </div>

      {/* CHAT AREA */}
      <div className="flex-1 overflow-y-auto p-4 space-y-6">
        {messages.map((msg, idx) => (
          <div key={idx} className="flex flex-col space-y-2">
            <div
              className={`max-w-2xl px-4 py-3 rounded-xl ${
                msg.role === "user"
                  ? "ml-auto bg-blue-600"
                  : "bg-neutral-800"
              }`}
            >
              {msg.content}
            </div>

            {/* 🔥 Sources */}
            {msg.role === "assistant" && msg.sources?.length ? (
              <div className="text-sm text-neutral-400 ml-1">
                <span className="font-semibold">Sources:</span>
                <ul className="list-disc list-inside">
                  {msg.sources.map((s, i) => (
                    <li key={i}>{s}</li>
                  ))}
                </ul>
              </div>
            ) : null}
          </div>
        ))}

        {/* 🔥 Loading Indicator */}
        {loading && (
          <div className="bg-neutral-800 px-4 py-3 rounded-xl w-fit">
            Thinking...
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      {/* INPUT */}
      <div className="p-4 border-t border-neutral-800 flex gap-2">
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendQuery()}
          placeholder="Ask something..."
          className="flex-1 bg-neutral-800 p-3 rounded-lg outline-none"
        />

        <button
          onClick={sendQuery}
          className="bg-blue-600 px-4 py-2 rounded-lg hover:bg-blue-500"
        >
          Send
        </button>
      </div>
    </div>
  );
}