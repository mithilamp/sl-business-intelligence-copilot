import { BusinessAdviceResponse } from "@/types/rag";

interface BusinessAdviceCardProps {
  result: BusinessAdviceResponse;
}

export default function BusinessAdviceCard({
  result,
}: BusinessAdviceCardProps) {
  const recommendation = result.recommendation;

  return (
    <div className="space-y-4">

      {/* Header / verdict */}
      <div className="relative overflow-hidden rounded-[3px] border border-[#D9CFB8] bg-[#F3EEE3] p-6">

        <div className="flex items-start justify-between gap-6">
          <div className="min-w-0">
            <p className="mb-1 font-mono text-[11px] uppercase tracking-[0.16em] text-[#79705C]">
              Dossier
            </p>
            <h2 className="font-serif text-2xl font-bold text-[#1B1F27]">
              {recommendation.business_name}
            </h2>
          </div>

          {recommendation.suitability_score !== null && (
            <div className="shrink-0">
              <div className="flex h-20 w-20 rotate-[-4deg] items-center justify-center rounded-full border-2 border-[#A9791F]">
                <div className="flex h-16 w-16 flex-col items-center justify-center rounded-full border border-[#A9791F] text-center">
                  <span className="font-mono text-lg font-bold leading-none text-[#A9791F]">
                    {recommendation.suitability_score}
                    <span className="text-xs font-normal">/10</span>
                  </span>
                  <span className="mt-1 font-mono text-[8px] uppercase tracking-[0.1em] text-[#A9791F]">
                    Suitability
                  </span>
                </div>
              </div>
            </div>
          )}
        </div>

        <p className="mt-4 max-w-2xl border-t border-[#D9CFB8] pt-4 leading-relaxed text-[#1B1F27]">
          {recommendation.summary}
        </p>

      </div>

      {/* Stat readouts */}
      <div className="grid gap-4 md:grid-cols-2">

        <div className="rounded-[3px] border border-[#D9CFB8] bg-[#F3EEE3] p-6">
          <p className="mb-2 font-mono text-[11px] uppercase tracking-[0.16em] text-[#79705C]">
            Startup Cost
          </p>
          <p className="font-mono text-2xl text-[#1B1F27]">
            {recommendation.estimated_startup_cost ?? "—"}
          </p>
          {!recommendation.estimated_startup_cost && (
            <p className="mt-1 text-xs text-[#B8AF98]">Not available from sources</p>
          )}
        </div>

        <div className="rounded-[3px] border border-[#D9CFB8] bg-[#F3EEE3] p-6">
          <p className="mb-2 font-mono text-[11px] uppercase tracking-[0.16em] text-[#79705C]">
            Break Even
          </p>
          <p className="font-mono text-2xl text-[#1B1F27]">
            {recommendation.break_even ?? "—"}
          </p>
          {!recommendation.break_even && (
            <p className="mt-1 text-xs text-[#B8AF98]">Not available from sources</p>
          )}
        </div>

      </div>

      {/* Licenses */}
      <div className="rounded-[3px] border border-[#D9CFB8] bg-[#F3EEE3] p-6">

        <p className="mb-3 font-mono text-[11px] uppercase tracking-[0.16em] text-[#79705C]">
          Required Licenses
        </p>

        {recommendation.required_licenses.length === 0 ? (
          <p className="text-sm text-[#79705C]">None identified from available sources.</p>
        ) : (
          <ul className="space-y-1.5">
            {recommendation.required_licenses.map(
              (license) => (
                <li key={license} className="flex items-start gap-2 text-[#1B1F27]">
                  <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-[#2B6660]" />
                  {license}
                </li>
              )
            )}
          </ul>
        )}

      </div>

      {/* Risks */}
      <div className="rounded-[3px] border border-[#D9CFB8] bg-[#F3EEE3] p-6">

        <p className="mb-3 font-mono text-[11px] uppercase tracking-[0.16em] text-[#79705C]">
          Top Risks
        </p>

        <ul className="space-y-1.5">
          {recommendation.top_risks.map((risk) => (
            <li key={risk} className="flex items-start gap-2 text-[#1B1F27]">
              <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-[#9B3B2E]" />
              {risk}
            </li>
          ))}
        </ul>

      </div>

      {/* Next steps */}
      <div className="rounded-[3px] border border-[#D9CFB8] bg-[#F3EEE3] p-6">

        <p className="mb-3 font-mono text-[11px] uppercase tracking-[0.16em] text-[#79705C]">
          Next Steps
        </p>

        <ol className="space-y-2">
          {recommendation.next_steps.map((step, i) => (
            <li key={step} className="flex items-start gap-3 text-[#1B1F27]">
              <span className="mt-0.5 font-mono text-xs text-[#A9791F]">
                {String(i + 1).padStart(2, "0")}
              </span>
              {step}
            </li>
          ))}
        </ol>

      </div>

    </div>
  );
}
