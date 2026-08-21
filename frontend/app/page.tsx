"use client";

import { useEffect, useState } from "react";

import QuestionForm from "@/components/QuestionForm";
import RAGAnswerCard from "@/components/RAGAnswerCard";
import SourceList from "@/components/SourceList";
import BusinessAdviceCard from "@/components/BusinessAdviceCard";

import {
  ask,
  getBusinessAdvice,
} from "@/services/api";

import {
  AskResponse,
  BusinessAdviceResponse,
} from "@/types/rag";

type Mode = "ask" | "business";

export default function Home() {

  const [mode, setMode] = useState<Mode>("ask");

  const [loading, setLoading] = useState(false);

  const [answer, setAnswer] =
    useState<AskResponse | null>(null);

  const [businessAdvice, setBusinessAdvice] =
    useState<BusinessAdviceResponse | null>(null);

  const [conversationId, setConversationId] =
    useState<number | null>(null);


  useEffect(() => {

    const savedConversationId =
      localStorage.getItem("conversation_id");

    if (savedConversationId) {
      setConversationId(
        Number(savedConversationId)
      );
    }

  }, []);

  async function handleQuestion(question: string) {

    setLoading(true);

    setAnswer(null);
    setBusinessAdvice(null);

    try {

      if (mode === "ask") {

        const response = await ask(question, conversationId);

        setConversationId(response.conversation_id)

        localStorage.setItem("conversation_id",String(response.conversation_id))
        
        setAnswer(response);

      } else {

        const response =
          await getBusinessAdvice(question);

        setBusinessAdvice(response);

      }

    } finally {

      setLoading(false);

    }
  }

  function newChat() {

    setConversationId(null);

    localStorage.removeItem(
      "conversation_id"
    );

    setAnswer(null);

    setBusinessAdvice(null);
  }

  return (
    <main className="mx-auto max-w-5xl p-8">

      <h1 className="mb-2 text-3xl font-bold">
        🇱🇰 SL Business Intelligence Copilot
      </h1>

      <p className="mb-8 text-gray-600">
        Ask questions about Sri Lankan business and
        economic information.
      </p>


      {/* Mode selector */}

      <div className="mb-6 flex gap-3">

        <button
          onClick={newChat}
          className="rounded border px-5 py-2">
          New Chat
        </button>

        <button
          onClick={() => setMode("ask")}
          className={`rounded px-5 py-2 ${
            mode === "ask"
              ? "bg-black text-white"
              : "border"
          }`}
        >
          Ask a Question
        </button>

        <button
          onClick={() => setMode("business")}
          className={`rounded px-5 py-2 ${
            mode === "business"
              ? "bg-black text-white"
              : "border"
          }`}
        >
          Business Advisor
        </button>

      </div>


      {/* Question form */}

      <QuestionForm
        onSubmit={handleQuestion}
        loading={loading}
      />


      {/* RAG answer */}

      {answer && mode === "ask" && (

        <div className="mt-8 space-y-6">

          <RAGAnswerCard
            result={answer}
          />

          <SourceList
            sources={answer.sources}
          />

        </div>

      )}


      {/* Business advice */}

      {businessAdvice && mode === "business" && (
        <div className="mt-8 space-y-6">

          <BusinessAdviceCard
            result={businessAdvice}
          />

          <SourceList
            sources={businessAdvice.sources}
          />

        </div>
      )}

    </main>
  );
}