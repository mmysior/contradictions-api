# Claude Code Documentation

## Commit Authorship

Commits made by Claude Code use the following author information:
```
Author: Claude <noreply@anthropic.com>
```

This is done using the `--author` flag without modifying git config:
```bash
git commit --author="Claude <noreply@anthropic.com>" -m "commit message"
```

This makes it easy to distinguish between human-authored and AI-assisted commits in the git history.
