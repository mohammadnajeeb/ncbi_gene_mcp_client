#!/usr/bin/env python3
"""
Web Interface Demo Script for NCBI Gene MCP Client.

This script demonstrates the new web interface capabilities by testing
various API endpoints and showing how to interact with the web application.
"""

import requests
import json
import time


def test_web_api():
    """Test the web API endpoints."""
    
    base_url = "http://localhost:8000"
    
    print("🌐 NCBI Gene MCP Client - Web Interface Demo")
    print("=" * 60)
    
    # Test 1: Health check
    print("\n🔍 Test 1: Health Check")
    try:
        response = requests.get(f"{base_url}/api/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Server Status: {data['status']}")
            print(f"   Service: {data['service']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        print("   Make sure the web server is running with: ncbi-gene-web")
        return False
    
    # Test 2: Gene search
    print("\n🧬 Test 2: Gene Search API")
    try:
        data = {
            'query': 'BRCA1[gene] AND human[organism]',
            'max_results': '5'
        }
        response = requests.post(f"{base_url}/api/search/genes", data=data)
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                search_data = result['data']
                print(f"✅ Found {search_data['count']} genes")
                print(f"   First 5 IDs: {', '.join(search_data['ids'][:5])}")
                print(f"   Query translation: {search_data.get('query_translation', 'N/A')}")
            else:
                print("❌ Search failed")
        else:
            print(f"❌ API request failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Gene search error: {e}")
    
    # Test 3: Gene details
    print("\n📊 Test 3: Gene Details API")
    try:
        response = requests.get(f"{base_url}/api/gene/672")  # BRCA1
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                gene = result['data']
                print(f"✅ Gene Details Retrieved:")
                print(f"   Name: {gene['name']}")
                print(f"   Description: {gene['description']}")
                print(f"   Organism: {gene['organism']}")
                print(f"   Chromosome: {gene['chromosome']}")
                print(f"   Aliases: {len(gene.get('other_aliases', []))} found")
            else:
                print("❌ Gene details failed")
        else:
            print(f"❌ API request failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Gene details error: {e}")
    
    # Test 4: Symbol search
    print("\n🏷️  Test 4: Symbol Search API")
    try:
        data = {
            'symbol': 'TP53',
            'organism': 'human'
        }
        response = requests.post(f"{base_url}/api/search/symbol", data=data)
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                symbol_data = result['data']
                print(f"✅ Found {symbol_data['count']} genes for {symbol_data['symbol']}")
                if symbol_data['genes']:
                    gene = symbol_data['genes'][0]
                    print(f"   First result: {gene['name']} (ID: {gene['gene_id']})")
                    print(f"   Description: {gene['description']}")
            else:
                print("❌ Symbol search failed")
        else:
            print(f"❌ API request failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Symbol search error: {e}")
    
    # Test 5: Examples endpoint
    print("\n📚 Test 5: Examples API")
    try:
        response = requests.get(f"{base_url}/api/examples")
        if response.status_code == 200:
            examples = response.json()
            print(f"✅ Examples Retrieved:")
            print(f"   Search examples: {len(examples['search_examples'])}")
            print(f"   Gene examples: {len(examples['gene_examples'])}")
            print(f"   Organisms: {len(examples['organisms'])}")
            print(f"   Sample search: {examples['search_examples'][0]}")
        else:
            print(f"❌ API request failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Examples error: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Web API Testing Complete!")
    print(f"\n🌐 Web Interface URLs:")
    print(f"   Main Interface: {base_url}")
    print(f"   API Documentation: {base_url}/api/docs")
    print(f"   Alternative Docs: {base_url}/api/redoc")
    print(f"   About Page: {base_url}/about")
    
    return True


def demo_usage_examples():
    """Show usage examples for different interfaces."""
    
    print("\n📖 NCBI Gene MCP Client - All Interfaces")
    print("=" * 60)
    
    print("\n1️⃣  Web Interface:")
    print("   🌐 http://localhost:8000")
    print("   - Interactive search forms")
    print("   - Gene detail pages")
    print("   - Cross-species comparison")
    print("   - JSON export functionality")
    
    print("\n2️⃣  CLI Interface:")
    print("   🖥️  Command Line Usage:")
    print("   ncbi-gene-client demo")
    print("   ncbi-gene-client gene-info 672")
    print("   ncbi-gene-client search-symbol BRCA1 --organism human")
    
    print("\n3️⃣  MCP Server:")
    print("   🔗 Model Context Protocol:")
    print("   ncbi-gene-mcp-server")
    print("   # Provides JSON-RPC tools for MCP clients")
    
    print("\n4️⃣  Python API:")
    print("   🐍 Programmatic Usage:")
    print("   from ncbi_gene_mcp_client.main import NCBIGeneMCPClientBridge")
    print("   client = NCBIGeneMCPClientBridge()")
    print("   gene_info = client.fetch_gene_info('672')")
    
    print("\n5️⃣  REST API:")
    print("   🌐 HTTP API Endpoints:")
    print("   GET  /api/health")
    print("   POST /api/search/genes")
    print("   GET  /api/gene/{gene_id}")
    print("   POST /api/search/symbol")


if __name__ == "__main__":
    print("Starting web interface tests...")
    
    if test_web_api():
        demo_usage_examples()
        
        print("\n✨ Next Steps:")
        print("1. Open http://localhost:8000 in your browser")
        print("2. Try searching for genes like 'BRCA1', 'TP53', or 'diabetes'")
        print("3. Explore the interactive API docs at /api/docs")
        print("4. Check out individual gene pages")
        print("5. Test cross-species comparisons")
        
        print("\n🛑 To stop the web server:")
        print("   Press Ctrl+C in the terminal where ncbi-gene-web is running")
    else:
        print("\n❌ Web server tests failed!")
        print("   Start the server with: ncbi-gene-web")
        print("   Then run this script again.")
