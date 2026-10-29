"""Reproduce offline results without credentials or external model calls."""
import csv
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from core.evaluation import run_evaluation


def main():
    output = ROOT / "evidence"
    output.mkdir(exist_ok=True)
    summaries = {}
    for name, filename in [("baseline", "evaluation_cases.json"), ("challenge", "challenge_cases.json")]:
        cases = json.loads((ROOT / "data/demo" / filename).read_text())
        report = run_evaluation(cases)
        report["hash_encoding"] = "UTF-8 with LF newlines, BOM removed"
        report["dataset"] = filename
        report["dataset_sha256"] = hashlib.sha256((ROOT / "data/demo" / filename).read_text(encoding="utf-8-sig").encode("utf-8")).hexdigest()
        report["source_sha256"] = {str(p.relative_to(ROOT)).replace("\\", "/"): hashlib.sha256(p.read_text(encoding="utf-8-sig").encode("utf-8")).hexdigest() for p in sorted((ROOT / "core").glob("*.py"))}
        report["set_description"] = "Original regression baseline" if name == "baseline" else "Synthetic challenge set authored during development, not an independent real-world holdout"
        (output / f"{name}_results.json").write_text(json.dumps(report, indent=2) + "\n")
        with (output / f"{name}_results.csv").open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=list(report["results"][0]))
            writer.writeheader()
            writer.writerows(report["results"])
        summaries[name] = {k: v for k, v in report.items() if k not in {"results", "source_sha256"}}
    (output / "evaluation_summary.json").write_text(json.dumps(summaries, indent=2) + "\n")
    print(json.dumps(summaries, indent=2))


if __name__ == "__main__":
    main()
