# GitHub Readme Stats renderer

Source: https://github.com/anuraghazra/github-readme-stats

Commit: `54a7985aeefda00d5eadb55b80c17c7f976c37d2`

This directory contains the statistics-card renderer, rank calculation,
and their transitive local imports from the source commit. The upstream MIT license
is retained in `LICENSE`. Trailing whitespace has been normalized. Only `emoji-name-map` and `word-wrap` are needed at runtime.

Data fetching is handled separately by `scripts/render_stats.mjs` so the profile
can use public aggregate counts with the repository's built-in GitHub token.
