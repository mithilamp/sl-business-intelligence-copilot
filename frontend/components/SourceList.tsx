import { Source } from "@/types/rag";

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
    <div className="rounded border p-6">

      <h2 className="mb-4 text-xl font-semibold">
        Data Sources
      </h2>

      <div className="space-y-3">

        {sources.map((source) => (

          <div
            key={source.filename}
            className="rounded border p-4"
          >

            {source.document_url ? (
              <a
                href={source.document_url}
                target="_blank"
                rel="noopener noreferrer"
                className="font-medium underline"
              >
                📄 {source.title}
              </a>
            ) : (
              <p className="font-medium">
                📄 {source.title}
              </p>
            )}

            <p className="text-sm text-gray-500">
              {source.filename}
            </p>

            <p className="text-sm text-gray-500">
              {source.source}
            </p>

            {source.category && (
              <p className="text-sm text-gray-500">
                Category: {source.category}
              </p>
            )}

            {source.document_type && (
              <p className="text-sm text-gray-500">
                Type: {source.document_type}
              </p>
            )}

            {source.chunks && source.chunks.length > 0 && (
              <div className="mt-3">

                <p className="text-sm font-medium">
                  Relevant sections:
                </p>

                <ul className="mt-1 space-y-1 text-sm text-gray-500">

                  {source.chunks.map((chunk) => (

                    <li key={chunk.chunk_index}>
                      ✓ Chunk {chunk.chunk_index}
                      {" "}
                      <span>
                        (score: {chunk.relevance_score})
                      </span>
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