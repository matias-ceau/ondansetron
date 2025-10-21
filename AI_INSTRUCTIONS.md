# AI Agent Instructions

This file provides instructions and context to guide general AI assistants when working on this repository.

> **📖 For comprehensive project information, see [README.md](README.md)**  
> **🤖 For multi-agent coordination, see [AGENTS.md](AGENTS.md)**  
> **📋 For tasks and roadmap, see [TODO.md](TODO.md)**

## Quick Reference

### Project Type
Academic research project: Master's thesis on **Ondansetron in alcohol use disorder** - systematic review with Python CLI automation tools.

### Project Overview

- **Title**: Ondansetron in alcohol use disorder: a systematic review
- **Authors**: Matias Ceau, Pr Mélina Fatseas
- **Date**: November 2024
- **Abstract**: Found in the YAML front matter of `manuscript/memoire.md`
- **Bibliography**: `manuscript/memoire.bib` and `ondansetron.bib`
- **Main manuscript**: `manuscript/memoire.md` (Markdown with Pandoc/LaTeX YAML front matter)

### Key Commands

**Build manuscript:**
```bash
cd manuscript
make pdf   # Generate memoire.pdf
make docx  # Generate memoire.docx
```

**Run CLI tools:**
```bash
uv run ondansetron --help
uv run ondansetron search "query"
uv run ondansetron update-trials --term "ondansetron alcohol" --days 30
uv run ondansetron review manuscript/memoire.md
```

### Project Structure

- `manuscript/` - Main manuscript and outputs
  - `memoire.md` - Master manuscript (Markdown + YAML)
  - `memoire.bib` - Bibliography
  - `archives/` - Previous versions
- `src/ondansetron/` - Python CLI tools package
- `sourcedata/` - Clinical trials and analysis data
- `ressources/` - PDFs, PRISMA flowchart, vector index
- `tests/` - Test suite


## Code and Data

- **Python package**: `src/ondansetron/` - Complete CLI toolkit with multiple tools
  - `search.py` - LLM-powered literature search
  - `update_trials.py` - Clinical trials metadata fetching
  - `review.py` - Manuscript review assistant
  - `compare_trials.py` - Trial comparison tool
  - `gen_memoire_llm.py` - LLM manuscript generation
  - `generate_prisma.py` - PRISMA flowchart generator
  - `build_vector_index.py` - Vector search index builder
  - `get_keys.py` - API key management
- **Notebooks**: `ondansetron.ipynb`, `presentation.ipynb` for interactive analysis
- **Resources**: PDFs in `ressources/` (PRISMA checklist, Cochrane tools, vector index)
- **Raw data**: JSON files in `sourcedata/` (trials, historical analyses)

### CLI Tools Available

```bash
uv run ondansetron --help                    # Main CLI with all subcommands
uv run ondansetron search "query"            # LLM-powered search
uv run ondansetron update-trials --days 30   # Fetch recent trials
uv run ondansetron review manuscript/memoire.md  # Interactive review
uv run ondansetron-compare-trials            # Compare trials
```

See [README.md](README.md) for complete CLI documentation.

## Typical Tasks

### Manuscript Work
- Edit manuscript text in `manuscript/memoire.md`
- Add and format citations in `manuscript/memoire.bib`
- Run `make pdf` or `make docx` in `manuscript/` for generation
- Update tables and figures; manage files in `ressources/`
- Maintain archives under `manuscript/archives/`

### Development Work
- Modify Python code in `src/ondansetron/`
- Add tests in `tests/`
- Update documentation
- Add dependencies with `uv add <package>`
- Run tests with `uv run pytest`

### Data Management
- Update trials data in `sourcedata/`
- Generate visualizations
- Run analysis scripts

See [TODO.md](TODO.md) for current task priorities.

## Tool Development & Features

### Implemented Tools ✅
- **ondansetron-search** - LLM-powered literature search (OpenAI/Perplexity/OpenRouter)
- **ondansetron-update-trials** - Clinical trials fetching and summarization from PubMed
- **ondansetron-review** - Interactive manuscript review with AI suggestions
- **ondansetron-compare-trials** - Trial comparison and analysis
- **Vector search** - FAISS-based semantic search over papers
- **PRISMA generator** - Automated flowchart generation

### Development Goals (See [TODO.md](TODO.md))
- Automated study screening using NLP
- Data extraction from PDFs (OCR + NLP)
- Meta-analysis tools with forest plots
- Interactive visualizations and dashboards
- Living systematic review automation
- Cost-effectiveness analysis tools

For detailed task list and roadmap, see **[TODO.md](TODO.md)**.
## Key Guidelines

### General Principles
- **Preserve YAML front matter** in `manuscript/memoire.md` - never modify it unintentionally
- **Keep changes minimal** and aligned with existing writing style
- **Follow existing patterns** in code, documentation, and manuscript
- **Coordinate with other agents** - see [AGENTS.md](AGENTS.md) for workflow

### Code Development
- Use `uv add <package>` to add Python dependencies
- Use `uv run <script>` to run project scripts (e.g., `ondansetron`, `ondansetron-search`)
- Use `rg` for searching (not `grep` or `ls -R`)
- Follow code style in [OpenCode.md](OpenCode.md)
- Run tests with `uv run pytest`

### Manuscript Editing
- Preserve YAML front matter in `manuscript/memoire.md`
- Follow existing Markdown and citation styles
- Ensure citation consistency in `manuscript/memoire.bib`
- Test PDF generation after changes: `cd manuscript && make pdf`

### Multi-Agent Coordination
- **Create new branch** for each task: `git checkout -b agent-name/task`
- **Check [AGENTS.md](AGENTS.md)** before editing shared files
- **Update TODO.md** with your progress
- **Commit regularly** with clear messages
- **See [AGENTS.md](AGENTS.md)** for complete coordination guidelines

## Documentation Files

This project includes multiple documentation files:

- **[README.md](README.md)** - Comprehensive project overview, installation, usage
- **[AGENTS.md](AGENTS.md)** - Multi-agent workflow coordination guidelines
- **[TODO.md](TODO.md)** - Project roadmap, tasks, and progress tracking
- **[CLAUDE.md](CLAUDE.md)** - Claude Code specific instructions
- **[OpenCode.md](OpenCode.md)** - OpenCode development guidelines
- **AI_INSTRUCTIONS.md** (this file) - General AI agent instructions

**Always check these files before starting work to understand context and avoid conflicts.**