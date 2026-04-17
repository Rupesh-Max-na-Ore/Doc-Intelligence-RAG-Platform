"use client";

import { useState, useEffect, useRef } from "react";

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

  // 🔥 Persist chat + auto scroll
  useEffect(() => {
    localStorage.setItem("chat_history", JSON.stringify(messages));
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  // 🔥 Ctrl + K shortcut (clear chat)
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.ctrlKey && e.key === "k") {
        e.preventDefault();
        localStorage.removeItem("chat_history");
        setMessages([]);
      }
    };

    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, []);

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

      await new Promise((r) => setTimeout(r, 8));
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
      
      {/* 🔥 HEADER */}
      <div className="p-4 border-b border-neutral-800 flex justify-between items-center">
        <div className="font-semibold text-lg">
          📚 Doc Intelligence RAG
        </div>

        <div className="flex gap-2">
          <button
            onClick={() => {
              localStorage.removeItem("chat_history");
              setMessages([]);
            }}
            className="text-sm px-3 py-1 rounded bg-neutral-800 hover:bg-neutral-700"
          >
            Clear
          </button>

          <button
            onClick={() => {
              if (confirm("Start a new chat?")) {
                localStorage.removeItem("chat_history");
                setMessages([]);
              }
            }}
            className="text-sm px-3 py-1 rounded bg-blue-600 hover:bg-blue-500"
          >
            New Chat
          </button>
        </div>
      </div>

      {/* 🔥 CHAT AREA */}
      <div className="flex-1 overflow-y-auto p-4">
        <div className="max-w-3xl mx-auto space-y-6">

          {/* Empty state */}
          {messages.length === 0 && (
            <div className="text-neutral-500 text-center mt-20">
              New session started. Ask anything 📚
            </div>
          )}

          {messages.map((msg, idx) => (
            <div key={idx} className="flex flex-col space-y-2">
              
              {/* Message bubble */}
              <div
                className={`max-w-2xl px-4 py-3 rounded-xl whitespace-pre-wrap ${
                  msg.role === "user"
                    ? "ml-auto bg-blue-600"
                    : "bg-neutral-800 border border-neutral-700 shadow-md"
                }`}
              >
                {msg.content}
              </div>

              {/* Sources */}
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

          {/* Loading */}
          {loading && (
            <div className="bg-neutral-800 px-4 py-3 rounded-xl w-fit animate-pulse">
              Thinking...
            </div>
          )}

          <div ref={bottomRef} />
        </div>
      </div>

      {/* 🔥 INPUT */}
      <div className="p-4 border-t border-neutral-800 flex gap-2">
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendQuery()}
          placeholder="Ask something..."
          className="flex-1 bg-neutral-800 p-3 pl-12 rounded-lg outline-none"
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