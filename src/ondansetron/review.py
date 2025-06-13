#!/usr/bin/env python3
"""Interactive manuscript review: suggest section edits via LLM with human confirmation."""

import os
import sys
import argparse

from ondansetron.search import _perplexity_search, _openrouter_search


def split_sections(text: str) -> list:
    """Split markdown text into sections by top-level headers."""
    sections = []
    current = {"title": None, "content": ""}
    for line in text.splitlines(keepends=True):
        if line.startswith("#"):
            if current["title"] or current["content"]:
                sections.append(current)
            current = {"title": line.rstrip(), "content": ""}
        else:
            current["content"] += line
    if current["title"] or current["content"]:
        sections.append(current)
    return sections


def get_search_credentials(provider: str):
    """Fetch API credentials for the selected LLM provider."""
    if provider == "openrouter":
        api_key = os.environ.get("OPENROUTER_API_KEY")
        api_url = os.environ.get(
            "OPENROUTER_API_URL", "https://openrouter.ai/api/v1/chat/completions"
        )
        if not api_key:
            print("Error: OPENROUTER_API_KEY is not set.", file=sys.stderr)
            sys.exit(1)
    else:
        # Use OPENAI_API_KEY or fall back to legacy PERPLEXITY_API_KEY
        api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("PERPLEXITY_API_KEY")
        api_url = os.environ.get(
            "PERPLEXITY_API_URL", "https://api.perplexity.ai/v1/search"
        )
        if not api_key:
            print("Error: OPENAI_API_KEY or PERPLEXITY_API_KEY is not set.", file=sys.stderr)
            sys.exit(1)
    return api_key, api_url


def suggest_edit(section: dict, api_key: str, api_url: str, provider: str) -> str:
    """Generate an improved version of the section via LLM."""
    prompt = (
        "Suggest edits to improve clarity, grammar, and style of this manuscript section. "
        "Provide only the updated text without commentary.\n\n"
        f"{section['title']}\n{section['content']}"
    )
    if provider == "openrouter":
        result = _openrouter_search(prompt, api_key, api_url)
        choice = result.get("choices", [{}])[0]
        return choice.get("message", {}).get("content", "")
    else:
        resp = _perplexity_search(prompt, api_key)
        return resp.choices[0].message.content


def review_file(filepath: str, provider: str) -> None:
    """Run interactive review on a manuscript file."""
    api_key, api_url = get_search_credentials(provider)
    with open(filepath, 'r') as f:
        text = f.read()
    sections = split_sections(text)
    updated = False

    for sec in sections:
        print(f"\n=== {sec['title']} ===")
        suggestion = suggest_edit(sec, api_key, api_url, provider)
        print(suggestion)
        resp = input("Apply this suggestion? [y/N] ")
        if resp.strip().lower() == 'y':
            sec['content'] = suggestion + '\n'
            updated = True

    if updated:
        new_text = ''
        for sec in sections:
            if sec['title']:
                new_text += sec['title'] + '\n'
            new_text += sec['content']
        with open(filepath, 'w') as f:
            f.write(new_text)
        print(f"Updated {filepath}")
    else:
        print("No changes applied.")


def main() -> None:
    """CLI entry point for interactive manuscript review."""
    parser = argparse.ArgumentParser(
        description="Interactively suggest and apply edits to manuscript sections."
    )
    parser.add_argument(
        "filepath", help="Path to the manuscript file (Markdown)."
    )
    parser.add_argument(
        "--provider", choices=["perplexity", "openrouter"],
        default=os.environ.get("SEARCH_PROVIDER", "perplexity").lower(),
        help="LLM provider to use for suggestions."
    )
    args = parser.parse_args()
    review_file(args.filepath, args.provider)


if __name__ == "__main__":
    main()