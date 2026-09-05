from unittest.mock import Mock, patch

from app.land.geolocation import GeoLocationService
from app.land.nearby import NearbyIntelligence


def _response(payload):
    response = Mock()
    response.raise_for_status.return_value = None
    response.json.return_value = payload
    return response


@patch("app.land.geolocation.requests.get")
def test_province_result_is_coarse_even_when_the_full_query_matches(mock_get):
    mock_get.return_value = _response([
        {
            "lat": "7.8731",
            "lon": "80.7718",
            "addresstype": "province",
            "display_name": "A province, Sri Lanka",
        }
    ])
    service = GeoLocationService()
    service.nearby.find_nearby = Mock(return_value=service.nearby.empty_result())

    result = service.locate("A province, Sri Lanka")

    assert result["accuracy"] == "coarse"
    assert result["match_quality"] == "coarse"
    assert result["confidence"] == "low"
    assert result["location_level"] == "province"


@patch("app.land.geolocation.requests.get")
def test_fallback_to_a_village_is_reported_as_local_not_exact(mock_get):
    mock_get.side_effect = [
        _response([]),
        _response([
            {
                "lat": "6.9271",
                "lon": "79.8612",
                "addresstype": "village",
                "display_name": "A village, Sri Lanka",
            }
        ]),
    ]
    service = GeoLocationService()
    service.nearby.find_nearby = Mock(return_value=service.nearby.empty_result())

    result = service.locate("Survey lot, A village, Sri Lanka")

    assert result["accuracy"] == "fallback"
    assert result["match_quality"] == "local"
    assert result["confidence"] == "medium"


@patch("app.land.nearby.requests.post")
def test_nearby_results_include_distance_and_keep_legacy_name_lists(mock_post):
    mock_post.return_value = _response({
        "elements": [
            {
                "type": "node",
                "id": 2,
                "lat": 6.001,
                "lon": 80.0,
                "tags": {"amenity": "school", "name": "Far School"},
            },
            {
                "type": "node",
                "id": 1,
                "lat": 6.0002,
                "lon": 80.0,
                "tags": {"amenity": "school", "name": "Near School"},
            },
            {
                "type": "way",
                "id": 3,
                "center": {"lat": 6.0005, "lon": 80.0},
                "tags": {"highway": "primary", "ref": "A1"},
            },
        ]
    })

    result = NearbyIntelligence().find_nearby(6.0, 80.0)

    assert result["schools"] == ["Near School", "Far School"]
    assert result["nearby_details"]["schools"][0]["distance_meters"] < 100
    assert result["roads"] == ["A1"]
    assert result["nearby_details"]["roads"][0]["osm_type"] == "way"
