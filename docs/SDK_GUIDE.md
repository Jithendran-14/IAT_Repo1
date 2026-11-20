# IAT Ingestion SDK context for this challenge

This project guide was checked against the installed `iat-rag-ingestion-sdk==3.0.6` implementation used by the working reference. It is not a replacement for licensed vendor documentation. The other SDK versions remain pinned for the shared environment.

## Concrete imports and responsibilities
`iat_rag_ingestion.core.core.IATIngestionPipeline` is the fluent builder. `iat_rag_ingestion.config.config_manager.ConfigManager` reads and validates the YAML. The project subclass `LocalIngestionPipeline` supplies a local-model indexer instead of OCI embedding authentication.

### Source selection
`with_loader(source_name=...)` asks the config manager for the matching key under `ingestion.sources`. The LocalStorage loader reads the configured directory and extensions. The name is a key, not a filesystem path. A missing key raises a source-not-found error.

### Parser and chunker
`with_parser()` adds the parser using the selected source configuration. `with_chunker()` creates the chunk processor from the `chunking` settings. The recursive text strategy splits on configured separators with controlled overlap. In this installed SDK, chunk overlap must be less than chunk size, and chunk size must be at least 100.

### Indexing
`with_indexer()` attaches the destination component. In this application, the provided override installs `LocalOracleVectorIndexer`, retaining Oracle persistence while using `LocalQwenEmbeddings`. That adapter is supplied infrastructure, not a participant task.

### Build versus process
`await builder.build()` produces a toolkit; it does not ingest. `await toolkit.process_documents_in_batches()` runs the configured producer/consumer stages. A toolkit without an indexer has no vector-writing consumer; the supplied runner detects this before starting processing. Do not remove the guard.

## Unrelated conceptual example
A policy-document pipeline might select a source named `office_policies`, parse text, apply a valid 300-character chunk size with 30-character overlap, attach an appropriate indexer, build, and then process. Those are example choices, not required values for this challenge.

## Follow the objects in your code
1. Open `example_ingest.py` and identify the builder chain.
2. Trace its source key into `ingestion_config.yaml`.
3. Inspect the recursive strategy's size, overlap and separators.
4. Find where the supplied indexer becomes part of the chain.
5. Distinguish successful assembly, processing statistics and verified database persistence.

## Installed reference locations
Use the active interpreter's package location, not a hardcoded trainer path. Under `iat_rag_ingestion`, inspect `core/core.py`, `config/config_manager.py`, `components/chunkers/strategies/text/recursive_chunker.py` and `components/indexers/oracle_indexer.py` if package source is available. Do not edit installed SDK files. Add your approved IAT documentation here before wider rollout.

## Learning check
Why can a pipeline build yet fail to index? What does overlap preserve? If size changes from 500 to 300 with valid overlap, what output differences do you expect? Verify rather than guess. Loading/indexing is not retrieval, and this round does not teach agent orchestration.

## Offline validation boundary
The installed SDK checks database connectivity during configuration construction. The supplied offline probe stubs database registration and blocks Oracle/HTTP operations. It validates real SDK configuration and pipeline assembly, but not database access, embedding or persistence. Live validation does not apply those stubs.
