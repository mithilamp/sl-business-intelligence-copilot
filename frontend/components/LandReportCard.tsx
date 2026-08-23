import {
  LandAnalysisPage,
  LandBusinessReport,
  NearbyPlace,
} from "@/types/rag";

interface LandReportCardProps {
  page: LandAnalysisPage;
  pageNumber: number;
  onAskAdvisor: (report: LandBusinessReport) => void;
}

const reportSectionClasses =
  "rounded-[3px] border border-[#D9CFB8] bg-[#F3EEE3] p-6";

function formatDistance(distance: number) {
  return distance >= 1000
    ? `${(distance / 1000).toFixed(1)} km`
    : `${distance} m`;
}

function renderValue(value: unknown) {
  if (Array.isArray(value)) return value.join(", ") || "—";
  if (value && typeof value === "object") return JSON.stringify(value);
  return String(value ?? "—");
}

function EvidenceList({
  title,
  items,
  markerClass,
}: {
  title: string;
  items: string[];
  markerClass: string;
}) {
  return (
    <section className={reportSectionClasses}>
      <p className="mb-3 font-mono text-[11px] uppercase tracking-[0.16em] text-[#79705C]">
        {title}
      </p>
      {items.length ? (
        <ul className="space-y-2">
          {items.map((item, index) => (
            <li key={`${item}-${index}`} className="flex items-start gap-2 text-[#1B1F27]">
              <span className={`mt-2 h-1.5 w-1.5 shrink-0 rounded-full ${markerClass}`} />
              {item}
            </li>
          ))}
        </ul>
      ) : (
        <p className="text-sm text-[#79705C]">No items identified from available evidence.</p>
      )}
    </section>
  );
}

function NearbyList({ title, places }: { title: string; places: NearbyPlace[] }) {
  return (
    <section className={reportSectionClasses}>
      <p className="mb-3 font-mono text-[11px] uppercase tracking-[0.16em] text-[#79705C]">
        {title}
      </p>
      {places.length ? (
        <ul className="space-y-2">
          {places.slice(0, 5).map((place) => (
            <li key={`${place.name}-${place.osm_id ?? place.distance_meters}`} className="flex items-baseline justify-between gap-3 text-sm text-[#1B1F27]">
              <span className="min-w-0 truncate">{place.name}</span>
              <span className="shrink-0 font-mono text-xs text-[#79705C]">
                {formatDistance(place.distance_meters)}
              </span>
            </li>
          ))}
        </ul>
      ) : (
        <p className="text-sm text-[#79705C]">No mapped results available.</p>
      )}
    </section>
  );
}

function LandMap({ report }: { report: LandBusinessReport }) {
  const coordinates = report.location_and_accessibility.geolocation?.coordinates;

  if (!coordinates) {
    return (
      <section className={reportSectionClasses}>
        <p className="font-mono text-[11px] uppercase tracking-[0.16em] text-[#79705C]">Map</p>
        <p className="mt-3 text-sm text-[#79705C]">Map unavailable because a reliable coordinate was not found.</p>
      </section>
    );
  }

  const { latitude, longitude } = coordinates;
  const delta = 0.015;
  const bbox = `${longitude - delta},${latitude - delta},${longitude + delta},${latitude + delta}`;
  const mapUrl = `https://www.openstreetmap.org/export/embed.html?bbox=${bbox}&layer=mapnik&marker=${latitude},${longitude}`;

  return (
    <section className={`${reportSectionClasses} overflow-hidden p-0`}>
      <div className="flex items-center justify-between border-b border-[#D9CFB8] px-6 py-4">
        <p className="font-mono text-[11px] uppercase tracking-[0.16em] text-[#79705C]">Map context</p>
        <a
          className="font-mono text-[11px] uppercase tracking-[0.1em] text-[#2B6660] hover:underline"
          href={`https://www.openstreetmap.org/?mlat=${latitude}&mlon=${longitude}#map=15/${latitude}/${longitude}`}
          target="_blank"
          rel="noreferrer"
        >
          Open map
        </a>
      </div>
      <iframe title="Land location map" src={mapUrl} className="h-64 w-full border-0" loading="lazy" />
    </section>
  );
}

