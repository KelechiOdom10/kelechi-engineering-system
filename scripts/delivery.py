import argparse
from contextlib import contextmanager
from dataclasses import asdict, dataclass
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import signal
import stat
import subprocess
import sys
import time
from typing import Iterator
from types import FrameType


class DeliveryError(Exception):
    pass


class Interrupted(Exception):
    def __init__(self, signum: int) -> None:
        self.signum = signum


def interrupt(signum: int, frame: FrameType | None) -> None:
    raise Interrupted(signum)


def obj(value: object, fields: set[str], required: set[str] | None = None) -> dict[str, object]:
    if not isinstance(value, dict) or set(value) - fields or not (fields if required is None else required) <= set(value):
        raise DeliveryError(f'Expected object fields {sorted(fields)}')
    return value


def text(value: object) -> str:
    if not isinstance(value, str) or not value.strip():
        raise DeliveryError('Expected a nonempty string')
    return value


def identifier(value: object) -> str:
    result = text(value)
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,99}', result):
        raise DeliveryError('Invalid identifier')
    return result


def strings(value: object) -> list[str]:
    if not isinstance(value, list) or not value:
        raise DeliveryError('Expected a nonempty list of strings')
    return [text(item) for item in value]


def positive(value: object, maximum: int) -> int:
    if type(value) is not int or not 1 <= value <= maximum:
        raise DeliveryError(f'Expected integer from 1 to {maximum}')
    return value


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def encoded(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, indent=2) + '\n').encode()


def read_json(path: Path) -> object:
    return json.loads(path.read_bytes())


def write_json(path: Path, value: object) -> None:
    with path.open('xb') as output:
        os.fchmod(output.fileno(), 0o600)
        output.write(encoded(value))
        output.flush()
        os.fsync(output.fileno())
    sync_directory(path.parent)


def sync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def finish_json(path: Path, value: object) -> None:
    temporary = path.with_suffix('.pending')
    write_json(temporary, value)
    temporary.replace(path)
    sync_directory(path.parent)


def git(repo: Path, *args: str) -> str:
    result = subprocess.run(['git', '-C', str(repo), *args], capture_output=True, text=True)
    if result.returncode:
        raise DeliveryError(result.stderr.strip())
    return result.stdout.strip()


def within(repo: Path, relative: str) -> Path:
    path = Path(relative)
    result = (repo / path).resolve()
    if path.is_absolute() or not result.is_relative_to(repo):
        raise DeliveryError('Check directories must stay inside the checkout')
    if not result.is_dir():
        raise DeliveryError(f'Check directory does not exist: {relative}')
    return result


def revision(repo: Path) -> str:
    head = git(repo, 'rev-parse', 'HEAD')
    listing = subprocess.check_output(['git', '-C', str(repo), 'ls-files', '--cached', '--others', '--exclude-standard', '-z'])
    entries = []
    for name in sorted(set(listing.split(b'\0')) - {b''}):
        path = repo / os.fsdecode(name)
        if not path.exists() and not path.is_symlink():
            entries.append([os.fsdecode(name), 'deleted'])
            continue
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode):
            content = os.fsencode(os.readlink(path))
        elif stat.S_ISREG(mode):
            content = path.read_bytes()
        else:
            raise DeliveryError('Nested repositories and submodules need their own delivery records')
        entries.append([os.fsdecode(name), mode, digest(content)])
    return digest(encoded([head, entries]))


@dataclass(frozen=True)
class Check:
    id: str
    argv: list[str]
    cwd: str
    timeout_seconds: float


@dataclass(frozen=True)
class Task:
    version: int
    id: str
    goal: str
    acceptance: list[str]
    trigger: str
    writes: list[str]
    human_return: str
    stop_conditions: list[str]
    max_check_attempts: int
    max_review_rounds: int
    checks: list[Check]


