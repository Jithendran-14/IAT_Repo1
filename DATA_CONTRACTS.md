# Repo 1 contracts

## Pipeline
Provide `async build_toolkit(config_path)` returning the assembled IAT toolkit. Loader, parser, chunker and indexer must all be present. Preserve the entry point so supplied validation can exercise behaviour without requiring identical implementation text.

## Input
The configured source is a repository-local directory of UTF-8 `.txt` documents. The original `documents/sample.txt` must remain present and unchanged for the trial. It documents order-management APIs, not actual customer data. Blank or unsupported files are outside the required trial fixture; full unsupported/empty-document ingestion semantics are not claimed.

## Chunk configuration
Use the supplied recursive text strategy. For the installed SDK, `chunk_size` is an integer >=100 and `0 <= chunk_overlap < chunk_size`. Chunk sizes are character-based for this strategy, not an exact token count. Source names in builder configuration must resolve to declared source keys.

## Output
Each live run uses an isolated embeddings table with the SDK schema: numeric ID, text CLOB, embedding VECTOR, metadata CLOB and supporting SDK columns. Every row must have non-empty text, a 1024-dimensional vector and valid JSON metadata containing `chunk_id`. Chunk numbers and strategy metadata come from the SDK. Row IDs alone are not document-version provenance; richer citations can be introduced in later workshop preparation.

All source vocabulary must be represented in the output. This trial's lexical coverage check is a useful smoke check, not a guarantee of semantic retrieval quality. The stored row count must match successful indexing statistics and failed chunks must be zero.

## Persistence and attempts
Verification opens a separate Oracle connection after ingestion. Fresh per-attempt tables prevent old data from masking failure; the runner never truncates or drops a table. Re-running creates another dataset. This **does not claim idempotent ingestion into one persistent table**. Record the latest verified table for the facilitator; Repo 2 will have its own reproducible reference baseline.

## Local report
`work/latest_result.json` records run namespace, UTC timestamp, implementation/source fingerprint and verification results. It excludes credentials. It is provisional and participant-editable; official grading must re-run trusted checks independently.
