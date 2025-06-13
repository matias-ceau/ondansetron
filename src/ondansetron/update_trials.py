#!/usr/bin/env python3
"""Pipeline to fetch recent clinical trials metadata and optionally summarize using an LLM."""

import argparse
import json
import os
import sys

import requests

from ondansetron.search import _openrouter_search, _perplexity_search


def fetch_new_trials(term: str, days: int = 7, max_results: int = 100) -> list:
    """Query PubMed for recent clinical trials matching a search term."""
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": term,
        "retmode": "json",
        "sort": "pub+date",
        "datetype": "pdat",
        "reldate": days,
        "retmax": max_results,
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()
    return data.get("esearchresult", {}).get("idlist", [])


def fetch_metadata(ids: list) -> list:
    """Retrieve metadata for a list of PubMed IDs via ESummary."""
    if not ids:
        return []
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
    params = {"db": "pubmed", "id": ",".join(ids), "retmode": "json"}
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()
    results = []
    for uid in data.get("result", {}).get("uids", []):
        rec = data["result"].get(uid, {})
        results.append(
            {
                "uid": uid,
                "title": rec.get("title"),
                "pubdate": rec.get("pubdate"),
                "source": rec.get("source"),
                "authors": rec.get("authors", []),
                "doi": rec.get("elocationid", ""),
            }
        )
    return results


def get_search_credentials(provider: str):
    """Fetch API key and URL for the chosen LLM provider."""
    if provider == "openrouter":
        api_key = os.environ.get("OPENROUTER_API_KEY")
        api_url = os.environ.get(
            "OPENROUTER_API_URL", "https://openrouter.ai/api/chat/completions"
        )
        if not api_key:
            print("Error: OPENROUTER_API_KEY is not set.", file=sys.stderr)
            sys.exit(1)
    else:
        # Use OPENAI_API_KEY or fall back to legacy PERPLEXITY_API_KEY
        api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("PERPLEXITY_API_KEY")
        api_url = os.environ.get(
            "PERPLEXITY_API_URL", "https://api.perplexity.ai/chat/completions"
        )
        if not api_key:
            print("Error: OPENAI_API_KEY or PERPLEXITY_API_KEY is not set.", file=sys.stderr)
            sys.exit(1)
    return api_key, api_url


def summarize_trial(metadata: dict, api_key: str, api_url: str, provider: str) -> str:
    """Generate a concise LLM summary for one trial's metadata."""
    authors = ", ".join(a.get("name", "") for a in metadata.get("authors", []))
    prompt = (
        f"Provide a concise summary of the following clinical trial metadata:\n"
        f"Title: {metadata.get('title')}\n"
        f"Authors: {authors}\n"
        f"Published: {metadata.get('pubdate')}\n"
        f"Journal: {metadata.get('source')}\n"
        f"DOI: {metadata.get('doi')}"
    )
    if provider == "openrouter":
        result = _openrouter_search(prompt, api_key, api_url)
        choices = result.get("choices", [])
        if choices:
            return choices[0].get("message", {}).get("content", "")
    else:
        resp = _perplexity_search(prompt, api_key)
        return resp.choices[0].message.content
    return ""


def main() -> None:
    """CLI entry point for updating trial metadata and summaries."""
    parser = argparse.ArgumentParser(
        description="Fetch recent clinical trials and extract metadata/summaries."
    )
    parser.add_argument(
        "--term",
        default=os.environ.get(
            "PUBMED_SEARCH_TERM", "ondansetron alcohol use disorder"
        ),
        help="Search term for PubMed (default: environment or 'ondansetron alcohol use disorder').",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=7,
        help="Look back this many days for new publications (default: 7).",
    )
    parser.add_argument(
        "--output",
        default="sourcedata/new_trials.json",
        help="Output path for metadata JSON (default: sourcedata/new_trials.json).",
    )
    parser.add_argument(
        "--summarize",
        action="store_true",
        help="Include LLM-generated summaries for each trial.",
    )
    parser.add_argument(
        "--provider",
        choices=["perplexity", "openrouter"],
        default=os.environ.get("SEARCH_PROVIDER", "perplexity").lower(),
        help="LLM provider for summaries (default: PERPLEXITY or OPENROUTER).",
    )
    args = parser.parse_args()

    ids = fetch_new_trials(args.term, args.days)
    metadata = fetch_metadata(ids)
    if args.summarize and metadata:
        api_key, api_url = get_search_credentials(args.provider)
        for entry in metadata:
            entry["summary"] = summarize_trial(entry, api_key, api_url, args.provider)

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w") as out_file:
        json.dump(metadata, out_file, indent=2)
    print(f"Wrote {len(metadata)} records to {args.output}")


if __name__ == "__main__":
    main()
