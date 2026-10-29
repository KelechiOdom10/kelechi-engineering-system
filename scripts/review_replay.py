import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys


def git(repo: Path, *args: str) -> bytes:
    return subprocess.check_output(['git', '-C', str(repo), *args], stderr=subprocess.PIPE)


def prepare(manifest: Path, repo: Path, output: Path) -> None:
    data = json.loads(manifest.read_bytes())
    if not isinstance(data, dict) or data.get('version') != 1 or not isinstance(data.get('cases'), list) or not data['cases']:
        raise ValueError('Expected version 1 and a nonempty cases list')
    cases = []
    for item in data['cases']:
        if not isinstance(item, dict) or not {'id', 'base', 'head', 'intent', 'paths', 'expected'} <= item.keys():
            raise ValueError('Each private case needs id, base, head, intent, paths and expected labels')
        if not isinstance(item['id'], str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,60}', item['id']):
            raise ValueError('Invalid case identifier')
        for name in ('base', 'head'):
            if not isinstance(item[name], str) or not re.fullmatch(r'[a-f0-9]{40}|[a-f0-9]{64}', item[name]):
                raise ValueError('Replay revisions must be immutable full commit SHAs')
            git(repo, 'cat-file', '-e', f'{item[name]}^{{commit}}')
        if not isinstance(item['intent'], str) or not item['intent'].strip():
            raise ValueError('A case needs the intended behavior, independent of hidden labels')
        if not isinstance(item['expected'], list):
            raise ValueError('Expected labels must be a list; [] is a clean control')
        if not isinstance(item['paths'], list) or not item['paths']:
            raise ValueError('A case needs an explicit file scope')
        context = item.get('context_paths', [])
        if not isinstance(context, list):
            raise ValueError('Context paths must be a list')
        paths = item['paths'] + context
        for path in paths:
            if not isinstance(path, str) or not path or PurePosixPath(path).is_absolute() or '..' in PurePosixPath(path).parts or '\\' in path:
                raise ValueError('Replay paths must stay inside their packet')
            mode = git(repo, 'ls-tree', item['head'], '--', path).split(b' ', 1)[0]
            if mode not in (b'100644', b'100755'):
                raise ValueError(f'Replay scope must contain regular files: {path}')
        cases.append(item)
    if len({item['id'] for item in cases}) != len(cases):
        raise ValueError('Case identifiers must be unique')
    output.mkdir(mode=0o700, parents=True, exist_ok=False)
    for item in cases:
        packet = output / item['id']
        packet.mkdir(mode=0o700)
        hashes = {}
        for path in dict.fromkeys(item['paths'] + item.get('context_paths', [])):
            contents = git(repo, 'show', f"{item['head']}:{path}")
            target = packet / 'source' / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(contents)
            hashes[path] = hashlib.sha256(contents).hexdigest()
        patch = git(repo, 'diff', '--no-ext-diff', '--no-textconv', '--binary', item['base'], item['head'], '--', *item['paths'])
        (packet / 'change.diff').write_bytes(patch)
        (packet / 'intent.md').write_text(item['intent'] + '\n')
        metadata = {'version': 1, 'case': item['id'], 'base': item['base'], 'head': item['head'],
                    'scope': 'Only the selected files; not a full repository review',
                    'changed_scope': item['paths'], 'context_paths': item.get('context_paths', []), 'source_digests': hashes,
                    'patch_digest': hashlib.sha256(patch).hexdigest()}
        (packet / 'packet.json').write_text(json.dumps(metadata, indent=2) + '\n')
        print(packet)


def main() -> int:
    parser = argparse.ArgumentParser(description='Prepare private, scoped historical review packets without labels or future fixes.')
    parser.add_argument('manifest', type=Path)
    parser.add_argument('--repo', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    try:
        prepare(args.manifest, args.repo.resolve(), args.output)
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        print(f'review-replay: {error}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
