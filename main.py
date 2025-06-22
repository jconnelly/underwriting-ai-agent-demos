#!/usr/bin/env python3
"""
Main entry point for the Automobile Insurance Underwriting System.

This script provides a unified command-line interface for all underwriting
operations including basic evaluations and comprehensive A/B testing.

Usage:
    python main.py --help                    # Show all available commands
    python main.py basic --help              # Basic underwriting help
    python main.py ab-test --help            # A/B testing help
    
Examples:
    # Basic underwriting evaluation
    python main.py basic --test
    python main.py basic --interactive
    
    # A/B testing operations
    python main.py ab-test --list-configs
    python main.py ab-test --rule-comparison standard liberal
    python main.py ab-test --comprehensive
"""

import os
import sys
import argparse
from pathlib import Path

# Add the project root to Python path for imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Set PYTHONPATH environment variable as well
os.environ['PYTHONPATH'] = str(project_root)

try:
    from underwriting.cli.basic import main as basic_main
    from underwriting.cli.ab_testing import main as ab_test_main
    from underwriting.cli.web_server import main as web_server_main
    from underwriting.cli.streamlit_server import main as streamlit_main
    from underwriting import __version__
except ImportError as e:
    print(f"Error importing underwriting modules: {e}")
    print("Please ensure you're running from the project root directory.")
    sys.exit(1)


