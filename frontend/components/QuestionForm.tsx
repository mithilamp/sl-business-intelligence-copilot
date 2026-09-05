"use client";

import { useState } from "react";

interface QuestionFormProps {
    onSubmit: (question: string) => Promise<void>;
    loading: boolean;
}

export default function QuestionForm({
    onSubmit,
    loading,
}: QuestionFormProps) {

    const [question, setQuestion] = useState("");

    async function handleSubmit(
        e: React.FormEvent<HTMLFormElement>
    ) {
        e.preventDefault();

        if (!question.trim()) return;

        await onSubmit(question.trim());
        setQuestion("");
    }

    return (
        <form
            onSubmit={handleSubmit}
            className="rounded-2xl border border-[#D9CFB8] bg-[#F8F5EE] p-4 shadow-sm sm:p-5"
        >
            <p className="mb-1 font-mono text-[11px] uppercase tracking-[0.16em] text-[#79705C]">
                Case Intake
            </p>
            <h2 className="mb-4 font-serif text-lg font-semibold text-[#1B1F27]">
                What do you want to know?
            </h2>

            <textarea
                className="w-full resize-none rounded-[3px] border border-[#D9CFB8] bg-white/70 p-3 font-sans text-[#1B1F27] leading-[28px] placeholder:text-[#B8AF98] focus:border-[#2B6660] focus:outline-none focus:ring-1 focus:ring-[#2B6660]"
                style={{
                    backgroundImage:
                        "repeating-linear-gradient(transparent, transparent 27px, #E4DCC6 28px)",
                    backgroundPosition: "0 4px",
                }}
                rows={3}
                placeholder="Ask about markets, investment, exports, policy, or the economy…"
                value={question}
                onChange={(e) =>
                    setQuestion(e.target.value)
                }
            />

            <div className="mt-4 flex items-center justify-between">
                <span className="font-mono text-[11px] text-[#B8AF98]">
                    {question.trim().length > 0
                        ? `${question.trim().length} characters`
                        : "Awaiting entry"}
                </span>

                <button
                    type="submit"
                    disabled={loading || !question.trim()}
                    className="rounded-[3px] bg-[#1B1F27] px-6 py-3 font-mono text-sm uppercase tracking-[0.08em] text-[#F3EEE3] transition-colors hover:bg-[#2B6660] disabled:opacity-50"
                >
                    {loading ? "Reviewing…" : "Submit Inquiry"}
                </button>
            </div>
        </form>
    );
}
