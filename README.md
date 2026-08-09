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

Then configure your API key using a `.env` file (recommended):

```bash
copy .env.example .env     # Windows
cp .env.example .env       # macOS / Linux
```

Open `.env` and paste your key after `OPENAI_API_KEY=`.

> `.env` is git-ignored, so your secrets never get committed. `smart-git` loads
> it automatically — no `setx`/`export` needed. An existing environment
> variable always wins over `.env`.

Alternatively, export it manually:

```bash
setx OPENAI_API_KEY "your-openai-api-key"   # Windows (restart terminal)
export OPENAI_API_KEY="..."                 # macOS / Linux
```

---

## ⚡ Quick start (in any project)

You don't need this repository in your project — just install the tool once and run it inside any Git repository.

**1. Install globally**

```bash
pip install git+https://github.com/Khayal07/Smart-Git-CLI.git
# or, if you cloned it locally:
# pip install -e /path/to/smart-git-cli
```

**2. Add your API key**

Place a `.env` file in the project where you will run `smart-git` (smart-git reads it from the **current folder**):

```bash
copy .env.example .env     # Windows  (if you cloned the repo, copy its .env.example)
cp .env.example .env       # macOS / Linux
```

Then open `.env` and set your key:

```
OPENAI_API_KEY=sk-your-api-key
```

> `.env` is git-ignored automatically, so the key never ends up in your commits.

**3. Use it anywhere**

```bash
smart-git commit     # in your project, after staging some changes
smart-git release    # writes ./CHANGELOG.md in your project
```

That's it — no code changes, no imports, no config files inside your app.

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