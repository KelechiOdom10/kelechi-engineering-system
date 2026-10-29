import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest


CLI = Path(__file__).resolve().parents[1] / 'scripts' / 'delivery.py'


class DeliveryTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.repo = self.root / 'repo'
        self.repo.mkdir()
        self.git('init', '-q')
        self.git('config', 'user.email', 'test@example.invalid')
        self.git('config', 'user.name', 'Test')
        (self.repo / 'value.txt').write_text('original\n')
        (self.repo / '.gitignore').write_text('.kelechi/\n')
        self.git('add', '.')
        self.git('commit', '-qm', 'initial')
        self.task = {
            'version': 1,
            'id': 'sample',
            'goal': 'Preserve the expected value',
            'acceptance': ['The stored value is original'],
            'trigger': 'manual change',
            'writes': ['value.txt'],
            'human_return': 'Review the behavior and proof',
            'stop_conditions': ['Unexpected data or required authority'],
            'max_check_attempts': 3,
            'max_review_rounds': 3,
            'checks': [{
                'id': 'value',
                'argv': [sys.executable, '-c', "from pathlib import Path; assert Path('value.txt').read_text() == 'original\\n'"],
                'cwd': '.',
                'timeout_seconds': 10,
            }],
        }
        self.task_file = self.root / 'task.json'

    def git(self, *args: str) -> str:
        return subprocess.check_output(['git', '-C', str(self.repo), *args], text=True).strip()

    def cli(self, *args: str, ok: bool = True) -> subprocess.CompletedProcess[str]:
        result = subprocess.run([sys.executable, str(CLI), *map(str, args)], capture_output=True, text=True)
        self.assertEqual(result.returncode == 0, ok, result.stdout + result.stderr)
        return result

    def start(self, key: str = 'event-1') -> Path:
        self.task_file.write_text(json.dumps(self.task))
        result = self.cli('init', self.task_file, '--repo', self.repo, '--base', 'HEAD', '--key', key, '--owner', 'author-session')
        return Path(result.stdout.strip())

    def status(self, run: Path) -> dict:
        return json.loads(self.cli('status', run).stdout)

    def review(self, run: Path, findings: list | None = None, **overrides: object) -> None:
        report = {
            'version': 1,
            'revision': self.status(run)['revision'],
            'reviewer': 'independent-session',
            'scope': 'All task acceptance and changed consumers',
            'findings': findings or [],
        } | overrides
        artifact = self.root / 'review.json'
        artifact.write_text(json.dumps(report))
        self.cli('review', run, artifact)

    def test_actual_checks_and_independent_review_are_needed_for_readiness(self) -> None:
        run = self.start()
        self.cli('ready', run, ok=False)
        self.cli('run', run)
        self.cli('ready', run, ok=False)
        self.review(run)
        self.cli('ready', run)
        self.assertEqual(self.status(run)['state'], 'ready-for-human-review')
        receipt = json.loads(next((run / 'checks').glob('*.json')).read_text())
        self.assertEqual(receipt['exit_code'], 0)
        self.assertEqual(receipt['argv'], self.task['checks'][0]['argv'])

    def test_failed_check_cannot_be_cleared_by_a_clean_review(self) -> None:
        self.task['checks'][0]['argv'] = [sys.executable, '-c', 'raise SystemExit(7)']
        run = self.start()
        self.cli('run', run, ok=False)
        self.review(run)
        self.cli('ready', run, ok=False)
        self.assertTrue(any('failed' in item for item in self.status(run)['blockers']))

    def test_source_changes_and_commits_invalidate_existing_proof(self) -> None:
        run = self.start()
        self.cli('run', run)
        self.review(run)
        (self.repo / 'value.txt').write_text('changed\n')
        self.cli('ready', run, ok=False)
        (self.repo / 'value.txt').write_text('original\n')
        self.cli('ready', run)
        self.git('commit', '--allow-empty', '-qm', 'new head')
        self.cli('ready', run, ok=False)

    def test_untracked_files_and_symlink_targets_are_included(self) -> None:
        run = self.start()
        before = self.status(run)['revision']
        (self.repo / 'extra.txt').write_text('new')
        self.assertNotEqual(self.status(run)['revision'], before)
        (self.repo / 'extra.txt').unlink()
        (self.repo / 'link').symlink_to('value.txt')
        linked = self.status(run)['revision']
        (self.repo / 'link').unlink()
        (self.repo / 'link').symlink_to('elsewhere.txt')
        self.assertNotEqual(self.status(run)['revision'], linked)

    def test_a_command_that_changes_source_does_not_prove_the_new_source(self) -> None:
        self.task['checks'][0]['argv'] = [sys.executable, '-c', "from pathlib import Path; Path('value.txt').write_text('new')"]
        run = self.start()
        self.cli('run', run, ok=False)
        self.review(run)
        self.cli('ready', run, ok=False)

    def test_altered_output_is_rejected(self) -> None:
        run = self.start()
        self.cli('run', run)
        self.review(run)
        next((run / 'checks').glob('*.log')).write_text('forged')
        self.cli('ready', run, ok=False)

    def test_repeated_event_is_claimed_across_worktrees(self) -> None:
        self.task_file.write_text(json.dumps(self.task))
        state = self.root / 'shared-state'
        run = Path(self.cli('init', self.task_file, '--repo', self.repo, '--base', 'HEAD', '--key', 'event-1', '--owner', 'author-session', '--state-dir', state).stdout.strip())
        self.cli('init', self.task_file, '--repo', self.repo, '--base', 'HEAD', '--key', 'event-1', '--owner', 'other', '--state-dir', state, ok=False)
        worktree = self.root / 'other'
        self.git('worktree', 'add', '--detach', '-q', str(worktree), 'HEAD')
        self.cli('init', self.task_file, '--repo', worktree, '--base', 'HEAD', '--key', 'event-1', '--owner', 'other', '--state-dir', state, ok=False)
        self.assertTrue(run.exists())

    def test_default_state_is_workspace_local_and_does_not_change_source(self) -> None:
        run = self.start()
        self.assertTrue(run.is_relative_to(self.repo / '.kelechi'))
        before = self.status(run)['revision']
        self.cli('run', run)
        self.review(run)
        self.assertEqual(self.status(run)['revision'], before)
        self.cli('ready', run)

    def test_nonignored_state_is_rejected_before_it_can_pollute_the_revision(self) -> None:
        self.task_file.write_text(json.dumps(self.task))
        self.cli('init', self.task_file, '--repo', self.repo, '--base', 'HEAD', '--key', 'event', '--owner', 'author', '--state-dir', self.repo / 'visible-state', ok=False)
        self.assertFalse((self.repo / 'visible-state').exists())

    def test_review_cannot_be_the_author_or_an_old_revision(self) -> None:
        run = self.start()
        report = {'version': 1, 'revision': 'wrong', 'reviewer': 'independent-session', 'scope': 'all', 'findings': []}
        artifact = self.root / 'bad-review.json'
        artifact.write_text(json.dumps(report))
        self.cli('review', run, artifact, ok=False)
        report['revision'] = self.status(run)['revision']
        report['reviewer'] = 'author-session'
        artifact.write_text(json.dumps(report))
        self.cli('review', run, artifact, ok=False)

    def test_omitting_an_old_blocker_does_not_close_it(self) -> None:
        run = self.start()
        self.cli('run', run)
        finding = {'id': 'F1', 'severity': 'blocking', 'summary': 'A real failure', 'evidence': 'source:12', 'disposition': 'open'}
        self.review(run, [finding])
        self.review(run)
        self.cli('ready', run, ok=False)
        finding |= {'disposition': 'disproved', 'resolution_evidence': 'The only caller rejects the input at source:8'}
        self.review(run, [finding])
        self.cli('ready', run)

    def test_review_and_check_budgets_stop_automatic_retries(self) -> None:
        self.task['max_review_rounds'] = 1
        self.task['max_check_attempts'] = 1
        run = self.start()
        self.cli('run', run)
        self.cli('run', run, ok=False)
        self.review(run)
        artifact = self.root / 'review.json'
        self.cli('review', run, artifact, ok=False)

    def test_timeout_is_a_failed_receipt_and_stops_the_process_group(self) -> None:
        marker = self.root / 'leaked-child'
        child = f"import time; from pathlib import Path; time.sleep(0.4); Path({str(marker)!r}).write_text('leaked')"
        parent = f'import subprocess, sys, time; subprocess.Popen([sys.executable, "-c", {child!r}]); time.sleep(30)'
        self.task['checks'][0]['argv'] = [sys.executable, '-c', parent]
        self.task['checks'][0]['timeout_seconds'] = 0.1
        run = self.start()
        self.cli('run', run, ok=False)
        receipt = json.loads(next((run / 'checks').glob('*.json')).read_text())
        self.assertTrue(receipt['timed_out'])
        time.sleep(0.5)
        self.assertFalse(marker.exists())
        self.cli('ready', run, ok=False)

    def test_downgrading_an_open_blocker_is_rejected_without_consuming_a_review(self) -> None:
        self.task['max_review_rounds'] = 2
        run = self.start()
        self.cli('run', run)
        finding = {'id': 'F1', 'severity': 'blocking', 'summary': 'Failure', 'evidence': 'source:12', 'disposition': 'open'}
        self.review(run, [finding])
        report = json.loads((self.root / 'review.json').read_text())
        report['findings'][0]['severity'] = 'advisory'
        (self.root / 'review.json').write_text(json.dumps(report))
        self.cli('review', run, self.root / 'review.json', ok=False)
        self.assertEqual(self.status(run)['budget']['reviews'], {'used': 1, 'limit': 2})
        finding |= {'disposition': 'disproved', 'resolution_evidence': 'Verified upstream guard at source:8'}
        self.review(run, [finding])
        self.cli('ready', run)

    def test_successful_commands_do_not_leave_background_children(self) -> None:
        marker = self.root / 'leaked-child'
        child = f"import time; from pathlib import Path; time.sleep(0.4); Path({str(marker)!r}).write_text('leaked')"
        self.task['checks'][0]['argv'] = [sys.executable, '-c', f'import subprocess, sys; subprocess.Popen([sys.executable, "-c", {child!r}])']
        run = self.start()
        self.cli('run', run)
        time.sleep(0.5)
        self.assertFalse(marker.exists())

    def test_task_rejects_unknown_fields_and_escaping_check_directories(self) -> None:
        self.task['checks'][0]['cwd'] = '../outside'
        self.task_file.write_text(json.dumps(self.task))
        self.cli('init', self.task_file, '--repo', self.repo, '--base', 'HEAD', '--key', 'bad', '--owner', 'owner', ok=False)
        self.task['checks'][0]['cwd'] = '.'
        self.task['pretend_approved'] = True
        self.task_file.write_text(json.dumps(self.task))
        self.cli('init', self.task_file, '--repo', self.repo, '--base', 'HEAD', '--key', 'bad', '--owner', 'owner', ok=False)


if __name__ == '__main__':
    unittest.main()
