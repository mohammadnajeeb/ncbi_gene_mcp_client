"""
Simple test app for Vercel deployment debugging.
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import os
from pathlib import Path

app = FastAPI(title="NCBI Gene MCP Client Test")

@app.get("/")
async def root():
    return JSONResponse({
        "message": "NCBI Gene MCP Client Test",
        "status": "working",
        "cwd": os.getcwd(),
        "files": os.listdir('.'),
        "path_exists": {
            "ncbi_gene_mcp_client": os.path.exists('ncbi_gene_mcp_client'),
            "templates": os.path.exists('ncbi_gene_mcp_client/templates') if os.path.exists('ncbi_gene_mcp_client') else False
        }
    })

@app.get("/api/health")
async def health():
    return {"status": "healthy", "service": "NCBI Gene MCP Client Test"}

@app.get("/test")
async def test():
    # Test NCBI API connection
    import requests
    try:
        response = requests.get(
            "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi",
            params={
                "db": "gene",
                "term": "BRCA1",
                "retmode": "json",
                "retmax": 1,
                "tool": "test"
            },
            timeout=10
        )
        return {
            "ncbi_test": "success",
            "status_code": response.status_code,
            "data": response.json() if response.status_code == 200 else "error"
        }
    except Exception as e:
        return {"ncbi_test": "failed", "error": str(e)}

# Export for Vercel
handler = app
