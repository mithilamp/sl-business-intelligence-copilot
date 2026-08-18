import { BusinessAdviceResponse } from "@/types/rag";

interface BusinessAdviceCardProps {
  result: BusinessAdviceResponse;
}

export default function BusinessAdviceCard({
  result,
}: BusinessAdviceCardProps) {
  const recommendation = result.recommendation;

  return (
    <div className="space-y-6">

      <div className="rounded border p-6">

        <h2 className="mb-2 text-2xl font-bold">
          {recommendation.business_name}
        </h2>

        {recommendation.suitability_score !== null && (
          <p className="mb-4 text-lg">
            Suitability Score:{" "}
            <strong>
              {recommendation.suitability_score}/10
            </strong>
          </p>
        )}

        <p className="text-gray-700">
          {recommendation.summary}
        </p>

      </div>

      <div className="grid gap-6 md:grid-cols-2">

        <div className="rounded border p-6">
          <h3 className="mb-3 text-lg font-semibold">
            Startup Cost
          </h3>

          <p>
            {recommendation.estimated_startup_cost ??
              "Not available"}
          </p>
        </div>

        <div className="rounded border p-6">
          <h3 className="mb-3 text-lg font-semibold">
            Break Even
          </h3>

          <p>
            {recommendation.break_even ??
              "Not available"}
          </p>
        </div>

      </div>

      <div className="rounded border p-6">

        <h3 className="mb-3 text-lg font-semibold">
          Required Licenses
        </h3>

        {recommendation.required_licenses.length === 0 ? (
          <p>None identified from available sources.</p>
        ) : (
          <ul className="list-disc space-y-1 pl-5">
            {recommendation.required_licenses.map(
              (license) => (
                <li key={license}>{license}</li>
              )
            )}
          </ul>
        )}

      </div>

      <div className="rounded border p-6">

        <h3 className="mb-3 text-lg font-semibold">
          Top Risks
        </h3>

        <ul className="list-disc space-y-1 pl-5">
          {recommendation.top_risks.map((risk) => (
            <li key={risk}>{risk}</li>
          ))}
        </ul>

      </div>

      <div className="rounded border p-6">

        <h3 className="mb-3 text-lg font-semibold">
          Next Steps
        </h3>

        <ol className="list-decimal space-y-1 pl-5">
          {recommendation.next_steps.map((step) => (
            <li key={step}>{step}</li>
          ))}
        </ol>

      </div>

    </div>
  );
}