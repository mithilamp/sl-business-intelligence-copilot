import { AskResponse } from "@/types/rag";

interface RAGAnswerCardProps {
  result: AskResponse;
}

export default function RAGAnswerCard({
  result,
}: RAGAnswerCardProps) {
  return (
    <div className="rounded border p-6">

      <h2 className="mb-4 text-xl font-semibold">
        Answer
      </h2>

      <p className="whitespace-pre-wrap">
        {result.answer}
      </p>

    </div>
  );
}