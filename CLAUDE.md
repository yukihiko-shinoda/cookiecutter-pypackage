# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Cookiecutter template for Python packages, forked from briggySmalls/cookiecutter-pypackage. It generates Python projects with modern tooling and development workflows.

## Key Architecture

- **Template Structure**: The `{{cookiecutter.github_repository_name}}/` directory contains the template files that will be generated
- **Hook System**: 
  - `hooks/pre_gen_project.py`: Validates cookiecutter inputs before generation
  - `hooks/post_gen_project.py`: Removes unused files and configures project based on user choices (CLI framework, license, etc.)
- **Configuration**: `cookiecutter.json` defines all template variables and their default values
- **Generated Projects**: Use `uv` for dependency management and `invoke` for task management

## Common Development Commands

### Main Repository (Template Development)
```bash
# Install dependencies
uv sync

# Run all tests (includes baking the template and testing generated projects)
uv run invoke test

# Run fast tests only (skip slow template baking tests)
uv run invoke test.fast

# Lint the template code
uv run invoke lint

# Format code
uv run invoke style

# Clean up build artifacts
uv run invoke clean

# Build distribution packages
uv run invoke dist

# Generate documentation
uv run invoke docs
```

### Generated Projects (Template Output)
Generated projects include these standardized commands via invoke:

```bash
# Test generated project
uv run invoke test           # Fast tests
uv run invoke test.all       # All tests including slow ones
uv run invoke test.coverage  # Tests with coverage report

# Linting and analysis
uv run invoke lint           # Fast linting (ruff, bandit, flake8, etc.)
uv run invoke lint.deep      # Comprehensive linting (mypy, pylint, semgrep)
uv run invoke lint.mypy      # Type checking
uv run invoke lint.pylint    # Pylint analysis

# Code formatting
uv run invoke style          # Format with docformatter and ruff

# Build and distribution
uv run invoke dist           # Build source and wheel packages

# Cleanup
uv run invoke clean          # Clean all build artifacts
```

## Template Configuration

The template supports these key options (in cookiecutter.json):
- **Command line interface**: Click, Argparse, or none
- **License**: MIT, GPL-3.0, Apache-2.0, BSD-3-Clause, or proprietary
- **PyPI deployment**: GitHub Actions workflow for automated publishing
- **Testing**: pytest integration (recommended)

## Development Workflow

1. **Testing Template Changes**: Always run `uv run invoke test` to ensure template generates correctly
2. **Generated Project Structure**: Each generated project includes:
   - Modern Python packaging with pyproject.toml
   - Comprehensive linting with ruff, flake8, mypy, pylint
   - Testing with pytest and coverage
   - CI/CD with GitHub Actions
   - Optional CLI with Click or argparse

## Important Files

- `cookiecutter.json`: Template configuration and variables
- `hooks/post_gen_project.py`: Post-generation cleanup and configuration logic
- `{{cookiecutter.github_repository_name}}/tasks.py`: Template for generated project's invoke tasks
- `{{cookiecutter.github_repository_name}}/pyproject.dist.toml`: Template pyproject.toml that becomes pyproject.toml in generated projects

## Quality Standards

Generated projects enforce strict code quality with:
- Line length: 88 characters (Black compatible)
- Type checking with mypy in strict mode
- Comprehensive linting rules via ruff with "ALL" rules enabled
- Security analysis with bandit and semgrep
- Code complexity analysis with radon and xenon
- Import sorting with single-line imports (compatible with flake8-hacking)