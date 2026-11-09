"""Keep the conventional upstream cards and fail closed before publication."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('publisher', 'scripts/generate_readme.py')
assert spec is not None and spec.loader is not None
publisher = importlib.util.module_from_spec(spec)
spec.loader.exec_module(publisher)


class ProfileTests(unittest.TestCase):
    def test_source_layout(self):
        source = Path('README.source.md').read_text()
        self.assertLess(source.index('header.svg'), source.index('stats.svg'))
        self.assertLess(source.index('stats.svg'), source.index('top-langs.svg'))
        self.assertLess(source.index('top-langs.svg'), source.index('streak.svg'))
        self.assertLess(source.index('streak.svg'), source.index('trophies.svg'))
        self.assertLess(source.index('trophies.svg'), source.index('footer.svg'))
        for heading in ['Stats', 'Languages', 'Streak', 'Achievements']:
            self.assertIn('## '+heading, source)
        self.assertIn('Raymond REDdington', source)
        for removed in ['github-stats -->', 'activity-', '```aura']:
            self.assertNotIn(removed, source)

    def test_invalid_cards_preserve_published_readme(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root/'README.md').write_text('published')
            (root/'README.source.md').write_text('new source')
            (root/'.github/assets').mkdir(parents=True)
            for svg in ['', '<svg xmlns="http://www.w3.org/2000/svg"><text>Something went wrong</text></svg>', '<html>unavailable</html>']:
                (root/'.github/assets/stats.svg').write_text(svg)
                with self.assertRaises((ValueError, publisher.ET.ParseError)):
                    publisher.publish(root)
                self.assertEqual((root/'README.md').read_text(), 'published')

    def test_workflow_uses_official_fail_closed_action(self):
        workflow = Path('.github/workflows/readme-aura.yml').read_text()
        generator = Path('scripts/generate_upstream.sh').read_text()
        self.assertIn('INPUT_FAIL_ON_ERROR=true', generator)
        self.assertIn('layout=compact', generator)
        self.assertIn('username=rrddngtnn', generator)
        self.assertIn('render_svg.ts', generator)
        self.assertIn('bin/generate-card.php', generator)
        self.assertIn('scripts/generate_upstream.sh', workflow)
        self.assertNotIn('profile_stats', workflow)


if __name__ == '__main__':
    unittest.main()
