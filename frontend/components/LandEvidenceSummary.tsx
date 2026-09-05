import { LandBusinessReport } from "@/types/rag";

interface LandEvidenceSummaryProps {
  report: LandBusinessReport;
  onRemove?: () => void;
}

export default function LandEvidenceSummary({
  report,
  onRemove,
}: LandEvidenceSummaryProps) {
  const location = report.location_and_accessibility.geolocation;
  const verificationItems = report.business_assessment.requires_verification;
  const documentEvidence = report.evidence_by_source.document_extracted;
  const geospatialEvidence = report.evidence_by_source.external_geospatial;

  return (
    <section className="rounded-[3px] border border-[#A9791F] bg-[#F3EEE3] p-6">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <p className="font-mono text-[11px] uppercase tracking-[0.16em] text-[#A9791F]">
            Attached land evidence
          </p>
          <h2 className="mt-1 font-serif text-xl font-semibold text-[#1B1F27]">
            This question will use the selected land report
          </h2>
        </div>
        {onRemove && (
          <button
            type="button"
            onClick={onRemove}
            className="font-mono text-[11px] uppercase tracking-[0.1em] text-[#79705C] hover:text-[#9B3B2E]"
          >
            Remove report
          </button>
        )}
      </div>

      <dl className="mt-4 grid gap-3 border-t border-[#D9CFB8] pt-4 text-sm md:grid-cols-3">
        <div>
          <dt className="font-mono text-[11px] uppercase tracking-[0.1em] text-[#79705C]">
            Document evidence
          </dt>
          <dd className="mt-1 text-[#1B1F27]">
            {documentEvidence && Object.keys(documentEvidence).length
              ? `${Object.keys(documentEvidence).length} evidence groups`
              : "Not available"}
          </dd>
        </div>
        <div>
          <dt className="font-mono text-[11px] uppercase tracking-[0.1em] text-[#79705C]">
            Geospatial evidence
          </dt>
          <dd className="mt-1 text-[#1B1F27]">
            {geospatialEvidence
              ? `${location?.confidence ?? "unknown"} confidence`
              : "Not available"}
          </dd>
        </div>
        <div>
          <dt className="font-mono text-[11px] uppercase tracking-[0.1em] text-[#79705C]">
            Verification required
          </dt>
          <dd className="mt-1 text-[#1B1F27]">
            {verificationItems.length
              ? `${verificationItems.length} item${verificationItems.length === 1 ? "" : "s"}`
              : "None identified"}
          </dd>
        </div>
      </dl>

      {verificationItems.length > 0 && (
        <ul className="mt-4 space-y-1 border-t border-dashed border-[#D9CFB8] pt-4 text-sm text-[#79705C]">
          {verificationItems.map((item, index) => (
            <li key={`${item}-${index}`}>Verify: {item}</li>
          ))}
        </ul>
      )}
    </section>
  );
}
