"""Authenticated GitHub measurements and self-contained SVG cards (stdlib only)."""
from collections import Counter
from datetime import date
from html import escape
import json
import os
from urllib.request import Request, urlopen

USER = 'rrddngtnn'


def unwrap(payload):
    if payload.get('errors') or not payload.get('data', {}).get('user'):
        raise ValueError('GitHub API returned errors or no user; refusing publication')
    return payload['data']['user']


def graphql(query, variables):
    request = Request('https://api.github.com/graphql',
                      data=json.dumps({'query': query, 'variables': variables}).encode(),
                      headers={'Authorization': 'Bearer ' + os.environ['GITHUB_TOKEN'],
                               'Content-Type': 'application/json', 'User-Agent': 'profile-stats'})
    with urlopen(request, timeout=45) as response:
        return unwrap(json.load(response))


def fetch():
    if not os.environ.get('GITHUB_TOKEN'):
        raise ValueError('GITHUB_TOKEN is required; refusing mock-data generation')
    user = graphql('''query($login:String!) { user(login:$login) {
      contributionsCollection { totalCommitContributions totalIssueContributions
        totalPullRequestContributions totalPullRequestReviewContributions
        contributionCalendar { totalContributions weeks { contributionDays { date contributionCount } } }
      }
    } }''', {'login': USER})
    languages, stars, repos, cursor = Counter(), 0, 0, None
    while True:
        page = graphql('''query($login:String!, $cursor:String) { user(login:$login) {
          repositories(first:100, after:$cursor, privacy:PUBLIC, ownerAffiliations:OWNER, isFork:false) {
            nodes { stargazerCount languages(first:100) {
              edges { size node { name } } pageInfo { hasNextPage }
            } }
            pageInfo { hasNextPage endCursor }
          }
        } }''', {'login': USER, 'cursor': cursor})['repositories']
        for repo in page['nodes']:
            if repo['languages']['pageInfo']['hasNextPage']:
                raise ValueError('Incomplete language data; refusing publication')
            repos += 1
            stars += repo['stargazerCount']
            for edge in repo['languages']['edges']:
                languages[edge['node']['name']] += edge['size']
        if not page['pageInfo']['hasNextPage']:
            break
        next_cursor = page['pageInfo']['endCursor']
        if not next_cursor or next_cursor == cursor:
            raise ValueError('Invalid pagination; refusing publication')
        cursor = next_cursor
    return {'contributions': user['contributionsCollection'], 'languages': languages,
            'stars': stars, 'repos': repos}


def text(x, y, value, size=14, css='label', anchor='start'):
    return (f'<text x="{x}" y="{y}" font-size="{size}" class="{css}" '
            f'text-anchor="{anchor}">{escape(str(value))}</text>')


def card(title, body, width=530, height=280):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}"
 viewBox="0 0 {width} {height}" role="img" aria-label="{escape(title)}">
