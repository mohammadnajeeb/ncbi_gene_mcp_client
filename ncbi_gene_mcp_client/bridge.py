"""
Bridge module for NCBI Gene MCP Client.
"""

import requests
import time
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from .models import GeneInfo, ProteinInfo, SearchResult, NCBIError


@dataclass
class Config:
    """Configuration for NCBI Gene MCP Client."""
    
    base_url: str = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    email: Optional[str] = None  # NCBI recommends providing email for API usage
    api_key: Optional[str] = None  # NCBI API key (optional but recommended)
    timeout: float = 30.0
    request_delay: float = 0.34  # NCBI rate limit: 3 requests per second without API key


class NCBIBridge:
    """
    Main bridge class for NCBI Entrez API.
    
    This class provides the main interface for interacting with NCBI Entrez databases
    to fetch gene and protein information.
    """
    
    def __init__(self, config: Optional[Config] = None):
        """
        Initialize the bridge.
        
        Args:
            config: Configuration object. If None, uses default configuration.
        """
        self.config = config or Config()
        self.session = requests.Session()
        
        # Set headers for NCBI API
        headers = {
            "User-Agent": "NCBI-Gene-MCP-Client/1.0"
        }
        if self.config.email:
            headers["email"] = self.config.email
        
        self.session.headers.update(headers)
        self.last_request_time = 0
    
    def _rate_limit(self):
        """Enforce rate limiting for NCBI API."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.config.request_delay:
            time.sleep(self.config.request_delay - time_since_last)
        
        self.last_request_time = time.time()
    
    def _make_request(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make a rate-limited request to NCBI API.
        
        Args:
            endpoint: API endpoint (esearch, esummary, efetch)
            params: Request parameters
            
        Returns:
            JSON response from API
            
        Raises:
            Exception: If request fails
        """
        self._rate_limit()
        
        url = f"{self.config.base_url}/{endpoint}.fcgi"
        
        # Add common parameters
        common_params = {
            "retmode": "json",
            "tool": "ncbi_gene_mcp_client"
        }
        if self.config.email:
            common_params["email"] = self.config.email
        if self.config.api_key:
            common_params["api_key"] = self.config.api_key
        
        params.update(common_params)
        
        response = self.session.get(url, params=params, timeout=self.config.timeout)
        
        if response.status_code != 200:
            raise Exception(f"NCBI API request failed with status {response.status_code}: {response.text}")
        
        return response.json()
    
    def search_genes(self, query: str, max_results: int = 20) -> SearchResult:
        """
        Search for genes using NCBI Entrez.
        
        Args:
            query: Search query (gene name, symbol, etc.)
            max_results: Maximum number of results to return
            
        Returns:
            SearchResult object containing IDs and metadata
        """
        params = {
            "db": "gene",
            "term": query,
            "retmax": max_results
        }
        
        response = self._make_request("esearch", params)
        
        esearch_result = response.get("esearchresult", {})
        
        return SearchResult(
            count=int(esearch_result.get("count", 0)),
            ids=esearch_result.get("idlist", []),
            query_translation=esearch_result.get("querytranslation")
        )
    
    def fetch_gene_info(self, gene_id: str) -> GeneInfo:
        """
        Fetch detailed information for a specific gene.
        
        Args:
            gene_id: NCBI Gene ID
            
        Returns:
            GeneInfo object with gene details
        """
        params = {
            "db": "gene",
            "id": gene_id
        }
        
        response = self._make_request("esummary", params)
        
        result = response.get("result", {})
        gene_data = result.get(gene_id)
        
        if not gene_data:
            raise Exception(f"No data found for gene ID: {gene_id}")
        
        # Extract organism information
        organism = gene_data.get("organism", {})
        organism_name = organism.get("scientificname", "Unknown") if isinstance(organism, dict) else str(organism)
        
        # Extract other aliases
        other_aliases = []
        if "otheraliases" in gene_data:
            aliases = gene_data["otheraliases"]
            if isinstance(aliases, str):
                other_aliases = [alias.strip() for alias in aliases.split(",")]
            elif isinstance(aliases, list):
                other_aliases = aliases
        
        return GeneInfo(
            gene_id=gene_id,
            name=gene_data.get("name", ""),
            description=gene_data.get("description", ""),
            organism=organism_name,
            chromosome=gene_data.get("chromosome"),
            map_location=gene_data.get("maplocation"),
            gene_type=gene_data.get("geneticsource"),
            other_aliases=other_aliases if other_aliases else None,
            summary=gene_data.get("summary")
        )
    
    def fetch_protein_info(self, protein_id: str) -> ProteinInfo:
        """
        Fetch detailed information for a specific protein.
        
        Args:
            protein_id: NCBI Protein ID
            
        Returns:
            ProteinInfo object with protein details
        """
        params = {
            "db": "protein",
            "id": protein_id
        }
        
        response = self._make_request("esummary", params)
        
        result = response.get("result", {})
        protein_data = result.get(protein_id)
        
        if not protein_data:
            raise Exception(f"No data found for protein ID: {protein_id}")
        
        return ProteinInfo(
            protein_id=protein_id,
            title=protein_data.get("title", ""),
            organism=protein_data.get("organism", ""),
            length=protein_data.get("slen"),
            mol_type=protein_data.get("moltype")
        )
    
    def search_by_gene_symbol(self, symbol: str, organism: Optional[str] = None) -> List[GeneInfo]:
        """
        Search for genes by symbol and optionally filter by organism.
        
        Args:
            symbol: Gene symbol (e.g., "BRCA1")
            organism: Optional organism filter (e.g., "human", "Homo sapiens")
            
        Returns:
            List of GeneInfo objects
        """
        query = f"{symbol}[gene]"
        if organism:
            query += f" AND {organism}[organism]"
        
        search_result = self.search_genes(query, max_results=10)
        
        genes = []
        for gene_id in search_result.ids:
            try:
                gene_info = self.fetch_gene_info(gene_id)
                genes.append(gene_info)
            except Exception as e:
                # Skip genes that can't be fetched
                continue
        
        return genes


# Backwards compatibility alias
Bridge = NCBIBridge 