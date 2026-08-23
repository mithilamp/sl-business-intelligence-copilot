import { Source } from "@/types/rag";
import ScoreGauge from "./ScoreGauge";

interface SourceListProps {
  sources: Source[];
}

export default function SourceList({
  sources,
}: SourceListProps) {

  if (sources.length === 0) {
    return null;
  }

  return (
    <div className="rounded-[3px] border border-[#D9CFB8] bg-[#F3EEE3] p-6">

      <p className="mb-1 font-mono text-[11px] uppercase tracking-[0.16em] text-[#79705C]">
        Exhibit
      </p>
      <h2 className="mb-5 font-serif text-xl font-semibold text-[#1B1F27]">
        Data Sources
      </h2>

      <div className="space-y-3">

        {sources.map((source, idx) => (

          <div
            key={source.filename}
            className="relative rounded-[3px] border border-[#D9CFB8] bg-white/60 p-4 pl-5"
          >
            {/* index tab */}
            <span className="absolute left-0 top-0 flex h-full w-1 items-start bg-[#2B6660]" />

            <div className="flex items-start justify-between gap-3">
              <div className="min-w-0">
                {source.document_url ? (
                  <a
                    href={source.document_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="font-serif text-base font-medium text-[#1B1F27] underline decoration-[#D9CFB8] underline-offset-4 hover:decoration-[#2B6660]"
                  >
                    {source.title}
                  </a>
                ) : (
                  <p className="font-serif text-base font-medium text-[#1B1F27]">
                    {source.title}
                  </p>
                )}

                <p className="mt-0.5 truncate font-mono text-xs text-[#79705C]">
                  {source.filename}
                </p>
              </div>

              <span className="shrink-0 font-mono text-[11px] text-[#B8AF98]">
                {String(idx + 1).padStart(2, "0")}
              </span>
            </div>

            <div className="mt-2 flex flex-wrap gap-x-4 gap-y-1 text-xs text-[#79705C]">
              <span>{source.source}</span>
              {source.category && (
                <span>Category — {source.category}</span>
              )}
              {source.document_type && (
                <span>Type — {source.document_type}</span>
              )}
            </div>

            {source.chunks && source.chunks.length > 0 && (
              <div className="mt-3 border-t border-dashed border-[#D9CFB8] pt-3">

                <p className="mb-2 font-mono text-[11px] uppercase tracking-[0.12em] text-[#79705C]">
                  Relevant sections
                </p>

                <ul className="space-y-1.5">

                  {source.chunks.map((chunk) => (

                    <li
                      key={chunk.chunk_index}
                      className="flex items-center justify-between gap-3"
                    >
                      <span className="font-mono text-xs text-[#1B1F27]">
                        Chunk {chunk.chunk_index}
                      </span>
                      <ScoreGauge value={chunk.relevance_score} />
                    </li>

                  ))}

                </ul>

              </div>
            )}

          </div>

        ))}

      </div>

    </div>
  );
}
