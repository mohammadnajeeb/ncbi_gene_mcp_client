"""
Tests for NCBI Gene MCP Client main module.
"""

import pytest
from ncbi_gene_mcp_client.main import Bridge, Config


class TestConfig:
    """Test the Config class."""
    
    def test_default_config(self):
        """Test default configuration."""
        config = Config()
        assert config.base_url == "https://api.example.com"
        assert config.api_key is None
        assert config.timeout == 30.0
        assert config.request_delay == 1.0
    
    def test_custom_config(self):
        """Test custom configuration."""
        config = Config(
            base_url="https://custom.api.com",
            api_key="test_key",
            timeout=60.0,
            request_delay=2.0
        )
        assert config.base_url == "https://custom.api.com"
        assert config.api_key == "test_key"
        assert config.timeout == 60.0
        assert config.request_delay == 2.0


class TestBridge:
    """Test the Bridge class."""
    
    def test_bridge_initialization(self):
        """Test bridge initialization with default config."""
        bridge = Bridge()
        assert bridge.config.base_url == "https://api.example.com"
        assert bridge.config.api_key is None
    
    def test_bridge_initialization_with_config(self):
        """Test bridge initialization with custom config."""
        config = Config(api_key="test_key")
        bridge = Bridge(config)
        assert bridge.config.api_key == "test_key"
        assert "Authorization" in bridge.session.headers
    
    def test_method1(self):
        """Test method1."""
        bridge = Bridge()
        result = bridge.method1("test_param")
        assert result["result"] == "Method 1 called with test_param"
    
    def test_method2(self):
        """Test method2."""
        bridge = Bridge()
        result = bridge.method2("test_param", 42)
        assert len(result) == 1
        assert result[0]["result"] == "Method 2 called with test_param and 42"
    
    def test_method3(self):
        """Test method3."""
        bridge = Bridge()
        result = bridge.method3()
        assert result == "Method 3 result" 