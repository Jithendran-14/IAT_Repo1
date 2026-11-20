"""Run the participant pipeline and verify its real, isolated Oracle output."""
import asyncio
import json
import os
from datetime import datetime,timezone
from pathlib import Path
import uuid
from workshop.common import ROOT,load_config,sources,fingerprint,prepare_config,safe_table,verify_rows,write_json

def require_credentials():
    missing=[n for n in ('IAT_RAG_USER','IAT_RAG_PASSWORD') if not os.environ.get(n)]
    if missing:
        raise RuntimeError('Missing environment variables: '+', '.join(missing)+'. See WORKSHOP_ENVIRONMENT_SETUP.md.')

def read_persisted(table):
    import oracledb
    require_credentials()
    with oracledb.connect(user=os.environ['IAT_RAG_USER'],password=os.environ['IAT_RAG_PASSWORD'],dsn=os.environ.get('IAT_RAG_DSN','localhost:1521/FREEPDB1')) as connection:
        with connection.cursor() as cursor:
            cursor.execute(f'SELECT text, VECTOR_DIMENSION_COUNT(embedding), metadata FROM {safe_table(table)} ORDER BY id')
            return [(text.read() if hasattr(text,'read') else text,dims,metadata.read() if hasattr(metadata,'read') else metadata) for text,dims,metadata in cursor]

def check_components(toolkit):
    missing=[name for name in ('loader','parser','chunker','indexer') if getattr(toolkit,name,None) is None]
    if missing:
        raise RuntimeError('Pipeline cannot run: missing component(s): '+', '.join(missing)+'. No processing was started. Consult SDK_GUIDE.md.')

async def ingest():
    from example_ingest import build_toolkit
    require_credentials()
    before=fingerprint()
    run_dir=ROOT/'work'/'runs'/uuid.uuid4().hex
    config_path,table=prepare_config(run_dir)
    toolkit=await build_toolkit(config_path)
    check_components(toolkit)
    print('Running real IAT ingestion into fresh workshop table:',table,flush=True)
    await asyncio.wait_for(toolkit.process_documents_in_batches(),timeout=300)
    stats=dict(toolkit.indexer.stats)
    if stats.get('failed_chunks',0) or stats.get('indexed_chunks',0)<1:
        raise RuntimeError('Indexer did not report a completely successful non-empty write.')
    original='\n'.join(p.read_text(encoding='utf-8') for p in sources(load_config()))
    verified=verify_rows(read_persisted(table),original)
    if verified['persisted_chunks'] != stats['indexed_chunks']:
        raise RuntimeError('Persisted chunk count differs from this run’s indexing result.')
    if before != fingerprint():
        raise RuntimeError('Source or implementation changed during execution. Re-run validation.')
    report={'stage':'repo1-ingestion','status':'live_verified','provisional':True,'timestamp':datetime.now(timezone.utc).isoformat(),'fingerprint':before,'table':table,'config_path':str(config_path.relative_to(ROOT)),'source_documents':len(sources(load_config())),'indexer_statistics':stats,'verification':verified}
    write_json(run_dir/'result.json',report)
    write_json(ROOT/'work'/'latest_result.json',report)
    print(json.dumps(report,indent=2))
    return report

def cli_ingest():
    try:
        asyncio.run(ingest())
        print('Live ingestion verified. Run: python scripts/completion_report.py')
        return 0
    except Exception as exc:
        # Do not echo database exception strings, which may contain connection details.
        print('Ingestion did not complete. Error category:',type(exc).__name__)
        if isinstance(exc,(ValueError,RuntimeError,TimeoutError)):
            print(str(exc))
        else:
            print('Review SDK logs locally and TROUBLESHOOTING.md; do not share secrets.')
        return 1

def completion():
    report_path=ROOT/'work'/'latest_result.json'
    if not report_path.exists():
        raise RuntimeError('No successful live result. Run python scripts/validate_local.py --live first.')
    report=json.loads(report_path.read_text(encoding='utf-8'))
    if report.get('status')!='live_verified' or report.get('fingerprint')!=fingerprint():
        raise RuntimeError('Result is missing, failed or stale. Re-run live validation.')
    original='\n'.join(p.read_text(encoding='utf-8') for p in sources(load_config()))
    evidence=verify_rows(read_persisted(report['table']),original)
    if evidence['persisted_chunks']!=report['verification']['persisted_chunks']:
        raise RuntimeError('Stored output changed after validation; run again.')
    print('\nREPO 1 COMPLETE — LOCAL RESULT (PROVISIONAL)')
    print('What was wrong: the starter selected a non-existent loader source, used invalid chunk overlap, and omitted the indexer.')
    print('What the working correction requires: a configured source, valid chunk settings, and a complete loader/parser/chunker/indexer pipeline.')
    print('How it works: local documents -> IAT loader -> parser -> recursive chunker -> supplied local embeddings -> Oracle indexing.')
    print('SDK concept: fluent builder methods connect stages; the YAML selects source, chunk strategy, and destination. Loading alone does not persist searchable vectors.')
    print('Verified now:',json.dumps(evidence))
    print('Next: Repo 2 will use the indexed knowledge through the Retrieval SDK. Its reference baseline may differ from your valid implementation.')
    print('Understanding check: explain the source-name binding and change chunk size while keeping valid overlap. Re-run and compare output.')
    print('Official completion and the next repository link come from the facilitator. This report cannot award points or unlock anything.')
    return report
