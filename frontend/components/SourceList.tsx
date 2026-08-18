import { SourceResponse } from "@/types/rag";

interface SourceListProps {
  sources: SourceResponse[];
}

export default function SourceList({
  sources,
}: SourceListProps) {

  if (!sources.length) {
    return null;
  }

  return (
    <div className="rounded border p-6">

      <h2 className="mb-4 text-xl font-semibold">
        Supporting Sources
      </h2>

      <div className="space-y-4">

        {sources.map((source) => (

          <div
            key={`${source.filename}-${source.title}`}
            className="rounded border p-4"
          >

            {source.document_url ? (
              <a
                href={`http://localhost:8000${source.document_url}`}
                target="_blank"
                rel="noopener noreferrer"
                className="font-semibold underline hover:no-underline"
              >
                📄 {source.title}
              </a>
            ) : (
              <p className="font-semibold">
                📄 {source.title}
              </p>
            )}

            <p className="mt-1 text-sm text-gray-600">
              {source.source}
            </p>

            <p className="text-sm text-gray-500">
              {source.filename}
            </p>

          </div>

        ))}

      </div>

    </div>
  );
}