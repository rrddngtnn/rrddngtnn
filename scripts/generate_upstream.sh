#!/usr/bin/env bash
# Run unmodified, commit-pinned upstream generators; never substitute measurements.
set -euo pipefail
: "${GITHUB_TOKEN:?An authenticated GitHub token is required}"
root="$PWD"
work="$(mktemp -d "${TMPDIR:-${RUNNER_TEMP:?}}/profile-generators.XXXXXX")"
trap 'rm -rf "$work"' EXIT
checkout() {
  git init -q "$work/$1"
  git -C "$work/$1" remote add origin "https://github.com/$2.git"
  git -C "$work/$1" fetch -q --depth=1 origin "$3"
  git -C "$work/$1" checkout -q --detach FETCH_HEAD
  test "$(git -C "$work/$1" rev-parse HEAD)" = "$3"
}
checkout stats stats-organization/github-readme-stats-action 2c498845f71017821efaad14293ebc736156ef21
checkout streak DenverCoder1/github-readme-streak-stats 125aaaf200620410446ebfa51897fca3607e04fd
checkout trophy ryo-ma/github-profile-trophy 43736b50a82fca73c8df1c81abb40aa03519975c
# Same locked production dependency installation as the official stats action.
npm install --prefix "$work/tools" --ignore-scripts=false pnpm@11.20.0 deno@2.5.6
export PATH="$work/tools/node_modules/.bin:$PATH"
(cd "$work/stats" && pnpm install --frozen-lockfile --prod --ignore-scripts)
export PAT_1="$GITHUB_TOKEN" INPUT_CORE_VERSION=2.3.0 INPUT_FAIL_ON_ERROR=true
colors='username=rrddngtnn&bg_color=091722&title_color=83d9f2&text_color=e3faff&icon_color=b7e7f3&border_color=1b4358'
INPUT_CARD=stats INPUT_OPTIONS="$colors&show_icons=true" INPUT_PATH="$root/.github/assets/stats.svg" node "$work/stats/index.js"
INPUT_CARD=top-langs INPUT_OPTIONS="$colors&layout=compact&langs_count=6" INPUT_PATH="$root/.github/assets/top-langs.svg" node "$work/stats/index.js"
(cd "$work/streak" && composer install --no-dev --no-interaction --prefer-dist --optimize-autoloader)
TOKEN="$GITHUB_TOKEN" INPUT_OPTIONS='user=rrddngtnn&background=091722&border=1b4358&stroke=1b4358&ring=83d9f2&fire=b7e7f3&currStreakNum=e3faff&sideNums=e3faff&currStreakLabel=83d9f2&sideLabels=83d9f2&dates=b7e7f3&disable_animations=true' INPUT_PATH="$root/.github/assets/streak.svg" php "$work/streak/bin/generate-card.php"
GITHUB_TOKEN1="$GITHUB_TOKEN" GITHUB_TOKEN2="$GITHUB_TOKEN" deno run --allow-net --allow-env --allow-read --allow-write "$work/trophy/render_svg.ts" rrddngtnn "$root/.github/assets/trophies.svg" nord
python3 scripts/generate_readme.py
