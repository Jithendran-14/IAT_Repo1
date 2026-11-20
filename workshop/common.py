"""Supplied exercise infrastructure. This is application code, not IAT SDK API."""
from pathlib import Path
import hashlib
import json
import os
import re
import uuid
import yaml

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_PACKAGES = {
    "iat-agent-sdk": "2.6.3", "iat-evaluation-sdk": "1.1.22",
    "iat-rag-ingestion-sdk": "3.0.6", "iat-rag-retrieval-sdk": "1.1.22",
    "iat-service-sdk": "1.1.26",
}

def load_config(path=None):
    config = yaml.safe_load(Path(path or ROOT/'ingestion_config.yaml').read_text(encoding='utf-8'))
    if not isinstance(config, dict):
        raise ValueError('The YAML must contain a mapping.')
    return config

def check_chunk_settings(config):
    text = config['chunking']['strategies']['text']
    size, overlap = text['chunk_size'], text['chunk_overlap']
    if type(size) is not int or size < 100:
        raise ValueError('chunk_size must be an integer of at least 100 for this SDK.')
    if type(overlap) is not int or not 0 <= overlap < size:
        raise ValueError('Invalid chunking configuration. Read docs/SDK_GUIDE.md and hints/README.md.')
    if text['type'] != 'recursive':
        raise ValueError('This trial targets the supplied recursive chunking strategy.')

def sources(config):
    entries=[]
    for value in config['ingestion']['sources'].values():
        directory=(ROOT / value['directory_path']).resolve()
        if not directory.is_relative_to(ROOT):
            raise ValueError('Document sources must stay within this repository.')
        if not directory.is_dir():
            raise ValueError('Configured source directory does not exist.')
        patterns=value.get('file_extensions',['.txt'])
        candidates=directory.rglob('*') if value.get('include_subdirectories',False) else directory.iterdir()
        entries.extend(p for p in candidates if p.is_file() and p.suffix in patterns)
    if not entries:
        raise ValueError('No supported source documents found.')
    return sorted(set(entries))

def fingerprint():
    paths=[ROOT/'example_ingest.py',ROOT/'ingestion_config.yaml',ROOT/'local_indexer.py',ROOT/'local_embeddings.py']
    paths += sorted((ROOT/'documents').glob('*.txt'))
    digest=hashlib.sha256()
    for path in paths:
        digest.update(path.relative_to(ROOT).as_posix().encode())
        digest.update(path.read_bytes())
    return digest.hexdigest()

def safe_table(value):
    if not re.fullmatch(r'IAT_R1_[ES]_[0-9A-F]{12}', value):
        raise ValueError('Only generated Repo 1 workshop table names are allowed.')
    return value

def prepare_config(directory, config_path=None):
    """Use new tables every run; never clear or reuse the original example tables."""
    config=load_config(config_path)
    check_chunk_settings(config)
    sources(config)
    for source in config['ingestion']['sources'].values():
        source['directory_path']=str((ROOT/source['directory_path']).resolve())
    config['chunking']['max_workers']=1
    db=config['databases'][config['indexer']['vector_store']]
    run_id=uuid.uuid4().hex[:12].upper()
    db['dsn']=os.environ.get('IAT_RAG_DSN','localhost:1521/FREEPDB1')
    db['embeddings_table_name']=safe_table('IAT_R1_E_'+run_id)
    db['source_table_name']=safe_table('IAT_R1_S_'+run_id)
    directory.mkdir(parents=True,exist_ok=True)
    target=directory/'resolved_config.yaml'
    target.write_text(yaml.safe_dump(config,sort_keys=False),encoding='utf-8')
    return target,db['embeddings_table_name']

def verify_rows(rows, source_text):
    if not rows:
        raise ValueError('No persisted chunks found in this run’s fresh table.')
    all_text=[]
    for text, dimensions, metadata in rows:
        if not isinstance(text,str) or not text.strip():
            raise ValueError('Every stored chunk needs non-empty text.')
        if dimensions != 1024:
            raise ValueError('Every embedding must have 1024 dimensions.')
        if isinstance(metadata,str):
            metadata=json.loads(metadata)
        if not isinstance(metadata,dict) or not metadata.get('chunk_id'):
            raise ValueError('Stored chunk metadata must retain chunk_id.')
        all_text.append(text)
    words=lambda value:set(re.findall(r'[A-Za-z0-9_]+',value.lower()))
    if not words(source_text) <= words('\n'.join(all_text)):
        raise ValueError('Stored text does not cover all source vocabulary; inspect loading/chunking.')
    return {'persisted_chunks':len(rows),'embedding_dimensions':1024,'source_vocabulary_covered':True,'chunk_metadata_present':True}

def write_json(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,indent=2),encoding='utf-8')
