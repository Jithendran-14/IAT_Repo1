"""SDK-backed assembly check with database registration explicitly stubbed."""
import asyncio
import os
from pathlib import Path
import sys
import tempfile
from unittest.mock import patch, AsyncMock
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from workshop.common import ROOT,prepare_config
from workshop.runtime import check_components

async def main():
    os.environ.setdefault('IAT_RAG_USER','OFFLINE_CONFIG_ONLY')
    os.environ.setdefault('IAT_RAG_PASSWORD','OFFLINE_CONFIG_ONLY')
    from example_ingest import build_toolkit
    from iat_rag_ingestion.components.indexers.oracle_indexer import OracleVectorIndexer
    (ROOT/'work').mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='assembly-',dir=ROOT/'work') as directory:
        config,_=prepare_config(Path(directory))
        # This SDK eagerly checks Oracle login from AppConfig validation.
        # Skip only registration/connectivity in this explicitly offline test.
        # All actual config, source lookup, builder, loader/parser/chunker and
        # local indexer construction remain real SDK behaviour.
        with patch('iat_rag_ingestion.core.db_connection_manager.get_db_manager',return_value=None), \
             patch('oracledb.connect',side_effect=AssertionError('Oracle calls forbidden in offline probe')), \
             patch('oracledb.create_pool',side_effect=AssertionError('Oracle pools forbidden in offline probe')), \
             patch('oracledb.create_pool_async',side_effect=AssertionError('Oracle pools forbidden in offline probe')), \
             patch('httpx.AsyncClient.send',new=AsyncMock(side_effect=AssertionError('HTTP calls forbidden in offline probe'))):
            toolkit=await build_toolkit(config)
            check_components(toolkit)
            assert toolkit.loader.__class__.__module__.startswith('iat_rag_ingestion.')
            assert toolkit.parser.__class__.__module__.startswith('iat_rag_ingestion.')
            assert toolkit.chunker.__class__.__module__.startswith('iat_rag_ingestion.')
            assert isinstance(toolkit.indexer,OracleVectorIndexer)
            await toolkit.indexer.cleanup()
    print('PASS: real SDK stages assembled; database-registration hook stubbed. No live persistence verified.')
if __name__=='__main__':
    try:asyncio.run(main())
    except Exception as exc:
        print('SDK assembly check failed:',type(exc).__name__,str(exc));raise SystemExit(1)
