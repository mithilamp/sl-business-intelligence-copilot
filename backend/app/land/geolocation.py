import requests

from app.land.nearby import NearbyIntelligence


class GeoLocationService:

    # Nominatim returns these administrative levels for broad area results.  A
    # result at one of these levels is useful as a hint, but must never be
    # represented as an exact property or local-area match.
    COARSE_LOCATION_TYPES = {
        "country",
        "state",
        "state_district",
        "province",
        "region",
        "county",
        "district",
        "city_district",
        "administrative",
    }

    LOCAL_LOCATION_TYPES = {
        "city",
        "town",
        "village",
        "suburb",
        "neighbourhood",
        "hamlet",
        "locality",
        "municipality",
    }

    def __init__(self):

        self.search_url = (
            "https://nominatim.openstreetmap.org/search"
        )

        self.reverse_url = (
            "https://nominatim.openstreetmap.org/reverse"
        )

        self.nearby = NearbyIntelligence()

    def locate(
        self,
        location_text: str,
        source_confidence: str | None = None,
    ):

        headers = {
            "User-Agent": "sl-business-intelligence-copilot"
        }

        # ---------------------------------
        # Build progressive search queries
        # ---------------------------------

        parts = [
            part.strip()
            for part in location_text.split(",")
            if part.strip()
        ]

        queries = [
            location_text
        ]

        # Remove less specific parts gradually
        for index in range(1, len(parts)):

            query = ", ".join(
                parts[index:]
            )

            if query not in queries:
                queries.append(query)

        result = None
        matched_query = None

        # ---------------------------------
        # Try geocoding
        # ---------------------------------

        for query in queries:

            params = {
                "q": query,
                "format": "json",
                "limit": 1,
                "countrycodes": "lk",
                "addressdetails": 1,
            }

            try:
                response = requests.get(
                    self.search_url,
                    params=params,
                    headers=headers,
                    timeout=10,
                )

                response.raise_for_status()

                data = response.json()

            except (requests.RequestException, ValueError):
                # A geocoding outage should not prevent analysis of the land
                # document.  The response below is also unambiguous to callers.
                data = []

            if data:

                result = data[0]
                matched_query = query

                break

        # ---------------------------------
        # Nothing found
        # ---------------------------------

        if result is None:
            return self._not_found_result(location_text, source_confidence)

        # ---------------------------------
        # Coordinates
        # ---------------------------------

        latitude = float(
            result["lat"]
        )

        longitude = float(
            result["lon"]
        )

        match = self._classify_match(
            result=result,
            matched_query=matched_query,
            original_query=location_text,
            source_confidence=source_confidence,
        )

        # ---------------------------------
        # Nearby intelligence
        # ---------------------------------

        nearby = self.nearby.find_nearby(
            latitude,
            longitude,
        )

        # ---------------------------------
        # Final result
        # ---------------------------------

        return {

            "query": location_text,

            "matched_query": matched_query,

            # ``accuracy`` is retained for existing consumers.  The new fields
            # explain whether this is an exact/local coordinate or a broad
            # administrative fallback.
            "accuracy": match["accuracy"],

            "match_quality": match["match_quality"],

            "confidence": match["confidence"],

            "location_level": match["location_level"],

            "source_confidence": match["source_confidence"],

            "found": True,

            "coordinates": {
                "latitude": latitude,
                "longitude": longitude,
            },

            "address": result.get(
                "display_name"
            ),

            "nearby": nearby

        }

    def _not_found_result(
        self,
        location_text: str,
        source_confidence: str | None,
    ) -> dict:
        return {
            "query": location_text,
            "found": False,
            "matched_query": None,
            "accuracy": "not_found",
            "match_quality": "not_found",
            "confidence": "none",
            "source_confidence": source_confidence,
            "location_level": "unknown",
            "coordinates": {"latitude": None, "longitude": None},
            "nearby": self.nearby.empty_result(),
        }

    def _classify_match(
        self,
        result: dict,
        matched_query: str,
        original_query: str,
        source_confidence: str | None,
    ) -> dict:
        """Classify the returned place, rather than trusting query equality.

        A full text query can resolve to a province, so matching the original
        query alone is not evidence of an exact location.
        """
        location_level = self._location_level(result)
        is_fallback = matched_query != original_query

        if location_level in self.COARSE_LOCATION_TYPES:
            return {
                "accuracy": "coarse",
                "match_quality": "coarse",
                "confidence": "low",
                "location_level": location_level,
                "source_confidence": source_confidence,
            }

        if not is_fallback:
            return {
                "accuracy": "exact",
                "match_quality": "exact",
                "confidence": "high",
                "location_level": location_level,
                "source_confidence": source_confidence,
            }

        if location_level in self.LOCAL_LOCATION_TYPES:
            return {
                "accuracy": "fallback",
                "match_quality": "local",
                "confidence": "medium",
                "location_level": location_level,
                "source_confidence": source_confidence,
            }

        return {
            "accuracy": "fallback",
            "match_quality": "fallback",
            "confidence": "low",
            "location_level": location_level,
            "source_confidence": source_confidence,
        }

    @staticmethod
    def _location_level(result: dict) -> str:
        address = result.get("address", {})
        addresstype = result.get("addresstype") or result.get("type")

        if addresstype:
            return str(addresstype).lower()

        # Older Nominatim responses may omit addresstype.  Address keys are a
        # reliable fallback for identifying broad administrative matches.
        for key in (
            "province", "state", "region", "county", "district",
            "city_district", "country",
        ):
            if key in address:
                return key

        for key in (
            "village", "town", "city", "suburb", "neighbourhood",
            "hamlet", "locality",
        ):
            if key in address:
                return key

        return "unknown"
