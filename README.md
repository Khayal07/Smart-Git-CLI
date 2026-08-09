# Smart Git CLI (`smart-git-cli`)

A lightweight CLI developer tool that inspects your `git diff` and automatically generates **Conventional Commits** messages and **release notes** using OpenAI's `gpt-4o-mini`.

---

## ✨ Features

- 🔍 Reads staged diff (falls back to unstaged diff when nothing is staged)
- ✍️ Generates a Conventional Commit message via `gpt-4o-mini`
- ✅ Interactive `[Y/n]` confirmation before committing
- 📝 Generates a clean `CHANGELOG.md` from commits between the last tag and `HEAD`
- 💸 Cost-effective: short prompts, small `max_tokens`, ~6k char diff cap
- 🧯 Graceful errors for missing API key, missing repo, or empty diffs

---

## 🛠️ Tech Stack

| Layer      | Tech                        |
| ---------- | --------------------------- |
| Language   | Python 3.10+                |
| CLI        | `typer` + `rich`            |
| Git        | `GitPython`                 |
| AI         | OpenAI SDK (`gpt-4o-mini`)  |

---

## 🚀 Installation

```bash
pip install -e .
# or install the dependencies directly
pip install typer rich GitPython openai
```

Then set your API key:

```bash
setx OPENAI_API_KEY "your-openai-api-key"   # Windows
# or: export OPENAI_API_KEY="..."           # macOS / Linux
```

> Restart your terminal after using `setx`.

---

## 📖 Usage

### Automated commit

```bash
smart-git commit              # uses the staged diff
smart-git commit --all        # stage everything first, then commit
```

Flow: read diff → generate message → preview with Rich → confirm `[Y/n]` → commit.

### Release notes

```bash
smart-git release                          # writes ./CHANGELOG.md
smart-git release --output NG.md         # custom output path
smart-git release --limit 50             # cap number of commits
```

---

## 🏗️ Project Layout

```
smart_git_cli/
├── __init__.py      # package metadata
├── __main__.py      # python -m smart_git_cli
├── cli.py           # typer app: `commit`, `release`
├── git_engine.py    # GitPython: diff, tags, commit parsing
├── ai_engine.py     # OpenAI: commit message + release notes
└── errors.py        # custom exceptions
```

---

## ⚠️ Error Handling

| Situation                         | Behavior                                |
| --------------------------------- | --------------------------------------- |
| `OPENAI_API_KEY` missing          | Clear error, exit code 1                |
| Not a git repository              | `NotARepoError`, exit code 1            |
| Empty diff                        | `NoChangesError`, exit code 1            |
| OpenAI API/JSON failure            | `AICallError`, graceful message          |

---

## 📝 License

MIT