def parse_task(value: object, repo: Path) -> Task:
    data = obj(value, set(Task.__dataclass_fields__))
    if data['version'] != 1 or type(data['version']) is not int:
        raise DeliveryError('Unsupported task version')
    if not isinstance(data['checks'], list) or not data['checks']:
        raise DeliveryError('A task needs at least one real check')
    checks = []
    for item in data['checks']:
        check = obj(item, set(Check.__dataclass_fields__))
        timeout = check['timeout_seconds']
        if type(timeout) not in (int, float) or not 0 < timeout <= 3600:
            raise DeliveryError('Check timeout must be between 0 and 3600 seconds')
        cwd = text(check['cwd'])
        within(repo, cwd)
        checks.append(Check(identifier(check['id']), strings(check['argv']), cwd, timeout))
    if len({check.id for check in checks}) != len(checks):
        raise DeliveryError('Check identifiers must be unique')
    writes = data['writes']
    if not isinstance(writes, list):
        raise DeliveryError('writes must be a list; use [] for read-only work')
    for path in writes:
        if Path(text(path)).is_absolute() or '..' in Path(path).parts:
            raise DeliveryError('Write scopes must be relative to the repository')
    return Task(1, identifier(data['id']), text(data['goal']), strings(data['acceptance']),
                text(data['trigger']), writes, text(data['human_return']), strings(data['stop_conditions']),
                positive(data['max_check_attempts'], 20), positive(data['max_review_rounds'], 10), checks)


@dataclass(frozen=True)
class Run:
    directory: Path
    repo: Path
    base: str
    owner: str
    task: Task


def load_run(directory: Path) -> Run:
    data = obj(read_json(directory / 'run.json'), {'version', 'repo', 'base', 'owner', 'key', 'task_digest'})
    if type(data['version']) is not int or data['version'] != 2:
        raise DeliveryError('Unsupported run version')
    repo = Path(text(data['repo'])).resolve()
    if git(repo, 'rev-parse', '--show-toplevel') != str(repo):
        raise DeliveryError('Recorded checkout no longer exists at its original root')
    task_data = (directory / 'task.json').read_bytes()
    if digest(task_data) != data['task_digest']:
        raise DeliveryError('Task definition changed after the event was claimed')
    return Run(directory, repo, text(data['base']), text(data['owner']), parse_task(json.loads(task_data), repo))


@contextmanager
def locked(directory: Path) -> Iterator[Run]:
    with (directory / '.lock').open('r') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        yield load_run(directory)


def init(args: argparse.Namespace) -> None:
    repo = Path(git(args.repo.resolve(), 'rev-parse', '--show-toplevel'))
    task = parse_task(read_json(args.task), repo)
    owner = text(args.owner)
    base = git(repo, 'rev-parse', '--verify', f'{args.base}^{{commit}}')
    common = Path(git(repo, 'rev-parse', '--git-common-dir'))
    common = (repo / common).resolve()
    state = (args.state_dir or repo / '.kelechi' / 'delivery').resolve()
    if state.is_relative_to(repo):
        ignored = subprocess.run(['git', '-C', str(repo), 'check-ignore', '-q', str(state / 'probe')])
        if ignored.returncode != 0:
            raise DeliveryError('State inside the checkout must be Git-ignored; choose an ignored --state-dir')
    directory = state / digest(str(common).encode())[:16] / task.id / digest(text(args.key).encode())
    try:
        directory.mkdir(mode=0o700, parents=True, exist_ok=False)
    except FileExistsError:
        raise DeliveryError(f'Task/event already claimed: {directory}') from None
    task_data = encoded(asdict(task))
    write_json(directory / 'task.json', asdict(task))
    write_json(directory / 'run.json', {'version': 2, 'repo': str(repo), 'base': base, 'owner': owner,
                                      'key': args.key, 'task_digest': digest(task_data)})
    (directory / 'checks').mkdir(mode=0o700)
    for check in task.checks:
        (directory / 'checks' / check.id).mkdir(mode=0o700)
    (directory / 'reviews').mkdir(mode=0o700)
    (directory / '.lock').touch(mode=0o600)
    print(directory)


