from iat_rag_ingestion.core.core import IATIngestionPipeline
from local_indexer import LocalOracleVectorIndexer


class LocalIngestionPipeline(IATIngestionPipeline):
    """Supplied local-Ollama indexer adaptation; not a challenge defect."""
    def with_indexer(self):
        indexing = self.config_manager.indexing_config
        database = self.config_manager.config.databases[indexing.vector_store]
        self._indexer = LocalOracleVectorIndexer(
            indexing, database, lexical_config=indexing.lexical_store
        )
        return self


async def build_toolkit(config_path):
    """Participant workspace: assemble the installed IAT ingestion components."""
    return await (
        LocalIngestionPipeline(config_path=str(config_path))
        .with_loader(source_name="workshop_documents")
        .with_parser()
        .with_chunker()
        .build()
    )


if __name__ == "__main__":
    from workshop.runtime import cli_ingest
    raise SystemExit(cli_ingest())
