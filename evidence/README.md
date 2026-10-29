# Reproducible prototype verification

Run `python scripts/evaluate.py` to regenerate JSON/CSV results and `pytest -q` for software and API/connector checks. GitHub Actions publishes its own verification artifact. A committed JUnit file records a local run.

| Set | Category matches | Priority matches | Safety routing | Retrieval hit at 3 |
|---|---:|---:|---:|---:|
| Original synthetic baseline | 12/13 | 13/13 | 4/4 | Not labelled |
| Synthetic challenge set | 30/36 | 36/36 | 6/6 | 26/30 labelled source queries |

Challenge MRR@3: 0.8444. Fallback precision: 5/8 (62.5%); fallback recall: 5/6 (83.3%). Six expected-unsupported questions are included in fallback evaluation and excluded from source-hit/MRR denominators.

The 36 challenge cases were authored during development, six per expected category. They include ambiguity, paraphrases, insufficient information and safety concerns. They are not an independent holdout or customer data. Labels are author expectations rather than proof of operational safety.

Evaluation disables external LLM calls. Results measure rules, lexical candidate retrieval and abstention, not LLM grounding or Copilot Studio. Retrieval hit@3 does not prove a generated answer is supported.

Known failures include symptom paraphrases without matching keywords, sensor/equipment ambiguity and an unsupported threshold request that nevertheless retrieves a source. Failures remain in CSV/JSON, including original case EVAL-013. Production performance and productivity savings remain unvalidated.

Source/dataset hashes use UTF-8 with LF newlines and no BOM for Windows/Linux reproducibility. No credentials, private tickets or candidate records are included.
