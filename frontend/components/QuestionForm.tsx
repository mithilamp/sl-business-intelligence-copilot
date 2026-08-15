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

        await onSubmit(question);
    }

    return (
        <form
            onSubmit={handleSubmit}
            className="space-y-4"
        >
            <textarea
                className="w-full rounded border p-3"
                rows={4}
                placeholder="Ask a question..."
                value={question}
                onChange={(e) =>
                    setQuestion(e.target.value)
                }
            />

            <button
                type="submit"
                disabled={loading}
                className="rounded bg-blue-600 px-6 py-3 text-white disabled:opacity-50"
            >
                {loading ? "Thinking..." : "Ask"}
            </button>
        </form>
    );
}