<title>{escape(title)}</title><style>
svg {{ font-family: DejaVu Sans,Segoe UI,Arial,sans-serif; }}
.bg {{ fill:#fff; stroke:#ddcbdc; }} .label {{ fill:#584b62; }}
.title {{ fill:#80546e; font-weight:600; }} .value {{ fill:#80546e; font-weight:600; }}
.rose {{ fill:#a34663; }} .lavender {{ fill:#75608f; }} .empty {{ fill:#eee7f1; }}
@media(prefers-color-scheme:dark) {{
.bg {{ fill:#16121c; stroke:#48354e; }} .label {{ fill:#cbbfd5; }}
.title,.value {{ fill:#f0afbe; }} .rose {{ fill:#e58d9e; }}
.lavender {{ fill:#b6a4d9; }} .empty {{ fill:#2c2235; }} }}
</style><rect class="bg" x="1" y="1" width="{width-2}" height="{height-2}" rx="16"/>
{text(28, 39, title, 20, 'title')}{body}</svg>'''


def render(data):
    c = data['contributions']
    calendar = c['contributionCalendar']
    days = [d for w in calendar['weeks'] for d in w['contributionDays']]
    counts = [d['contributionCount'] for d in days]
    if (not days or any(type(n) is not int or n < 0 for n in counts)
            or sum(counts) != calendar['totalContributions']):
        raise ValueError('Incomplete or inconsistent contribution calendar')
    dates = [date.fromisoformat(d['date']) for d in days]
    if any((b-a).days != 1 for a, b in zip(dates, dates[1:])):
        raise ValueError('Contribution calendar has missing or repeated dates')
    span = f'{days[0]["date"]} – {days[-1]["date"]}'
    body = text(28, 65, 'Contributions · GitHub calendar window', 12)
    rows = [('Total contributions', calendar['totalContributions']),
            ('Commit contributions', c['totalCommitContributions']),
            ('Pull requests', c['totalPullRequestContributions']),
            ('Issues / reviews', f'{c["totalIssueContributions"]} / {c["totalPullRequestReviewContributions"]}')]
    for i, (label, value) in enumerate(rows):
        y = 101 + i*30
        body += text(28, y, label) + text(500, y, value, 18, 'value', 'end')
    body += text(28, 235, span, 12)
    body += text(28, 257, f'{data["stars"]} stars · {data["repos"]} public non-fork repos', 12)
    stats = card('GitHub Stats', body)
    total = sum(data['languages'].values())
    if any(type(v) is not int or v < 0 for v in data['languages'].values()):
        raise ValueError('Invalid language bytes')
    body = text(28, 65, 'Code bytes · owned public non-fork repos', 12)
    top = data['languages'].most_common(6)
    if not total:
        body += text(28, 120, 'No language bytes reported by GitHub')
    for i, (name, size) in enumerate(top):
        y = 91 + i*25
        share = '<0.1%' if 0 < size/total < .001 else f'{size/total:.1%}'
        body += text(28, y, name, 13) + text(500, y, share, 13, 'label', 'end')
        body += f'<rect class="empty" x="28" y="{y+5}" width="472" height="4" rx="2"/>'
        body += f'<rect class="{"rose" if i%2==0 else "lavender"}" x="28" y="{y+5}" width="{472*size/total:.2f}" height="4" rx="2"/>'
    body += text(28, 257, 'Share of all detected bytes; top 6 shown', 12)
    languages = card('Top Languages', body)
    body = text(28, 65, f'{calendar["totalContributions"]} contributions · {span}', 13)
    # Calendar heatmap: one column per week, exact daily GitHub contribution counts.
    weeks = calendar['weeks']
    step = min(19, 1000 / len(weeks))
    colors = ['empty', 'lavender', 'rose']
    last_month = None
    for x, week in enumerate(weeks):
        for d in week['contributionDays']:
            day = date.fromisoformat(d['date'])
            px, py = 56+x*step, 100+((day.weekday()+1)%7)*18
            n = d['contributionCount']
            color = colors[0 if not n else 1 if n < 10 else 2]
            body += (f'<rect x="{px:.2f}" y="{py}" width="14" height="14" rx="3" '
                     f'class="{color}"><title>{d["date"]}: {n} contributions</title></rect>')
            if day.month != last_month and (day.day <= 7 or last_month is None):
                body += text(round(px, 2), 90, day.strftime('%b'), 11)
                last_month = day.month
    for y, label in [(130, 'Mon'), (166, 'Wed'), (202, 'Fri')]:
        body += text(28, y, label, 10)
    body += text(28, 253, 'Daily contributions reported by GitHub · not repository commit history', 12)
    for x, css, label in [(800, 'empty', '0'), (866, 'lavender', '1–9'), (950, 'rose', '10+')]:
        body += f'<rect x="{x}" y="242" width="14" height="14" rx="3" class="{css}"/>'
        body += text(x+21, 253, label, 11)
    return {'stats': stats, 'languages': languages,
            'activity': card('Contribution Activity', body, 1100, 280)}
