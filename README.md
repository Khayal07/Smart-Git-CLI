# Smart Git CLI (`smart-git-cli`) 🚀

A lightweight, cost-effective CLI tool built with Python and OpenAI (`gpt-4o-mini`) to automate Git workflows.

> **Status:** 🚧 Under Active Development

---

## 📌 Project Overview

`smart-git-cli` is a developer tool designed to inspect `git diff` outputs and automatically generate:
- **Conventional Commits** messages following standard specifications.
- **Release Notes** and `CHANGELOG` summaries based on commit history.

It leverages `gpt-4o-mini` with structured JSON output to keep execution speed high and token costs minimal (< $0.0001 per run).

---

## 🛠️ Planned Tech Stack

- **Language:** Python 3.10+
- **CLI Framework:** `typer` & `rich`
- **Git Integration:** `GitPython`
- **AI Engine:** OpenAI API (`gpt-4o-mini`)