export default function LandReportCard({
  page,
  pageNumber,
  onAskAdvisor,
}: LandReportCardProps) {
  const report = page.land_business_report;
  const assessment = report.business_assessment;
  const location = report.location_and_accessibility.geolocation;
  const overviewEntries = Object.entries(report.property_overview);

  return (
    <article className="space-y-4">
      <header className="rounded-[3px] border border-[#D9CFB8] bg-[#F3EEE3] p-6">
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div>
            <p className="mb-1 font-mono text-[11px] uppercase tracking-[0.16em] text-[#79705C]">Land Business Report</p>
            <h2 className="font-serif text-2xl font-bold text-[#1B1F27]">Survey page {pageNumber}</h2>
          </div>
          <span className={`rounded-full border px-3 py-1 font-mono text-[11px] uppercase tracking-[0.1em] ${location?.confidence === "high" ? "border-[#2B6660] text-[#2B6660]" : "border-[#A9791F] text-[#A9791F]"}`}>
            Location: {location?.match_quality ?? "unavailable"}
          </span>
        </div>
        <p className="mt-4 border-t border-[#D9CFB8] pt-4 text-sm leading-relaxed text-[#79705C]">
          Document evidence, external map results, and AI inferences are kept separate below.
        </p>
        <div className="mt-4 flex justify-end">
          <button
            type="button"
            onClick={() => onAskAdvisor(report)}
            className="rounded-[3px] bg-[#1B1F27] px-5 py-3 font-mono text-xs uppercase tracking-[0.08em] text-[#F3EEE3] transition-colors hover:bg-[#2B6660]"
          >
            Ask Business Advisor about this land
          </button>
        </div>
      </header>

      <div className="grid gap-4 lg:grid-cols-2">
        <section className={reportSectionClasses}>
          <p className="mb-3 font-mono text-[11px] uppercase tracking-[0.16em] text-[#79705C]">Property overview</p>
          {overviewEntries.length ? (
            <dl className="space-y-3">
              {overviewEntries.map(([label, value]) => (
                <div key={label} className="border-b border-[#E4DCC6] pb-3 last:border-0 last:pb-0">
                  <dt className="font-mono text-[11px] uppercase tracking-[0.1em] text-[#79705C]">{label.replaceAll("_", " ")}</dt>
                  <dd className="mt-1 break-words text-sm text-[#1B1F27]">{renderValue(value)}</dd>
                </div>
              ))}
            </dl>
          ) : <p className="text-sm text-[#79705C]">No property details extracted.</p>}
        </section>

        <section className={reportSectionClasses}>
          <p className="mb-3 font-mono text-[11px] uppercase tracking-[0.16em] text-[#79705C]">Location & access</p>
          <dl className="space-y-3 text-sm">
            <div><dt className="font-mono text-[11px] uppercase tracking-[0.1em] text-[#79705C]">Matched location</dt><dd className="mt-1 text-[#1B1F27]">{location?.address ?? "Not found"}</dd></div>
            <div><dt className="font-mono text-[11px] uppercase tracking-[0.1em] text-[#79705C]">Confidence</dt><dd className="mt-1 text-[#1B1F27]">{location?.confidence ?? "none"} ({location?.location_level ?? "unknown"})</dd></div>
            <div><dt className="font-mono text-[11px] uppercase tracking-[0.1em] text-[#79705C]">Nearby roads</dt><dd className="mt-1 text-[#1B1F27]">{report.location_and_accessibility.nearby_roads.length ? report.location_and_accessibility.nearby_roads.slice(0, 3).map((road) => `${road.name} · ${formatDistance(road.distance_meters)}`).join(", ") : "No mapped roads available"}</dd></div>
          </dl>
        </section>
      </div>

      <LandMap report={report} />

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {Object.entries(report.nearby_intelligence).map(([category, places]) => (
          <NearbyList key={category} title={category.replaceAll("_", " ")} places={places} />
        ))}
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        <EvidenceList title="Opportunities" items={assessment.opportunities} markerClass="bg-[#2B6660]" />
        <EvidenceList title="Risks" items={assessment.risks} markerClass="bg-[#9B3B2E]" />
        <EvidenceList title="Requires verification" items={assessment.requires_verification} markerClass="bg-[#A9791F]" />
        <EvidenceList title="Recommended next steps" items={assessment.next_steps} markerClass="bg-[#1B1F27]" />
      </div>
    </article>
  );
}
