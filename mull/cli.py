"""CLI entry point for mull."""

import argparse
import sys

from . import __version__
from .pipeline import think


# ANSI colors
CYAN = "\033[96m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
DIM = "\033[2m"
RESET = "\033[0m"
BOLD = "\033[1m"


def print_step(name: str, content: str):
    """Print a pipeline step with formatting."""
    print(f"\n{CYAN}{BOLD}[{name}]{RESET}")
    print(f"{DIM}{'─' * 50}{RESET}")
    print(content)
    print()


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="mull",
        description="A thinking partner that critiques and refines its own responses.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  mull "Should I quit my job to start a company?"
  mull -v "What's the best way to give difficult feedback?"

Environment variables:
  MULL_API_BASE  LLM endpoint (default: http://localhost:1234/v1)
  MULL_API_KEY   API key if required (default: not-needed)
  MULL_MODEL     Model name (default: llama3)
        """,
    )

    parser.add_argument(
        "prompt",
        nargs="?",
        help="The question or prompt to think through",
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show all thinking steps (initial, critique, refined)",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"mull {__version__}",
    )

    args = parser.parse_args()

    # Handle no prompt
    if not args.prompt:
        # Check if stdin has data (piped input)
        if not sys.stdin.isatty():
            args.prompt = sys.stdin.read().strip()
        else:
            parser.print_help()
            sys.exit(1)

    if not args.prompt:
        print("Error: No prompt provided.", file=sys.stderr)
        sys.exit(1)

    # Run the pipeline
    try:
        if args.verbose:
            print(f"{DIM}Thinking...{RESET}\n")

            def on_step(step: str, content: str):
                labels = {
                    "initial": "Initial Response",
                    "critique": "Self-Critique",
                    "refined": "Refined Response",
                }
                print_step(labels.get(step, step), content)

            result = think(args.prompt, on_step=on_step)
        else:
            result = think(args.prompt)
            print(result.refined)

    except ConnectionError as e:
        print(f"{YELLOW}Error:{RESET} {e}", file=sys.stderr)
        sys.exit(1)

    except RuntimeError as e:
        print(f"{YELLOW}Error:{RESET} {e}", file=sys.stderr)
        sys.exit(1)

    except KeyboardInterrupt:
        print(f"\n{DIM}Interrupted.{RESET}", file=sys.stderr)
        sys.exit(130)


if __name__ == "__main__":
    main()
