"use client";

import { useCallback, useEffect, useState } from "react";
import BusinessAdviceCard from "@/components/BusinessAdviceCard";
import LandAnalysisForm from "@/components/LandAnalysisForm";
import LandEvidenceSummary from "@/components/LandEvidenceSummary";
import LandReportCard from "@/components/LandReportCard";
import QuestionForm from "@/components/QuestionForm";
import SourceList from "@/components/SourceList";
import { analyzeLand, ask, getBusinessAdvice, getConversation, getConversations } from "@/services/api";
import { AskResponse, BusinessAdviceResponse, ConversationMessage, ConversationSummary, LandAnalysisResponse, LandBusinessReport } from "@/types/rag";

type Mode = "ask" | "business" | "land";

const modes: { id: Mode; label: string; description: string }[] = [
  { id: "ask", label: "Ask AI", description: "Research Sri Lankan business information" },
  { id: "business", label: "Business Advisor", description: "Turn evidence into an action plan" },
  { id: "land", label: "Land Intelligence", description: "Analyze a survey or site plan" },
];

function formatHistoryDate(value: string) {
  const date = new Date(value);
  if (date.toDateString() === new Date().toDateString()) return "Today";
  return new Intl.DateTimeFormat(undefined, { month: "short", day: "numeric" }).format(date);
}

