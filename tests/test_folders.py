import tempfile
import unittest
from pathlib import Path
from app import build, handle


class FolderComparisonTests(unittest.TestCase):
    def test_actual_folder_changes(self):
        with tempfile.TemporaryDirectory() as temporary:
            first, second = Path(temporary) / 'first', Path(temporary) / 'second'
            first.mkdir(); second.mkdir()
            for root in (first, second):
                (root / 'same').write_text('same')
            (first / 'changed').write_text('before')
            (second / 'changed').write_text('after')
            (first / 'removed').write_text('old')
            (second / 'added').write_text('new')
            args = build().parse_args(['compare-folders', '--root', str(first), '--other', str(second)])
            result = handle(args)
            self.assertEqual(result['changed'], ['changed'])
            self.assertEqual(result['missing'], ['removed'])
            self.assertEqual(result['new'], ['added'])
            self.assertEqual(result['unchanged'], ['same'])
            self.assertFalse(result['ok'])