def execute(run: Run, check: Check) -> bool:
    directory = run.directory / 'checks' / check.id
    receipts = list(directory.glob('*.json'))
    if len(receipts) >= run.task.max_check_attempts:
        raise DeliveryError(f'Check {check.id} exhausted its attempt budget; reassess with the owner')
    source = revision(run.repo)
    log = directory / f'{len(receipts) + 1:04d}.log'
    started = time.time()
    timed_out = False
    cwd = within(run.repo, check.cwd)
    receipt = {'check': check.id, 'argv': check.argv, 'cwd': check.cwd, 'phase': 'started',
               'started': started, 'finished': None, 'exit_code': None, 'timed_out': False,
               'revision': source, 'after_revision': None, 'log': log.name, 'log_digest': None}
    write_json(log.with_suffix('.json'), receipt)
    with log.open('xb') as output:
        os.chmod(log, 0o600)
        try:
            process = subprocess.Popen(check.argv, cwd=cwd, stdout=output, stderr=subprocess.STDOUT, start_new_session=True)
        except OSError as error:
            output.write(str(error).encode())
            exit_code = 127
        else:
            try:
                exit_code = process.wait(timeout=check.timeout_seconds)
            except subprocess.TimeoutExpired:
                timed_out = True
            finally:
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                exit_code = process.wait()
    after = revision(run.repo)
    receipt |= {'phase': 'finished', 'finished': time.time(), 'exit_code': exit_code, 'timed_out': timed_out,
                'after_revision': after, 'log_digest': digest(log.read_bytes())}
    finish_json(log.with_suffix('.json'), receipt)
    return exit_code == 0 and not timed_out and source == after


def run_checks(args: argparse.Namespace) -> None:
    with locked(args.run) as run:
        selected = [check for check in run.task.checks if not args.check or check.id == args.check]
        if not selected:
            raise DeliveryError('Unknown check identifier')
        for check in selected:
            if not execute(run, check):
                raise DeliveryError(f'Check {check.id} failed, timed out, or changed source; inspect the receipt')


def parse_review(value: object) -> dict:
    data = obj(value, {'version', 'revision', 'reviewer', 'scope', 'findings'})
    if type(data['version']) is not int or data['version'] != 1 or not isinstance(data['findings'], list):
        raise DeliveryError('Invalid review format')
    for key in ('revision', 'reviewer', 'scope'):
        text(data[key])
    seen = set()
    for item in data['findings']:
        finding = obj(item, {'id', 'severity', 'summary', 'evidence', 'disposition', 'resolution_evidence'},
                      {'id', 'severity', 'summary', 'evidence', 'disposition'})
        name = identifier(finding['id'])
        if name in seen:
            raise DeliveryError('Finding identifiers must be unique within a review')
        seen.add(name)
        if finding['severity'] not in ('blocking', 'advisory') or finding['disposition'] not in ('open', 'fixed', 'disproved'):
            raise DeliveryError('Invalid finding severity or disposition')
        text(finding['summary'])
        text(finding['evidence'])
        if finding['disposition'] != 'open':
            text(finding.get('resolution_evidence'))
    return data


def record_review(args: argparse.Namespace) -> None:
    with locked(args.run) as run:
        if len(list((run.directory / 'reviews').glob('*.json'))) >= run.task.max_review_rounds:
            raise DeliveryError('Review budget exhausted; reassess the approach with the owner')
        data = parse_review(read_json(args.artifact))
        if data['reviewer'] == run.owner:
            raise DeliveryError('The author cannot supply the independent review')
        if data['revision'] != revision(run.repo):
            raise DeliveryError('Review does not cover the current revision')
        prior = {}
        for path in sorted((run.directory / 'reviews').glob('*.json')):
            for finding in parse_review(read_json(path))['findings']:
                prior[finding['id']] = finding
        for finding in data['findings']:
            previous = prior.get(finding['id'])
            if previous and previous['severity'] == 'blocking' and finding['severity'] != 'blocking' and finding['disposition'] == 'open':
                raise DeliveryError('An open blocker needs an explicit resolution, not a severity downgrade')
        index = len(list((run.directory / 'reviews').glob('*.json'))) + 1
        write_json(run.directory / 'reviews' / f'{index:04d}.json', data)


