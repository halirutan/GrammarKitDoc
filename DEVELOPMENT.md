# GrammarKit Documentation Development

This documentation project uses [uv](https://github.com/astral-sh/uv) for Python dependency management and [MkDocs](https://www.mkdocs.org/) with Material theme for building the documentation.

## Prerequisites

- Python 3.12 or later
- uv (install from https://github.com/astral-sh/uv)

## Quick Start

1. Install dependencies:
   ```bash
   make install
   # or
   python scripts.py install
   ```

2. Run development server:
   ```bash
   make serve
   # or
   python scripts.py serve
   ```

3. Open http://127.0.0.1:8000 in your browser

## Available Commands

### Using Make (Linux/macOS)
- `make install` - Install all dependencies
- `make serve` - Run local development server with live reload
- `make build` - Build static documentation site
- `make clean` - Clean build artifacts
- `make deploy` - Deploy to GitHub Pages
- `make requirements` - Export dependencies to requirements.txt

### Using Python scripts (Cross-platform)
- `python scripts.py install` - Install all dependencies
- `python scripts.py serve` - Run local development server
- `python scripts.py build` - Build static documentation
- `python scripts.py clean` - Clean build artifacts
- `python scripts.py deploy` - Deploy to GitHub Pages
- `python scripts.py requirements` - Export dependencies

## Project Structure

```
.
├── mkdocs.yml           # MkDocs configuration
├── pyproject.toml       # Project metadata and dependencies
├── .python-version      # Python version for uv
├── Makefile            # Build commands for Unix-like systems
├── scripts.py          # Cross-platform build scripts
├── docs/               # Documentation source files
│   ├── index.md
│   ├── getting-started/
│   ├── core-concepts/
│   └── ...
└── site/               # Generated documentation (git-ignored)
```

## Dependencies

### Documentation
- **mkdocs** - Static site generator
- **mkdocs-material** - Material Design theme
- **mkdocs-minify-plugin** - HTML/CSS/JS minification
- **pymdown-extensions** - Enhanced Markdown features

### Development
- **watchdog** - File system monitoring for live reload
- **ruff** - Python linting and formatting
- **pre-commit** - Git hook management

## Working with uv

uv automatically manages virtual environments and dependencies:

```bash
# Sync dependencies
uv sync

# Add a new dependency
uv add package-name

# Add a development dependency
uv add --dev package-name

# Run commands in the environment
uv run mkdocs --help
```

## Building Documentation

### Development Build
The development server automatically rebuilds on file changes:
```bash
make serve
```

### Production Build
Create optimized static files in the `site/` directory:
```bash
make build
```

### GitHub Pages Deployment
Deploy directly to GitHub Pages (requires push permissions):
```bash
make deploy
```

## Tips

1. **Live Preview**: The development server supports live reload. Save your Markdown files and see changes instantly.

2. **Strict Mode**: Production builds use `--strict` flag to catch broken links and other issues.

3. **Clean Builds**: Run `make clean` before building if you encounter caching issues.

4. **Compatibility**: Use `make requirements` to generate a requirements.txt file for users without uv.

## Troubleshooting

### Port Already in Use
If port 8000 is busy, you can modify the port in Makefile or scripts.py.

### Module Not Found
Ensure you're using uv to run commands:
```bash
uv run mkdocs serve  # Correct
mkdocs serve        # May fail if not in virtual environment
```

### Permission Errors
Make sure scripts.py is executable:
```bash
chmod +x scripts.py
```