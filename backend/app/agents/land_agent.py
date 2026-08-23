from app.land.parser import LandDocumentParser
from app.land.vision import LandVisionAnalyzer, LandVisionResponseError
from app.land.geolocation import GeoLocationService
from app.land.location_normalizer import LocationNormalizer
from app.llm.openai_llm import OpenAILLM
from app.land.business_analyzer import LandBusinessAnalyzer
from app.land.report_builder import LandBusinessReportBuilder

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


    def analyze(
        self,
        file_path: str,
    ):

        pages = self.parser.parse(file_path)

        results = []


        for page in pages:

            vision_result = self.vision.analyze(page)


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
                    self.location_normalizer.normalize(
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
                    self.geo.locate(
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
            business_analysis = self.business_analyzer.analyze(
                analysis
            )

            analysis["business_analysis"] = (
                business_analysis.model_dump()
            )

            analysis["land_business_report"] = (
                self.report_builder.build(analysis).model_dump()
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
