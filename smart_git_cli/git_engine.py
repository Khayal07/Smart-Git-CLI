"""Git integration layer wrapping GitPython."""

from __future__ import annotations

from typing import Optional

import git

from smart_git_cli.errors import NoChangesError, NotARepoError


class GitEngine:
    """Thin wrapper around the underlying git repository."""

    def __init__(self, repo: git.Repo) -> None:
        self.repo = repo

    @classmethod
    def from_dir(cls, path: str = ".") -> "GitEngine":
        try:
            repo = git.Repo(path, search_parent_directories=True)
        except (git.InvalidGitRepositoryError, git.NoSuchPathError) as exc:
            raise NotARepoError(path) from exc
        return cls(repo)

    def diff_text(self) -> str:
        """Return the staged diff, falling back to the unstaged diff."""
        diff = self._staged_diff()
        if not diff:
            diff = self._unstaged_diff()
        if not diff:
            raise NoChangesError()
        return diff

    def _staged_diff(self) -> str:
        return self.repo.git.diff("--cached", "--no-ext-diff").strip()

    def _unstaged_diff(self) -> str:
        return self.repo.git.diff("--no-ext-diff").strip()

    def last_tag(self) -> Optional[str]:
        """Return the newest tag reachable from HEAD, if any."""
        tags = sorted(
            (t for t in self.repo.tags if t.commit is not None),
            key=lambda t: t.commit.committed_datetime,
            reverse=True,
        )
        return tags[0].name if tags else None

    def commits_since_tag(self, limit: int = 100) -> list[str]:
        """Return commit messages between the last tag and HEAD."""
        tag = self.last_tag()
        if tag:
            messages = [
                c.message.strip()
                for c in self.repo.iter_commits(f"{tag}..HEAD", max_count=limit)
            ]
        else:
            messages = [
                c.message.strip()
                for c in self.repo.iter_commits("HEAD", max_count=limit)
            ]
        return messages if messages else ["No commits available yet."]

    @staticmethod
    def truncate(text: str, max_chars: int = 6000) -> str:
        """Truncate text at a word boundary to cap token usage."""
        if len(text) <= max_chars:
            return text
        cut = text[:max_chars]
        idx = cut.rfind("\n")
        if idx > max_chars * 0.75:
            cut = cut[:idx]
        return cut + "\n... [diff truncated]"