def status(run: Run) -> dict:
    current = revision(run.repo)
    blockers = []
    attempts = {}
    for check in run.task.checks:
        receipts = sorted((run.directory / 'checks' / check.id).glob('*.json'))
        attempts[check.id] = {'used': len(receipts), 'limit': run.task.max_check_attempts}
        if not receipts:
            blockers.append(f'Check {check.id} missing')
            continue
        data = obj(read_json(receipts[-1]), {'check', 'argv', 'cwd', 'phase', 'started', 'finished', 'exit_code', 'timed_out',
                                           'revision', 'after_revision', 'log', 'log_digest'})
        if data['check'] != check.id or data['argv'] != check.argv or data['cwd'] != check.cwd:
            blockers.append(f'Check {check.id} receipt does not match task')
        if data['phase'] != 'finished':
            blockers.append(f'Check {check.id} started but did not finish')
        if type(data['exit_code']) is not int or data['exit_code'] != 0 or data['timed_out'] is not False:
            blockers.append(f'Check {check.id} failed')
        if data['revision'] != current or data['after_revision'] != current:
            blockers.append(f'Check {check.id} stale')
        log = receipts[-1].with_suffix('.log')
        if data['log'] != log.name or not log.is_file() or log.is_symlink() or digest(log.read_bytes()) != data['log_digest']:
            blockers.append(f'Check {check.id} output changed or missing')
    reviews = sorted((run.directory / 'reviews').glob('*.json'))
    findings = {}
    latest = None
    for path in reviews:
        latest = parse_review(read_json(path))
        if latest['reviewer'] == run.owner:
            blockers.append('Review came from the author')
        for finding in latest['findings']:
            previous = findings.get(finding['id'])
            if previous and previous['severity'] == 'blocking' and finding['severity'] != 'blocking' and finding['disposition'] == 'open':
                blockers.append(f"Finding {finding['id']} downgraded without resolution")
            findings[finding['id']] = finding
    if not latest:
        blockers.append('Independent review missing')
    elif latest['revision'] != current:
        blockers.append('Independent review stale')
    for finding in findings.values():
        if finding['severity'] == 'blocking' and finding['disposition'] == 'open':
            blockers.append(f"Finding {finding['id']} unresolved: {finding['summary']}")
    if revision(run.repo) != current:
        blockers.append('Source changed while assessing readiness')
    return {'state': 'incomplete' if blockers else 'ready-for-human-review', 'revision': current,
            'base': run.base, 'head': git(run.repo, 'rev-parse', 'HEAD'), 'blockers': blockers,
            'human_return': run.task.human_return, 'reviewer': latest['reviewer'] if latest else None,
            'budget': {'checks': attempts, 'reviews': {'used': len(reviews), 'limit': run.task.max_review_rounds}}}


def main() -> int:
    for signum in (signal.SIGINT, signal.SIGTERM):
        signal.signal(signum, interrupt)
    parser = argparse.ArgumentParser(description='Collect revision-bound delivery evidence; readiness never grants merge authority.')
    commands = parser.add_subparsers(dest='command', required=True)
    start = commands.add_parser('init', help='Claim one task/event across this repository’s worktrees')
    start.add_argument('task', type=Path)
    start.add_argument('--repo', type=Path, required=True)
    start.add_argument('--base', required=True)
    start.add_argument('--key', required=True)
    start.add_argument('--owner', required=True)
    start.add_argument('--state-dir', type=Path, help='Host-writable state shared explicitly across participating checkouts; default .kelechi/delivery')
    checks = commands.add_parser('run', help='Run declared checks sequentially and retain actual results')
    checks.add_argument('run', type=Path)
    checks.add_argument('--check')
    review = commands.add_parser('review', help='Record a current independent review and finding dispositions')
    review.add_argument('run', type=Path)
    review.add_argument('artifact', type=Path)
    for command in ('status', 'ready'):
        state = commands.add_parser(command)
        state.add_argument('run', type=Path)
    args = parser.parse_args()
    try:
        if args.command == 'init':
            init(args)
        elif args.command == 'run':
            run_checks(args)
        elif args.command == 'review':
            record_review(args)
        else:
            with locked(args.run) as run:
                result = status(run)
            print(json.dumps(result, indent=2))
            if args.command == 'ready' and result['blockers']:
                return 1
    except (DeliveryError, OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f'delivery: {error}', file=sys.stderr)
        return 1
    except Interrupted as error:
        print('delivery: interrupted; any started check remains incomplete', file=sys.stderr)
        return 128 + error.signum
    return 0


if __name__ == '__main__':
    sys.exit(main())
