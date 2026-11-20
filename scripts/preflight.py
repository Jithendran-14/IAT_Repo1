"""Check environment prerequisites, independently of planted challenge defects."""
import argparse
from importlib.metadata import version,PackageNotFoundError
import os
from pathlib import Path
import sys
import urllib.request
import json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from workshop.common import EXPECTED_PACKAGES

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--services',action='store_true',help='Also connect to Oracle and check local Ollama model availability.')
    args=parser.parse_args()
    failed=False
    ok=(3,11)<=sys.version_info[:2]<(3,14)
    print(('PASS' if ok else 'FAIL'),'Python',sys.version.split()[0]);failed|=not ok
    print('Interpreter:',sys.executable)
    print('Shared/virtual environment:',sys.prefix!=sys.base_prefix)
    for package,expected in EXPECTED_PACKAGES.items():
        try: actual=version(package)
        except PackageNotFoundError: actual='NOT INSTALLED'
        ok=actual==expected;failed|=not ok
        print(('PASS' if ok else 'FAIL'),package,actual,'expected',expected)
    for name in ('IAT_RAG_USER','IAT_RAG_PASSWORD'):
        present=bool(os.environ.get(name))
        print(('PASS' if present else 'NEEDED FOR LIVE RUN'),name,'set' if present else 'not set')
        if args.services:failed|=not present
    if args.services:
        try:
            with urllib.request.urlopen('http://localhost:11434/api/tags',timeout=10) as response:
                models=json.load(response)['models']
            if not any(m.get('name')=='qwen3-embedding:0.6b' for m in models):raise RuntimeError('required embedding model not present')
            print('PASS Ollama embedding model available')
        except Exception:
            print('FAIL Ollama unavailable or embedding model missing');failed=True
        try:
            import oracledb
            with oracledb.connect(user=os.environ['IAT_RAG_USER'],password=os.environ['IAT_RAG_PASSWORD'],dsn=os.environ.get('IAT_RAG_DSN','localhost:1521/FREEPDB1')) as connection:
                with connection.cursor() as cursor:
                    cursor.execute('SELECT 1 FROM dual');assert cursor.fetchone()[0]==1
            print('PASS Oracle read-only connectivity check')
        except Exception:
            print('FAIL Oracle connectivity/credentials; ask the facilitator. No password printed.');failed=True
    return int(failed)
if __name__=='__main__':raise SystemExit(main())
