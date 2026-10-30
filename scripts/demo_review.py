"""Reproduce a synthetic local review session without external services."""
import json
import gc
import os
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from fastapi.testclient import TestClient
from api import app


def main():
    transcript = []
    previous = os.environ.get('CRITICALOPS_DB_PATH')
    previous_model = os.environ.pop('LLM_API_KEY', None)
    try:
        with TemporaryDirectory() as folder:
            os.environ['CRITICALOPS_DB_PATH'] = str(Path(folder) / 'demo.sqlite')
            with TestClient(app) as client:
                def step(label, method, path, expected, body=None):
                    response = client.request(method, path, json=body)
                    assert response.status_code == expected, (label, response.text)
                    data = response.json()
                    transcript.append({'step': label, 'method': method, 'path': path,
                                       'request': body, 'status': response.status_code, 'response': data})
                    return data
                ticket = {'incident_id':'DEMO-REVIEW-1', 'description':'Pump bearing vibration and unusual noise'}
                step('Intake', 'POST', '/api/incidents/triage', 200, ticket)
                step('Duplicate rejected', 'POST', '/api/incidents/triage', 409, ticket)
                review_path = '/api/incidents/DEMO-REVIEW-1/review'
                step('Request details', 'POST', review_path, 200, {'decision':'needs_more_information','expected_version':0,'comment':'Confirm observation time'})
                step('Stale review rejected', 'POST', review_path, 409, {'decision':'approved','expected_version':0})
                step('Approve current version', 'POST', review_path, 200, {'decision':'approved','expected_version':1,'comment':'Synthetic details reviewed'})
                final = step('Inspect final record', 'GET', '/api/incidents/DEMO-REVIEW-1', 200)
                assert final['version'] == 2 and final['review_status'] == 'approved'
                audit = step('Inspect history', 'GET', '/api/incidents/DEMO-REVIEW-1/audit', 200)
                assert len(audit) == 3
            # sqlite transaction context managers do not close connections;
            # release unreachable handles before Windows removes this temp DB.
            gc.collect()
        output = ROOT / 'evidence/local_review_demo.json'
        output.write_text(json.dumps({'scope':'Actual local TestClient run, synthetic data; no Microsoft integration or authenticated reviewer identity.', 'steps':transcript}, indent=2)+'\n')
        print(f'{len(transcript)} steps verified; transcript: {output.name}')
    finally:
        if previous is None:
            os.environ.pop('CRITICALOPS_DB_PATH', None)
        else:
            os.environ['CRITICALOPS_DB_PATH'] = previous
        if previous_model is not None:
            os.environ['LLM_API_KEY'] = previous_model


if __name__ == '__main__':
    main()
