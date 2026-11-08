"""Generate profile cards with live public GitHub data; never publish mock stats."""
import os
from pathlib import Path
import re
import subprocess
import sys


def main():
    if not os.environ.get("GITHUB_TOKEN"):
        raise SystemExit("GITHUB_TOKEN is required; refusing mock-data generation")
    source = Path("README.source.md").read_text()
    if not re.search(r"^```aura\b", source, re.M):
        Path("README.md").write_text(source)
        for asset in Path(".github/assets").glob("*.svg"):
            asset.unlink()
        print("Static profile published; no statistics cards requested.")
        return
    result = subprocess.run(
        ["npx", "--yes", "readme-aura@1.0.20", "build", "--source", "README.source.md",
         "--output", "README.md", "--assets", ".github/assets", "--github-user", "rrddngtnn"],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, check=False,
    )
    print(result.stdout, end="")
    if result.returncode:
        raise SystemExit(result.returncode)
    # readme-aura exits successfully even when the API fails and it renders mocks.
    if re.search(r"mock (?:repo )?data|GitHub API failed|Repo API failed", result.stdout, re.I):
        raise SystemExit("Refusing to publish: GitHub data fetch failed or mock data was used")
    if "Fetched:" not in result.stdout or "Fetched repo:" not in result.stdout:
        raise SystemExit("Missing confirmation of live GitHub data")
    readme = Path("README.md").read_text()
    refs = set(re.findall(r"\.github/assets/[\w.-]+\.svg", readme))
    assets = {str(p) for p in Path(".github/assets").glob("*.svg")}
    expected = len(re.findall(r"^```aura\b", Path("README.source.md").read_text(), re.M))
    if not refs or refs != assets or len(refs) != expected:
        raise SystemExit("Generated SVG references are missing, orphaned, or incomplete")
    print(f"Validated {len(refs)} generated cards using live public GitHub data.")


if __name__ == "__main__":
    main()
