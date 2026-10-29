# Local connector definition

`criticalops.swagger.json` is an OpenAPI 2.0 definition generated from typed FastAPI routes. It covers triage, incident reads, reviews, audit history and metrics. Swagger validation and actual TestClient response-schema checks are automated.

```sh
python scripts/build_connector.py
pytest tests/test_connector.py -q
```

Status: locally validated only; not imported or exercised in Power Platform. The localhost HTTP host and absence of authentication are local-demo settings. A live connector requires an authorised reachable HTTPS host or suitable gateway, authentication, licensed environment access and actual platform tests.

A custom connector is a possible option because this prototype has its own incident API. No comparison against a customer's standard connector has been performed.

Review requests include `expected_version`, initially 0. Re-read the incident before follow-up review and send its current version. Missing IDs return 404; stale/finalised reviews and duplicate IDs return 409; invalid payloads return 422. Reviewer identity remains an unverified demo label.

Reference: https://learn.microsoft.com/en-us/connectors/custom-connectors/faq
