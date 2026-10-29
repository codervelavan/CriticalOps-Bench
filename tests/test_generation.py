import pytest
import requests
from core import generation, triage


@pytest.mark.parametrize("failure", [requests.Timeout("secret-token"), ValueError("secret-token"), KeyError("secret-token")])
def test_provider_failures_use_safe_fallback(monkeypatch, failure):
    for key in ["LLM_BASE_URL", "LLM_API_KEY", "LLM_MODEL"]:
        monkeypatch.setenv(key, "configured")
    def fail(*args, **kwargs):
        raise failure
    monkeypatch.setattr(generation.requests, "post", fail)
    result = generation.generate_grounded_response("pump", "vibration", "medium", "demo", "queue", "review", [{"article_id":"SOP-1","title":"Demo","content":"Fictional"}], "fallback")
    assert result["text"] == "fallback"
    assert result["mode"] == "offline-template-fallback"
    assert "secret-token" not in result["error"]


def test_empty_model_response_uses_fallback(monkeypatch):
    for key in ["LLM_BASE_URL", "LLM_API_KEY", "LLM_MODEL"]:
        monkeypatch.setenv(key, "configured")
    class Response:
        def raise_for_status(self): pass
        def json(self): return {"choices":[{"message":{"content":" "}}]}
    monkeypatch.setattr(generation.requests, "post", lambda *a, **kw: Response())
    result = generation.generate_grounded_response("pump", "vibration", "medium", "demo", "queue", "review", [{"article_id":"SOP-1","title":"Demo","content":"Fictional"}], "fallback")
    assert result["text"] == "fallback"


@pytest.mark.parametrize("ticket", [{"description":"Motor smoke is visible"}, {"description":"QZX-999 purple icon"}])
def test_safety_and_insufficient_evidence_bypass_model(monkeypatch, ticket):
    def unexpected(**kwargs): raise AssertionError("Model must not be called")
    monkeypatch.setattr(triage, "generate_grounded_response", unexpected)
    assert triage.triage_incident(ticket)["human_review_required"]
