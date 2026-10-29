import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile


THREAD_QUERY = '''query($owner:String!,$name:String!,$number:Int!,$endCursor:String){
  repository(owner:$owner,name:$name){pullRequest(number:$number){
    reviewThreads(first:100,after:$endCursor){
      nodes{id isResolved isOutdated comments(first:100){nodes{databaseId} pageInfo{hasNextPage endCursor}}}
      pageInfo{hasNextPage endCursor}
    }
  }}
}'''
COMMENT_QUERY = '''query($id:ID!,$endCursor:String){
  node(id:$id){... on PullRequestReviewThread{
    comments(first:100,after:$endCursor){nodes{databaseId} pageInfo{hasNextPage endCursor}}
  }}
}'''
DECISIONS = {'untriaged', 'fix', 'fixed', 'disproved', 'out-of-scope', 'no-action'}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def digest(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def read(path: Path) -> dict:
    value = json.loads(path.read_text())
    require(isinstance(value, dict) and value.get('version') == 1, f'Invalid versioned object: {path}')
    return value


def write(path: Path, value: dict) -> None:
    with tempfile.NamedTemporaryFile(mode='w', dir=path.parent, delete=False) as handle:
        temporary = Path(handle.name)
        try:
            handle.write(json.dumps(value, indent=2) + '\n')
            handle.flush()
            os.fsync(handle.fileno())
            os.replace(temporary, path)
        finally:
            temporary.unlink(missing_ok=True)


def requirements(value: dict) -> dict:
    require(set(value) == {'version', 'checks', 'statuses'} and value['version'] == 1, 'Invalid CI requirements')
    for field, keys in [('checks', {'name', 'app_slug'}), ('statuses', {'context', 'creator'})]:
        rows = value[field]
        require(isinstance(rows, list), f'{field} must be a list')
        require(all(isinstance(row, dict) and set(row) == keys and all(text(v) for v in row.values()) for row in rows), f'Invalid {field} requirement')
        require(len({digest(row) for row in rows}) == len(rows), f'Duplicate {field} requirement')
    return value


def api(endpoint: str, *, pages: bool = False, fields: dict | None = None) -> object:
    argv = ['gh', 'api', '--hostname', 'github.com', endpoint]
    if fields is not None:
        for key, value in fields.items():
            argv.extend(['-F' if isinstance(value, int) else '-f', f'{key}={value}'])
    else:
        argv.extend(['--method', 'GET'])
    if pages:
        argv.extend(['--paginate', '--slurp'])
    result = subprocess.run(argv, capture_output=True, text=True, timeout=120, check=True)
    value = json.loads(result.stdout)
    require(not pages or isinstance(value, list) and bool(value), 'Missing paginated GitHub response')
    for page in value if pages else [value]:
        require(not isinstance(page, dict) or not page.get('errors'), 'GitHub returned GraphQL errors')
    return value


def rows(endpoint: str, field: str | None = None) -> list:
    pages = api(endpoint, pages=True)
    require(isinstance(pages, list) and bool(pages), 'Missing paginated GitHub response')
    result = []
    for page in pages:
        values = page[field] if field else page
        require(isinstance(values, list), 'Invalid paginated GitHub collection')
        result.extend(values)
    return result


def threads(repo: str, number: int) -> dict:
    owner, name = repo.split('/')
    fields = {'query': THREAD_QUERY, 'owner': owner, 'name': name, 'number': number}
    result = {}
    cursors = set()
    while True:
        page = api('graphql', fields=fields)
        connection = page['data']['repository']['pullRequest']['reviewThreads']
        for thread in connection['nodes']:
            comments = list(thread['comments']['nodes'])
            info = thread['comments']['pageInfo']
            if info['hasNextPage']:
                more = api('graphql', pages=True, fields={'query': COMMENT_QUERY, 'id': thread['id'], 'endCursor': info['endCursor']})
                for part in more:
                    comments.extend(part['data']['node']['comments']['nodes'])
            require(type(thread['isResolved']) is bool and type(thread['isOutdated']) is bool, 'Invalid thread state')
            for comment in comments:
                result[comment['databaseId']] = {'id': thread['id'], 'resolved': thread['isResolved'], 'outdated': thread['isOutdated']}
        info = connection['pageInfo']
        require(type(info['hasNextPage']) is bool, 'Invalid thread pagination')
        if not info['hasNextPage']:
            break
        cursor = info['endCursor']
        require(text(cursor) and cursor not in cursors, 'Missing or repeated thread cursor')
        cursors.add(cursor)
        fields['endCursor'] = cursor
    return result


def source(kind: str, value: dict, thread: dict | None = None) -> dict:
    require(type(value['id']) is int and value['id'] > 0, 'Invalid review source id')
    body = value['body']
    require(body is None or isinstance(body, str), 'Invalid review source body')
    require(text(value['html_url']), 'Missing review source URL')
    return {
        'id': f'{kind}:{value["id"]}', 'kind': kind, 'url': value['html_url'],
        'author': value['user']['login'] if value['user'] else '[deleted]',
        'body': body or '', 'path': value.get('path'), 'line': value.get('line'),
        'review_state': value.get('state'), 'thread': thread,
    }


def collect(repo: str, number: int, expected: dict) -> dict:
    require(bool(re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', repo)) and number > 0, 'Use owner/repo and a positive PR number')
    requirements(expected)
    root = f'repos/{repo}'
    pr = api(f'{root}/pulls/{number}')
    head = pr['head']['sha']
    require(bool(re.fullmatch(r'[0-9a-f]{40}', head)), 'Invalid PR head SHA')
    sources = [source('comment', item) for item in rows(f'{root}/issues/{number}/comments?per_page=100')]
    sources.extend(source('review', item) for item in rows(f'{root}/pulls/{number}/reviews?per_page=100') if item['body'] or item['state'] == 'CHANGES_REQUESTED')
    inline = rows(f'{root}/pulls/{number}/comments?per_page=100')
    thread_by_comment = threads(repo, number)
    for item in inline:
        require(item['id'] in thread_by_comment, 'Review thread coverage changed or is incomplete; collect again')
        sources.append(source('inline', item, thread_by_comment[item['id']]))
    require(len({item['id'] for item in sources}) == len(sources), 'Duplicate review source IDs')
    checks = rows(f'{root}/commits/{head}/check-runs?per_page=100&filter=all', 'check_runs')
    statuses = rows(f'{root}/commits/{head}/statuses?per_page=100')
    after = api(f'{root}/pulls/{number}')
    require(after['head']['sha'] == head and after['base']['sha'] == pr['base']['sha'], 'PR head or base changed during capture; collect again')
    return {
        'version': 1, 'repository': repo, 'pr': number, 'head': head,
        'base': pr['base']['sha'], 'state': after['state'], 'mergeable': after['mergeable'],
        'captured_at': datetime.now(timezone.utc).isoformat(),
        'requirements': expected, 'sources': sources, 'checks': checks, 'statuses': statuses,
    }


def entries(ledger: dict, snapshot: dict) -> dict:
    require(ledger.get('repository') == snapshot['repository'] and ledger.get('pr') == snapshot['pr'], 'Ledger belongs to another PR')
    require(isinstance(ledger.get('entries'), list), 'Invalid ledger entries')
    result = {}
    for entry in ledger['entries']:
        require(isinstance(entry, dict) and isinstance(entry.get('source'), dict), 'Invalid ledger entry')
        key = entry['source']['id']
        require(key not in result, 'Duplicate ledger entry')
        require(entry.get('decision') in DECISIONS, f'Invalid decision for {key}')
        result[key] = entry
    return result


def sync(snapshot: dict, ledger: dict) -> dict:
    result = entries(ledger, snapshot)
    for item in snapshot['sources']:
        previous = result.get(item['id'])
        if previous and previous['source'] == item:
            continue
        history = previous.get('history', []) + [previous | {'history': []}] if previous else []
        result[item['id']] = {
            'source': item, 'impact': 'unclassified', 'decision': 'untriaged',
            'rationale': '', 'evidence': '', 'head': '', 'history': history,
        }
    return ledger | {'entries': list(result.values())}


def ci(snapshot: dict) -> list:
    expected = requirements(snapshot['requirements'])
    outcomes = []
    groups = {}
    for item in snapshot['checks']:
        require(item['head_sha'] == snapshot['head'], 'Check belongs to another commit')
        key = (item['app']['slug'], item['name'], item['check_suite']['id'])
        require(type(item['id']) is int and type(key[2]) is int, 'Invalid check identity')
        groups.setdefault(key, []).append(item)
    for wanted in expected['checks']:
        matched_groups = [items for (app, name, _), items in groups.items() if app == wanted['app_slug'] and name == wanted['name']]
        matching = [item for group in matched_groups for item in group]
        state = 'missing'
        if matching:
            states = {('passed' if item['conclusion'] == 'success' else item['conclusion']) if item['status'] == 'completed' else 'pending' for item in matching}
            state = 'passed' if states == {'passed'} else 'ambiguous' if any(len(group) > 1 for group in matched_groups) else 'pending' if 'pending' in states else 'failed'
        outcomes.append({'kind': 'check', **wanted, 'state': state, 'runs': matching})
    for wanted in expected['statuses']:
        matching = [item for item in snapshot['statuses'] if item['context'] == wanted['context'] and item['creator']['login'] == wanted['creator']]
        require(all(type(item['id']) is int for item in matching), 'Invalid status identity')
        latest_status = max(matching, key=lambda item: item['id'], default=None)
        state = 'missing' if latest_status is None else {'success': 'passed', 'pending': 'pending'}.get(latest_status['state'], 'failed')
        outcomes.append({'kind': 'status', **wanted, 'state': state, 'run': latest_status})
    return outcomes


def assess(snapshot: dict, ledger: dict, previous: dict) -> dict:
    current = entries(ledger, snapshot)
    catalog = {entry['source']['id']: entry['source'] for entry in current.values()}
    catalog.update({item['id']: item for item in previous['sources']})
    catalog.update({item['id']: item for item in snapshot['sources']})
    blockers = []
    if snapshot['state'] != 'open':
        blockers.append('PR is not open')
    if snapshot['mergeable'] is not True:
        blockers.append('PR mergeability is conflicting or unknown')
    for key, item in catalog.items():
        entry = current.get(key)
        if not entry or entry['source'] != item or entry.get('head') != snapshot['head']:
            blockers.append(f'{key}: missing, changed or stale triage')
            continue
        decision, impact = entry['decision'], entry.get('impact')
        if decision in {'untriaged', 'fix'} or impact not in {'blocking', 'advisory'}:
            blockers.append(f'{key}: unresolved triage')
        elif impact == 'blocking' and decision not in {'fixed', 'disproved'}:
            blockers.append(f'{key}: blocking risk cannot be waived by triage')
        elif not text(entry.get('rationale')) or not text(entry.get('evidence')):
            blockers.append(f'{key}: decision needs rationale and evidence')
    outcomes = ci(snapshot)
    if not outcomes:
        blockers.append('CI requirements are unconfigured; no green claim is available')
    blockers.extend(f'CI {item.get("name", item.get("context"))}: {item["state"]}' for item in outcomes if item['state'] != 'passed')
    return {
        'version': 1, 'state': 'incomplete' if blockers else 'ready-for-human-review',
        'repository': snapshot['repository'], 'pr': snapshot['pr'], 'head': snapshot['head'],
        'captured_at': snapshot['captured_at'], 'blockers': blockers, 'ci': outcomes,
        'ledger_digest': digest(ledger), 'snapshot': snapshot,
        'limits': 'Point-in-time read-only assessment of declared CI and triage. Not branch-policy discovery, independent semantic review, merge authority, or protection against forged local records.',
    }


def main() -> None:
    parser = argparse.ArgumentParser(description='Collect PR review sources and assess declared CI against a fresh exact head. Never modifies GitHub.')
    commands = parser.add_subparsers(dest='command', required=True)
    capture = commands.add_parser('collect')
    capture.add_argument('--repo', required=True)
    capture.add_argument('--pr', type=int, required=True)
    capture.add_argument('--requirements', type=Path, required=True)
    capture.add_argument('--out', type=Path, required=True)
    for name in ('triage', 'check'):
        command = commands.add_parser(name)
        command.add_argument('snapshot', type=Path)
        command.add_argument('--ledger', type=Path, required=True)
        if name == 'check':
            command.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command != 'collect':
            require(args.snapshot.resolve() != args.ledger.resolve(), 'Snapshot and ledger must be separate files')
        if args.command == 'check':
            require(args.out.resolve() not in {args.snapshot.resolve(), args.ledger.resolve()}, 'Report must not overwrite its inputs')
            write(args.out, {'version': 1, 'state': 'incomplete', 'blockers': ['Fresh GitHub assessment has not completed']})
        if args.command == 'collect':
            write(args.out, collect(args.repo, args.pr, read(args.requirements)))
        else:
            snapshot = read(args.snapshot)
            if args.command == 'triage':
                ledger = read(args.ledger) if args.ledger.exists() else {'version': 1, 'repository': snapshot['repository'], 'pr': snapshot['pr'], 'entries': []}
                write(args.ledger, sync(snapshot, ledger))
            else:
                fresh = collect(snapshot['repository'], snapshot['pr'], snapshot['requirements'])
                report = assess(fresh, read(args.ledger), snapshot)
                write(args.out, report)
                print(json.dumps({key: value for key, value in report.items() if key not in {'snapshot', 'ci'}}, indent=2))
                if report['blockers']:
                    sys.exit(1)
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as error:
        parser.exit(2, f'pr completion: {error}\n')


if __name__ == '__main__':
    main()
