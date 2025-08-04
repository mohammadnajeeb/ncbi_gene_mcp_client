"""
Command-line interface for NCBI Gene MCP Client.
"""

import argparse
import sys
from typing import Optional

from .bridge import Bridge, Config


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        description="MCP client for fetching gene metadata from NCBI Entrez",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ncbi_gene_mcp_client method1 --param1 "test"
  ncbi_gene_mcp_client method2 --param1 "test" --param2 42
  ncbi_gene_mcp_client method3
        """
    )
    
    # Global options
    parser.add_argument(
        "--config",
        help="Path to configuration file"
    )
    parser.add_argument(
        "--api-key",
        help="API key for authentication"
    )
    parser.add_argument(
        "--base-url",
        help="Base URL for the API"
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        help="Request timeout in seconds (default: 30.0)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    # Subcommands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Method 1 command
    method1_parser = subparsers.add_parser("method1", help="Run method 1")
    method1_parser.add_argument("param1", help="Parameter 1")
    
    # Method 2 command
    method2_parser = subparsers.add_parser("method2", help="Run method 2")
    method2_parser.add_argument("param1", help="Parameter 1")
    method2_parser.add_argument("param2", type=int, help="Parameter 2")
    
    # Method 3 command
    method3_parser = subparsers.add_parser("method3", help="Run method 3")
    
    return parser


def load_config(config_path: Optional[str]) -> Config:
    """Load configuration from file or use defaults."""
    # TODO: Implement configuration file loading
    return Config()


def main(args: Optional[list] = None) -> int:
    """Main entry point for CLI."""
    parser = create_parser()
    parsed_args = parser.parse_args(args)
    
    if not parsed_args.command:
        parser.print_help()
        return 1
    
    # Load configuration
    config = load_config(parsed_args.config)
    
    # Override with command line arguments
    if parsed_args.api_key:
        config.api_key = parsed_args.api_key
    if parsed_args.base_url:
        config.base_url = parsed_args.base_url
    if parsed_args.timeout:
        config.timeout = parsed_args.timeout
    
    # Initialize bridge
    bridge = Bridge(config)
    
    try:
        if parsed_args.command == "method1":
            result = bridge.method1(parsed_args.param1)
            print(result)
        elif parsed_args.command == "method2":
            result = bridge.method2(parsed_args.param1, parsed_args.param2)
            print(result)
        elif parsed_args.command == "method3":
            result = bridge.method3()
            print(result)
        else:
            print(f"Unknown command: {parsed_args.command}")
            return 1
        
        return 0
        
    except Exception as e:
        if parsed_args.verbose:
            raise
        else:
            print(f"Error: {e}", file=sys.stderr)
            return 1


if __name__ == "__main__":
    sys.exit(main()) 