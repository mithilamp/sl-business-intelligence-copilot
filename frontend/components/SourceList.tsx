interface SourceListProps {
    sources: string[];
}

export default function SourceList({
    sources,
}: SourceListProps) {

    return (
        <div className="rounded border p-6">

            <h2 className="mb-4 text-xl font-semibold">
                Sources
            </h2>

            <ul className="list-disc pl-5">

                {sources.map((source) => (
                    <li key={source} className="flex items-center gap-2">
                        <span>📄</span>
                        <span>{source}</span>
                    </li>
                ))}

            </ul>

        </div>
    );
}