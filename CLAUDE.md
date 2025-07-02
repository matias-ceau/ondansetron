# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an academic research project for a systematic review manuscript on "Ondansetron in alcohol use disorder" with supporting Python CLI automation tools. The project combines traditional academic writing with modern AI-powered research assistance.

## Development Commands

### Python Package Management
- `uv add <package>` - Add Python dependencies
- `uv run <script>` - Run project scripts 
- `uv run ondansetron` - Main CLI interface
- `uv run ondansetron-search "query"` - LLM-powered literature search
- `uv run ondansetron-update-trials` - Fetch clinical trials data
- `uv run ondansetron-review` - Interactive manuscript review assistant

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
- `ondansetron` - Main entry point with help system

### Academic Workflow Integration
- Main manuscript: `manuscript/memoire.md` (Markdown with YAML front matter)
- Bibliography: `manuscript/memoire.bib`
- Archives: Previous versions in `manuscript/archives/`
- Supporting data: `sourcedata/` and `ressources/`

## Environment Requirements

### Required APIs
- Primary: `OPENAI_API_KEY`
- Alternatives: `PERPLEXITY_API_KEY`, `OPENROUTER_API_KEY`

### External Dependencies  
- Pandoc (document conversion)
- LaTeX distribution (PDF generation)
- Python 3.12+

## Key Guidelines

- Preserve YAML front matter in `manuscript/memoire.md`
- Use `rg` for searching (not `grep`)
- Keep manuscript changes minimal and style-consistent
- Use `uv` for all Python package operations
- Test CLI tools with `uv run <command>` before suggesting usage

## Manuscript Review Strategy

- The goal is to update a reference manuscript interactively
- Critique the current form of the manuscript
- Suggest updates that did not exist at the time of the last available manuscript
- Provide deeper critiques and suggestions for additional analyses

## Development Workflow Guidelines

- ALWAYS create a new branch when a new modification round begins, then finish by adding all, committing, merge pull request and the cycle continues. You'll be working on parallel with other agents but with common goals and different files each time, so take a look at the coherence of the whole every so often