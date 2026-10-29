import json
from pathlib import Path
from fastapi.testclient import TestClient
from jsonschema import Draft4Validator, RefResolver
from openapi_spec_validator import OpenAPIV2SpecValidator
from api import app
from scripts.build_connector import build_connector

ROOT = Path(__file__).resolve().parents[1]


def test_swagger_contract_valid_and_matches_export():
    spec = build_connector()
    OpenAPIV2SpecValidator(spec).validate()
    assert json.loads((ROOT / "connectors/criticalops.swagger.json").read_text()) == spec
    ids = [op["operationId"] for path in spec["paths"].values() for op in path.values()]
    assert len(ids) == len(set(ids))
    assert spec["swagger"] == "2.0"
    assert spec["host"].startswith("localhost")


def test_connector_schemas_match_real_api_responses(tmp_path, monkeypatch):
    monkeypatch.setenv("CRITICALOPS_DB_PATH", str(tmp_path / "connector.sqlite"))
    spec = build_connector()
    resolver = RefResolver.from_schema(spec)
    def check(path, method, code, response):
        assert response.status_code == code
        schema = spec["paths"][path][method]["responses"][str(code)]["schema"]
        # Swagger x-nullable is an extension; JSON Schema needs explicit null support.
        def nullable(v):
            if isinstance(v, list): return [nullable(x) for x in v]
            if not isinstance(v, dict): return v
            v = {k: nullable(x) for k, x in v.items()}
            if v.pop("x-nullable", False): return {"anyOf": [v, {"type": "null"}]}
            return v
        adjusted = nullable(spec)
        Draft4Validator(nullable(schema), resolver=RefResolver.from_schema(adjusted)).validate(response.json())
    with TestClient(app) as client:
        payload = {"incident_id":"CONNECTOR-1", "description":"Pump bearing vibration"}
        check("/api/incidents/triage", "post", 200, client.post("/api/incidents/triage", json=payload))
        check("/api/incidents/triage", "post", 409, client.post("/api/incidents/triage", json=payload))
        check("/api/incidents/triage", "post", 422, client.post("/api/incidents/triage", json={"description":"bad"}))
        check("/api/incidents/{incident_id}", "get", 200, client.get("/api/incidents/CONNECTOR-1"))
        check("/api/incidents/{incident_id}/review", "post", 200, client.post("/api/incidents/CONNECTOR-1/review", json={"decision":"approved", "expected_version":0}))
        check("/api/incidents/{incident_id}/review", "post", 409, client.post("/api/incidents/CONNECTOR-1/review", json={"decision":"rejected", "expected_version":0}))
        check("/api/incidents/{incident_id}/audit", "get", 200, client.get("/api/incidents/CONNECTOR-1/audit"))
        check("/api/incidents", "get", 200, client.get("/api/incidents"))
        check("/api/metrics", "get", 200, client.get("/api/metrics"))
        check("/api/incidents/{incident_id}", "get", 404, client.get("/api/incidents/UNKNOWN"))

