"use client";

import { useState } from "react";
import ChatMessage from "../components/chatmessage";
import ChatInput from "../components/chatinput";

export default function ChatPage() {
  const [messages, setMessages] = useState<
    { sender: "user" | "ai"; text: string }[]
  >([]);

  const sendMessage = async (text: string) => {
    // Add user message
    setMessages((prev) => [...prev, { sender: "user", text }]);

    // Call FastAPI backend
    try {
      const res = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          message: text,
          phone: "demo-user" // Using a placeholder phone for demo purposes
        }),
      });

      const data = await res.json();

      // Add AI response
      setMessages((prev) => [...prev, { sender: "ai", text: data.response }]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { sender: "ai", text: "⚠️ Error contacting backend." },
      ]);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      <header className="p-4 bg-green-600 text-white text-lg font-bold">
        🌱 AgriProject Chat
      </header>

      <main className="flex-1 overflow-y-auto p-4 space-y-3">
        {messages.map((msg, i) => (
          <ChatMessage key={i} sender={msg.sender} text={msg.text} />
        ))}
      </main>

      <footer className="p-4 bg-white shadow-inner">
        <ChatInput onSend={sendMessage} />
      </footer>
    </div>
  );
}
