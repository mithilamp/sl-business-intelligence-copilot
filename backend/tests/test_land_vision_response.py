from unittest.mock import Mock

import pytest

from app.agents.land_agent import LandAgent
from app.land.vision import LandVisionAnalyzer, LandVisionResponseError


def test_vision_analyzer_rejects_an_empty_model_response(tmp_path):
    image = tmp_path / "survey.png"
    image.write_bytes(b"image")

    choice = Mock()
    choice.message.content = ""
    choice.message.refusal = None
    choice.finish_reason = "stop"
    analyzer = LandVisionAnalyzer.__new__(LandVisionAnalyzer)
    analyzer.client = Mock()
    analyzer.client.chat.completions.create.return_value.choices = [choice]

    with pytest.raises(LandVisionResponseError, match="returned no"):
        analyzer.analyze(str(image))


def test_land_agent_rejects_invalid_json_before_enrichment():
    agent = LandAgent.__new__(LandAgent)
    agent.parser = Mock()
    agent.parser.parse.return_value = ["survey.png"]
    agent.vision = Mock()
    agent.vision.analyze.return_value = "not JSON"

    with pytest.raises(LandVisionResponseError, match="invalid"):
        agent.analyze("survey.png")


def test_land_agent_traced_steps_preserve_analysis_flow():
    agent = LandAgent.__new__(LandAgent)
    agent.parser = Mock()
    agent.parser.parse.return_value = ["survey.png"]
    agent.vision = Mock()
    agent.vision.analyze.return_value = '{"location_information": ["Kandy, Sri Lanka"]}'
    agent.location_normalizer = Mock()
    agent.location_normalizer.normalize.return_value = {"search_query": "Kandy, Sri Lanka", "confidence": "high"}
    agent.geo = Mock()
    agent.geo.locate.return_value = {"found": True}
    agent.business_analyzer = Mock()
    agent.business_analyzer.analyze.return_value.model_dump.return_value = {"opportunities": []}
    agent.report_builder = Mock()
    agent.report_builder.build.return_value.model_dump.return_value = {"property_summary": {}}

    result = agent.analyze("survey.png")

    agent.parser.parse.assert_called_once_with("survey.png")
    agent.vision.analyze.assert_called_once_with("survey.png")
    agent.location_normalizer.normalize.assert_called_once_with(["Kandy, Sri Lanka"])
    agent.geo.locate.assert_called_once_with("Kandy, Sri Lanka", source_confidence="high")
    agent.business_analyzer.analyze.assert_called_once()
    agent.report_builder.build.assert_called_once()
    assert result["pages_processed"] == 1
