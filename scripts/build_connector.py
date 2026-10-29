"""Export a local-only Swagger 2 connector contract from the typed FastAPI routes."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from api import app


def schema_v2(value):
    if isinstance(value, list):
        return [schema_v2(item) for item in value]
    if not isinstance(value, dict):
        return value
    value = dict(value)
    if "anyOf" in value:
        variants = [v for v in value.pop("anyOf") if v.get("type") != "null"]
        if len(variants) == 1:
            value.update(variants[0])
            value["x-nullable"] = True
        else:
            # JSON scalar union (validation error locations): unconstrained schema.
            return {}
    if value.get("default", object()) is None:
        value.pop("default")
    return {key: (item.replace("#/components/schemas/", "#/definitions/") if key == "$ref" else schema_v2(item))
            for key, item in value.items() if key not in {"examples"}}


def build_connector():
    source = app.openapi()
    paths = {}
    for path, methods in source["paths"].items():
        if not (path.startswith("/api/incidents") or path == "/api/metrics"):
            continue
        paths[path] = {}
        for method, operation in methods.items():
            result = {key: operation[key] for key in ("operationId", "summary", "description") if key in operation}
            parameters = []
            for parameter in operation.get("parameters", []):
                item = {k: v for k, v in parameter.items() if k != "schema"}
                item.update(schema_v2(parameter["schema"]))
                item.pop("title", None)
                parameters.append(item)
            if "requestBody" in operation:
                body = operation["requestBody"]
                parameters.append({"in": "body", "name": "body", "required": body.get("required", False),
                                   "schema": schema_v2(body["content"]["application/json"]["schema"])})
            result["parameters"] = parameters
            result["responses"] = {}
            for status, response in operation["responses"].items():
                item = {"description": response.get("description", "Response")}
                if "application/json" in response.get("content", {}):
                    item["schema"] = schema_v2(response["content"]["application/json"]["schema"])
                result["responses"][status] = item
            paths[path][method] = result
    return {"swagger": "2.0", "info": {"title": "CriticalOps local connector prototype", "version": app.version,
            "description": "Locally validated definition only. No Power Platform import or live integration is asserted. Unauthenticated synthetic demo; do not expose publicly."},
            "host": "localhost:8000", "basePath": "/", "schemes": ["http"], "consumes": ["application/json"],
            "produces": ["application/json"], "paths": paths,
            "definitions": {k: schema_v2(v) for k, v in source["components"]["schemas"].items()}}


if __name__ == "__main__":
    target = ROOT / "connectors/criticalops.swagger.json"
    target.write_text(json.dumps(build_connector(), indent=2) + "\n", encoding="utf-8")
    print(target)