def create_parser():
    """Create the main argument parser with subcommands."""
    
    parser = argparse.ArgumentParser(
        prog="underwriting",
        description="Automobile Insurance Underwriting System with AI and A/B Testing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s basic --test                    Run basic underwriting tests
  %(prog)s basic --interactive             Interactive underwriting mode
  %(prog)s ab-test --list-configs          List available A/B test configurations
  %(prog)s ab-test --comprehensive         Run comprehensive A/B test suite
  %(prog)s ab-test --rule-comparison standard liberal
        """
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version=f"Automobile Underwriting System v{__version__}"
    )
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(
        dest="command",
        help="Available commands",
        metavar="COMMAND"
    )
    
    # Basic underwriting subcommand
    basic_parser = subparsers.add_parser(
        "basic",
        help="Basic underwriting operations",
        description="Perform basic underwriting evaluations on individual applicants"
    )
    
    basic_parser.add_argument(
        "--test",
        action="store_true",
        help="Run automated tests with sample applicants"
    )
    
    basic_parser.add_argument(
        "--interactive",
        action="store_true", 
        help="Start interactive underwriting session"
    )
    
    basic_parser.add_argument(
        "--applicant-id",
        type=str,
        help="Evaluate specific applicant by ID"
    )
    
    basic_parser.add_argument(
        "--rules-file",
        type=str,
        default="config/rules/underwriting_rules.json",
        help="Path to underwriting rules file"
    )
    
    # A/B testing subcommand
    ab_parser = subparsers.add_parser(
        "ab-test",
        help="A/B testing operations",
        description="Run A/B tests to compare different underwriting approaches"
    )
    
    ab_parser.add_argument(
        "--list-configs",
        action="store_true",
        help="List available test configurations"
    )
    
    ab_parser.add_argument(
        "--rule-comparison",
        nargs=2,
        metavar=("VARIANT_A", "VARIANT_B"),
        help="Compare two rule configurations (e.g., standard liberal)"
    )
    
    ab_parser.add_argument(
        "--prompt-comparison", 
        nargs=2,
        metavar=("VARIANT_A", "VARIANT_B"),
        help="Compare two prompt templates (e.g., balanced conservative)"
    )
    
    ab_parser.add_argument(
        "--comprehensive",
        action="store_true",
        help="Run comprehensive A/B test suite"
    )
    
    ab_parser.add_argument(
        "--single-variant",
        type=str,
        help="Test single variant configuration"
    )
    
    ab_parser.add_argument(
        "--confidence-level",
        type=float,
        default=0.95,
        help="Statistical confidence level (default: 0.95)"
    )
    
    ab_parser.add_argument(
        "--monthly-applications",
        type=int,
        default=10000,
        help="Monthly application volume for business impact analysis"
    )
    
    ab_parser.add_argument(
        "--export",
        type=str,
        help="Export results to JSON file"
    )
    
    # Web server subcommand
    web_parser = subparsers.add_parser(
        "web",
        help="Web server operations",
        description="Start the web interface for the underwriting system"
    )
    
    web_parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="Host to bind to (default: 127.0.0.1)"
    )
    
    web_parser.add_argument(
        "--port",
        type=int,
        default=5000,
        help="Port to bind to (default: 5000)"
    )
    
    web_parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode"
    )
    
    web_parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reload on file changes"
    )
    
    # Streamlit server subcommand
    streamlit_parser = subparsers.add_parser(
        "streamlit",
        help="Streamlit web application",
        description="Start the Streamlit web interface for the underwriting system"
    )
    
    streamlit_parser.add_argument(
        "--host",
        type=str,
        default="localhost",
        help="Host to bind to (default: localhost)"
    )
    
    streamlit_parser.add_argument(
        "--port",
        type=int,
        default=8501,
        help="Port to bind to (default: 8501)"
    )
    
    streamlit_parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode with auto-reload"
    )
    
    streamlit_parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Do not automatically open browser"
    )
    
    return parser


def main():
    """Main entry point for the underwriting system."""
    
    parser = create_parser()
    args = parser.parse_args()
    
    # If no command specified, show help
    if not args.command:
        parser.print_help()
        return 0
    
    try:
        if args.command == "basic":
            # Convert args to format expected by basic CLI
            basic_args = []
            
            if args.test:
                basic_args.append("--test")
            elif args.interactive:
                basic_args.append("--interactive")
            elif args.applicant_id:
                basic_args.extend(["--applicant-id", args.applicant_id])
            
            if args.rules_file != "config/rules/underwriting_rules.json":
                basic_args.extend(["--rules-file", args.rules_file])
            
            # Override sys.argv for the basic CLI
            original_argv = sys.argv
            sys.argv = ["basic"] + basic_args
            
            try:
                return basic_main()
            finally:
                sys.argv = original_argv
                
        elif args.command == "ab-test":
            # Convert args to format expected by A/B testing CLI
            ab_args = []
            
            if args.list_configs:
                ab_args.append("--list-configs")
            elif args.rule_comparison:
                ab_args.extend(["--rule-comparison"] + args.rule_comparison)
            elif args.prompt_comparison:
                ab_args.extend(["--prompt-comparison"] + args.prompt_comparison)
            elif args.comprehensive:
                ab_args.append("--comprehensive")
            elif args.single_variant:
                ab_args.extend(["--single-variant", args.single_variant])
            
            if args.confidence_level != 0.95:
                ab_args.extend(["--confidence-level", str(args.confidence_level)])
            
            if args.monthly_applications != 10000:
                ab_args.extend(["--monthly-applications", str(args.monthly_applications)])
            
            if args.export:
                ab_args.extend(["--export", args.export])
            
            # Override sys.argv for the A/B testing CLI
            original_argv = sys.argv
            sys.argv = ["ab_test"] + ab_args
            
            try:
                return ab_test_main()
            finally:
                sys.argv = original_argv
        
        elif args.command == "web":
            # Convert args to format expected by web server CLI
            web_args = []
            
            if args.host != "127.0.0.1":
                web_args.extend(["--host", args.host])
            
            if args.port != 5000:
                web_args.extend(["--port", str(args.port)])
            
            if args.debug:
                web_args.append("--debug")
            
            if args.reload:
                web_args.append("--reload")
            
            # Override sys.argv for the web server CLI
            original_argv = sys.argv
            sys.argv = ["web_server"] + web_args
            
            try:
                return web_server_main()
            finally:
                sys.argv = original_argv
        
        elif args.command == "streamlit":
            # Convert args to format expected by Streamlit CLI
            return streamlit_main(args)
        
        else:
            parser.print_help()
            return 1
            
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

