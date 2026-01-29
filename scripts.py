#!/usr/bin/env python3
"""
Convenience scripts for GrammarKit documentation development.
Alternative to Makefile for Windows users.
"""

import sys
import subprocess
import shutil
from pathlib import Path


def run_command(cmd: list[str]) -> int:
    """Run a command and return its exit code."""
    print(f"Running: {' '.join(cmd)}")
    return subprocess.call(cmd)


def install():
    """Install all dependencies using uv."""
    return run_command(["uv", "sync"])


def serve():
    """Run local development server."""
    install()
    return run_command(
        ["uv", "run", "mkdocs", "serve", "--dev-addr", "127.0.0.1:8000", "--livereload"]
    )


def build():
    """Build static documentation site."""
    install()
    return run_command(["uv", "run", "mkdocs", "build", "--strict", "--verbose"])


def clean():
    """Clean build artifacts."""
    dirs_to_remove = ["site", ".cache"]
    for dir_name in dirs_to_remove:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print(f"Removing {dir_name}/")
            shutil.rmtree(dir_path)

    # Remove __pycache__ directories
    for pycache in Path(".").rglob("__pycache__"):
        print(f"Removing {pycache}")
        shutil.rmtree(pycache)

    # Remove .pyc files
    for pyc in Path(".").rglob("*.pyc"):
        print(f"Removing {pyc}")
        pyc.unlink()

    print("Clean complete")
    return 0


def deploy():
    """Deploy to GitHub Pages."""
    build()
    return run_command(["uv", "run", "mkdocs", "gh-deploy", "--force", "--clean", "--verbose"])


def requirements():
    """Export dependencies to requirements.txt."""
    install()
    with open("requirements.txt", "w") as f:
        result = subprocess.run(
            ["uv", "export", "--no-dev", "--format", "requirements-txt"],
            capture_output=True,
            text=True,
        )
        f.write(result.stdout)
    print("Dependencies exported to requirements.txt")
    return 0


def main():
    """Main entry point."""
    commands = {
        "install": install,
        "serve": serve,
        "build": build,
        "clean": clean,
        "deploy": deploy,
        "requirements": requirements,
    }

    if len(sys.argv) < 2 or sys.argv[1] not in commands:
        print("Usage: python scripts.py <command>")
        print("\nAvailable commands:")
        print("  install      - Install all dependencies using uv")
        print("  serve        - Run local development server")
        print("  build        - Build static documentation site")
        print("  clean        - Clean build artifacts")
        print("  deploy       - Deploy to GitHub Pages")
        print("  requirements - Export dependencies to requirements.txt")
        return 1

    command = sys.argv[1]
    return commands[command]()


if __name__ == "__main__":
    sys.exit(main())
