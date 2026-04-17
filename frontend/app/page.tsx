"use client";

import { useState, useEffect, useRef } from "react";
import ReactMarkdown from "react-markdown";

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

  // 🔥 Load chat history
  useEffect(() => {
    const saved = localStorage.getItem("chat_history");
    if (saved) setMessages(JSON.parse(saved));
  }, []);

  // 🔥 Persist chat history
  useEffect(() => {
    localStorage.setItem("chat_history", JSON.stringify(messages));
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  // 🔥 Typing animation
  const typeMessage = async (text: string) => {
    let current = "";
    for (let i = 0; i < text.length; i++) {
      current += text[i];

      setMessages((prev) => {
        const copy = [...prev];
        copy[copy.length - 1].content = current;
        return copy;
      });

      await new Promise((r) => setTimeout(r, 10));
    }
  };

  const sendQuery = async () => {
    if (!query.trim() || loading) return;

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

      // 🔥 placeholder assistant message
      const botMessage: Message = {
        role: "assistant",
        content: "",
        sources: data.sources,
      };

      setMessages((prev) => [...prev, botMessage]);

      await typeMessage(data.answer);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "❌ Error connecting to server.",
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
        {/* 🔥 Empty state */}
        {messages.length === 0 && (
          <div className="text-neutral-500 text-center mt-20">
            Ask questions about your documents 📚
          </div>
        )}

        {messages.map((msg, idx) => (
          <div key={idx} className="flex flex-col space-y-2">
            {/* MESSAGE */}
            <div
              className={`max-w-2xl px-4 py-3 rounded-xl whitespace-pre-wrap ${
                msg.role === "user"
                  ? "ml-auto bg-blue-600"
                  : "bg-neutral-800"
              }`}
            >
             <ReactMarkdown>{msg.content}</ReactMarkdown>
            </div>

            {/* 🔥 Expandable Sources */}
            {msg.role === "assistant" && msg.sources?.length ? (
              <details className="text-sm text-neutral-400 ml-1 cursor-pointer">
                <summary className="font-semibold">Sources</summary>
                <ul className="list-disc list-inside mt-1">
                  {msg.sources.map((s, i) => (
                    <li key={i}>{s}</li>
                  ))}
                </ul>
              </details>
            ) : null}
          </div>
        ))}

        {/* 🔥 Loading */}
        {loading && (
          <div className="bg-neutral-800 px-4 py-3 rounded-xl w-fit animate-pulse">
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