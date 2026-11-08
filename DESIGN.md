# Profile design

Original editorial layout: identity, two selected public repositories, evidenced tools, then live public statistics. Inspired by the reference profile's identity/project/tools/statistics hierarchy, not its prose, experience claims or decorative assets. No upstream design code was copied.

## Palette

| Role | Previous | Current |
| --- | --- | --- |
| Base | `#06080d` | ivory `#f3efe6` / charcoal `#242522` |
| Primary accent | cyan `#38bdf8` | copper `#8c4b30` |
| Secondary accent | violet `#a78bfa` | sage `#b9c4a6` |
| Extra accents | `#22d3ee`, `#7dd3fc`, `#60a5fa` | removed |
| Light text | white / translucent blue-white | `#f3efe6`, `#d2d2c7` |
| Muted text | translucent blue-grey | `#64675d` |
| Rules | translucent cyan/white | `#c9c6bb`, `#50534b` |

Inter 400/700, 48px shared content rail, 4px spacing grid. Flat backgrounds, no animation, glows, badge clouds or external icon dependencies. The copper wordmark is the only high-emphasis color on the light panel; all nonzero statistics share sage. Zero values stay neutral.

## Public evidence

- Headline: [StyxRouter](https://github.com/rrddngtnn/styxrouter) AI gateway and [s0ulctl](https://github.com/rrddngtnn/s0ulctl) CLI. No employment, seniority or years-of-experience claims.
- TypeScript, Bun, Hono: StyxRouter `apps/server/package.json` and public `.ts` entry points.
- React: StyxRouter `apps/panel/package.json`.
- JavaScript, Shell, Node.js, node:test, ShellCheck: s0ulctl `package.json`, `bin/`, `src/`, `tests/`.
- Python: public `domain-probeclaim` and `gsuite-seatpool` source/language metadata.
- GitHub Actions: s0ulctl `.github/workflows/ci.yml` and this repository's generator.

The reference repository currently uses `master`; its contents API, recursive tree and path history show no `README.source.md`. Both `main` and `master` raw source paths return 404. Its actual authored `README.md` was inspected instead; no claim is made to have recovered a nonexistent source file.

## Pipeline ownership

Retain the existing pinned renderer, SHA-pinned actions, serialization, fail-closed live-data wrapper and sole CI ownership of generated output. Daily schedule: 03:17 UTC / 10:17 WIB, subject to GitHub scheduling delays. Push and manual dispatch remain supported. Local rendering is preview-only; do not commit locally generated `README.md` or `.github/assets` alongside source edits.

The profile remote returned 404 to authenticated REST, GraphQL and Git while the account and other public repositories resolved. Local history was recovered into a dedicated clone from `resources/github-profile-auto-update`; nothing in that checkout was modified. Do not silently create a replacement repository or claim a deployment while this is unresolved.
