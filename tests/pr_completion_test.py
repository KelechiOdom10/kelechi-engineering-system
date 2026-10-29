import copy
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


CLI = Path(__file__).resolve().parents[1] / 'scripts' / 'pr_completion.py'
SPEC = importlib.util.spec_from_file_location('pr_completion', CLI)
completion = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(completion)
HEAD = 'a' * 40


def check_run(identifier: int = 1, suite: int = 1, **changes: object) -> dict:
    return {
        'id': identifier, 'head_sha': HEAD, 'name': 'Python checks',
        'app': {'slug': 'github-actions'}, 'check_suite': {'id': suite},
        'status': 'completed', 'conclusion': 'success',
    } | changes


def snapshot() -> dict:
    return {
        'version': 1, 'repository': 'owner/repo', 'pr': 1, 'head': HEAD,
        'base': 'b' * 40, 'state': 'open', 'mergeable': True, 'captured_at': '2026-10-29T12:00:00Z',
        'requirements': {'version': 1, 'checks': [{'name': 'Python checks', 'app_slug': 'github-actions'}], 'statuses': []},
        'sources': [{'id': 'inline:1', 'body': 'The retry writes twice', 'thread': {'resolved': False, 'outdated': False}}],
        'checks': [check_run()], 'statuses': [],
    }


def ledger(value: dict) -> dict:
    result = completion.sync(value, {'version': 1, 'repository': value['repository'], 'pr': value['pr'], 'entries': []})
    for entry in result['entries']:
        entry.update(impact='blocking', decision='fixed', rationale='Retry deduplicates writes', evidence='commit and duplicate-event regression', head=value['head'])
    return result


class AssessmentTest(unittest.TestCase):
    def setUp(self) -> None:
        self.snapshot = snapshot()
        self.ledger = ledger(self.snapshot)

    def assess(self, value: dict | None = None) -> dict:
        return completion.assess(value or self.snapshot, self.ledger, self.snapshot)

    def test_proven_finding_and_exact_current_ci_allow_human_review(self) -> None:
        self.assertEqual(self.assess()['state'], 'ready-for-human-review')

    def test_no_runs_and_unconfigured_requirements_never_mean_green(self) -> None:
        self.snapshot['checks'] = []
        self.assertIn('CI Python checks: missing', self.assess()['blockers'])
        self.snapshot['requirements']['checks'] = []
        self.assertEqual(self.assess()['state'], 'incomplete')

    def test_pending_skipped_neutral_failed_and_canceled_required_checks_block(self) -> None:
        for changes in [{'status': 'queued', 'conclusion': None}, {'status': 'in_progress', 'conclusion': None}, *[{'conclusion': state} for state in ['skipped', 'neutral', 'failure', 'cancelled', 'timed_out', None]]]:
            with self.subTest(changes=changes):
                self.snapshot['checks'] = [check_run(**changes)]
                self.assertEqual(self.assess()['state'], 'incomplete')

    def test_wrong_app_cannot_satisfy_a_required_check(self) -> None:
        self.snapshot['checks'] = [check_run(app={'slug': 'unrelated-app'})]
        self.assertIn('CI Python checks: missing', self.assess()['blockers'])

    def test_another_commit_is_rejected_even_when_its_check_passed(self) -> None:
        self.snapshot['checks'] = [check_run(head_sha='c' * 40)]
        with self.assertRaisesRegex(ValueError, 'another commit'):
            self.assess()

    def test_later_success_cannot_hide_another_job_with_the_same_name(self) -> None:
        self.snapshot['checks'] = [check_run(1, conclusion='failure'), check_run(2)]
        self.assertEqual(self.assess()['ci'][0]['state'], 'ambiguous')
        self.snapshot['checks'].append(check_run(3, suite=2, conclusion='failure'))
        self.assertEqual(self.assess()['state'], 'incomplete')
        self.snapshot['checks'].append(check_run(4, suite=2))
        self.assertEqual(self.assess()['state'], 'incomplete')
        self.snapshot['checks'] = [check_run(2), check_run(4, suite=2)]
        self.assertEqual(self.assess()['state'], 'ready-for-human-review')

    def test_legacy_status_requires_the_named_creator_and_latest_attempt(self) -> None:
        self.snapshot['requirements'] = {'version': 1, 'checks': [], 'statuses': [{'context': 'build', 'creator': 'build-bot'}]}
        self.snapshot['statuses'] = [{'id': 2, 'context': 'build', 'creator': {'login': 'other-bot'}, 'state': 'success'}]
        self.assertEqual(self.assess()['ci'][0]['state'], 'missing')
        self.snapshot['statuses'].extend([{'id': 1, 'context': 'build', 'creator': {'login': 'build-bot'}, 'state': 'success'}, {'id': 3, 'context': 'build', 'creator': {'login': 'build-bot'}, 'state': 'pending'}])
        self.assertEqual(self.assess()['ci'][0]['state'], 'pending')

    def test_new_edited_or_omitted_sources_cannot_disappear_from_triage(self) -> None:
        edited = copy.deepcopy(self.snapshot)
        edited['sources'][0]['body'] = 'The final write also fails'
        self.assertEqual(self.assess(edited)['state'], 'incomplete')
        refreshed = completion.sync(edited, self.ledger)
        self.assertEqual(refreshed['entries'][0]['decision'], 'untriaged')
        self.assertEqual(len(refreshed['entries'][0]['history']), 1)
        self.ledger['entries'] = []
        self.assertEqual(self.assess()['state'], 'incomplete')

    def test_refresh_retains_deleted_sources_and_resets_resolved_thread_changes(self) -> None:
        changed = copy.deepcopy(self.snapshot)
        changed['sources'] = []
        retained = completion.sync(changed, self.ledger)
        self.assertEqual(len(retained['entries']), 1)
        changed['sources'] = copy.deepcopy(self.snapshot['sources'])
        changed['sources'][0]['thread']['resolved'] = True
        self.assertEqual(completion.sync(changed, self.ledger)['entries'][0]['decision'], 'untriaged')

    def test_a_new_head_invalidates_triage_even_if_ci_has_passed(self) -> None:
        changed = copy.deepcopy(self.snapshot)
        changed['head'] = 'd' * 40
        changed['checks'][0]['head_sha'] = changed['head']
        self.assertEqual(self.assess(changed)['state'], 'incomplete')

    def test_open_fixes_and_unsupported_or_waived_blockers_are_incomplete(self) -> None:
        entry = self.ledger['entries'][0]
        for decision in ['untriaged', 'fix', 'out-of-scope', 'no-action']:
            entry['decision'] = decision
            self.assertEqual(self.assess()['state'], 'incomplete')
        entry.update(decision='disproved', evidence='')
        self.assertEqual(self.assess()['state'], 'incomplete')
        entry.update(impact='advisory', decision='no-action', evidence='Formatter preference; behavior unchanged')
        self.assertEqual(self.assess()['state'], 'ready-for-human-review')

    def test_other_pr_duplicate_ids_and_unknown_mergeability_fail_closed(self) -> None:
        self.ledger['pr'] = 2
        with self.assertRaisesRegex(ValueError, 'another PR'):
            self.assess()
        self.ledger['pr'] = 1
        self.ledger['entries'] *= 2
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            self.assess()
        self.ledger = ledger(self.snapshot)
        self.snapshot['mergeable'] = None
        self.assertEqual(self.assess()['state'], 'incomplete')


class GitHubBoundaryTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.responses = {
            'repos/owner/repo/pulls/1': {'head': {'sha': HEAD}, 'base': {'sha': 'b' * 40}, 'state': 'open', 'mergeable': True},
            'repos/owner/repo/issues/1/comments?per_page=100': [[{'id': 1, 'body': 'Check retries', 'html_url': 'https://github.com/owner/repo/issues/1#issuecomment-1', 'user': {'login': 'owner'}}], [{'id': 2, 'body': 'Summary only', 'html_url': 'https://github.com/owner/repo/issues/1#issuecomment-2', 'user': None}]],
            'repos/owner/repo/pulls/1/reviews?per_page=100': [[{'id': 3, 'body': '', 'state': 'CHANGES_REQUESTED', 'html_url': 'https://github.com/owner/repo/pull/1#pullrequestreview-3', 'user': {'login': 'owner'}}]],
            'repos/owner/repo/pulls/1/comments?per_page=100': [[{'id': 4, 'body': 'Double write', 'path': 'write.py', 'line': 2, 'html_url': 'https://github.com/owner/repo/pull/1#discussion_r4', 'user': {'login': 'owner'}}]],
            'threads': [{'data': {'repository': {'pullRequest': {'reviewThreads': {'nodes': [{'id': 'thread1', 'isResolved': True, 'isOutdated': True, 'comments': {'nodes': [], 'pageInfo': {'hasNextPage': True, 'endCursor': 'cursor'}}}], 'pageInfo': {'hasNextPage': False, 'endCursor': None}}}}}}],
            'comments': [{'data': {'node': {'comments': {'nodes': [{'databaseId': 4}]}}}}],
            f'repos/owner/repo/commits/{HEAD}/check-runs?per_page=100&filter=all': [{'check_runs': []}, {'check_runs': [check_run()]}],
            f'repos/owner/repo/commits/{HEAD}/statuses?per_page=100': [[]],
        }
        fake = self.root / 'gh'
        fake.write_text(f'#!{sys.executable}\n' + '''import json, os, pathlib, sys
args = sys.argv[1:]
with open(os.environ['GH_TEST_CALLS'], 'a') as log:
    log.write(json.dumps(args) + '\\n')
data = json.loads(pathlib.Path(os.environ['GH_TEST_RESPONSES']).read_text())
endpoint = args[3]
if endpoint == 'graphql':
    assert not any('mutation' in arg for arg in args)
    endpoint = 'threads' if any('repository(owner:' in arg for arg in args) else 'comments'
else:
    assert '--method' in args and args[args.index('--method') + 1] == 'GET'
if endpoint not in data:
    sys.exit(7)
value = data[endpoint]
if endpoint == 'threads':
    if '--paginate' in args:
        value = value[:1]
    else:
        value = value[1 if 'endCursor=outer-cursor' in args else 0]
print(json.dumps(value))
''')
        fake.chmod(0o755)
        self.env = os.environ | {'PATH': str(self.root) + os.pathsep + os.environ['PATH'], 'GH_TEST_RESPONSES': str(self.root / 'responses.json'), 'GH_TEST_CALLS': str(self.root / 'calls.jsonl')}
        self.expected = self.root / 'requirements.json'
        self.expected.write_text(json.dumps(snapshot()['requirements']))
        self.snapshot_file = self.root / 'snapshot.json'
        self.ledger_file = self.root / 'ledger.json'
        self.report = self.root / 'report.json'

    def cli(self, *args: object, code: int = 0) -> subprocess.CompletedProcess:
        Path(self.env['GH_TEST_RESPONSES']).write_text(json.dumps(self.responses))
        result = subprocess.run([sys.executable, str(CLI), *map(str, args)], env=self.env, capture_output=True, text=True)
        self.assertEqual(result.returncode, code, result.stdout + result.stderr)
        return result

    def capture(self) -> None:
        self.cli('collect', '--repo', 'owner/repo', '--pr', 1, '--requirements', self.expected, '--out', self.snapshot_file)
        self.cli('triage', self.snapshot_file, '--ledger', self.ledger_file)

    def test_paginated_all_source_capture_and_live_recheck(self) -> None:
        self.capture()
        captured = json.loads(self.snapshot_file.read_text())
        self.assertEqual([item['id'] for item in captured['sources']], ['comment:1', 'comment:2', 'review:3', 'inline:4'])
        self.assertTrue(captured['sources'][-1]['thread']['resolved'])
        self.ledger_file.write_text(json.dumps(ledger(captured)))
        self.cli('check', self.snapshot_file, '--ledger', self.ledger_file, '--out', self.report)
        self.assertEqual(json.loads(self.report.read_text())['state'], 'ready-for-human-review')
        self.responses[f'repos/owner/repo/commits/{HEAD}/check-runs?per_page=100&filter=all'] = [{'check_runs': []}]
        self.cli('check', self.snapshot_file, '--ledger', self.ledger_file, '--out', self.report, code=1)
        self.assertIn('missing', json.loads(self.report.read_text())['blockers'][0])

    def test_api_error_cannot_leave_a_previous_green_report(self) -> None:
        self.capture()
        self.report.write_text(json.dumps({'state': 'ready-for-human-review'}))
        del self.responses['threads']
        self.cli('check', self.snapshot_file, '--ledger', self.ledger_file, '--out', self.report, code=2)
        self.assertEqual(json.loads(self.report.read_text())['state'], 'incomplete')

    def test_outer_thread_cursor_is_independent_of_short_nested_comment_pages(self) -> None:
        first = {'nodes': [{'id': 'old-thread', 'isResolved': False, 'isOutdated': False, 'comments': {'nodes': [], 'pageInfo': {'hasNextPage': False, 'endCursor': None}}}], 'pageInfo': {'hasNextPage': True, 'endCursor': 'outer-cursor'}}
        second = copy.deepcopy(self.responses['threads'][0]['data']['repository']['pullRequest']['reviewThreads'])
        self.responses['threads'] = [{'data': {'repository': {'pullRequest': {'reviewThreads': item}}}} for item in [first, second]]
        self.capture()
        captured = json.loads(self.snapshot_file.read_text())
        self.assertEqual(captured['sources'][-1]['id'], 'inline:4')
        calls = [json.loads(line) for line in Path(self.env['GH_TEST_CALLS']).read_text().splitlines()]
        self.assertTrue(any('endCursor=outer-cursor' in call for call in calls))

    def test_missing_thread_coverage_and_graphql_errors_do_not_hide_inline_findings(self) -> None:
        for response in [[{'data': {'repository': {'pullRequest': {'reviewThreads': {'nodes': []}}}}}], [{'errors': [{'message': 'Unavailable'}]}]]:
            self.responses['threads'] = response
            self.cli('collect', '--repo', 'owner/repo', '--pr', 1, '--requirements', self.expected, '--out', self.snapshot_file, code=2)


if __name__ == '__main__':
    unittest.main()
