# Environment help

- **Chunk configuration or source-not-found error:** likely part of the intended exercise. Use the SDK guide and progressive hints.
- **Missing pipeline component:** the guard prevented queued processing without a consumer. Repair assembly; do not disable the guard.
- **No module named iat_rag_ingestion:** wrong interpreter or missing internal dependencies. Follow the shared-environment guide.
- **Oracle user/password missing:** set process environment variables. `.env.example` is not auto-loaded.
- **ORA-01017 / connection / quota / VECTOR error:** ask the facilitator to check the workshop schema and database. Do not change the original application's tables.
- **Ollama unavailable/model absent:** start the supplied service and confirm the embedding model. Configuration defects do not require changing its adapter.
- **Wrong vector dimension:** use the documented embedding model; this storage contract expects 1024.
- **Code checks pass but completion fails:** offline assembly is not live persistence. Run `validate_local.py --live` with services ready.
- **Completion report stale:** code/config/sample changed after ingestion. Re-run live validation.
- **Repeated runs create more tables:** intentional fresh namespaces prevent false success. Ask the facilitator to clean the trial tables after review. No automatic destructive cleanup is supplied.
- **No evidence for full live verification in the delivered scaffold:** a trainer must exercise the repaired reference with supplied Oracle credentials before distributing this as a timed event.

Never paste credentials or complete sensitive logs into ChatGPT/screenshares. This trial fixture is synthetic. All AI assistance is allowed, but you must explain your fix.

The code-only probe stubs the SDK database-registration hook because this SDK tests credentials during config validation. Do not apply this stub to the real ingestion path.
