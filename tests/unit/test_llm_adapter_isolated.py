"""Isolated unit tests for LLM Adapter (mocked endpoints for negative paths; labelled as MOCK/SYNTHETIC)."""
import json
import pytest
from unittest.mock import patch, MagicMock
import urllib.error

from agentos.core.llm_adapter import LocalAdapter, FakeAdapter, AdaptedResult


def test_fake_adapter_contract():
    adapter = FakeAdapter()
    res = adapter.call("prompt", "tier", "agent")
    assert isinstance(res, AdaptedResult)
    assert res.text == "FAKE"
    assert res.cost_estimate == 0.0
    assert "input_tokens" in res.usage


def test_local_adapter_mock_valid_parsing():
    """SYNTHETIC MOCK: Tests valid response parsing without live network."""
    adapter = LocalAdapter("http://mock-endpoint:11434")
    mock_payload = {
        "model": "qwen2.5:7b",
        "response": "Analysis complete: no security risks detected.",
        "prompt_eval_count": 25,
        "eval_count": 8,
        "done": True
    }
    mock_resp = MagicMock()
    mock_resp.read.return_value = json.dumps(mock_payload).encode("utf-8")
    mock_resp.__enter__.return_value = mock_resp
    mock_resp.__exit__.return_value = None

    with patch("urllib.request.urlopen", return_value=mock_resp):
        res = adapter.call("Analyze this text", "tier", "agent")
        assert res.text == "Analysis complete: no security risks detected."
        assert res.usage["input_tokens"] == 25
        assert res.usage["output_tokens"] == 8
        assert res.cost_estimate == 0.0


def test_local_adapter_mock_malformed_json():
    """SYNTHETIC MOCK: Verifies fail-closed behavior on malformed JSON."""
    adapter = LocalAdapter("http://mock-endpoint:11434")
    mock_resp = MagicMock()
    mock_resp.read.return_value = b"NOT_VALID_JSON{{"
    mock_resp.__enter__.return_value = mock_resp
    mock_resp.__exit__.return_value = None

    with patch("urllib.request.urlopen", return_value=mock_resp):
        res = adapter.call("Analyze this text", "tier", "agent")
        assert res.text.startswith("ERROR: endpoint call failed")
        assert "JSONDecodeError" in res.text


def test_local_adapter_mock_empty_output():
    """SYNTHETIC MOCK: Verifies empty response body handling."""
    adapter = LocalAdapter("http://mock-endpoint:11434")
    mock_payload = {"model": "qwen2.5:7b", "response": "", "prompt_eval_count": 10, "eval_count": 0}
    mock_resp = MagicMock()
    mock_resp.read.return_value = json.dumps(mock_payload).encode("utf-8")
    mock_resp.__enter__.return_value = mock_resp
    mock_resp.__exit__.return_value = None

    with patch("urllib.request.urlopen", return_value=mock_resp):
        res = adapter.call("Test empty", "tier", "agent")
        assert res.text == ""
        assert res.usage["output_tokens"] == 0


def test_local_adapter_mock_http_error():
    """SYNTHETIC MOCK: Verifies fail-closed behavior on HTTP 500 error."""
    adapter = LocalAdapter("http://mock-endpoint:11434")
    with patch("urllib.request.urlopen", side_effect=urllib.error.HTTPError("http://mock", 500, "Internal Server Error", {}, None)):
        res = adapter.call("Test error", "tier", "agent")
        assert res.text.startswith("ERROR: endpoint call failed")
        assert "HTTPError" in res.text


def test_local_adapter_mock_timeout():
    """SYNTHETIC MOCK: Verifies fail-closed behavior on TimeoutError."""
    adapter = LocalAdapter("http://mock-endpoint:11434")
    with patch("urllib.request.urlopen", side_effect=TimeoutError("Request timed out")):
        res = adapter.call("Test timeout", "tier", "agent")
        assert res.text.startswith("ERROR: endpoint call failed")
        assert "TimeoutError" in res.text


def test_local_adapter_mock_connection_refused():
    """SYNTHETIC MOCK: Verifies fail-closed behavior on URLError (connection refused)."""
    adapter = LocalAdapter("http://127.0.0.1:9999")  # Unreachable port
    with patch("urllib.request.urlopen", side_effect=urllib.error.URLError("Connection refused")):
        res = adapter.call("Test conn refused", "tier", "agent")
        assert res.text.startswith("ERROR: endpoint call failed")
        assert "URLError" in res.text
