 # AI Agent Instructions

 This file provides instructions and context to guide the AI assistant (Codex CLI) when working on this repository.

 ## Project Overview

 - **Title**: Ondansetron in alcohol use disorder: a systematic review
 - **Authors**: Matias Ceau, Pr Mélina Fatseas
 - **Date**: November 2024
 - **Abstract**: Found in the YAML front matter of `manuscript/memoire.md`
 - **Bibliography**: `manuscript/memoire.bib`
 - **Main manuscript**: `manuscript/memoire.md` (Markdown with Pandoc/LaTeX YAML front matter)
 - **Build**:
   - Requires Pandoc and LaTeX for PDF generation
   - Run `make pdf` in the `manuscript` directory to generate `memoire.pdf`
   - Run `make docx` in the `manuscript` directory to generate `memoire.docx`
 - **Archives**:
   - Old references: `manuscript/archives/old_references.md`
   - Previous drafts: Word and PDF files in `sourcedata/`
   - LaTeX archives: `manuscript/archives/tex/`, `manuscript/archives/tex_old/`

 ## Code and Data

 - **Python package**: `src/ondansetron` (stub with a `main()` entry point)
 - **Notebook**: `ondansetron.ipynb` for interactive analysis
 - **Resources**: PDFs in `ressources/` (e.g., PRISMA checklist, Cochrane tools)
 - **Raw data**: Word documents and spreadsheets in `sourcedata/`

 ## Typical Tasks

 - Edit manuscript text in `manuscript/memoire.md`
 - Add and format citations in `manuscript/memoire.bib`
 - Run `make` commands in `manuscript/` for PDF/DOCX generation
 - Update tables and figures; manage files in `ressources/`
 - Maintain archives under `manuscript/archives/`
 - Run or modify Python code in `src/ondansetron` and notebooks as needed

 ## Additional Tool Development Goals

 - Develop Python tools for automating literature search and retrieval using machine learning and LLMs
 - Implement data science workflows for data extraction, processing, and visualization of study characteristics
 - Create interactive visualizations (plots, dashboards) to track paper metrics and study results
 - Integrate LLM-based summarization and draft revision utilities to assist in updating the manuscript
- Build a search interface over the bibliography and notes to quickly find and cite relevant references
- Initial implementation: `ondansetron-search` CLI tool using the Perplexity API (`src/ondansetron/search.py`)

 ## Guidelines

- Preserve the YAML front matter in `manuscript/memoire.md`
 - Follow existing Markdown and citation styles
 - When updating references, ensure consistency in `manuscript/memoire.bib`
- Use `rg` to search (avoid `grep` or `ls -R`)
- Use `uv add <package>` to add Python dependencies via uv.
- Use `uv run <script>` to run the project scripts (e.g., `ondansetron`, `ondansetron-search`).
- Use `uv help` or `uv help <cmd>` for uv usage and available commands.
- Keep changes minimal and aligned with the writing style