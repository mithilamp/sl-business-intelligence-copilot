interface ScoreGaugeProps {
  /** 0–1 relevance score, or 0–10 suitability score */
  value: number;
  max?: number;
  ticks?: number;
  size?: "sm" | "lg";
}

/**
 * A hand-measured gauge: a row of filled/unfilled ticks plus the raw
 * mono figure. Used for chunk relevance scores and echoed at larger
 * scale for business suitability — the dossier's recurring "measured,
 * not guessed" motif.
 */
export default function ScoreGauge({
  value,
  max = 1,
  ticks = 5,
  size = "sm",
}: ScoreGaugeProps) {
  const pct = Math.max(0, Math.min(1, value / max));
  const filled = Math.round(pct * ticks);

  const tickHeight = size === "lg" ? "h-3" : "h-2";
  const tickWidth = size === "lg" ? "w-1.5" : "w-1";

  return (
    <div className="inline-flex items-center gap-2">
      <div className="flex items-end gap-[3px]">
        {Array.from({ length: ticks }).map((_, i) => (
          <span
            key={i}
            className={`${tickWidth} ${tickHeight} ${
              i < filled ? "bg-[#A9791F]" : "bg-[#D9CFB8]"
            }`}
            style={{
              height:
                size === "lg"
                  ? `${8 + i * 3}px`
                  : `${6 + i * 2}px`,
            }}
          />
        ))}
      </div>
      <span className="font-mono text-xs text-[#79705C]">
        {max === 1 ? value.toFixed(2) : `${value}/${max}`}
      </span>
    </div>
  );
}
