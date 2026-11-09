# Current profile contract

Ice wave header → existing centered introduction/headline → standard GitHub Readme Stats card and compact Top Languages card side by side at 48% width → unchanged ice wave footer. No contribution graph, streak, repository list or custom-designed statistics.

Header and footer SVGs are unchanged. The header's RED lettering alone stays red (`#d93848`). Card colors are upstream options: background `091722`, title `83d9f2`, text `e3faff`, icons `b7e7f3`, border `1b4358`. No custom card renderer or metric calculation is used.

README.source.md is authoritative; CI copies it verbatim only after both upstream-generated SVGs pass validation. The official maintained stats-organization/github-readme-stats-action and core versions are pinned in the workflow. Generation uses GITHUB_TOKEN for public data, explicitly fails on upstream errors, and commits output only after both cards succeed. Old custom SVGs are pruned at successful publication.

Daily schedule: 03:17 UTC (10:17 WIB), subject to GitHub delays. Push triggers cover source/icons/scripts/workflow; manual dispatch remains available. See ATTRIBUTION.md for upstream/provider limitations and metric semantics.
