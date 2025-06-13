#!/usr/bin/env python3
"""Search interface for external APIs (e.g. Perplexity AI)."""
import os
import sys
import argparse

import requests
import openai


def _perplexity_search(query: str, api_key: str, api_url: str = None):
    """Perform a search query via OpenAI ChatCompletion (replacing direct Perplexity API)."""
    # Use a dedicated OpenAI client so api_key is honored
    client = openai.OpenAI(api_key=api_key)
    resp = client.chat.completions.create(
        model=os.environ.get("OPENAI_PERPLEXITY_MODEL", "gpt-3.5-turbo"),
        messages=[{"role": "user", "content": query}],
    )
    return resp


def _openrouter_search(query: str, api_key: str, api_url: str) -> dict:
    """Perform a search-like chat query using OpenRouter (multiple models including Perplexity)."""
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    model = os.environ.get("OPENROUTER_MODEL", "perplexity")
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": query}],
    }
    response = requests.post(api_url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()


def search(query: str) -> None:
    """Search for a query using the available provider."""
    provider = os.environ.get("SEARCH_PROVIDER", "perplexity").lower()
    if provider == "openrouter":
        api_key = os.environ.get("OPENROUTER_API_KEY")
        if not api_key:
            print("Error: OPENROUTER_API_KEY environment variable is not set.")
            sys.exit(1)
        api_url = os.environ.get(
            "OPENROUTER_API_URL", "https://openrouter.ai/api/chat/completions"
        )
        result = _openrouter_search(query, api_key, api_url)
        choice = result.get("choices", [{}])[0]
        msg = choice.get("message", {}).get("content")
        if msg:
            print(msg)
        else:
            print(result)
        return

    # Default to Perplexity-like search via OpenAI SDK (reads OPENAI_API_KEY or PERPLEXITY_API_KEY)
    api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("PERPLEXITY_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY or PERPLEXITY_API_KEY environment variable is not set.", file=sys.stderr)
        sys.exit(1)
    # api_url is ignored when using OpenAI SDK
    resp = _perplexity_search(query, api_key)
    # Print only the assistant's content (dict or attribute access)
    choice = resp.choices[0]
    msg = (choice.message.content if hasattr(choice, 'message')
           else choice.get('message', {}).get('content', ''))
    print(msg)


def main() -> None:
    """Command-line entry point for the 'search' subcommand."""
    parser = argparse.ArgumentParser(
        prog="ondansetron search",
        description="Query LLM search interface (Perplexity/OpenRouter)",
    )
    parser.add_argument(
        "query",
        nargs=argparse.REMAINDER,
        help="Search query text",
    )
    args = parser.parse_args()
    if not args.query:
        parser.error("the following arguments are required: query")
    search(" ".join(args.query))


if __name__ == "__main__":
    main()
