# Makefile for GrammarKit Documentation
.PHONY: help install serve build clean deploy requirements

# Default target
help:
	@echo "Available commands:"
	@echo "  make install      - Install all dependencies using uv"
	@echo "  make serve        - Run local development server"
	@echo "  make build        - Build static documentation site"
	@echo "  make clean        - Clean build artifacts"
	@echo "  make deploy       - Deploy to GitHub Pages"
	@echo "  make requirements - Export dependencies to requirements.txt"

# Install dependencies
install:
	uv sync

# Run local development server
serve: install
	uv run mkdocs serve --dev-addr 127.0.0.1:8000 --livereload

# Build static site
build: install
	uv run mkdocs build --strict --verbose

# Clean build artifacts
clean:
	rm -rf site/
	rm -rf .cache/
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

# Deploy to GitHub Pages
deploy: build
	uv run mkdocs gh-deploy --force --clean --verbose

# Export dependencies for non-uv users
requirements: install
	uv export --no-dev --format requirements-txt > requirements.txt
	@echo "Dependencies exported to requirements.txt"