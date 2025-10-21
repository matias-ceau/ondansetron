# Ondansetron in Alcohol Use Disorder: Systematic Review

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

> **A comprehensive academic research project combining traditional systematic review methodology with modern AI-powered research assistance tools.**

## 📚 Project Overview

This repository contains an academic Master's thesis and supporting automation toolkit for a systematic review on **"Ondansetron in alcohol use disorder"**. The project combines:

- **Academic Manuscript**: A full systematic review following PRISMA guidelines
- **Python CLI Tools**: Automated literature search, trial tracking, and manuscript review assistance
- **Data Resources**: Clinical trials metadata, bibliography, and analysis data
- **AI Integration**: LLM-powered search, summarization, and editing assistance

**Authors**: Matias Ceau, Pr Mélina Fatseas  
**Institution**: Academic research (MD thesis)  
**Date**: November 2024

## 🎯 Key Features

### 🔬 Research Components
- Systematic review manuscript in Markdown with YAML front matter
- Comprehensive bibliography (500+ references)
- Clinical trials metadata from multiple sources
- PRISMA flowchart generation
- Risk of bias assessment tools

### 🛠️ Automation Tools
- **Literature Search**: LLM-powered search across multiple providers (OpenAI, Perplexity, OpenRouter)
- **Trial Updates**: Automated fetching and summarization of clinical trials from PubMed
- **Manuscript Review**: Interactive AI-assisted editing and improvement suggestions
- **Trial Comparison**: Comparative analysis of trial metadata
- **Vector Search**: FAISS-based semantic search over papers

