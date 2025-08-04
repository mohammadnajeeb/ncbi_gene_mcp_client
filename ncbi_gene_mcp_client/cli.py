"""
Command-line interface for NCBI Gene MCP Client.
"""

import argparse
import json
import sys
from .main import NCBIGeneMCPClientBridge


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="NCBI Gene MCP Client - Fetch gene and protein information from NCBI Entrez"
    )
    
    parser.add_argument(
        "--email",
        help="Your email address (recommended by NCBI for API usage)"
    )
    
    parser.add_argument(
        "--api-key",
        help="NCBI API key (optional but recommended for higher rate limits)"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Search genes command
    search_parser = subparsers.add_parser("search-genes", help="Search for genes")
    search_parser.add_argument("query", help="Search query (gene name, symbol, etc.)")
    search_parser.add_argument("--max-results", type=int, default=20, help="Maximum results to return")
    
    # Fetch gene info command
    gene_parser = subparsers.add_parser("gene-info", help="Fetch gene information by ID")
    gene_parser.add_argument("gene_id", help="NCBI Gene ID (e.g., 672 for BRCA1)")
    
    # Fetch protein info command
    protein_parser = subparsers.add_parser("protein-info", help="Fetch protein information by ID")
    protein_parser.add_argument("protein_id", help="NCBI Protein ID")
    
    # Search by gene symbol command
    symbol_parser = subparsers.add_parser("search-symbol", help="Search genes by symbol")
    symbol_parser.add_argument("symbol", help="Gene symbol (e.g., BRCA1, TP53)")
    symbol_parser.add_argument("--organism", help="Optional organism filter (e.g., human, Homo sapiens)")
    
    # Demo command
    demo_parser = subparsers.add_parser("demo", help="Run demo with BRCA1 gene")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize the bridge
    bridge = NCBIGeneMCPClientBridge(email=args.email, api_key=args.api_key)
    
    try:
        if args.command == "search-genes":
            result = bridge.search_genes(args.query, args.max_results)
            print(f"Found {result.count} genes matching '{args.query}':")
            print(f"Gene IDs: {', '.join(result.ids[:10])}")
            if result.query_translation:
                print(f"Query translation: {result.query_translation}")
        
        elif args.command == "gene-info":
            result = bridge.fetch_gene_info(args.gene_id)
            print(json.dumps(result.model_dump(), indent=2))
        
        elif args.command == "protein-info":
            result = bridge.fetch_protein_info(args.protein_id)
            print(json.dumps(result.model_dump(), indent=2))
        
        elif args.command == "search-symbol":
            results = bridge.search_by_gene_symbol(args.symbol, args.organism)
            if not results:
                print(f"No genes found for symbol '{args.symbol}'")
                if args.organism:
                    print(f"in organism '{args.organism}'")
            else:
                print(f"Found {len(results)} gene(s) for symbol '{args.symbol}':")
                if args.organism:
                    print(f"in organism '{args.organism}'")
                print()
                
                for i, gene in enumerate(results, 1):
                    print(f"{i}. {gene.name} (ID: {gene.gene_id})")
                    print(f"   Description: {gene.description}")
                    print(f"   Organism: {gene.organism}")
                    if gene.chromosome:
                        print(f"   Chromosome: {gene.chromosome}")
                    print()
        
        elif args.command == "demo":
            print("🧬 NCBI Gene MCP Client Demo")
            print("=" * 40)
            
            print("\n1. Searching for BRCA1 gene...")
            brca1_search = bridge.search_genes("BRCA1[gene] AND human[organism]", max_results=5)
            print(f"   Found {brca1_search.count} results")
            
            if brca1_search.ids:
                gene_id = brca1_search.ids[0]
                print(f"\n2. Fetching details for gene ID: {gene_id}")
                gene_info = bridge.fetch_gene_info(gene_id)
                print(f"   Gene: {gene_info.name}")
                print(f"   Description: {gene_info.description}")
                print(f"   Organism: {gene_info.organism}")
                print(f"   Chromosome: {gene_info.chromosome}")
                
            print("\n3. Searching by gene symbol...")
            symbol_results = bridge.search_by_gene_symbol("BRCA1", "human")
            print(f"   Found {len(symbol_results)} genes for BRCA1 in humans")
            
            print("\n✅ Demo completed successfully!")
    
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
