"""
NCBI Gene MCP Client - MCP client for fetching gene metadata from NCBI Entrez
"""

__version__ = "0.1.0"
__author__ = "Mohammad Najeeb"
__email__ = "mona00002@uni-saarland.de"

from .bridge import Bridge, Config

__all__ = ["Bridge", "Config"] 