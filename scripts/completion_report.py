from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from workshop.runtime import completion
if __name__=='__main__':
    try:completion()
    except Exception as exc:
        print('Completion unavailable:',type(exc).__name__,str(exc) if isinstance(exc,RuntimeError) else 'See TROUBLESHOOTING.md.')
        raise SystemExit(1)
