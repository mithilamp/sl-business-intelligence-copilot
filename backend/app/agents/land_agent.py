from app.land.parser import LandDocumentParser
from app.land.vision import LandVisionAnalyzer, LandVisionResponseError
from app.land.geolocation import GeoLocationService
from app.land.location_normalizer import LocationNormalizer
from app.llm.openai_llm import OpenAILLM
from app.land.business_analyzer import LandBusinessAnalyzer
from app.land.report_builder import LandBusinessReportBuilder
from app.core.langsmith import traceable

import json


class LandAgent:

    def __init__(self):

        self.parser = LandDocumentParser()

        self.vision = LandVisionAnalyzer()

        self.geo = GeoLocationService()

        self.location_normalizer = LocationNormalizer(
            OpenAILLM()
        )

        self.business_analyzer = LandBusinessAnalyzer(
            OpenAILLM()
        )

        self.report_builder = LandBusinessReportBuilder()


    @traceable(name="Land Intelligence Analysis", run_type="chain", tags=["land-intelligence", "multimodal"])
    def analyze(
        self,
        file_path: str,
    ):

        pages = self._parse_document(file_path)

        results = []


        for page in pages:

            vision_result = self._extract_land_evidence(page)


            print("====================")
            print("VISION RAW OUTPUT")
            print(vision_result)
            print("====================")


            try:
                analysis = json.loads(vision_result)
            except (json.JSONDecodeError, TypeError) as error:
                raise LandVisionResponseError(
                    "The vision model returned invalid land-analysis JSON. "
                    "Please retry with a clearer image or PDF."
                ) from error

            if not isinstance(analysis, dict):
                raise LandVisionResponseError(
                    "The vision model returned an unexpected land-analysis format."
                )


            # ---------------------------------
            # AI Location Normalization
            # ---------------------------------

            location_information = analysis.get(
                "location_information",
                []
            )


            if location_information:


                normalized_location = (
                    self._normalise_location(
                        location_information
                    )
                )


                print("====================")
                print("NORMALIZED LOCATION")
                print(normalized_location)
                print("====================")


                analysis["location_query"] = (
                    normalized_location
                )


                # ---------------------------------
                # Geolocation enrichment
                # ---------------------------------

                analysis["geolocation"] = (
                    self._geolocate(
                        normalized_location["search_query"],
                        source_confidence=normalized_location.get(
                            "confidence"
                        ),
                    )
                )

            # ---------------------------------
            # Business intelligence analysis + report
            # ---------------------------------
            # Run the analysis even when the location cannot be extracted: the
            # survey itself can still provide grounded observations and gaps.
            business_analysis = self._analyse_business_fit(
                analysis
            )

            analysis["business_analysis"] = (
                business_analysis.model_dump()
            )

            analysis["land_business_report"] = (
                self._build_report(analysis).model_dump()
            )


            results.append(
                analysis
            )


        return {
            "agent": "land_intelligence",
            "input_file": file_path,
            "pages_processed": len(pages),
            "analysis": results
        }

    @traceable(name="Parse Land Document", run_type="tool", tags=["land-parser"])
    def _parse_document(self, file_path: str):
        return self.parser.parse(file_path)

    @traceable(name="Vision Evidence Extraction", run_type="llm", tags=["vision", "multimodal"])
    def _extract_land_evidence(self, page):
        return self.vision.analyze(page)

    @traceable(name="Normalize Location", run_type="chain", tags=["location-normalization"])
    def _normalise_location(self, location_information):
        return self.location_normalizer.normalize(location_information)

    @traceable(name="Geolocate and Enrich", run_type="tool", tags=["geospatial", "openstreetmap"])
    def _geolocate(self, search_query: str, source_confidence: str | None = None):
        return self.geo.locate(search_query, source_confidence=source_confidence)

    @traceable(name="Land Business Analysis", run_type="llm", tags=["business-analysis"])
    def _analyse_business_fit(self, analysis: dict):
        return self.business_analyzer.analyze(analysis)

    @traceable(name="Build Land Intelligence Report", run_type="chain", tags=["report"])
    def _build_report(self, analysis: dict):
        return self.report_builder.build(analysis)