export default function Home() {
  const [mode, setMode] = useState<Mode>("ask");
  const [loading, setLoading] = useState(false);
  const [historyLoading, setHistoryLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [answer, setAnswer] = useState<AskResponse | null>(null);
  const [messages, setMessages] = useState<ConversationMessage[]>([]);
  const [conversations, setConversations] = useState<ConversationSummary[]>([]);
  const [businessAdvice, setBusinessAdvice] = useState<BusinessAdviceResponse | null>(null);
  const [landAnalysis, setLandAnalysis] = useState<LandAnalysisResponse | null>(null);
  const [selectedLandReport, setSelectedLandReport] = useState<LandBusinessReport | null>(null);
  const [conversationId, setConversationId] = useState<number | null>(null);

  const refreshConversations = useCallback(async () => {
    try {
      setConversations(await getConversations());
    } catch {
      setConversations([]);
    } finally {
      setHistoryLoading(false);
    }
  }, []);

  const openConversation = useCallback(async (id: number, closeSidebar = true) => {
    setHistoryLoading(true);
    setError(null);
    try {
      const conversation = await getConversation(id);
      setConversationId(id);
      setMessages(conversation.messages);
      setAnswer(null);
      setMode("ask");
      window.localStorage.setItem("conversation_id", String(id));
      if (closeSidebar) setSidebarOpen(false);
    } catch (requestError) {
      window.localStorage.removeItem("conversation_id");
      setError(requestError instanceof Error ? requestError.message : "Could not reopen that conversation.");
    } finally {
      setHistoryLoading(false);
    }
  }, []);

  useEffect(() => {
    const timer = window.setTimeout(() => {
      const savedId = window.localStorage.getItem("conversation_id");
      if (savedId && Number.isFinite(Number(savedId))) void openConversation(Number(savedId), false);
      void refreshConversations();
    }, 0);
    return () => window.clearTimeout(timer);
  }, [openConversation, refreshConversations]);

  async function handleQuestion(question: string) {
    setLoading(true);
    setError(null);
    setBusinessAdvice(null);
    setLandAnalysis(null);
    if (mode === "ask") {
      setMessages((current) => [...current, { id: Date.now(), role: "user", content: question, created_at: new Date().toISOString() }]);
    }
    try {
      if (mode === "ask") {
        const response = await ask(question, conversationId);
        setConversationId(response.conversation_id);
        window.localStorage.setItem("conversation_id", String(response.conversation_id));
        setMessages((current) => [...current, { id: Date.now() + 1, role: "assistant", content: response.answer, created_at: new Date().toISOString() }]);
        setAnswer(response);
        await refreshConversations();
      } else {
        setBusinessAdvice(await getBusinessAdvice(question, selectedLandReport));
      }
    } catch (requestError) {
      if (mode === "ask") setMessages((current) => current.slice(0, -1));
      setError(requestError instanceof Error ? requestError.message : "Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  async function handleLandAnalysis(file: File) {
    setLoading(true);
    setError(null);
    setAnswer(null);
    setBusinessAdvice(null);
    setLandAnalysis(null);
    setSelectedLandReport(null);
    try {
      setLandAnalysis(await analyzeLand(file));
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Could not analyze that document.");
      throw requestError;
    } finally {
      setLoading(false);
    }
  }

  function newChat() {
    setConversationId(null);
    setMessages([]);
    setAnswer(null);
    setBusinessAdvice(null);
    setLandAnalysis(null);
    setSelectedLandReport(null);
    setError(null);
    setMode("ask");
    setSidebarOpen(false);
    window.localStorage.removeItem("conversation_id");
  }

  function askAdvisorAboutLand(report: LandBusinessReport) {
    setSelectedLandReport(report);
    setBusinessAdvice(null);
    setAnswer(null);
    setMode("business");
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  const currentConversation = conversations.find((item) => item.id === conversationId);
  const activeMode = modes.find((item) => item.id === mode)!;

  return (
    <main className="min-h-screen bg-[#F4F1E9] text-[#18201F]">
      {sidebarOpen && <button aria-label="Close conversation history" className="fixed inset-0 z-30 bg-[#10201E]/40 lg:hidden" onClick={() => setSidebarOpen(false)} />}
      <aside className={`fixed inset-y-0 left-0 z-40 flex w-[286px] flex-col border-r border-[#D8D2C2] bg-[#172624] text-[#F7F4EB] transition-transform duration-200 lg:translate-x-0 ${sidebarOpen ? "translate-x-0" : "-translate-x-full"}`}>
        <div className="border-b border-white/10 p-5">
          <div className="flex items-center gap-3"><div className="grid h-10 w-10 place-items-center rounded-xl bg-[#D7A842] text-lg font-bold text-[#172624]">SL</div><div><p className="text-sm font-semibold">Business Intelligence</p><p className="text-xs text-white/55">Sri Lanka Copilot</p></div></div>
          <button onClick={newChat} className="mt-5 flex w-full items-center justify-center gap-2 rounded-xl border border-white/15 bg-white/10 px-4 py-3 text-sm font-medium transition hover:bg-white/15"><span className="text-lg leading-none">＋</span> New conversation</button>
        </div>
        <div className="min-h-0 flex-1 overflow-y-auto px-3 py-4">
          <div className="mb-2 flex items-center justify-between px-2"><p className="text-[11px] font-semibold uppercase tracking-[0.16em] text-white/45">Recent questions</p><button onClick={() => void refreshConversations()} className="text-xs text-white/45 hover:text-white" aria-label="Refresh conversations">↻</button></div>
          {historyLoading && conversations.length === 0 ? <div className="space-y-2 px-2" aria-label="Loading conversations">{[1, 2, 3].map((item) => <div key={item} className="h-14 animate-pulse rounded-xl bg-white/10" />)}</div> : conversations.length === 0 ? <div className="mx-2 rounded-xl border border-dashed border-white/15 p-4 text-sm leading-relaxed text-white/50">Your previous questions will appear here after you start a conversation.</div> : <nav aria-label="Conversation history" className="space-y-1">{conversations.map((conversation) => <button key={conversation.id} onClick={() => void openConversation(conversation.id)} className={`w-full rounded-xl px-3 py-3 text-left transition ${conversation.id === conversationId ? "bg-white/15" : "hover:bg-white/8"}`}><span className="block truncate text-sm text-white/90">{conversation.title}</span><span className="mt-1 block text-[11px] text-white/40">{formatHistoryDate(conversation.updated_at)}</span></button>)}</nav>}
        </div>
        <div className="border-t border-white/10 p-4 text-xs leading-relaxed text-white/45">Evidence-led answers from your connected knowledge base.</div>
      </aside>

      <div className="min-h-screen lg:pl-[286px]">
        <header className="sticky top-0 z-20 border-b border-[#D8D2C2] bg-[#F4F1E9]/95 backdrop-blur">
          <div className="mx-auto flex max-w-6xl items-center gap-3 px-4 py-3 sm:px-6"><button onClick={() => setSidebarOpen(true)} className="rounded-lg border border-[#D8D2C2] p-2 lg:hidden" aria-label="Open conversation history">☰</button><div className="min-w-0 flex-1"><p className="truncate text-sm font-semibold">{mode === "ask" && currentConversation ? currentConversation.title : activeMode.label}</p><p className="hidden truncate text-xs text-[#6D756F] sm:block">{activeMode.description}</p></div><span className="flex items-center gap-2 rounded-full border border-[#C9D8D0] bg-[#EDF5F0] px-3 py-1.5 text-xs font-medium text-[#28604E]"><span className="h-2 w-2 rounded-full bg-[#3E8B6C]" />Ready</span></div>
          <div className="mx-auto flex max-w-6xl gap-1 overflow-x-auto px-4 pb-3 sm:px-6">{modes.map((item) => <button key={item.id} onClick={() => { setMode(item.id); setError(null); }} className={`whitespace-nowrap rounded-lg px-4 py-2 text-sm font-medium transition ${mode === item.id ? "bg-[#183D37] text-white shadow-sm" : "text-[#5E6863] hover:bg-white/70"}`}>{item.label}</button>)}</div>
        </header>

        <div className="mx-auto max-w-4xl px-4 py-8 sm:px-6 sm:py-10">
          {error && <div role="alert" className="mb-5 flex items-start justify-between gap-4 rounded-xl border border-[#E1B9AE] bg-[#FFF1ED] p-4 text-sm text-[#873D2E]"><span>{error}</span><button onClick={() => setError(null)} aria-label="Dismiss error">×</button></div>}
          {mode === "ask" && <section>{messages.length === 0 ? <div className="mb-8 py-8 text-center sm:py-14"><div className="mx-auto grid h-14 w-14 place-items-center rounded-2xl bg-[#DCEAE4] text-2xl">✦</div><h1 className="mt-5 font-serif text-3xl font-semibold tracking-tight sm:text-4xl">How can I help your decision?</h1><p className="mx-auto mt-3 max-w-xl text-sm leading-6 text-[#69736D] sm:text-base">Ask a question about Sri Lankan markets, investment, exports, regulations, or economic conditions.</p><div className="mx-auto mt-7 grid max-w-2xl gap-2 sm:grid-cols-2">{["Which sectors are promoted for foreign investment?", "What should I consider before starting an export business?"].map((prompt) => <button key={prompt} onClick={() => void handleQuestion(prompt)} disabled={loading} className="rounded-xl border border-[#D8D2C2] bg-white/65 p-4 text-left text-sm leading-5 transition hover:border-[#799B8E] hover:bg-white disabled:opacity-50">{prompt}</button>)}</div></div> : <div className="mb-7 space-y-6" aria-live="polite">{messages.map((message) => <div key={message.id} className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}><div className={message.role === "user" ? "max-w-[86%] rounded-2xl rounded-br-sm bg-[#183D37] px-4 py-3 text-sm leading-6 text-white sm:max-w-[75%]" : "max-w-full whitespace-pre-wrap rounded-2xl rounded-bl-sm border border-[#D8D2C2] bg-white/70 px-5 py-4 text-sm leading-7 text-[#27312D] shadow-sm"}>{message.content}</div></div>)}{loading && <div className="flex justify-start"><div className="flex items-center gap-2 rounded-2xl border border-[#D8D2C2] bg-white/70 px-5 py-4 text-sm text-[#69736D]"><span className="h-2 w-2 animate-pulse rounded-full bg-[#3E8B6C]" />Reviewing sources and preparing an answer…</div></div>}</div>}<QuestionForm onSubmit={handleQuestion} loading={loading} />{answer && <div className="mt-6"><SourceList sources={answer.sources} /></div>}</section>}
          {mode === "business" && <section className="space-y-5">{selectedLandReport && <LandEvidenceSummary report={selectedLandReport} onRemove={() => setSelectedLandReport(null)} />}<QuestionForm onSubmit={handleQuestion} loading={loading} />{loading && <div className="rounded-xl border border-[#D8D2C2] bg-white/60 p-5 text-sm text-[#69736D]">Building a recommendation from the available evidence…</div>}{businessAdvice && <div className="space-y-6"><BusinessAdviceCard result={businessAdvice} /><SourceList sources={businessAdvice.sources} /></div>}</section>}
          {mode === "land" && <section className="space-y-7"><LandAnalysisForm onSubmit={handleLandAnalysis} loading={loading} />{loading && <div className="rounded-xl border border-[#D8D2C2] bg-white/60 p-5 text-sm text-[#69736D]">Reading the document, resolving the location, and gathering nearby intelligence…</div>}{landAnalysis && <div className="space-y-8">{landAnalysis.analysis.map((page, index) => <LandReportCard key={index} page={page} pageNumber={index + 1} onAskAdvisor={askAdvisorAboutLand} />)}</div>}</section>}
        </div>
      </div>
    </main>
  );
}
