"""Regression tests for the live-data publisher; fixtures are never publishable data."""
import importlib.util
from pathlib import Path
import unittest


class StatsTests(unittest.TestCase):
    def test_graphql_errors_fail_closed(self):
        spec = importlib.util.spec_from_file_location('stats', 'scripts/profile_stats.py')
        self.assertTrue(Path(spec.origin).exists(), 'live stats generator is missing')
        stats = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(stats)
        with self.assertRaisesRegex(ValueError, 'GitHub API'):
            stats.unwrap({'data': {'user': {}}, 'errors': [{'message': 'rate limit'}]})
        with self.assertRaises(ValueError):
            stats.unwrap({'data': {'user': None}})

    def test_render_real_snapshot_and_reject_inconsistent_calendar(self):
        import profile_stats as stats
        from collections import Counter
        sample = {'contributions': {'totalCommitContributions': 1,
                  'totalIssueContributions': 0, 'totalPullRequestContributions': 0,
                  'totalPullRequestReviewContributions': 0,
                  'contributionCalendar': {'totalContributions': 1, 'weeks': [
                      {'contributionDays': [{'date': '2026-11-08', 'contributionCount': 1}]}]}},
                  'languages': Counter({'Python': 30, 'Shell': 10}), 'stars': 2, 'repos': 1}
        cards = stats.render(sample)
        self.assertEqual(set(cards), {'stats', 'languages', 'activity'})
        self.assertIn('75.0%', cards['languages'])
        self.assertIn('Commit contributions', cards['stats'])
        self.assertNotIn('Repo commits', cards['stats'])
        sample['contributions']['contributionCalendar']['totalContributions'] = 99
        with self.assertRaises(ValueError):
            stats.render(sample)

    def test_incomplete_languages_abort(self):
        import profile_stats as stats
        from unittest.mock import patch
        pages = [{'contributionsCollection': {}}, {'repositories': {'nodes': [
            {'stargazerCount': 0, 'languages': {'edges': [], 'pageInfo': {'hasNextPage': True}}}],
            'pageInfo': {'hasNextPage': False}}}]
        with patch.dict('os.environ', {'GITHUB_TOKEN': 'unit-test-only'}), patch.object(stats, 'graphql', side_effect=pages):
            with self.assertRaisesRegex(ValueError, 'Incomplete language'):
                stats.fetch()

    def test_paginated_public_nonfork_language_bytes(self):
        import profile_stats as stats
        from unittest.mock import patch
        def page(size, more, cursor):
            return {'repositories': {'nodes': [{'stargazerCount': 2, 'languages': {
                'edges': [{'size': size, 'node': {'name': 'Python'}}],
                'pageInfo': {'hasNextPage': False}}}],
                'pageInfo': {'hasNextPage': more, 'endCursor': cursor}}}
        with patch.dict('os.environ', {'GITHUB_TOKEN': 'unit-test-only'}), patch.object(
                stats, 'graphql', side_effect=[{'contributionsCollection': {}}, page(30, True, 'next'), page(10, False, None)]) as api:
            result = stats.fetch()
        self.assertEqual(result['languages']['Python'], 40)
        self.assertEqual(result['stars'], 4)
        self.assertEqual(result['repos'], 2)
        self.assertEqual(api.call_args_list[2].args[1]['cursor'], 'next')
        self.assertIn('privacy:PUBLIC', api.call_args_list[1].args[0])
        self.assertIn('isFork:false', api.call_args_list[1].args[0])

    def test_fetch_requires_token_before_network(self):
        import profile_stats as stats
        from unittest.mock import patch
        with patch.dict('os.environ', {}, clear=True):
            with self.assertRaisesRegex(ValueError, 'GITHUB_TOKEN'):
                stats.fetch()


if __name__ == '__main__':
    unittest.main()
