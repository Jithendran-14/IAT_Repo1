# Round 1 — Why is the knowledge index not being built?

## Goal
Repair the actual IAT Ingestion SDK integration. Learn source selection, recursive chunking configuration and builder-stage composition.

## Symptoms
The starter cannot produce a verified index. You may encounter a configuration validation error, a source lookup failure, and a pipeline with a missing component as you fix successive blockers. There are **three intentional defects** in the participant files.

## Change area
- `ingestion_config.yaml`
- The assembly inside `build_toolkit()` in `example_ingest.py`

You may choose any valid chunk size of at least 100 and non-negative overlap smaller than that size. Keep recursive chunking for this trial. Equivalent SDK-based solutions are acceptable; do not copy a specific patch merely to satisfy string matching.

## Supplied, not broken
`LocalIngestionPipeline.with_indexer()` adapts the original Oracle indexer to local Ollama embeddings. Its private-field usage is a project-local adapter for ingestion SDK 3.0.6, not a general public extension guarantee. Keep it and `local_embeddings.py` unchanged for this trial. Runtime safety checks, tests and completion scripts are not the challenge.

## Finish
Pass code-only checks, run live validation, inspect the persisted result, then explain how the stages connect. The completion explanation appears only after current implementation and Oracle output validate. A later repo starts from the trainer's correct baseline, even if your valid solution differs.
