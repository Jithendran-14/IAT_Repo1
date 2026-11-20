# Published acceptance criteria

1. The original `.txt` sample remains discoverable.
2. Chunk configuration satisfies actual installed SDK constraints.
3. The participant builder assembles real IAT loader/parser/chunker components and the supplied Oracle indexer adaptation.
4. Live processing calls the real embedding service and writes non-empty chunks into a fresh workshop-only table.
5. Persisted vectors have 1024 dimensions; chunk text and chunk identity metadata are present.
6. Output covers the source vocabulary; database row count agrees with successful indexer statistics; failed chunks are zero.
7. A separate database connection can read the output.
8. Missing pipeline stages fail clearly before queued processing, rather than hanging.
9. Completion refuses missing, failed or stale local results and rechecks live output.

Code-only tests are not live completion. An unavailable database/model or missing credentials is an environment blocker, not proof the participant solution is wrong. Exact chunk counts and identical source-code patches are not graded.

Facilitator: verify the submitted immutable commit with trusted tests/runtime copies, fresh table namespace and expected unchanged source. Local JSON/reports are not scoring evidence on their own.
