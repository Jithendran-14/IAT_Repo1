from iat_rag_ingestion.components.indexers.base import BaseIndexer
from iat_rag_ingestion.components.indexers.oracle_indexer import (
    OracleVectorIndexer,
)

from local_embeddings import LocalQwenEmbeddings


class LocalOracleVectorIndexer(OracleVectorIndexer):
    """Project-local adaptation of IAT Ingestion SDK 3.0.6."""

    def __init__(self, config, db_config, **additional_kwargs):
        # Initialize the base without creating the OCI embedding client.
        BaseIndexer.__init__(self)

        self.config = config
        self.db_config = db_config
        self.db_table_name = db_config.embeddings_table_name
        self.embeddings = LocalQwenEmbeddings()
        self.stats = {
            "total_chunks": 0,
            "indexed_chunks": 0,
            "failed_chunks": 0,
        }
        self.lexical_config = additional_kwargs.get("lexical_config")

    async def _embed_documents_with_auth_retry(self, texts):
        # Local Ollama calls do not use OCI authentication or token refresh.
        return await self.embeddings.aembed_documents(texts)

    def _reload_embeddings_client(self):
        self.embeddings = LocalQwenEmbeddings()

    async def cleanup(self):
        # The adapter closes its HTTP client after each request.
        pass