"""
MCP Server implementation for NCBI Gene MCP Client.
"""

import json
import sys
from typing import Any, Dict, List, Optional

from .bridge import NCBIBridge, Config


class MCPServer:
    """MCP Server for NCBI Gene MCP Client."""
    
    def __init__(self):
        """Initialize the MCP server."""
        self.bridge = NCBIBridge()
        self.request_id = 0
    
    def send_response(self, result: Any, error: Optional[str] = None):
        """Send a JSON-RPC response."""
        response = {
            "jsonrpc": "2.0",
            "id": self.request_id,
        }
        
        if error:
            response["error"] = {"code": -1, "message": error}
        else:
            response["result"] = result
        
        print(json.dumps(response))
        sys.stdout.flush()
    
    def handle_request(self, request: Dict[str, Any]):
        """Handle a JSON-RPC request."""
        method = request.get("method")
        params = request.get("params", {})
        self.request_id = request.get("id", 0)
        
        try:
            if method == "initialize":
                self.handle_initialize(params)
            elif method == "tools/list":
                self.handle_list_tools()
            elif method == "tools/call":
                self.handle_call_tool(params)
            else:
                self.send_response(None, f"Unknown method: {method}")
        except Exception as e:
            self.send_response(None, str(e))
    
    def handle_initialize(self, params: Dict[str, Any]):
        """Handle initialize request."""
        response = {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {}
            },
            "serverInfo": {
                "name": "ncbi_gene_mcp_client-mcp",
                "version": "0.1.0"
            }
        }
        self.send_response(response)
    
    def handle_list_tools(self):
        """Handle tools/list request."""
        tools = [
            {
                "name": "search_genes",
                "description": "Search for genes in NCBI database using a query",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query (gene name, symbol, etc.)"
                        },
                        "max_results": {
                            "type": "integer",
                            "description": "Maximum number of results to return (default: 20)",
                            "default": 20
                        }
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "fetch_gene_info",
                "description": "Fetch detailed information for a specific gene ID",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "gene_id": {
                            "type": "string",
                            "description": "NCBI Gene ID (e.g., '672' for BRCA1)"
                        }
                    },
                    "required": ["gene_id"]
                }
            },
            {
                "name": "fetch_protein_info",
                "description": "Fetch detailed information for a specific protein ID",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "protein_id": {
                            "type": "string",
                            "description": "NCBI Protein ID"
                        }
                    },
                    "required": ["protein_id"]
                }
            },
            {
                "name": "search_by_gene_symbol",
                "description": "Search for genes by symbol with optional organism filter",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "symbol": {
                            "type": "string",
                            "description": "Gene symbol (e.g., 'BRCA1', 'TP53')"
                        },
                        "organism": {
                            "type": "string",
                            "description": "Optional organism filter (e.g., 'human', 'Homo sapiens')"
                        }
                    },
                    "required": ["symbol"]
                }
            }
        ]
        
        self.send_response({"tools": tools})
    
    def handle_call_tool(self, params: Dict[str, Any]):
        """Handle tools/call request."""
        name = params.get("name")
        arguments = params.get("arguments", {})
        
        try:
            if name == "search_genes":
                query = arguments.get("query")
                max_results = arguments.get("max_results", 20)
                if not query:
                    raise ValueError("query is required")
                
                result = self.bridge.search_genes(query, max_results)
                self.send_response({
                    "content": [{
                        "type": "text", 
                        "text": f"Found {result.count} genes matching '{query}':\n\nGene IDs: {', '.join(result.ids[:10])}\n\nQuery translation: {result.query_translation or 'N/A'}"
                    }]
                })
            
            elif name == "fetch_gene_info":
                gene_id = arguments.get("gene_id")
                if not gene_id:
                    raise ValueError("gene_id is required")
                
                result = self.bridge.fetch_gene_info(gene_id)
                gene_json = result.model_dump_json(indent=2)
                self.send_response({
                    "content": [{
                        "type": "text", 
                        "text": f"Gene Information for ID {gene_id}:\n\n{gene_json}"
                    }]
                })
            
            elif name == "fetch_protein_info":
                protein_id = arguments.get("protein_id")
                if not protein_id:
                    raise ValueError("protein_id is required")
                
                result = self.bridge.fetch_protein_info(protein_id)
                protein_json = result.model_dump_json(indent=2)
                self.send_response({
                    "content": [{
                        "type": "text", 
                        "text": f"Protein Information for ID {protein_id}:\n\n{protein_json}"
                    }]
                })
            
            elif name == "search_by_gene_symbol":
                symbol = arguments.get("symbol")
                organism = arguments.get("organism")
                if not symbol:
                    raise ValueError("symbol is required")
                
                results = self.bridge.search_by_gene_symbol(symbol, organism)
                if not results:
                    response_text = f"No genes found for symbol '{symbol}'"
                    if organism:
                        response_text += f" in organism '{organism}'"
                else:
                    response_text = f"Found {len(results)} gene(s) for symbol '{symbol}'"
                    if organism:
                        response_text += f" in organism '{organism}'"
                    response_text += ":\n\n"
                    
                    for i, gene in enumerate(results, 1):
                        response_text += f"{i}. {gene.name} (ID: {gene.gene_id})\n"
                        response_text += f"   Description: {gene.description}\n"
                        response_text += f"   Organism: {gene.organism}\n"
                        if gene.chromosome:
                            response_text += f"   Chromosome: {gene.chromosome}\n"
                        response_text += "\n"
                
                self.send_response({
                    "content": [{
                        "type": "text", 
                        "text": response_text
                    }]
                })
            
            else:
                raise ValueError(f"Unknown tool: {name}")
        
        except Exception as e:
            self.send_response(None, str(e))
    
    def run(self):
        """Main event loop for the MCP server."""
        print("NCBI Gene MCP Client MCP server ready...", file=sys.stderr)
        
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            
            try:
                request = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"Bad JSON from host: {e}", file=sys.stderr)
                continue
            
            self.handle_request(request) 