### 🤖 Multi-Agent Support
- Integrated with Claude Code, GitHub Copilot, OpenCode
- Coordinated multi-agent workflows for parallel development
- Comprehensive AI agent instructions and guidelines

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [CLI Tools](#cli-tools)
- [Project Structure](#project-structure)
- [Manuscript Workflow](#manuscript-workflow)
- [Development](#development)
- [Documentation](#documentation)
- [Contributing](#contributing)

## 🚀 Installation

### Prerequisites

- **Python 3.12+**
- **uv** package manager ([installation guide](https://github.com/astral-sh/uv))
- **Pandoc** (for document generation)
- **LaTeX distribution** (for PDF generation, e.g., TeX Live or MiKTeX)

### Setup

```bash
# Clone the repository
git clone https://github.com/matias-ceau/ondansetron.git
cd ondansetron

# Install Python dependencies (uv handles this automatically)
# No separate installation step needed

# Set up API keys (choose one or more)
export OPENAI_API_KEY="your-openai-key"
export PERPLEXITY_API_KEY="your-perplexity-key"  # Alternative
export OPENROUTER_API_KEY="your-openrouter-key"  # Alternative

# Optional: Configure model preferences
export OPENAI_PERPLEXITY_MODEL="gpt-4"
export SEARCH_PROVIDER="perplexity"  # or "openrouter"
```

## ⚡ Quick Start

```bash
# Run the main CLI to see available commands
uv run ondansetron --help

# Search for literature
uv run ondansetron search "ondansetron mechanism of action"

# Update clinical trials data
uv run ondansetron update-trials --term "ondansetron alcohol" --days 30 --summarize

# Review manuscript sections interactively
uv run ondansetron review manuscript/memoire.md

# Generate PDF from manuscript
cd manuscript && make pdf
```

## 🔧 CLI Tools

The project provides a unified CLI with multiple specialized commands:

### Main Commands

#### `ondansetron help [command]`
Show help information for all commands or a specific command.

```bash
uv run ondansetron help
uv run ondansetron help search
```

#### `ondansetron search <query>`
LLM-powered literature search using OpenAI, Perplexity, or OpenRouter APIs.

```bash
# Basic search
uv run ondansetron search "ondansetron 5-HT3 antagonist"

# Or use the dedicated script
uv run ondansetron-search "alcohol use disorder genetics"
```

**Features**:
- Natural language queries
- Multiple LLM provider support
- Configurable models and providers
- JSON response parsing

#### `ondansetron update-trials [options]`
Fetch and summarize clinical trials metadata from PubMed.

```bash
# Fetch trials from last 30 days
uv run ondansetron update-trials --term "ondansetron alcohol" --days 30

# Fetch with automatic LLM summarization
uv run ondansetron update-trials --term "ondansetron AUD" --days 60 --summarize

# Specify date range
uv run ondansetron update-trials --term "ondansetron" --start-date 2020-01-01 --end-date 2024-12-31
```

**Options**:
- `--term`: Search term for PubMed
- `--days`: Fetch trials from last N days
- `--start-date`, `--end-date`: Explicit date range (YYYY-MM-DD)
- `--max-results`: Maximum number of results (default: 100)
- `--summarize`: Generate LLM summaries of fetched trials
- `--output`: Output JSON file path

#### `ondansetron review [file]`
Interactive manuscript review with AI-powered suggestions.

```bash
uv run ondansetron review manuscript/memoire.md

# Or use the dedicated script
uv run ondansetron-review --provider openrouter
```

**Features**:
- Section-by-section review
- AI-generated improvement suggestions
- Interactive confirmation before applying changes
- Preserves YAML front matter
- Multiple LLM provider support

#### `ondansetron compare-trials`
Compare and analyze clinical trials metadata.

```bash
uv run ondansetron-compare-trials
```

#### `ondansetron memoire-llm [options]`
Generate updated manuscript versions using LLM with recent trials.

```bash
uv run ondansetron memoire-llm --provider perplexity --model gpt-4 -o manuscript/llm
```

### Utility Scripts

Additional standalone scripts in `src/ondansetron/`:

- **`build_vector_index.py`**: Build FAISS vector index for semantic search
- **`generate_prisma.py`**: Generate PRISMA flowchart
- **`get_keys.py`**: API key management utility

## 📁 Project Structure

```
ondansetron/
├── manuscript/               # Main manuscript and outputs
│   ├── memoire.md           # Master manuscript (Markdown + YAML)
│   ├── memoire.bib          # Bibliography
│   ├── memoire.pdf          # Generated PDF
│   ├── memoire.docx         # Generated DOCX
│   ├── Makefile             # Build system
│   ├── archives/            # Previous versions
│   │   ├── old_references.md
│   │   ├── tex/             # LaTeX archives
│   │   └── tex_old/
│   └── llm/                 # LLM-generated versions
│
├── src/ondansetron/         # Python package
│   ├── __init__.py          # Main CLI entry point
│   ├── __main__.py          # Package execution entry
│   ├── search.py            # LLM search interface
│   ├── update_trials.py     # Clinical trials fetching
│   ├── review.py            # Manuscript review assistant
│   ├── compare_trials.py    # Trial comparison tool
│   ├── gen_memoire_llm.py   # LLM manuscript generation
│   ├── generate_prisma.py   # PRISMA flowchart generator
│   ├── build_vector_index.py # Vector index builder
│   └── get_keys.py          # API key utilities
│
├── sourcedata/              # Raw data and analysis
│   ├── trials.json          # Current trials data
│   ├── new_trials.json      # Recently added trials
│   ├── complete_historical_ondansetron_aud.json
│   ├── all_trials_comprehensive.json
│   └── 2020/, 2021/, ...    # Historical data by year
│
├── ressources/              # Supporting resources
│   ├── papers/              # PDF papers
│   ├── vector_index.faiss   # FAISS vector index
│   ├── vector_index.fpaths  # File paths for vector index
│   ├── prisma_flowchart.png
│   └── *.pdf                # Reference documents
│
├── tests/                   # Test suite
│   └── test_search.py
│
├── .mcp/                    # MCP tools configuration
├── .obsidian/               # Obsidian vault configuration
├── .pandoc/                 # Pandoc templates and CSL
│
├── README.md                # This file
├── AGENTS.md                # Multi-agent coordination guide
├── TODO.md                  # Project roadmap and tasks
├── CLAUDE.md                # Claude Code instructions
├── AI_INSTRUCTIONS.md       # General AI agent instructions
├── OpenCode.md              # OpenCode guidelines
│
├── pyproject.toml           # Python project configuration
├── pytest.ini               # Pytest configuration
├── uv.lock                  # Dependency lock file
└── ondansetron.bib          # Root bibliography file
```

## 📝 Manuscript Workflow

### Building the Manuscript

The manuscript is written in Markdown with YAML front matter and can be converted to PDF or DOCX:

```bash
cd manuscript

# Generate PDF (requires Pandoc + LaTeX)
make pdf

# Generate DOCX (requires Pandoc)
make docx

# Clean build artifacts
make clean
```

### Manuscript Structure

The main manuscript (`manuscript/memoire.md`) includes:
- **YAML Front Matter**: Metadata (authors, date, abstract, bibliography)
- **Main Sections**: Introduction, Methods, Results, Discussion, Conclusion
- **Citations**: BibTeX format in `memoire.bib`
- **PRISMA Compliance**: Systematic review follows PRISMA guidelines

### Editing Guidelines

When editing the manuscript:
1. **Preserve YAML front matter** at the beginning of the file
2. **Follow existing Markdown style** (consistent heading levels, citation format)
3. **Update bibliography** in `memoire.bib` for new references
4. **Use inline citations**: `[@author2024]` or `@author2024`
5. **Keep changes minimal** and style-consistent
6. **Test PDF generation** after major changes

## 💻 Development

### Adding Dependencies

```bash
# Add a new Python package
uv add package-name

# Add a development dependency
uv add --dev package-name
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/test_search.py

# Run with coverage
uv run pytest --cov=ondansetron tests/
```

### Code Style

The project follows these conventions:
- **Formatting**: Black (88 columns), isort for imports
- **Type hints**: All public functions should have type annotations
- **Docstrings**: Google style with Args, Returns, Raises
- **Naming**: snake_case for functions/variables, PascalCase for classes
- **Imports**: Standard library, blank line, third-party, blank line, local modules

```bash
# Format code (if tools are installed)
black .
isort .
```

### Development Workflow

1. **Create a new branch** for each feature/fix
2. **Make minimal changes** focused on the specific task
3. **Test your changes** thoroughly
4. **Commit with clear messages**
5. **Create a pull request** for review
6. **Merge after approval**

See [AGENTS.md](AGENTS.md) for multi-agent coordination guidelines.

## 📖 Documentation

This project includes multiple documentation files tailored for different audiences and AI assistants:

- **[README.md](README.md)** (this file): General project overview and usage guide
- **[AGENTS.md](AGENTS.md)**: Multi-agent workflow coordination and guidelines
- **[TODO.md](TODO.md)**: Project roadmap, tasks, and future improvements
- **[CLAUDE.md](CLAUDE.md)**: Instructions for Claude Code assistant
- **[AI_INSTRUCTIONS.md](AI_INSTRUCTIONS.md)**: General AI agent instructions
- **[OpenCode.md](OpenCode.md)**: OpenCode-specific guidelines

## 🔑 Environment Variables

The following environment variables can be configured:

### API Keys (choose one or more)
- `OPENAI_API_KEY`: OpenAI API key (primary)
- `PERPLEXITY_API_KEY`: Perplexity API key (alternative)
- `OPENROUTER_API_KEY`: OpenRouter API key (alternative)

### Configuration
- `SEARCH_PROVIDER`: LLM provider (`perplexity` or `openrouter`)
- `OPENAI_PERPLEXITY_MODEL`: Model to use with OpenAI (e.g., `gpt-4`, `gpt-3.5-turbo`)
- `OPENROUTER_MODEL`: Model to use with OpenRouter
- `PERPLEXITY_API_URL`: Custom Perplexity API URL
- `OPENROUTER_API_URL`: Custom OpenRouter API URL

## 🤝 Contributing

This is an academic research project, but contributions are welcome:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes following the code style guidelines
4. Test your changes thoroughly
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

For multi-agent development, see [AGENTS.md](AGENTS.md).

## 📄 License

This project is part of academic research. Please contact the authors for licensing information.

## 👥 Authors

- **Matias Ceau** - Primary Author - [matias@ceau.net](mailto:matias@ceau.net)
- **Pr Mélina Fatseas** - Supervisor

## 🙏 Acknowledgments

- PRISMA guidelines for systematic review methodology
- Cochrane Collaboration for risk of bias assessment tools
- OpenAI, Perplexity, and OpenRouter for LLM API access
- The Python and open-source communities

## 📚 Citation

If you use this work in your research, please cite:

```bibtex
@mastersthesis{ceau2024ondansetron,
  title={Ondansetron in alcohol use disorder: a systematic review},
  author={Ceau, Matias and Fatseas, M{\'e}lina},
  year={2024},
  school={[Institution Name]},
  type={Master's thesis}
}
```

## 🔗 Related Resources

- [PRISMA Guidelines](http://www.prisma-statement.org/)
- [Cochrane Handbook](https://training.cochrane.org/handbook)
- [PubMed](https://pubmed.ncbi.nlm.nih.gov/)
- [uv Package Manager](https://github.com/astral-sh/uv)

---

**For detailed usage instructions and AI agent coordination, see [AGENTS.md](AGENTS.md) and [TODO.md](TODO.md).**
