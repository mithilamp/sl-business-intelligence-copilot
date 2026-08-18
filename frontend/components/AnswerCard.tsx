import { BusinessAdviceResponse } from "@/types/rag";

interface AnswerCardProps {
    result: BusinessAdviceResponse;
}

export default function AnswerCard({
    result,
}: AnswerCardProps) {

    const recommendation = result.recommendation;

    return (
        <div className="rounded border p-6 space-y-6">

            {/* Recommended Business */}
            <div>
                <p className="text-sm text-gray-500">
                    Recommended Business
                </p>

                <h2 className="text-2xl font-semibold">
                    {recommendation.business_name}
                </h2>
            </div>

            {/* Summary */}
            <div>
                <h3 className="mb-2 text-lg font-semibold">
                    Summary
                </h3>

                <p className="whitespace-pre-wrap">
                    {recommendation.summary}
                </p>
            </div>

            {/* Suitability Score */}
            <div>
                <h3 className="mb-2 text-lg font-semibold">
                    Suitability Score
                </h3>

                <p>
                    {recommendation.suitability_score !== null
                        ? `${recommendation.suitability_score} / 10`
                        : "Not enough evidence"}
                </p>
            </div>

            {/* Financials */}
            <div>
                <h3 className="mb-2 text-lg font-semibold">
                    Financials
                </h3>

                <div className="space-y-1">
                    <p>
                        <strong>Startup Cost:</strong>{" "}
                        {recommendation.estimated_startup_cost ??
                            "Not available"}
                    </p>

                    <p>
                        <strong>Break-even:</strong>{" "}
                        {recommendation.break_even ??
                            "Not available"}
                    </p>
                </div>
            </div>

            {/* Required Licenses */}
            <div>
                <h3 className="mb-2 text-lg font-semibold">
                    Required Licenses
                </h3>

                {recommendation.required_licenses.length > 0 ? (
                    <ul className="space-y-1">
                        {recommendation.required_licenses.map(
                            (license) => (
                                <li key={license}>
                                    ✓ {license}
                                </li>
                            )
                        )}
                    </ul>
                ) : (
                    <p>Not available</p>
                )}
            </div>

            {/* Top Risks */}
            <div>
                <h3 className="mb-2 text-lg font-semibold">
                    Top Risks
                </h3>

                {recommendation.top_risks.length > 0 ? (
                    <ul className="list-disc space-y-1 pl-5">
                        {recommendation.top_risks.map(
                            (risk) => (
                                <li key={risk}>
                                    {risk}
                                </li>
                            )
                        )}
                    </ul>
                ) : (
                    <p>Not available</p>
                )}
            </div>

            {/* Next Steps */}
            <div>
                <h3 className="mb-2 text-lg font-semibold">
                    Recommended Next Steps
                </h3>

                {recommendation.next_steps.length > 0 ? (
                    <ol className="list-decimal space-y-1 pl-5">
                        {recommendation.next_steps.map(
                            (step) => (
                                <li key={step}>
                                    {step}
                                </li>
                            )
                        )}
                    </ol>
                ) : (
                    <p>Not available</p>
                )}
            </div>

        </div>
    );
}