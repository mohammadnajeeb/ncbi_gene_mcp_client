# NCBI Gene MCP Client

🧬 **MCP client for fetching gene and protein metadata from NCBI Entrez API**

This project provides a Model Context Protocol (MCP) client that interfaces with the NCBI Entrez API to fetch detailed information about genes and proteins. It's designed to be used both as a standalone command-line tool and as an MCP server for integration with MCP-compatible clients.

## 🚀 Features

- **Gene Search**: Search for genes using flexible queries
- **Gene Information**: Fetch detailed gene metadata by NCBI Gene ID
- **Protein Information**: Fetch protein details by NCBI Protein ID
- **Symbol Search**: Search genes by symbol with optional organism filtering
- **Rate Limiting**: Built-in respect for NCBI API rate limits
- **MCP Server**: JSON-RPC server for MCP protocol integration
- **CLI Interface**: Easy-to-use command-line interface

## 📦 Installation

### From Source (Development)

```bash
# Clone the repository
git clone <repository-url>
cd ncbi_gene_mcp_client

# Install in development mode
pip install -e .
```

### From PyPI (when available)

```bash
pip install ncbi_gene_mcp_client
```

## 🔧 Usage

### Command Line Interface

After installation, you can use the CLI commands:

#### Demo (Quick Start)
```bash
ncbi-gene-client demo
```

#### Search for genes
```bash
ncbi-gene-client search-genes "BRCA1"
ncbi-gene-client search-genes "breast cancer" --max-results 10
```

#### Get gene information by ID
```bash
ncbi-gene-client gene-info 672  # BRCA1 gene
```

#### Search by gene symbol
```bash
ncbi-gene-client search-symbol BRCA1 --organism human
ncbi-gene-client search-symbol TP53
```

#### Get protein information
```bash
ncbi-gene-client protein-info <protein_id>
```

#### With NCBI credentials (recommended)
```bash
ncbi-gene-client --email your@email.com --api-key YOUR_API_KEY demo
```

### Python API

```python
from ncbi_gene_mcp_client.main import NCBIGeneMCPClientBridge

# Initialize the client
client = NCBIGeneMCPClientBridge(
    email="your@email.com",  # Recommended by NCBI
    api_key="your_api_key"   # Optional, for higher rate limits
)

# Search for genes
results = client.search_genes("BRCA1[gene] AND human[organism]")
print(f"Found {results.count} genes")

# Get detailed gene information
gene_info = client.fetch_gene_info("672")  # BRCA1
print(f"Gene: {gene_info.name}")
print(f"Description: {gene_info.description}")
print(f"Organism: {gene_info.organism}")

# Search by gene symbol
genes = client.search_by_gene_symbol("BRCA1", organism="human")
for gene in genes:
    print(f"{gene.name}: {gene.description}")
```

### MCP Server

Run as an MCP server for integration with MCP-compatible clients:

```bash
ncbi-gene-mcp-server
```

The MCP server provides the following tools:
- **search_genes**: Search for genes using a query
- **fetch_gene_info**: Get detailed gene information by ID
- **fetch_protein_info**: Get protein information by ID  
- **search_by_gene_symbol**: Search genes by symbol with optional organism filter

## 🧪 Examples

### Example 1: Basic Gene Search
```python
from ncbi_gene_mcp_client.main import NCBIGeneMCPClientBridge

client = NCBIGeneMCPClientBridge()

# Search for BRCA1 gene
results = client.search_genes("BRCA1")
print(f"Found {results.count} results")

# Get details for the first result
if results.ids:
    gene_info = client.fetch_gene_info(results.ids[0])
    print(f"Gene: {gene_info.name}")
    print(f"Chromosome: {gene_info.chromosome}")
```

### Example 2: Disease Gene Search
```python
# Search for genes related to a disease
results = client.search_genes("diabetes[disease] AND human[organism]")
for gene_id in results.ids[:5]:  # First 5 results
    gene = client.fetch_gene_info(gene_id)
    print(f"{gene.name}: {gene.description}")
```

### Example 3: Cross-species Gene Comparison
```python
# Compare BRCA1 across species
for organism in ["human", "mouse", "rat"]:
    genes = client.search_by_gene_symbol("BRCA1", organism=organism)
    if genes:
        gene = genes[0]
        print(f"{organism}: {gene.name} on chromosome {gene.chromosome}")
```

## 📊 Data Models

