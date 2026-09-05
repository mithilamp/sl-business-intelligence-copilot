import { AskResponse } from "@/types/rag";

interface RAGAnswerCardProps {
  result: AskResponse;
}

export default function RAGAnswerCard({
  result,
}: RAGAnswerCardProps) {
  return (
    <div className="rounded-[3px] border border-[#D9CFB8] bg-[#F3EEE3] p-6">

      <div className="mb-4 flex items-baseline justify-between border-b border-[#D9CFB8] pb-3">
        <div>
          <p className="mb-1 font-mono text-[11px] uppercase tracking-[0.16em] text-[#79705C]">
            Findings
          </p>
          <h2 className="font-serif text-xl font-semibold text-[#1B1F27]">
            Answer
          </h2>
        </div>
        <span className="font-mono text-[11px] text-[#B8AF98]">
          §1
        </span>
      </div>

      <p className="whitespace-pre-wrap font-sans leading-relaxed text-[#1B1F27]">
        {result.answer}
      </p>

    </div>
  );
}
