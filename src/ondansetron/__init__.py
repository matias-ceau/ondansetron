import sys
import argparse

from ondansetron.search import main as _search_main
from ondansetron.update_trials import main as _update_trials_main
from ondansetron.review import main as _review_main
from ondansetron.gen_memoire_llm import main as _memoire_llm_main


def main() -> None:
    """Main entry point for the ondansetron CLI with subcommands."""
    parser = argparse.ArgumentParser(
        prog="ondansetron",
        description="Ondansetron toolkit: search, update-trials, review"
    )
    subparsers = parser.add_subparsers(dest="command", metavar="<command>")

    # search subcommand
    parser_search = subparsers.add_parser(
        "search", help="Query LLM search interface (Perplexity/OpenRouter)"
    )
    parser_search.add_argument(
        "query", nargs=argparse.REMAINDER, help="Search query text"
    )

    # update-trials subcommand
    subparsers.add_parser(
        "update-trials", help="Fetch recent clinical trials metadata and generate summaries"
    )

    # review subcommand
    subparsers.add_parser(
        "review", help="Interactively suggest and apply edits to manuscript sections"
    )
    # memoire-llm subcommand: replicate/improve memoire with recent trials via LLM
    parser_memoire_llm = subparsers.add_parser(
        "memoire-llm",
        help="Generate updated memoire manuscript via LLM, add recent trials, save to manuscript/llm"
    )
    parser_memoire_llm.add_argument(
        "--provider", choices=["perplexity", "openrouter"], default=None,
        help="LLM provider to use (overrides SEARCH_PROVIDER env)"
    )
    parser_memoire_llm.add_argument(
        "--model", "-m", default=None,
        help="LLM model identifier for metadata in output filename"
    )
    parser_memoire_llm.add_argument(
        "--output-dir", "-o", default="manuscript/llm",
        help="Directory to save the generated LLM manuscript"
    )
    parser_memoire_llm.add_argument(
        "input_file", nargs="?", default="manuscript/memoire.md",
        help="Path to the base memoire manuscript to update"
    )

    # help subcommand
    parser_help = subparsers.add_parser(
        "help", help="Show help for commands"
    )
    parser_help.add_argument(
        "subcommand", nargs="?", help="Command to show detailed help for"
    )

    args, _ = parser.parse_known_args()

    if args.command == "help":
        # Delegate help display to sub-modules for full detail
        if args.subcommand:
            sub = args.subcommand
            if sub in ("search", "update-trials", "review"):
                import subprocess
                module = sub.replace('-', '_')
                subprocess.run([
                    sys.executable, '-m', f'ondansetron.{module}', '--help'
                ])
            else:
                print(f"Unknown command '{sub}'\n", file=sys.stderr)
                parser.print_help()
                sys.exit(1)
        else:
            parser.print_help()
        return

    if args.command == "search":
        sys.argv = [sys.argv[0]] + sys.argv[2:]
        _search_main()
    elif args.command == "update-trials":
        sys.argv = [sys.argv[0]] + sys.argv[2:]
        _update_trials_main()
    elif args.command == "review":
        sys.argv = [sys.argv[0]] + sys.argv[2:]
        _review_main()
    elif args.command == "memoire-llm":
        sys.argv = [sys.argv[0]] + sys.argv[2:]
        _memoire_llm_main()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
