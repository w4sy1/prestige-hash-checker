from pathlib import Path
import tempfile
import unittest
from app import manifest,compare,validate

class ManifestTests(unittest.TestCase):
    def test_changes(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);(p/'changed').write_text('old');(p/'missing').write_text('x');before=manifest(p)
            (p/'changed').write_text('new');(p/'missing').unlink();(p/'new').write_text('y')
            r=compare(before,manifest(p));self.assertEqual(r['changed'],['changed']);self.assertEqual(r['new'],['new']);self.assertEqual(r['missing'],['missing']);self.assertFalse(r['ok'])
    def test_empty(self):
        with tempfile.TemporaryDirectory() as d:self.assertTrue(compare(manifest(d),manifest(d))['ok'])
    def test_traversal(self):
        with self.assertRaises(ValueError):validate({'schema_version':1,'algorithm':'sha256','files':{'../bad':{'hash':'0'*64}}})
