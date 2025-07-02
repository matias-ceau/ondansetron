#!/usr/bin/env python3
"""Pipeline to fetch clinical trials metadata and optionally summarize using an LLM."""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional

import requests

from ondansetron.search import _openrouter_search, _perplexity_search


def fetch_trials_by_date_range(
    term: str, 
    start_date: Optional[str] = None, 
    end_date: Optional[str] = None,
    days: Optional[int] = None,
    max_results: int = 100
) -> Dict:
    """Query PubMed for clinical trials matching a search term within a date range."""
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": term,
        "retmode": "json",
        "sort": "pub+date",
        "datetype": "pdat",
        "retmax": max_results,
    }
    
    # Handle date parameters - prefer explicit dates over relative days
    if start_date and end_date:
        params["mindate"] = start_date
        params["maxdate"] = end_date
    elif days is not None:
        params["reldate"] = days
    elif end_date:
        # Search everything up to end_date
        params["maxdate"] = end_date
    
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()
    
    # Return full response with metadata
    return {
        "search_metadata": {
            "query_term": term,
            "start_date": start_date,
            "end_date": end_date,
            "days_back": days,
            "max_results": max_results,
            "search_date": datetime.now().isoformat(),
            "total_found": data.get("esearchresult", {}).get("count", "0"),
            "returned_count": len(data.get("esearchresult", {}).get("idlist", [])),
            "search_params": params
        },
        "ids": data.get("esearchresult", {}).get("idlist", [])
    }


def fetch_new_trials(term: str, days: int = 7, max_results: int = 100) -> list:
    """Legacy function - Query PubMed for recent clinical trials matching a search term."""
    result = fetch_trials_by_date_range(term, days=days, max_results=max_results)
    return result["ids"]


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


def load_previous_trials(filepath: str) -> Dict:
    """Load previously saved trials data."""
    if not os.path.exists(filepath):
        return {"search_metadata": {}, "trials": []}
    
    with open(filepath, "r") as f:
        data = json.load(f)
    
    # Handle both old and new format
    if isinstance(data, list):
        # Old format - just a list of trials
        return {"search_metadata": {}, "trials": data}
    else:
        # New format with metadata
        return data


def compare_trials(old_data: Dict, new_data: Dict) -> Dict:
    """Compare two trial datasets and identify new trials."""
    old_ids = {trial.get("uid") for trial in old_data.get("trials", [])}
    new_trials = [trial for trial in new_data.get("trials", []) if trial.get("uid") not in old_ids]
    
    return {
        "comparison_metadata": {
            "comparison_date": datetime.now().isoformat(),
            "old_trials_count": len(old_data.get("trials", [])),
            "new_search_count": len(new_data.get("trials", [])),
            "new_trials_found": len(new_trials)
        },
        "new_trials": new_trials,
        "all_trials": new_data.get("trials", [])
    }


def main() -> None:
    """CLI entry point for updating trial metadata and summaries."""
    parser = argparse.ArgumentParser(
        description="Fetch clinical trials and extract metadata/summaries with comparison capabilities."
    )
    parser.add_argument(
        "--term",
        default=os.environ.get(
            "PUBMED_SEARCH_TERM", 
            '("ondansetron"[MeSH Terms] OR "ondansetron"[All Fields]) AND ("alcoholism"[MeSH Terms] OR "alcoholism"[All Fields] OR "alcohol use disorder"[All Fields] OR "alcohol abuse"[All Fields] OR "AUD"[All Fields])'
        ),
        help="Search term for PubMed (default: systematic review MeSH terms strategy or environment variable).",
    )
    parser.add_argument(
        "--days",
        type=int,
        help="Look back this many days for new publications. Mutually exclusive with --start-date/--end-date.",
    )
    parser.add_argument(
        "--start-date",
        help="Start date for search (YYYY/MM/DD format). Use with --end-date for date range.",
    )
    parser.add_argument(
        "--end-date",
        help="End date for search (YYYY/MM/DD format). If used alone, searches everything up to this date.",
    )
    parser.add_argument(
        "--output",
        default="sourcedata/trials.json",
        help="Output path for metadata JSON (default: sourcedata/trials.json).",
    )
    parser.add_argument(
        "--compare",
        action="store_true",
        help="Compare with existing data and identify new trials.",
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
    parser.add_argument(
        "--max-results",
        type=int,
        default=1000,
        help="Maximum number of results to fetch (default: 1000).",
    )
    args = parser.parse_args()

    # Default to searching everything up to today if no date parameters provided
    if not args.days and not args.start_date and not args.end_date:
        args.end_date = datetime.now().strftime("%Y/%m/%d")
        print(f"No date parameters provided. Searching all trials up to {args.end_date}")

    # Fetch trials using new date-range function
    search_result = fetch_trials_by_date_range(
        args.term, 
        args.start_date, 
        args.end_date, 
        args.days,
        args.max_results
    )
    
    ids = search_result["ids"]
    metadata = fetch_metadata(ids)
    
    if args.summarize and metadata:
        api_key, api_url = get_search_credentials(args.provider)
        print(f"Generating summaries for {len(metadata)} trials...")
        for entry in metadata:
            entry["summary"] = summarize_trial(entry, api_key, api_url, args.provider)

    # Create final data structure with metadata
    final_data = {
        "search_metadata": search_result["search_metadata"],
        "trials": metadata
    }

    # Handle comparison if requested
    if args.compare:
        previous_data = load_previous_trials(args.output)
        comparison = compare_trials(previous_data, final_data)
        final_data["comparison"] = comparison["comparison_metadata"]
        
        print(f"Comparison results:")
        print(f"  Previous trials: {comparison['comparison_metadata']['old_trials_count']}")
        print(f"  Current search: {comparison['comparison_metadata']['new_search_count']}")
        print(f"  New trials found: {comparison['comparison_metadata']['new_trials_found']}")
        
        if comparison["new_trials"]:
            print(f"\nNew trials:")
            for trial in comparison["new_trials"]:
                print(f"  - {trial.get('title', 'No title')} ({trial.get('pubdate', 'No date')})")

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w") as out_file:
        json.dump(final_data, out_file, indent=2)
    
    print(f"\nWrote {len(metadata)} trials to {args.output}")
    print(f"Search found {search_result['search_metadata']['total_found']} total matches in PubMed")


if __name__ == "__main__":
    main()