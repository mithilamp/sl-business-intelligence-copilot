import requests
from math import asin, cos, radians, sin, sqrt
from app.core.langsmith import traceable


class NearbyIntelligence:

    def __init__(self):

        self.url = (
            "https://overpass-api.de/api/interpreter"
        )

        self.radius = 3000

        self.headers = {
            "User-Agent": "sl-business-intelligence-copilot",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }


    @traceable(
        name="Nearby OpenStreetMap Intelligence",
        run_type="tool",
        tags=["openstreetmap", "nearby"],
    )
    def find_nearby(
        self,
        latitude: float,
        longitude: float,
    ):

        query = f"""
        [out:json][timeout:25];

        (
          nwr(around:{self.radius},{latitude},{longitude})
          ["amenity"="school"];

          nwr(around:{self.radius},{latitude},{longitude})
          ["amenity"="hospital"];

          nwr(around:{self.radius},{latitude},{longitude})
          ["amenity"="bank"];

          nwr(around:{self.radius},{latitude},{longitude})
          ["shop"];

          nwr(around:{self.radius},{latitude},{longitude})
          ["amenity"="restaurant"];

          nwr(around:{self.radius},{latitude},{longitude})
          ["tourism"="hotel"];

          way(around:{self.radius},{latitude},{longitude})
          ["highway"];
        );

        out center;
        """

        result = self.empty_result()

        details = {
            category: []
            for category in result
        }

        # Kept separate from the legacy name-only result.  Existing clients can
        # continue reading ``nearby.schools`` etc.; new clients can use the
        # coordinates and straight-line distance in ``nearby_details``.
        result["nearby_details"] = details

        try:
            response = requests.post(
                self.url,
                data=query,
                headers=self.headers,
                timeout=30,
            )

            response.raise_for_status()

            data = response.json()

        except requests.RequestException as exc:

            print(
                "Nearby intelligence request failed:",
                exc,
            )

            return result

        except ValueError as exc:

            print(
                "Nearby intelligence returned invalid JSON:",
                exc,
            )

            return result

        candidates = {
            "schools": [],
            "hospitals": [],
            "businesses": [],
            "banks": [],
            "restaurants": [],
            "hotels": [],
            "roads": [],
        }


        # ---------------------------------
        # Process OSM elements
        # ---------------------------------

        for item in data.get(
            "elements",
            []
        ):

            tags = item.get(
                "tags",
                {}
            )

            name = tags.get("name") or tags.get("ref")

            if not name:
                continue

            coordinates = self._element_coordinates(item)
            if coordinates is None:
                continue

            item_latitude, item_longitude = coordinates
            distance_meters = self._distance_meters(
                latitude, longitude, item_latitude, item_longitude
            )

            entry = {
                "name": name,
                "distance_meters": distance_meters,
                "coordinates": {
                    "latitude": item_latitude,
                    "longitude": item_longitude,
                },
                "osm_type": item.get("type"),
                "osm_id": item.get("id"),
            }


            # -----------------------------
            # Schools
            # -----------------------------

            if tags.get(
                "amenity"
            ) == "school":

                candidates["schools"].append(entry)


            # -----------------------------
            # Hospitals
            # -----------------------------

            elif tags.get(
                "amenity"
            ) == "hospital":

                candidates["hospitals"].append(entry)


            # -----------------------------
            # Banks
            # -----------------------------

            elif tags.get(
                "amenity"
            ) == "bank":

                candidates["banks"].append(entry)
                candidates["businesses"].append(entry)


            # -----------------------------
            # Restaurants
            # -----------------------------

            elif tags.get(
                "amenity"
            ) == "restaurant":

                candidates["restaurants"].append(entry)
                candidates["businesses"].append(entry)


            # -----------------------------
            # Hotels
            # -----------------------------

            elif tags.get(
                "tourism"
            ) == "hotel":

                candidates["hotels"].append(entry)
                candidates["businesses"].append(entry)


            # -----------------------------
            # Shops / businesses
            # -----------------------------

            elif "shop" in tags:

                candidates["businesses"].append(entry)


            # -----------------------------
            # Roads
            # -----------------------------

            elif "highway" in tags:

                candidates["roads"].append(entry)


        # ---------------------------------
        # Convert sets → sorted lists
        # ---------------------------------

        for category, entries in candidates.items():
            unique_entries = self._deduplicate(entries)
            result["nearby_details"][category] = unique_entries
            result[category] = [entry["name"] for entry in unique_entries]


        limits = {
            "schools": 10,
            "hospitals": 10,
            "businesses": 15,
            "banks": 10,
            "restaurants": 10,
            "hotels": 10,
            "roads": 10,
        }
        for category, limit in limits.items():
            result["nearby_details"][category] = (
                result["nearby_details"][category][:limit]
            )
            result[category] = [
                entry["name"]
                for entry in result["nearby_details"][category]
            ]


        return result

    @staticmethod
    def empty_result() -> dict:
        return {
            "schools": [],
            "hospitals": [],
            "businesses": [],
            "banks": [],
            "restaurants": [],
            "hotels": [],
            "roads": [],
        }

    @staticmethod
    def _element_coordinates(item: dict) -> tuple[float, float] | None:
        if "lat" in item and "lon" in item:
            return float(item["lat"]), float(item["lon"])

        center = item.get("center", {})
        if "lat" in center and "lon" in center:
            return float(center["lat"]), float(center["lon"])

        return None

    @staticmethod
    def _distance_meters(
        from_latitude: float,
        from_longitude: float,
        to_latitude: float,
        to_longitude: float,
    ) -> int:
        """Great-circle distance, rounded for display and sorting."""
        latitude_delta = radians(to_latitude - from_latitude)
        longitude_delta = radians(to_longitude - from_longitude)
        a = (
            sin(latitude_delta / 2) ** 2
            + cos(radians(from_latitude))
            * cos(radians(to_latitude))
            * sin(longitude_delta / 2) ** 2
        )
        return round(6_371_000 * 2 * asin(sqrt(a)))

    @staticmethod
    def _deduplicate(entries: list[dict]) -> list[dict]:
        nearest_by_name = {}
        for entry in entries:
            key = entry["name"].casefold()
            previous = nearest_by_name.get(key)
            if previous is None or entry["distance_meters"] < previous["distance_meters"]:
                nearest_by_name[key] = entry

        return sorted(
            nearest_by_name.values(),
            key=lambda entry: (entry["distance_meters"], entry["name"].casefold()),
        )
