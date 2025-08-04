"""
FastAPI web application for NCBI Gene MCP Client.

This module provides a web interface for the NCBI Gene MCP Client,
allowing users to search and explore gene data through a browser.
"""

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Optional, List
import uvicorn
import json
from pathlib import Path

from .main import NCBIGeneMCPClientBridge
from .models import GeneInfo, SearchResult


# Initialize FastAPI app
app = FastAPI(
    title="NCBI Gene MCP Client Web Interface",
    description="Web interface for searching and exploring gene data from NCBI Entrez",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Setup templates and static files
templates_dir = Path(__file__).parent / "templates"
static_dir = Path(__file__).parent / "static"

templates = Jinja2Templates(directory=str(templates_dir))

# Mount static files if directory exists
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Initialize the NCBI client
client = NCBIGeneMCPClientBridge()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with search interface."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "NCBI Gene MCP Client"}


@app.post("/api/search/genes")
async def search_genes_api(
    query: str = Form(...),
    max_results: int = Form(20)
):
    """API endpoint to search for genes."""
    try:
        if not query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        result = client.search_genes(query, max_results)
        return {
            "success": True,
            "data": {
                "count": result.count,
                "ids": result.ids,
                "query_translation": result.query_translation,
                "query": query
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@app.get("/api/gene/{gene_id}")
async def get_gene_info_api(gene_id: str):
    """API endpoint to get detailed gene information."""
    try:
        gene_info = client.fetch_gene_info(gene_id)
        return {
            "success": True,
            "data": gene_info.model_dump()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch gene info: {str(e)}")


@app.post("/api/search/symbol")
async def search_by_symbol_api(
    symbol: str = Form(...),
    organism: Optional[str] = Form(None)
):
    """API endpoint to search genes by symbol."""
    try:
        if not symbol.strip():
            raise HTTPException(status_code=400, detail="Gene symbol cannot be empty")
        
        genes = client.search_by_gene_symbol(symbol, organism)
        return {
            "success": True,
            "data": {
                "genes": [gene.model_dump() for gene in genes],
                "count": len(genes),
                "symbol": symbol,
                "organism": organism
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Symbol search failed: {str(e)}")


@app.get("/search", response_class=HTMLResponse)
async def search_page(request: Request):
    """Search results page."""
    return templates.TemplateResponse("search.html", {"request": request})


@app.get("/gene/{gene_id}", response_class=HTMLResponse)
async def gene_detail_page(request: Request, gene_id: str):
    """Gene detail page."""
    try:
        gene_info = client.fetch_gene_info(gene_id)
        return templates.TemplateResponse("gene_detail.html", {
            "request": request,
            "gene": gene_info,
            "gene_json": json.dumps(gene_info.model_dump(), indent=2)
        })
    except Exception as e:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": f"Failed to fetch gene information: {str(e)}",
            "gene_id": gene_id
        })


@app.get("/api/examples")
async def get_examples():
    """Get example queries and gene IDs."""
    return {
        "search_examples": [
            "BRCA1[gene] AND human[organism]",
            "breast cancer[disease] AND human[organism]",
            "TP53",
            "diabetes[disease]",
            "APOE[gene]"
        ],
        "gene_examples": [
            {"id": "672", "name": "BRCA1", "description": "Breast cancer gene"},
            {"id": "7157", "name": "TP53", "description": "Tumor suppressor"},
            {"id": "348", "name": "APOE", "description": "Alzheimer's risk factor"},
            {"id": "2043", "name": "EPHA4", "description": "Receptor tyrosine kinase"},
            {"id": "1956", "name": "EGFR", "description": "Epidermal growth factor receptor"}
        ],
        "organisms": [
            "human",
            "Homo sapiens",
            "mouse",
            "Mus musculus",
            "rat",
            "Rattus norvegicus"
        ]
    }


@app.get("/about", response_class=HTMLResponse)
async def about_page(request: Request):
    """About page with information about the tool."""
    return templates.TemplateResponse("about.html", {"request": request})


@app.get("/api", response_class=HTMLResponse)
async def api_page(request: Request):
    """API documentation page."""
    return templates.TemplateResponse("api.html", {"request": request})


def main():
    """Main entry point for the web application."""
    print("🌐 Starting NCBI Gene MCP Client Web Interface...")
    print("📡 Initializing NCBI client...")
    
    # Test the client connection
    try:
        test_result = client.search_genes("BRCA1", max_results=1)
        print("✅ NCBI client connection successful!")
    except Exception as e:
        print(f"⚠️  Warning: NCBI client test failed: {e}")
        print("   The web interface will still start, but NCBI queries may fail.")
    
    print("\n🚀 Starting web server...")
    print("   Web interface: http://localhost:8000")
    print("   API docs: http://localhost:8000/api/docs")
    print("   Press Ctrl+C to stop")
    
    uvicorn.run(
        "ncbi_gene_mcp_client.web_app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )


if __name__ == "__main__":
    main()
