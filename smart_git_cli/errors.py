"""Custom exceptions for graceful CLI error handling."""

from __future__ import annotations


class SmartGitError(Exception):
    """Base class for all expected, user-facing failures."""


class NotARepoError(SmartGitError):
    def __init__(self, path: str) -> None:
        super().__init__(f"No git repository found at '{path}'.")
        self.path = path


class NoChangesError(SmartGitError):
    def __init__(self) -> None:
        super().__init__("Nothing to commit - no staged or unstaged changes found.")


class ConfigError(SmartGitError):
    """Raised when required configuration (e.g. an API key) is missing."""


class AICallError(SmartGitError):
    """Raised when the AI provider fails or returns an invalid response."""