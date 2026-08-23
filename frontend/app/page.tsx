"use client";

import { useState } from "react";

import QuestionForm from "@/components/QuestionForm";
import RAGAnswerCard from "@/components/RAGAnswerCard";
import SourceList from "@/components/SourceList";
import BusinessAdviceCard from "@/components/BusinessAdviceCard";
import LandAnalysisForm from "@/components/LandAnalysisForm";
import LandReportCard from "@/components/LandReportCard";
import LandEvidenceSummary from "@/components/LandEvidenceSummary";

import {
  ask,
  getBusinessAdvice,
  analyzeLand,
} from "@/services/api";

import {
  AskResponse,
  BusinessAdviceResponse,
  LandAnalysisResponse,
  LandBusinessReport,
} from "@/types/rag";

type Mode = "ask" | "business" | "land";

export default function Home() {

  const [mode, setMode] = useState<Mode>("ask");

  const [loading, setLoading] = useState(false);

  const [answer, setAnswer] =
    useState<AskResponse | null>(null);

  const [businessAdvice, setBusinessAdvice] =
    useState<BusinessAdviceResponse | null>(null);

  const [landAnalysis, setLandAnalysis] =
    useState<LandAnalysisResponse | null>(null);

  const [selectedLandReport, setSelectedLandReport] =
    useState<LandBusinessReport | null>(null);

  const [conversationId, setConversationId] =
    useState<number | null>(() => {
      if (typeof window === "undefined") return null;

      const savedConversationId = localStorage.getItem("conversation_id");
      return savedConversationId ? Number(savedConversationId) : null;
    });

  async function handleQuestion(question: string) {

    setLoading(true);

    setAnswer(null);
    setBusinessAdvice(null);
    setLandAnalysis(null);

    try {

      if (mode === "ask") {

        const response = await ask(question, conversationId);

        setConversationId(response.conversation_id)

        localStorage.setItem("conversation_id",String(response.conversation_id))
        
        setAnswer(response);

      } else {

        const response = await getBusinessAdvice(
          question,
          selectedLandReport
        );

        setBusinessAdvice(response);

      }

    } finally {

      setLoading(false);

    }
  }

  async function handleLandAnalysis(file: File) {
    setLoading(true);
    setAnswer(null);
    setBusinessAdvice(null);
    setLandAnalysis(null);
    setSelectedLandReport(null);

    try {
      const response = await analyzeLand(file);
      setLandAnalysis(response);
    } finally {
      setLoading(false);
    }
  }

  function askAdvisorAboutLand(report: LandBusinessReport) {
    setSelectedLandReport(report);
    setBusinessAdvice(null);
    setAnswer(null);
    setMode("business");
  }

  function newChat() {

    setConversationId(null);

    localStorage.removeItem(
      "conversation_id"
    );

    setAnswer(null);

    setBusinessAdvice(null);
    setLandAnalysis(null);
    setSelectedLandReport(null);
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
          onClick={() => setMode("land")}
          className={`rounded px-5 py-2 ${
            mode === "land"
              ? "bg-black text-white"
              : "border"
          }`}
        >
          Land Intelligence
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

      {mode === "land" ? (
        <LandAnalysisForm
          onSubmit={handleLandAnalysis}
          loading={loading}
        />
      ) : (
        <div className="space-y-4">
          {mode === "business" && selectedLandReport && (
            <LandEvidenceSummary
              report={selectedLandReport}
              onRemove={() => setSelectedLandReport(null)}
            />
          )}
          <QuestionForm
            onSubmit={handleQuestion}
            loading={loading}
          />
        </div>
      )}


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

      {landAnalysis && mode === "land" && (
        <div className="mt-8 space-y-8">
          {landAnalysis.analysis.map((page, index) => (
            <LandReportCard
              key={index}
              page={page}
              pageNumber={index + 1}
              onAskAdvisor={askAdvisorAboutLand}
            />
          ))}
        </div>
      )}

    </main>
  );
}
