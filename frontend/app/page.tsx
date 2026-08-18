"use client";

import { useState } from "react";

import QuestionForm from "@/components/QuestionForm";
import AnswerCard from "@/components/AnswerCard";
import SourceList from "@/components/SourceList";

import { getBusinessAdvice } from "@/services/api";
import { BusinessAdviceResponse } from "@/types/rag";

export default function Home() {

    const [loading, setLoading] = useState(false);

    const [result, setResult] =
        useState<BusinessAdviceResponse | null>(null);

    async function handleQuestion(
        question: string
    ) {

        setLoading(true);

        try {

            const response = await getBusinessAdvice(question);

            setResult(response);

        } finally {

            setLoading(false);

        }
    }

    return (
        <main className="mx-auto max-w-4xl p-8">

            <h1 className="mb-8 text-3xl font-bold">
                🇱🇰 SL Business Intelligence Copilot
            </h1>

            <QuestionForm
                onSubmit={handleQuestion}
                loading={loading}
            />

            {result && (
                <div className="mt-8 space-y-6">

                    <AnswerCard
                        result={result}
                    />

                    <SourceList
                        sources={result.sources}
                    />

                </div>
            )}

        </main>
    );
}