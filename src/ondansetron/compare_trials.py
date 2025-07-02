#!/usr/bin/env python3
"""Standalone tool to compare trial datasets and identify differences."""

import argparse
import json
import sys
from datetime import datetime
from typing import Dict, List


def load_trials_data(filepath: str) -> Dict:
    """Load trials data from JSON file."""
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
        
        # Handle both old and new format
        if isinstance(data, list):
            # Old format - just a list of trials
            return {"search_metadata": {}, "trials": data}
        else:
            # New format with metadata
            return data
    except FileNotFoundError:
        print(f"Error: File {filepath} not found.", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {filepath}: {e}", file=sys.stderr)
        sys.exit(1)


def compare_datasets(old_data: Dict, new_data: Dict) -> Dict:
    """Compare two trial datasets and provide detailed analysis."""
    old_trials = old_data.get("trials", [])
    new_trials = new_data.get("trials", [])
    
    old_ids = {trial.get("uid") for trial in old_trials}
    new_ids = {trial.get("uid") for trial in new_trials}
    
    # Find new, removed, and common trials
    added_ids = new_ids - old_ids
    removed_ids = old_ids - new_ids
    common_ids = old_ids & new_ids
    
    added_trials = [trial for trial in new_trials if trial.get("uid") in added_ids]
    removed_trials = [trial for trial in old_trials if trial.get("uid") in removed_ids]
    
    return {
        "comparison_metadata": {
            "comparison_date": datetime.now().isoformat(),
            "old_dataset_info": {
                "file_search_date": old_data.get("search_metadata", {}).get("search_date"),
                "trial_count": len(old_trials),
                "search_term": old_data.get("search_metadata", {}).get("query_term")
            },
            "new_dataset_info": {
                "file_search_date": new_data.get("search_metadata", {}).get("search_date"),
                "trial_count": len(new_trials),
                "search_term": new_data.get("search_metadata", {}).get("query_term")
            },
            "comparison_stats": {
                "trials_added": len(added_ids),
                "trials_removed": len(removed_ids),
                "trials_common": len(common_ids),
                "net_change": len(new_trials) - len(old_trials)
            }
        },
        "added_trials": added_trials,
        "removed_trials": removed_trials,
        "added_trial_ids": list(added_ids),
        "removed_trial_ids": list(removed_ids)
    }


def print_comparison_summary(comparison: Dict) -> None:
    """Print a human-readable summary of the comparison."""
    meta = comparison["comparison_metadata"]
    stats = meta["comparison_stats"]
    
    print("=== TRIAL COMPARISON SUMMARY ===")
    print(f"Comparison performed: {meta['comparison_date']}")
    print()
    
    print("Dataset Information:")
    print(f"  Old dataset: {stats['trials_common'] + stats['trials_removed']} trials")
    if meta['old_dataset_info']['file_search_date']:
        print(f"    Search date: {meta['old_dataset_info']['file_search_date']}")
    if meta['old_dataset_info']['search_term']:
        print(f"    Search term: {meta['old_dataset_info']['search_term']}")
    
    print(f"  New dataset: {stats['trials_common'] + stats['trials_added']} trials")
    if meta['new_dataset_info']['file_search_date']:
        print(f"    Search date: {meta['new_dataset_info']['file_search_date']}")
    if meta['new_dataset_info']['search_term']:
        print(f"    Search term: {meta['new_dataset_info']['search_term']}")
    print()
    
    print("Changes:")
    print(f"  Added trials: {stats['trials_added']}")
    print(f"  Removed trials: {stats['trials_removed']}")
    print(f"  Common trials: {stats['trials_common']}")
    print(f"  Net change: {stats['net_change']:+d}")
    print()
    
    if comparison["added_trials"]:
        print("New Trials Added:")
        for trial in comparison["added_trials"][:10]:  # Show first 10
            title = trial.get("title", "No title")[:80]
            date = trial.get("pubdate", "No date")
            print(f"  + {title}... ({date})")
        if len(comparison["added_trials"]) > 10:
            print(f"  ... and {len(comparison['added_trials']) - 10} more")
        print()
    
    if comparison["removed_trials"]:
        print("Trials Removed:")
        for trial in comparison["removed_trials"][:5]:  # Show first 5
            title = trial.get("title", "No title")[:80]
            date = trial.get("pubdate", "No date")
            print(f"  - {title}... ({date})")
        if len(comparison["removed_trials"]) > 5:
            print(f"  ... and {len(comparison['removed_trials']) - 5} more")


def main() -> None:
    """CLI entry point for comparing trial datasets."""
    parser = argparse.ArgumentParser(
        description="Compare two clinical trial datasets and identify differences."
    )
    parser.add_argument(
        "old_file",
        help="Path to the older/reference trial dataset (JSON)."
    )
    parser.add_argument(
        "new_file", 
        help="Path to the newer trial dataset (JSON)."
    )
    parser.add_argument(
        "--output",
        help="Save detailed comparison results to JSON file."
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Only show summary statistics."
    )
    
    args = parser.parse_args()
    
    # Load datasets
    old_data = load_trials_data(args.old_file)
    new_data = load_trials_data(args.new_file)
    
    # Perform comparison
    comparison = compare_datasets(old_data, new_data)
    
    # Print summary
    if not args.quiet:
        print_comparison_summary(comparison)
    else:
        stats = comparison["comparison_metadata"]["comparison_stats"]
        print(f"Added: {stats['trials_added']}, Removed: {stats['trials_removed']}, Net: {stats['net_change']:+d}")
    
    # Save detailed results if requested
    if args.output:
        with open(args.output, "w") as f:
            json.dump(comparison, f, indent=2)
        print(f"Detailed comparison saved to {args.output}")


if __name__ == "__main__":
    main()