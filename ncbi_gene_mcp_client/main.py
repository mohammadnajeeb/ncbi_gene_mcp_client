"""
Main module for NCBI Gene MCP Client.
"""

from .mcp_server import MCPServer
from .bridge import NCBIBridge, Config


class NCBIGeneMCPClientBridge:
    """
    Main bridge class for NCBI Gene MCP Client.
    
    This class provides a convenient interface for using the NCBI client functionality.
    """
    
    def __init__(self, email: str = None, api_key: str = None):
        """
        Initialize the bridge.
        
        Args:
            email: Your email (recommended by NCBI for API usage)
            api_key: NCBI API key (optional but recommended for higher rate limits)
        """
        config = Config(email=email, api_key=api_key)
        self.bridge = NCBIBridge(config)
    
    def search_genes(self, query: str, max_results: int = 20):
        """Search for genes using NCBI Entrez."""
        return self.bridge.search_genes(query, max_results)
    
    def fetch_gene_info(self, gene_id: str):
        """Fetch detailed information for a specific gene."""
        return self.bridge.fetch_gene_info(gene_id)
    
    def fetch_protein_info(self, protein_id: str):
        """Fetch detailed information for a specific protein."""
        return self.bridge.fetch_protein_info(protein_id)
    
    def search_by_gene_symbol(self, symbol: str, organism: str = None):
        """Search for genes by symbol with optional organism filter."""
        return self.bridge.search_by_gene_symbol(symbol, organism)


def main() -> None:
    """Main entry point for MCP server."""
    server = MCPServer()
    server.run()


if __name__ == "__main__":
    main()
     