#!/usr/bin/env python3
"""Generate updated memoire manuscript via LLM, adding recent trials and metadata."""

import os
import sys
import argparse
from datetime import datetime

from ondansetron.search import _perplexity_search, _openrouter_search
from ondansetron.update_trials import get_search_credentials


def main() -> None:
    """Generate an LLM-updated memoire manuscript and save to output directory."""
    parser = argparse.ArgumentParser(
        prog="ondansetron memoire-llm",
        description="Replicate and improve memoire with recent clinical trials via LLM"
    )
    parser.add_argument(
        "--provider", choices=["perplexity", "openrouter"], default=None,
        help="LLM provider to use (overrides SEARCH_PROVIDER env)"
    )
    parser.add_argument(
        "--model", "-m", default=None,
        help="LLM model identifier for metadata in output filename"
    )
    parser.add_argument(
        "--output-dir", "-o", default="manuscript/llm",
        help="Directory to save the generated LLM manuscript"
    )
    parser.add_argument(
        "input_file", nargs="?", default="manuscript/memoire.md",
        help="Path to the base memoire manuscript to update"
    )
    args = parser.parse_args()

    provider = (args.provider or os.environ.get("SEARCH_PROVIDER", "perplexity")).lower()
    api_key, api_url = get_search_credentials(provider)

    try:
        text = open(args.input_file, 'r').read()
    except Exception as e:
        print(f"Error reading {args.input_file}: {e}", file=sys.stderr)
        sys.exit(1)

    prompt = (
        "You are an expert in alcohol use disorder research. "
        "Update the following systematic review manuscript in Markdown by adding clinical trials of ondansetron in alcohol use disorder published since the date in the YAML front matter. "
        "Preserve the YAML front matter, but add two fields: 'generated_date' with the current ISO datetime, and 'model' with the LLM identifier. "
        "Output only the complete Markdown text.\n\n"
        f"{text}"
    )

    if provider == "openrouter":
        result = _openrouter_search(prompt, api_key, api_url)
        choice = result.get("choices", [{}])[0]
        content = choice.get("message", {}).get("content", "")
    else:
        resp = _perplexity_search(prompt, api_key)
        choice = resp.choices[0]
        content = (choice.message.content if hasattr(choice, 'message')
                   else choice.get('message', {}).get('content', ''))

    os.makedirs(args.output_dir, exist_ok=True)
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_name = args.model or os.environ.get("OPENROUTER_MODEL") or os.environ.get("OPENAI_PERPLEXITY_MODEL") or provider
    filename = f"{now}-{model_name}.md"
    output_path = os.path.join(args.output_dir, filename)

    try:
        with open(output_path, 'w') as out:
            out.write(content)
    except Exception as e:
        print(f"Error writing {output_path}: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Wrote updated manuscript to {output_path}")


if __name__ == "__main__":
    main()