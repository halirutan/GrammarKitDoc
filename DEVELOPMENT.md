# Development Guide

This repository contains the user documentation for [Grammar-Kit](https://github.com/JetBrains/Grammar-Kit), built with [MkDocs](https://www.mkdocs.org/) and the Material theme. It uses [uv](https://github.com/astral-sh/uv) for Python dependency management.

You need Python 3.12 or later and uv installed before you begin. Install uv from https://github.com/astral-sh/uv if you do not already have it.

## Quick Start

Run `make install` to install dependencies, then `make serve` to start the development server. Open http://127.0.0.1:8000 in your browser to preview the site. The server watches for file changes and reloads automatically.

On Windows, use `python scripts.py install` and `python scripts.py serve` instead.

## Commands

All commands are available through `make` (Linux/macOS) or `python scripts.py` (Windows). Both interfaces support the same set of operations.

| Command | What it does |
|---------|-------------|
| `make install` | Install all dependencies via `uv sync` |
| `make serve` | Start the dev server at http://127.0.0.1:8000 with live reload |
| `make build` | Build the static site in `site/` with `--strict` mode |
| `make clean` | Remove `site/`, `.cache/`, and Python bytecode files |
| `make deploy` | Build and deploy to GitHub Pages (requires push permissions) |
| `make requirements` | Export production dependencies to `requirements.txt` |

The `build` and `deploy` commands run in strict mode, which catches broken links and other issues that the dev server does not flag. Run `make clean` before building if you encounter stale output from a previous build.

## Project Structure

```
.
├── mkdocs.yml              # MkDocs configuration and nav structure
├── pyproject.toml           # Python dependencies (managed by uv)
├── Makefile                 # Build commands (Linux/macOS)
├── scripts.py               # Build commands (Windows)
├── docs/                    # Documentation source (Markdown)
│   ├── index.md
│   ├── grammar-development/
│   ├── code-generation/
│   ├── integration/
│   ├── advanced/
│   ├── reference/
│   └── appendices/
├── evidence-ledger/         # Evidence files that back each topic
├── Grammar-Kit/             # Grammar-Kit source (read-only submodule)
├── info/                    # Project planning and outlines
└── site/                    # Generated output (git-ignored)
```

### Documentation content

The `docs/` directory contains the Markdown source files organized by section. The navigation structure is defined in `mkdocs.yml`. When you add or move pages, update the `nav` key in that file.

### Evidence ledger

Documentation in this project follows an evidence-based workflow. The `evidence-ledger/` directory mirrors the structure of `docs/` and contains supporting files for each topic:

- `code-evidence.md` has technical facts extracted from Grammar-Kit source code.
- `examples.md` has code examples and snippets.
- `references.md` has links and external references.
- `topic-summary.md` has writing guidance and content structure for the topic.

When writing or editing documentation, treat the evidence files as the source of truth for technical claims. The `Grammar-Kit/` submodule is the upstream source, but contributors working on docs should rely on the evidence ledger rather than reading source code directly.

### Project planning

The `info/` directory contains the documentation outline, user personas, and a catalog of documentation-relevant files from Grammar-Kit. These files guide content planning and prioritization.

## Working with uv

Dependencies are declared in `pyproject.toml` and locked in `uv.lock`. The `make install` command runs `uv sync`, which creates a virtual environment and installs everything automatically. You do not need to activate the environment manually.

To add a new MkDocs plugin or extension, run `uv add package-name`. For tools only needed during development, run `uv add --dev package-name`. If you need to run an arbitrary command inside the managed environment, prefix it with `uv run`, for example `uv run mkdocs --help`.

## Troubleshooting

If port 8000 is already in use, edit the `--dev-addr` value in `Makefile` or `scripts.py` to use a different port.

If you see "module not found" errors, make sure you are running commands through uv. Running `mkdocs serve` directly will fail unless the virtual environment is activated. Use `uv run mkdocs serve` or `make serve` instead.
