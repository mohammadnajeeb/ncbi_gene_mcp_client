"""
Data models for NCBI Gene MCP Client.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class GeneInfo(BaseModel):
    """Model for gene information from NCBI Entrez."""
    
    gene_id: str = Field(description="NCBI Gene ID")
    name: str = Field(description="Gene symbol/name")
    description: str = Field(description="Gene description")
    organism: str = Field(description="Organism scientific name")
    chromosome: Optional[str] = Field(default=None, description="Chromosome location")
    map_location: Optional[str] = Field(default=None, description="Map location on chromosome")
    gene_type: Optional[str] = Field(default=None, description="Type of gene")
    other_aliases: Optional[List[str]] = Field(default=None, description="Other gene aliases")
    summary: Optional[str] = Field(default=None, description="Gene summary")


class ProteinInfo(BaseModel):
    """Model for protein information from NCBI Entrez."""
    
    protein_id: str = Field(description="NCBI Protein ID")
    title: str = Field(description="Protein title")
    organism: str = Field(description="Organism scientific name")
    length: Optional[int] = Field(default=None, description="Protein sequence length")
    mol_type: Optional[str] = Field(default=None, description="Molecule type")


class SearchResult(BaseModel):
    """Model for search results from NCBI Entrez."""
    
    count: int = Field(description="Total number of results")
    ids: List[str] = Field(description="List of IDs found")
    query_translation: Optional[str] = Field(default=None, description="Translated query")


class NCBIError(BaseModel):
    """Model for NCBI API errors."""
    
    error_code: str = Field(description="Error code")
    message: str = Field(description="Error message")
    details: Optional[Dict[str, Any]] = Field(default=None, description="Additional error details")
