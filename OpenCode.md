# OpenCode Guidelines

This file provides OpenCode-specific development guidelines for this repository.

> **📖 For comprehensive project information, see [README.md](README.md)**  
> **🤖 For multi-agent coordination, see [AGENTS.md](AGENTS.md)**  
> **📋 For tasks and roadmap, see [TODO.md](TODO.md)**

## Build & Test
- Install dependencies: `uv add <package>`
- Run CLI tools: `uv run ondansetron`, `uv run ondansetron-search "query"`, etc.
- Generate manuscript PDF/DOCX in `manuscript/`: `make pdf` / `make docx`
- Run full test suite: `pytest`
- Run a single test: `pytest tests/test_search.py::test_function_name` or `pytest -k "search"`
- Lint & format: `black . && isort .`

## Code Style
- Imports: stdlib first, blank line, third-party, blank line, local modules (PEP8)
- Formatting: use Black (88 cols), f-strings, no trailing commas in function calls
- Type hints: annotate public functions and methods using `typing` types
- Naming: `snake_case` for functions/vars, `PascalCase` for classes, `UPPER_SNAKE` for constants
- Error handling: raise specific exceptions, avoid bare `except`, use `logging` for errors
- Logging: configure via `logging` module at entrypoint; avoid `print` in library code
- Docstrings: Google style with `Args`, `Returns`, `Raises`
- Modules: small focused modules, one main class per file, functions <50 lines
- Avoid wildcard imports; always use explicit imports

## Notebooks
- Launch with Jupyter or convert: `jupyter nbconvert --to html presentation.ipynb`

## Related Documentation

- **[README.md](README.md)** - Complete project overview, installation, usage, CLI documentation
- **[AGENTS.md](AGENTS.md)** - Multi-agent workflow coordination and guidelines
- **[TODO.md](TODO.md)** - Project roadmap, current tasks, and progress tracking
- **[AI_INSTRUCTIONS.md](AI_INSTRUCTIONS.md)** - General AI agent instructions
- **[CLAUDE.md](CLAUDE.md)** - Claude Code specific instructions
- **OpenCode.md** (this file) - OpenCode guidelines

**For multi-agent coordination and avoiding conflicts, see [AGENTS.md](AGENTS.md).**
