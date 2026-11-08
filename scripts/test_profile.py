"""Profile publication guards and visual-structure contract."""
import os
from pathlib import Path
import subprocess
import sys
import unittest

class ProfileTests(unittest.TestCase):
    def test_reference_section_order(self):
        source = Path('README.source.md').read_text()
        markers = ['header.svg', 'control.svg', 'access.svg', 'portal.svg', 'gateway.svg', 'core.svg', 'Technologies, Projects, and Domains', 'Vital Statistics', 'Collaboration', 'footer.svg']
        positions = [source.index(m) for m in markers]
        self.assertEqual(positions, sorted(positions))

    def test_api_failure_fail_closed(self):
        import tempfile
        with tempfile.TemporaryDirectory(dir=os.environ.get('TMPDIR')) as folder:
            fake = Path(folder) / 'npx'
            fake.write_text('#!/bin/sh\nprintf "GitHub API failed; using mock data\\n"\nexit 0\n')
            fake.chmod(0o755)
            env = dict(os.environ, GITHUB_TOKEN='test-not-a-real-token', PATH=folder + os.pathsep + os.environ['PATH'])
            result = subprocess.run([sys.executable, 'scripts/generate_readme.py'], env=env, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('Refusing to publish', result.stderr)

    def test_missing_credentials_fail_closed(self):
        env = dict(os.environ)
        env.pop('GITHUB_TOKEN', None)
        result = subprocess.run([sys.executable, 'scripts/generate_readme.py'], env=env, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('refusing mock-data', result.stderr)

if __name__ == '__main__':
    unittest.main()