### GeneInfo
```python
{
    "gene_id": "672",
    "name": "BRCA1",
    "description": "BRCA1 DNA repair associated",
    "organism": "Homo sapiens",
    "chromosome": "17",
    "map_location": "17q21.31",
    "gene_type": "protein-coding",
    "other_aliases": ["BRCAI", "BRCC1", "BROVCA1"],
    "summary": "This gene encodes a 190 kD nuclear phosphoprotein..."
}
```

### SearchResult
```python
{
    "count": 1,
    "ids": ["672"],
    "query_translation": "BRCA1[gene]"
}
```

## ⚙️ Configuration

### NCBI API Guidelines

It's recommended to provide your email address when using the NCBI API:

```python
client = NCBIGeneMCPClientBridge(email="your@email.com")
```

For higher rate limits, you can also provide an API key:

```python
client = NCBIGeneMCPClientBridge(
    email="your@email.com",
    api_key="your_ncbi_api_key"
)
```

### Rate Limiting

The client automatically handles NCBI's rate limiting requirements:
- Without API key: 3 requests per second
- With API key: 10 requests per second

## 🧪 Testing

Run the test suite:

```bash
# Install test dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=ncbi_gene_mcp_client

# Run integration tests (requires internet)
pytest -m integration
```

## 🔍 Development

### Setting up for development

```bash
# Clone and install in development mode
git clone <repository-url>
cd ncbi_gene_mcp_client
pip install -e ".[dev]"

# Run linting
flake8 ncbi_gene_mcp_client/
mypy ncbi_gene_mcp_client/

# Format code
black ncbi_gene_mcp_client/
```

### Project Structure

```
ncbi_gene_mcp_client/
├── ncbi_gene_mcp_client/
│   ├── __init__.py
│   ├── main.py          # Main client class
│   ├── bridge.py        # NCBI API bridge
│   ├── models.py        # Data models
│   ├── mcp_server.py    # MCP server implementation
│   └── cli.py           # Command-line interface
├── tests/
│   ├── __init__.py
│   └── test_main.py     # Test suite
├── pyproject.toml       # Project configuration
├── README.md           # This file
└── LICENSE             # MIT License
```

## 📝 NCBI Resources

- [NCBI Entrez Programming Utilities](https://www.ncbi.nlm.nih.gov/books/NBK25501/)
- [NCBI Gene Database](https://www.ncbi.nlm.nih.gov/gene/)
- [E-utilities API Documentation](https://www.ncbi.nlm.nih.gov/books/NBK25499/)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Mohammad Najeeb**  
📧 mona00002@uni-saarland.de

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Features

- **Feature 1**: Description of feature 1
- **Feature 2**: Description of feature 2
- **Feature 3**: Description of feature 3

- **MCP Integration**: Full Model Context Protocol server implementation


## API Methods

### Core Methods

- `method1()`: Description of method1
- `method2()`: Description of method2
- `method3()`: Description of method3

### Configuration

The package uses a configuration class for settings:

```python
from ncbi_gene_mcp_client.main import NCBIGeneMCPClientConfig, NCBIGeneMCPClientBridge

config = NCBIGeneMCPClientConfig(
    base_url="https://api.example.com",
    api_key="your_api_key",
    timeout=30.0
)

bridge = NCBIGeneMCPClientBridge(config)
```


## MCP Server Configuration

To use the MCP server with an MCP client, configure it as follows:

```json
{
  "mcpServers": {
    "ncbi_gene_mcp_client": {
      "command": "ncbi_gene_mcp_client-server",
      "env": {}
    }
  }
}
```

The server will automatically handle:
- JSON-RPC communication
- Tool discovery and invocation
- Error handling and reporting


## Development

### Setup Development Environment

```bash
# Install in development mode with dev dependencies
pip install -e .[dev]

# Run tests
pytest

# Format code
black ncbi_gene_mcp_client/

# Type checking
mypy ncbi_gene_mcp_client/
```

### Project Structure

```
ncbi_gene_mcp_client/
├── pyproject.toml      # Package configuration
├── README.md          # This file
├── LICENSE            # MIT License
├── ncbi_gene_mcp_client/         # Main package
│   ├── __init__.py    # Package initialization
│   ├── main.py        # Core functionality


│   └── mcp_server.py  # MCP server implementation

└── tests/             # Test files
    ├── __init__.py
    └── test_main.py   # Tests for main functionality
```

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run the test suite
6. Submit a pull request

## Support

For issues and questions, please use the GitHub issue tracker. 