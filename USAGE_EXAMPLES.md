# NCBI Gene MCP Client - Usage Examples

## Installation

```bash
pip install -e .
```

## Quick Start

### 1. Python API Usage

```python
from ncbi_gene_mcp_client.main import NCBIGeneMCPClientBridge

# Initialize client
client = NCBIGeneMCPClientBridge()

# Get gene information
gene_info = client.fetch_gene_info("672")  # BRCA1
print(f"Gene: {gene_info.name}")
print(f"Description: {gene_info.description}")
```

### 2. Command Line Usage

```bash
# Demo
ncbi-gene-client demo

# Search for genes
ncbi-gene-client search-genes "BRCA1"

# Get gene information by ID
ncbi-gene-client gene-info 672

# Search by gene symbol
ncbi-gene-client search-symbol BRCA1 --organism human
```

### 3. MCP Server Usage

```bash
# Start the MCP server
ncbi-gene-mcp-server

# The server provides these tools:
# - search_genes
# - fetch_gene_info  
# - fetch_protein_info
# - search_by_gene_symbol
```

## NCBI API Best Practices

1. **Provide your email** (recommended by NCBI):
   ```python
   client = NCBIGeneMCPClientBridge(email="your@email.com")
   ```

2. **Use API key for higher rate limits**:
   ```python
   client = NCBIGeneMCPClientBridge(
       email="your@email.com",
       api_key="your_ncbi_api_key"
   )
   ```

3. **Rate limiting is automatically handled**:
   - Without API key: 3 requests/second
   - With API key: 10 requests/second

## Example Use Cases

### Cancer Research - BRCA1 Analysis
```python
# Get BRCA1 gene details
brca1 = client.fetch_gene_info("672")
print(f"BRCA1 is located on chromosome {brca1.chromosome}")
print(f"Map location: {brca1.map_location}")
```

### Cross-Species Comparison
```python
# Compare BRCA1 across species
for organism in ["human", "mouse", "rat"]:
    genes = client.search_by_gene_symbol("BRCA1", organism=organism)
    if genes:
        gene = genes[0]
        print(f"{organism}: Chr {gene.chromosome}")
```

### Disease Gene Discovery
```python
# Find genes associated with diabetes
results = client.search_genes("diabetes[disease] AND human[organism]")
print(f"Found {results.count} genes associated with diabetes")
```

## Data Models

### GeneInfo
- `gene_id`: NCBI Gene ID
- `name`: Gene symbol/name
- `description`: Gene description
- `organism`: Scientific name
- `chromosome`: Chromosome location
- `map_location`: Precise location
- `gene_type`: Type of gene
- `other_aliases`: Alternative names
- `summary`: Detailed description

### SearchResult  
- `count`: Total number of results
- `ids`: List of gene IDs found
- `query_translation`: How NCBI interpreted the query

## Testing

```bash
# Run basic tests
pytest tests/ -v

# Run integration tests (requires internet)
pytest tests/ -m integration -v
```
