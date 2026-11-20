# Crack the Code — Repo 1: Restore Ingestion

Trial application: an API-documentation RAG assistant. This round builds its knowledge index; it is **not the UPI application**.

## Start here
1. Follow [the shared environment guide](WORKSHOP_ENVIRONMENT_SETUP.md). Reuse that environment for every future round.
2. Run `python scripts/preflight.py`. For live checks, configure credentials and run `python scripts/preflight.py --services`.
3. Read [the challenge](CHALLENGE.md), [contracts](DATA_CONTRACTS.md), and [SDK guide](docs/SDK_GUIDE.md).
4. Repair `example_ingest.py` and `ingestion_config.yaml`.
5. Run `python scripts/validate_local.py --code-only` for configuration and real-SDK assembly feedback.
6. Run `python scripts/validate_local.py --live` for real embedding, fresh-table ingestion and completion feedback.
7. To recheck saved output later, run `python scripts/completion_report.py`.

Run commands from this repository root. The supplied runner resolves document paths independently of your shell directory. Do not run `uv run` without configuring the shared environment; it may create a repo-local environment.

## What is supplied
- Original sample API documentation and local Ollama embedding/Oracle indexer adapters.
- Five pinned IAT dependencies and the original resolved `uv.lock`, shared with later stages.
- SDK-context documentation, hints, public tests and a conditional completion explanation.
- Fresh Oracle tables for each live attempt, using `IAT_R1_E_<run-id>` and `IAT_R1_S_<run-id>`. The original application's tables are never cleared or reused.

## Expected progress
The starter **must fail**: there are three SDK integration defects. A failed code check is not an environment failure. Work through the observed errors, fix the integration and run again.

A correct implementation reads the sample, parses and chunks it, generates local embeddings and persists verified chunks to Oracle. Exact chunk counts can vary with a valid configuration. No retrieval, agent, UI or Service SDK coding is required in Round 1.

`work/latest_result.json` holds a provisional local result. No local script awards official points or unlocks repositories. Submit your commit and explain your changes to the facilitator, who releases Repo 2 manually.

## Repository layout
`example_ingest.py` — participant pipeline assembly; `ingestion_config.yaml` — participant configuration; `local_*.py` — supplied infrastructure; `workshop/` and `scripts/` — feedback/runtime support; `tests/public/` — visible checks; `documents/` — sample input.

Do not publish credentials, `.venv`, generated configs or `work/` data. Keep this internal trial private and follow your organisation's repository/data policies.
