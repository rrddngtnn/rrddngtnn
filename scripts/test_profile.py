"""Publication is all-or-nothing on API failures; CI alone owns generated files."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


class ProfileTests(unittest.TestCase):
    def test_source_layout(self):
        source = Path('README.source.md').read_text()
        self.assertIn('header.svg', source)
        self.assertIn('Raymond REDdington', source)
        self.assertIn('<!-- github-stats -->', source)
        for removed in ['control.svg', 'Collaboration', '```aura', 'streak']:
            self.assertNotIn(removed, source)

    def test_api_failure_preserves_outputs(self):
        script = Path('scripts/generate_readme.py').resolve()
        with tempfile.TemporaryDirectory(dir=os.environ.get('TMPDIR')) as folder:
            root = Path(folder)
            (root/'README.source.md').write_text('<!-- github-stats -->')
            (root/'README.md').write_text('existing published output')
            (root/'profile_stats.py').write_text('def fetch():\n raise ValueError("GitHub API unavailable")\n')
            # PYTHONPATH cannot shadow script-directory imports: inject failure through runpy.
            code = ('import sys,runpy; sys.path.insert(0, sys.argv[1]); '
                    'script=sys.argv[2]; sys.argv=[script]; '
                    'runpy.run_path(script,run_name="__main__")')
            env = dict(os.environ, GITHUB_TOKEN='unit-test-only')
            result = subprocess.run([sys.executable, '-c', code, folder, str(script)],
                                    cwd=folder, env=env, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('GitHub API unavailable', result.stderr)
            self.assertEqual((root/'README.md').read_text(), 'existing published output')
            self.assertFalse((root/'.github/assets').exists())

    def test_missing_credentials_fail_closed(self):
        env = dict(os.environ)
        env.pop('GITHUB_TOKEN', None)
        result = subprocess.run([sys.executable, 'scripts/generate_readme.py'],
                                env=env, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('refusing mock-data', result.stderr)


if __name__ == '__main__':
    unittest.main()
