"""
Tests for NCBI Gene MCP Client.
"""

import pytest
from unittest.mock import Mock, patch
from ncbi_gene_mcp_client.main import NCBIGeneMCPClientBridge
from ncbi_gene_mcp_client.bridge import NCBIBridge, Config
from ncbi_gene_mcp_client.models import GeneInfo, SearchResult


class TestNCBIGeneMCPClientBridge:
    """Test the main bridge class."""
    
    def test_init_default(self):
        """Test initialization with default parameters."""
        bridge = NCBIGeneMCPClientBridge()
        assert bridge.bridge is not None
        assert isinstance(bridge.bridge, NCBIBridge)
    
    def test_init_with_params(self):
        """Test initialization with email and API key."""
        bridge = NCBIGeneMCPClientBridge(
            email="test@example.com", 
            api_key="test_key"
        )
        assert bridge.bridge.config.email == "test@example.com"
        assert bridge.bridge.config.api_key == "test_key"
    
    @patch('ncbi_gene_mcp_client.bridge.NCBIBridge.search_genes')
    def test_search_genes(self, mock_search):
        """Test gene search functionality."""
        # Mock the return value
        mock_result = SearchResult(
            count=5,
            ids=["672", "675", "676"],
            query_translation="BRCA1[gene]"
        )
        mock_search.return_value = mock_result
        
        bridge = NCBIGeneMCPClientBridge()
        result = bridge.search_genes("BRCA1", max_results=10)
        
        mock_search.assert_called_once_with("BRCA1", 10)
        assert result.count == 5
        assert "672" in result.ids
    
    @patch('ncbi_gene_mcp_client.bridge.NCBIBridge.fetch_gene_info')
    def test_fetch_gene_info(self, mock_fetch):
        """Test gene info fetching."""
        # Mock the return value
        mock_gene = GeneInfo(
            gene_id="672",
            name="BRCA1",
            description="BRCA1 DNA repair associated",
            organism="Homo sapiens",
            chromosome="17"
        )
        mock_fetch.return_value = mock_gene
        
        bridge = NCBIGeneMCPClientBridge()
        result = bridge.fetch_gene_info("672")
        
        mock_fetch.assert_called_once_with("672")
        assert result.gene_id == "672"
        assert result.name == "BRCA1"


class TestConfig:
    """Test the configuration class."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = Config()
        assert config.base_url == "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
        assert config.email is None
        assert config.api_key is None
        assert config.timeout == 30.0
        assert config.request_delay == 0.34
    
    def test_custom_config(self):
        """Test custom configuration values."""
        config = Config(
            email="test@example.com",
            api_key="test_key",
            timeout=60.0,
            request_delay=1.0
        )
        assert config.email == "test@example.com"
        assert config.api_key == "test_key"
        assert config.timeout == 60.0
        assert config.request_delay == 1.0


@pytest.mark.integration
class TestNCBIBridgeIntegration:
    """Integration tests for NCBI Bridge (requires internet connection)."""
    
    def test_search_brca1_real(self):
        """Test real search for BRCA1 gene."""
        bridge = NCBIBridge()
        result = bridge.search_genes("BRCA1[gene] AND human[organism]", max_results=5)
        
        assert result.count > 0
        assert len(result.ids) > 0
        assert "672" in result.ids  # BRCA1 gene ID
    
    def test_fetch_brca1_info_real(self):
        """Test real gene info fetch for BRCA1."""
        bridge = NCBIBridge()
        gene_info = bridge.fetch_gene_info("672")  # BRCA1 gene ID
        
        assert gene_info.gene_id == "672"
        assert "BRCA1" in gene_info.name
        assert "Homo sapiens" in gene_info.organism
        assert gene_info.chromosome == "17"


if __name__ == "__main__":
    pytest.main([__file__])
