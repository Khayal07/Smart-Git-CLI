"""AI-powered generation of commit messages and release notes."""

from __future__ import annotations

import json
import os
from typing import Any

from smart_git_cli.errors import AICallError, ConfigError

MODEL = "gpt-4o-mini"
TEMPERATURE = 0.2
MAX_TOKENS = 300

COMMIT_PROMPT = """You are an experienced Git engineer. Turn this diff into one Conventional Commits message.

Rules:
- Format: <type>(<scope>)?: <subject>
- type in: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert
- scope optional and short
- subject in imperative mood, lowercase, under 72 characters
- Add a body only if really useful; max 2 lines, no emojis

Reply with JSON only: {"type": "...", "scope": "...", "subject": "...", "body": "..."}

DIFF:
{diff}"""

RELEASE_PROMPT = """Write clean release notes for a CHANGELOG.md based on these commit messages.

Group them into: ## New features / ## Bug fixes / ## Improvements / ## Documentation
Drop trivial commits. One short imperative line per bullet. No emojis, no numbers.

Reply with JSON only: {"notes": "full markdown here"}

COMMITS:
{commits}"""


def _client() -> Any:
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ConfigError(
            "OPENAI_API_KEY is not set. Run `setx OPENAI_API_KEY \"your-key\"` "
            "or set the env var before running smart-git."
        )
    from openai import OpenAI

    return OpenAI(api_key=key)


def _chat_json(client: Any, prompt: str) -> dict:
    response = client.chat.completions.create(
        model=MODEL,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
        messages=[
            {"role": "system", "content": "Reply ONLY with valid JSON."},
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_object"},
    )
    content = response.choices[0].message.content or "{}"
    try:
        return json.loads(content)
    except json.JSONDecodeError as exc:
        raise AICallError(f"Model returned invalid JSON: {exc}") from exc


def generate_commit_message(diff_text: str) -> str:
    """Return a Conventional Commit message for the given diff."""
    client = _client()
    try:
        data = _chat_json(client, COMMIT_PROMPT.format(diff=diff_text))
    except AICallError:
        raise
    except Exception as exc:
        raise AICallError(f"Failed to generate commit message: {exc}") from exc

    ctype = data.get("type", "").strip() or "chore"
    scope = data.get("scope", "").strip()
    subject = data.get("subject", "").strip().lower()
    if not subject:
        raise AICallError("Model did not produce a subject for the commit message.")
    header = f"{ctype}({scope}): {subject}" if scope else f"{ctype}: {subject}"
    body = data.get("body", "").strip()
    return f"{header}\n\n{body}" if body else header


def generate_release_notes(commits: list[str]) -> str:
    """Return Markdown release notes for the given commit subjects."""
    client = _client()
    prompt = RELEASE_PROMPT.format(commits="\n".join(commits))
    try:
        data = _chat_json(client, prompt)
    except AICallError:
        raise
    except Exception as exc:
        raise AICallError(f"Failed to generate release notes: {exc}") from exc

    notes = data.get("notes") or data.get("output") or data.get("changelog")
    if not isinstance(notes, str) or not notes.strip():
        raise AICallError("Empty release notes returned by the model.")
    return notes.strip() + "\n"