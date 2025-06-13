# Ondansetron Systematic Review Toolkit

This repository contains the manuscript and supporting tools for the **Ondansetron in alcohol use disorder** systematic review.

## CLI Tools

- `ondansetron <command>`: unified CLI for all subcommands (`search`, `update-trials`, `review`, `help`).

**Commands:**
- `help [command]`          Show short help or detailed help for a subcommand
- `search [query]`          Query LLM search interface (Perplexity/OpenRouter)
- `update-trials [options]` Fetch recent clinical trials metadata and generate summaries
- `review [options]`        Interactively suggest and apply edits to manuscript sections

### Usage

Set your `OPENAI_API_KEY` (or legacy `PERPLEXITY_API_KEY`), and optionally `OPENAI_PERPLEXITY_MODEL`, then:

```bash
# General help (lists commands)
ondansetron --help
ondansetron help

# Detailed help for a subcommand
ondansetron help search

# Perform a free-text LLM search
ondansetron search "your search query here"

# Fetch trial metadata (last 30 days) and generate summaries
ondansetron update-trials --term "ondansetron alcohol use disorder" --days 30 --summarize

# Review the manuscript interactively
ondansetron review manuscript/memoire.md
```

## Environment & Installation

This project uses **uv** for dependency management and running scripts. To get started:

```bash
# View uv help and available commands
uv help

# Add a Python dependency (e.g., requests)
uv add requests

# Run the main CLI
uv run ondansetron

# Run the search tool
uv run ondansetron-search "your search query here"
```
