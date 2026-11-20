"""Participant feedback, not a trusted scoring authority."""
import argparse
from pathlib import Path
import subprocess
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from workshop.common import ROOT

def main():
    parser=argparse.ArgumentParser()
    mode=parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--code-only',action='store_true')
    mode.add_argument('--live',action='store_true')
    args=parser.parse_args()
    commands=[['-m','unittest','discover','-s',str(ROOT/'tests/public'),'-v'],[str(ROOT/'scripts/probe_sdk.py')]]
    for command in commands:
        try:result=subprocess.run([sys.executable,'-B',*command],cwd=ROOT,timeout=90)
        except subprocess.TimeoutExpired:
            print('FAIL: check timed out. Ask the facilitator.');return 1
        if result.returncode:
            print('Checkpoint not complete. Consult the SDK guide and staged hints.');return 1
    if not args.live:
        print('CODE CHECKS PASSED. This is not completion: no embeddings or Oracle writes were tested.')
        print('Next: python scripts/validate_local.py --live');return 0
    from workshop.runtime import cli_ingest,completion
    if cli_ingest():return 1
    try:completion()
    except Exception as exc:
        print('Final verification failed:',type(exc).__name__);return 1
    return 0
if __name__=='__main__':raise SystemExit(main())
