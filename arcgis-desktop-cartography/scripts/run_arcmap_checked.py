"""Run one ArcMap worker with a bounded wait and a persistent log (Python 3)."""
import argparse
import json
import subprocess
import time
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--python', required=True, help='Licensed ArcMap Python 2.7 executable')
    parser.add_argument('--timeout', type=float, default=120)
    parser.add_argument('--log', required=True, type=Path)
    parser.add_argument('script', type=Path)
    parser.add_argument('arguments', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error('--timeout must be positive')
    if not Path(args.python).is_file() or not args.script.is_file():
        parser.error('Python executable and worker script must exist')
    args.log.parent.mkdir(parents=True, exist_ok=True)
    command = [args.python, '-u', str(args.script.resolve())] + args.arguments
    started = time.monotonic()
    timed_out = False
    # Exclusive creation preserves evidence from earlier attempts.
    with args.log.open('xb') as log:
        child = subprocess.Popen(command, stdout=log, stderr=subprocess.STDOUT)
        try:
            child.wait(timeout=args.timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            child.kill()
            child.wait()
        except BaseException:
            if child.poll() is None:
                child.kill()
                child.wait()
            raise
    result = dict(command=command, pid=child.pid, timed_out=timed_out,
                  returncode=child.returncode,
                  seconds=round(time.monotonic() - started, 3), log=str(args.log.resolve()))
    args.log.with_suffix(args.log.suffix + '.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result, indent=2))
    print(args.log.read_bytes().decode('utf-8', errors='replace'))
    return 124 if timed_out else child.returncode


if __name__ == '__main__':
    raise SystemExit(main())
