# Verified version scope

The working reference pins Ingestion 3.0.6, Retrieval 1.1.22, Agent 2.6.3, Service 1.1.26 and Evaluation 1.1.22. The workshop retains its `uv.lock`.

The loader's configured-source lookup, ChunkConfig overlap validation, pipeline builder methods, toolkit processing and Oracle schema were inspected in the installed ingestion source. The local indexer/embedding adaptations are copied from the working reference, not asserted to be official local-model SDK APIs.

No new venv, SDK installation, original database access or model downloads are performed by generating this repository. Runtime confirmation and test results are recorded in the accompanying trainer review. Live completion still requires Oracle and Ollama.
