# GitHub Copilot Instructions

This file provides guidance for GitHub Copilot when working with this repository.

## Project Overview

This is an academic research project for a systematic review manuscript on "Ondansetron in alcohol use disorder" with supporting Python CLI automation tools. The project combines traditional academic writing with modern AI-powered research assistance.

**Key Information:**
- **Authors**: Matias Ceau, Pr Mélina Fatseas
- **Date**: October 2025
- **Main manuscript**: `manuscript/memoire.md` (Markdown with YAML front matter)
- **Bibliography**: `manuscript/memoire.bib`
- **Python package**: `src/ondansetron` - CLI tools for literature search, trial updates, and manuscript review

## Development Commands

### Python Package Management
- `uv add <package>` - Add Python dependencies
- `uv run <script>` - Run project scripts 
- `uv run ondansetron` - Main CLI interface
- `uv run ondansetron-search "query"` - LLM-powered literature search
- `uv run ondansetron-update-trials` - Fetch clinical trials data
- `uv run ondansetron-review` - Interactive manuscript review assistant
- `uv run ondansetron-compare-trials` - Compare clinical trials

### Document Generation
Run in `manuscript/` directory:
- `make pdf` - Generate memoire.pdf using Pandoc + LaTeX
- `make docx` - Generate memoire.docx

### Testing
- `pytest` - Run tests (configured with pythonpath = src)

## Architecture

### CLI Tools Structure
The Python package provides a unified CLI with subcommands:
- `ondansetron.search` - LLM search interface (OpenAI/OpenRouter/Perplexity APIs)
- `ondansetron.update_trials` - Clinical trials metadata fetching
- `ondansetron.review` - AI-assisted manuscript editing
- `ondansetron.compare_trials` - Clinical trials comparison
- `ondansetron` - Main entry point with help system

### Project Structure
```
├── manuscript/
│   ├── memoire.md          # Main manuscript (Markdown + YAML front matter)
│   ├── memoire.bib         # Bibliography
│   └── archives/           # Previous versions
├── src/ondansetron/        # Python CLI tools
├── sourcedata/             # Raw data and drafts
├── ressources/             # PDFs (PRISMA checklist, Cochrane tools)
├── tests/                  # Test suite
└── .github/                # GitHub configuration
```

## Environment Requirements

### Required APIs
- Primary: `OPENAI_API_KEY`
- Alternatives: `PERPLEXITY_API_KEY`, `OPENROUTER_API_KEY`

### External Dependencies  
- Pandoc (document conversion)
- LaTeX distribution (PDF generation)
- Python 3.12+
- uv (Python package manager)

## Coding Guidelines

### General Principles
- Make minimal, surgical changes to achieve the goal
- Preserve existing functionality unless explicitly fixing bugs
- Follow the existing code style and conventions
- Use `uv` for all Python package operations
- Test CLI tools with `uv run <command>` before suggesting usage

### Manuscript Editing
- **Always preserve YAML front matter** in `manuscript/memoire.md`
- Keep manuscript changes minimal and style-consistent
- When updating references, ensure consistency in `manuscript/memoire.bib`
- Follow existing Markdown and citation styles
- Maintain archives under `manuscript/archives/`

### Code Development
- Use `rg` (ripgrep) for searching, not `grep`
- Add tests for new functionality in `tests/`
- Follow existing patterns in CLI tool implementation
- Handle API keys securely (use environment variables)
- Provide helpful error messages for missing dependencies

### Data and Resources
- Raw data: Word documents and spreadsheets in `sourcedata/`
- Resources: PDFs in `ressources/`
- Maintain separation between source data and generated outputs

## Development Workflow

### Branch Strategy
- Create a new branch when starting a new modification round
- After completing work: add all changes, commit, and merge pull request
- Multiple agents may work in parallel on different files
- Regularly check for coherence across the entire project

### Manuscript Review Strategy
- Update the reference manuscript interactively
- Critique the current form of the manuscript
- Suggest updates that didn't exist in the last version
- Provide deeper critiques and suggestions for additional analyses

## Tool Development Goals

Current and planned features:
- Automate literature search and retrieval using LLMs
- Implement data science workflows for study characteristics extraction
- Create interactive visualizations (plots, dashboards) for metrics
- Integrate LLM-based summarization for manuscript updates
- Build search interface over bibliography and notes
- Enable quick citation lookup and insertion

## Common Tasks

When asked to:
- **Edit manuscript**: Modify `manuscript/memoire.md`, preserve YAML front matter
- **Add citations**: Update `manuscript/memoire.bib` with consistent formatting
- **Build documents**: Run `make pdf` or `make docx` in `manuscript/` directory
- **Add Python dependencies**: Use `uv add <package>`
- **Run CLI tools**: Use `uv run <command>`
- **Search codebase**: Use `rg` instead of `grep`
- **Add features**: Update relevant files in `src/ondansetron/`, add tests in `tests/`
- **Update data**: Modify files in `sourcedata/` or `ressources/`

## Security Considerations

- Never commit API keys or secrets
- Use environment variables for sensitive configuration
- Handle user data with appropriate privacy considerations
- Validate inputs to CLI tools
- Follow secure coding practices for external API calls
