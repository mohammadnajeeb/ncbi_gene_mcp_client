"""
Standalone FastAPI application for Vercel deployment.
This version includes all necessary components without relative imports.
"""

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from typing import Optional, List, Dict, Any
import requests
import time
from pathlib import Path
from pydantic import BaseModel


# Data Models
class GeneInfo(BaseModel):
    gene_id: str
    name: str
    description: str
    organism: str
    chromosome: Optional[str] = None
    map_location: Optional[str] = None
    gene_type: Optional[str] = None
    other_aliases: List[str] = []
    summary: Optional[str] = None


class SearchResult(BaseModel):
    count: int
    ids: List[str]
    query_translation: Optional[str] = None


# NCBI Bridge (simplified for Vercel)
class NCBIBridge:
    def __init__(self):
        self.base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
        self.last_request_time = 0
        self.request_delay = 0.34  # 3 requests per second
    
    def _rate_limit(self):
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.request_delay:
            time.sleep(self.request_delay - time_since_last)
        self.last_request_time = time.time()
    
    def _make_request(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        self._rate_limit()
        url = f"{self.base_url}/{endpoint}.fcgi"
        
        common_params = {
            "retmode": "json",
            "tool": "ncbi_gene_mcp_client"
        }
        params.update(common_params)
        
        response = requests.get(url, params=params, timeout=30)
        if response.status_code != 200:
            raise Exception(f"NCBI API request failed: {response.status_code}")
        
        return response.json()
    
    def search_genes(self, query: str, max_results: int = 20) -> SearchResult:
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
        params = {
            "db": "gene",
            "id": gene_id
        }
        
        response = self._make_request("esummary", params)
        result = response.get("result", {})
        gene_data = result.get(gene_id)
        
        if not gene_data:
            raise Exception(f"No data found for gene ID: {gene_id}")
        
        organism = gene_data.get("organism", {})
        organism_name = organism.get("scientificname", "Unknown") if isinstance(organism, dict) else str(organism)
        
        aliases = []
        if "otheraliases" in gene_data:
            aliases = gene_data["otheraliases"].split(", ") if gene_data["otheraliases"] else []
        
        return GeneInfo(
            gene_id=gene_id,
            name=gene_data.get("name", "Unknown"),
            description=gene_data.get("description", "No description available"),
            organism=organism_name,
            chromosome=gene_data.get("chromosome"),
            map_location=gene_data.get("maplocation"),
            gene_type=gene_data.get("geneticsource"),
            other_aliases=aliases,
            summary=gene_data.get("summary")
        )
    
    def search_by_gene_symbol(self, symbol: str, organism: Optional[str] = None) -> List[GeneInfo]:
        query = f"{symbol}[gene symbol]"
        if organism:
            if organism.lower() == "human":
                organism = "Homo sapiens"
            query += f" AND {organism}[organism]"
        
        search_result = self.search_genes(query, max_results=50)
        
        genes = []
        for gene_id in search_result.ids[:10]:  # Limit to avoid timeout
            try:
                gene_info = self.fetch_gene_info(gene_id)
                if gene_info.name.upper() == symbol.upper():
                    genes.append(gene_info)
            except Exception:
                continue
        
        return genes


# Initialize FastAPI app
app = FastAPI(
    title="NCBI Gene MCP Client",
    description="Web interface for searching gene data from NCBI Entrez",
    version="0.1.0"
)

# Setup templates
templates_dir = Path(__file__).parent.parent / "ncbi_gene_mcp_client" / "templates"
templates = Jinja2Templates(directory=str(templates_dir))

# Initialize NCBI client
client = NCBIBridge()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with search interface."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    """About page."""
    return templates.TemplateResponse("about.html", {"request": request})


@app.get("/api", response_class=HTMLResponse)
async def api_docs(request: Request):
    """API documentation page."""
    return templates.TemplateResponse("api.html", {"request": request})


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "NCBI Gene MCP Client"}


@app.post("/api/search/genes")
async def search_genes(query: str = Form(...), max_results: int = Form(20)):
    """Search for genes using a query."""
    try:
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
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/gene/{gene_id}")
async def get_gene_info(gene_id: str):
    """Get detailed information for a specific gene."""
    try:
        gene_info = client.fetch_gene_info(gene_id)
        return {
            "success": True,
            "data": gene_info.dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/search/symbol")
async def search_by_symbol(symbol: str = Form(...), organism: Optional[str] = Form(None)):
    """Search genes by symbol with optional organism filter."""
    try:
        genes = client.search_by_gene_symbol(symbol, organism)
        return {
            "success": True,
            "data": {
                "genes": [gene.dict() for gene in genes],
                "count": len(genes),
                "symbol": symbol,
                "organism": organism
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/gene/{gene_id}", response_class=HTMLResponse)
async def gene_detail(request: Request, gene_id: str):
    """Gene detail page."""
    try:
        gene_info = client.fetch_gene_info(gene_id)
        return templates.TemplateResponse("gene_detail.html", {
            "request": request, 
            "gene": gene_info.dict()
        })
    except Exception as e:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": f"Gene not found: {str(e)}"
        })


# Export the app for Vercel
handler = app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
