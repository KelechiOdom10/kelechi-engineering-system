import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest


spec = importlib.util.spec_from_file_location('review_replay', Path(__file__).resolve().parents[1] / 'scripts/review_replay.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ReplayTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / 'repo'
        self.repo.mkdir()
        self.git('init', '-q')
        self.git('config', 'user.email', 'test@example.invalid')
        self.git('config', 'user.name', 'Test')
        (self.repo / 'source.ts').write_text('export const value = 1\n')
        (self.repo / 'producer.ts').write_text('export const readValue = () => 42\n')
        self.git('add', '.')
        self.git('commit', '-qm', 'initial')
        self.base = self.git('rev-parse', 'HEAD')
        (self.repo / 'source.ts').write_text('export const value = 2\n')
        self.git('commit', '-qam', 'change')
        self.head = self.git('rev-parse', 'HEAD')
        self.manifest = self.root / 'private.json'
        self.output = self.root / 'packets'
        self.data = {'version': 1, 'cases': [{'id': 'C01', 'base': self.base, 'head': self.head,
                                           'intent': 'Preserve the required behavior', 'paths': ['source.ts'],
                                           'expected': [{'hidden': 'SECRET-ANSWER'}], 'future_fix': 'DO-NOT-EXPOSE'}]}

    def git(self, *args: str) -> str:
        return subprocess.check_output(['git', '-C', str(self.repo), *args], text=True).strip()

    def prepare(self) -> None:
        self.manifest.write_text(json.dumps(self.data))
        module.prepare(self.manifest, self.repo, self.output)

    def test_packets_use_the_pinned_tree_and_exclude_hidden_answers(self) -> None:
        (self.repo / 'source.ts').write_text('unrelated present-day content')
        self.prepare()
        packet = self.output / 'C01'
        self.assertEqual((packet / 'source/source.ts').read_text(), 'export const value = 2\n')
        for path in packet.rglob('*'):
            if path.is_file():
                self.assertNotIn('SECRET-ANSWER', path.read_text())
                self.assertNotIn('DO-NOT-EXPOSE', path.read_text())
        self.assertIn('+export const value = 2', (packet / 'change.diff').read_text())

    def test_clean_controls_keep_an_empty_expected_set_private(self) -> None:
        self.data['cases'][0]['expected'] = []
        self.prepare()
        self.assertNotIn('expected', (self.output / 'C01/packet.json').read_text())

    def test_producer_context_is_supplied_without_expanding_the_changed_scope(self) -> None:
        self.data['cases'][0]['context_paths'] = ['producer.ts']
        self.prepare()
        packet = self.output / 'C01'
        self.assertEqual((packet / 'source/producer.ts').read_text(), 'export const readValue = () => 42\n')
        metadata = json.loads((packet / 'packet.json').read_text())
        self.assertEqual(metadata['changed_scope'], ['source.ts'])
        self.assertEqual(metadata['context_paths'], ['producer.ts'])
        self.assertNotIn('producer.ts', (packet / 'change.diff').read_text())

    def test_a_packet_cannot_overwrite_an_existing_run(self) -> None:
        self.prepare()
        with self.assertRaises(FileExistsError):
            self.prepare()

    def test_path_escape_and_mutable_refs_are_rejected_before_output(self) -> None:
        for field, value in [('paths', ['../secret']), ('head', 'main'), ('paths', ['/etc/passwd'])]:
            original = self.data['cases'][0][field]
            self.data['cases'][0][field] = value
            with self.assertRaises(ValueError):
                self.prepare()
            self.assertFalse(self.output.exists())
            self.data['cases'][0][field] = original


if __name__ == '__main__':
    unittest.main()
