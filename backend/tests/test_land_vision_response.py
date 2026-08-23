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
