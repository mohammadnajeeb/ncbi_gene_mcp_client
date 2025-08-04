#!/usr/bin/env python3
"""
Comprehensive demonstration script for NCBI Gene MCP Client.

This script showcases all the main functionality of the NCBI Gene MCP Client,
including gene search, gene information retrieval, and protein data fetching.
"""

import json
import sys
from ncbi_gene_mcp_client.main import NCBIGeneMCPClientBridge


def main():
    """Run comprehensive demonstration of NCBI Gene MCP Client."""
    
    print("🧬 NCBI Gene MCP Client - Comprehensive Demo")
    print("=" * 60)
    
    # Initialize the client
    print("\n📡 Initializing NCBI client...")
    client = NCBIGeneMCPClientBridge()
    print("✅ Client initialized successfully!")
    
    # Demo 1: Search for genes
    print("\n🔍 Demo 1: Searching for genes related to 'breast cancer'")
    print("-" * 50)
    try:
        search_results = client.search_genes("breast cancer[disease] AND human[organism]", max_results=5)
        print(f"Found {search_results.count} genes related to breast cancer")
        print(f"First 5 gene IDs: {', '.join(search_results.ids[:5])}")
        if search_results.query_translation:
            print(f"Query translation: {search_results.query_translation}")
    except Exception as e:
        print(f"❌ Error in gene search: {e}")
    
    # Demo 2: Get detailed gene information for BRCA1
    print("\n🧬 Demo 2: Detailed information for BRCA1 gene (ID: 672)")
    print("-" * 50)
    try:
        brca1_info = client.fetch_gene_info("672")
        print(f"Gene Name: {brca1_info.name}")
        print(f"Description: {brca1_info.description}")
        print(f"Organism: {brca1_info.organism}")
        print(f"Chromosome: {brca1_info.chromosome}")
        print(f"Map Location: {brca1_info.map_location}")
        print(f"Gene Type: {brca1_info.gene_type}")
        if brca1_info.other_aliases:
            print(f"Other Aliases: {', '.join(brca1_info.other_aliases[:5])}...")
        if brca1_info.summary:
            summary_short = brca1_info.summary[:200] + "..." if len(brca1_info.summary) > 200 else brca1_info.summary
            print(f"Summary: {summary_short}")
    except Exception as e:
        print(f"❌ Error fetching gene info: {e}")
    
    # Demo 3: Search by gene symbol
    print("\n🔎 Demo 3: Search by gene symbol 'TP53' in human")
    print("-" * 50)
    try:
        tp53_genes = client.search_by_gene_symbol("TP53", organism="human")
        print(f"Found {len(tp53_genes)} genes for symbol 'TP53' in humans")
        for i, gene in enumerate(tp53_genes[:3], 1):  # Show first 3 results
            print(f"  {i}. {gene.name} (ID: {gene.gene_id})")
            print(f"     Description: {gene.description}")
            print(f"     Chromosome: {gene.chromosome}")
            print()
    except Exception as e:
        print(f"❌ Error in symbol search: {e}")
    
    # Demo 4: Test with another well-known gene - APOE
    print("\n🧠 Demo 4: Information for APOE gene (Alzheimer's disease risk factor)")
    print("-" * 50)
    try:
        apoe_search = client.search_genes("APOE[gene] AND human[organism]", max_results=1)
        if apoe_search.ids:
            apoe_info = client.fetch_gene_info(apoe_search.ids[0])
            print(f"Gene: {apoe_info.name}")
            print(f"Description: {apoe_info.description}")
            print(f"Location: Chromosome {apoe_info.chromosome}, {apoe_info.map_location}")
        else:
            print("No APOE gene found")
    except Exception as e:
        print(f"❌ Error fetching APOE info: {e}")
    
    # Demo 5: Cross-species comparison
    print("\n🐭 Demo 5: Cross-species comparison of BRCA1")
    print("-" * 50)
    species = ["human", "mouse", "rat"]
    for organism in species:
        try:
            genes = client.search_by_gene_symbol("BRCA1", organism=organism)
            if genes:
                gene = genes[0]
                print(f"  {organism.capitalize()}: {gene.name} (ID: {gene.gene_id}) - Chr {gene.chromosome}")
            else:
                print(f"  {organism.capitalize()}: No BRCA1 found")
        except Exception as e:
            print(f"  {organism.capitalize()}: Error - {e}")
    
    # Demo 6: JSON export example
    print("\n📄 Demo 6: JSON export of gene data")
    print("-" * 50)
    try:
        brca1_info = client.fetch_gene_info("672")
        json_output = json.dumps(brca1_info.model_dump(), indent=2)
        print("BRCA1 gene data in JSON format:")
        print(json_output[:500] + "..." if len(json_output) > 500 else json_output)
    except Exception as e:
        print(f"❌ Error in JSON export: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Comprehensive demo completed successfully!")
    print("\n💡 To use this in your own projects:")
    print("   from ncbi_gene_mcp_client.main import NCBIGeneMCPClientBridge")
    print("   client = NCBIGeneMCPClientBridge()")
    print("   gene_info = client.fetch_gene_info('672')  # BRCA1")
    print("\n📚 For MCP server usage:")
    print("   ncbi-gene-mcp-server")
    print("\n🖥️  For CLI usage:")
    print("   ncbi-gene-client demo")
    print("   ncbi-gene-client gene-info 672")
    print("   ncbi-gene-client search-symbol BRCA1 --organism human")


if __name__ == "__main__":
    main()
