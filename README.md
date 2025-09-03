# TRIZ Contradiction API

![TRIZ API Architecture](docs/assets/scheme.png)

*Technical Contradiction processing framework - the core workflow for analyzing problems and generating inventive solutions through the `/contradictions/` endpoint.*

A FastAPI backend for TRIZ (Theory of Inventive Problem Solving) Contradictions with semantic search and LLM-powered contradiction extraction.

## Quick Start

### Environment Setup

Create a `.env` file in the project root with required API keys:

```bash
OPENAI_API_KEY=your_openai_api_key_here
```

### Run the API

**Using Docker (with custom data):**
```bash
docker-compose up
```

**Using Justfile for development (with default data):**
```bash
just dev
```

API available at `http://localhost:8000` with docs at `/docs`

### Data Customization

- **Docker deployment**: Uses custom data files from `./data/` directory
- **Development mode**: Uses built-in default data files
- Customize TRIZ parameters, principles, and matrix by editing files in `./data/`

## Core Features

- **TRIZ Parameters & Principles**: Semantic search across 39 parameters and 40 inventive principles
- **Matrix Lookup**: Get principles from classical TRIZ contradiction matrix
- **Technical Contradiction Extraction**: Extract contradictions from text using LLMs
- **Patent Analysis**: Specialized extraction and classification for patent content

## API Usage

```python
import httpx

# Search parameters
resp = httpx.get("http://localhost:8000/api/v1/parameters/search?q=strength&top_k=5")
params = resp.json()

# Matrix lookup  
resp = httpx.get("http://localhost:8000/api/v1/principles/matrix?improving=1&preserving=3")
principles = resp.json()

# Extract contradictions with full TRIZ analysis
resp = httpx.post("http://localhost:8000/api/v1/contradictions/extract-tc", 
    json={"description": "Need lightweight but strong material"})
contradictions = resp.json()

# Extract contradictions with parameter limit
resp = httpx.post("http://localhost:8000/api/v1/contradictions/extract-tc?limit=2", 
    json={"description": "Need lightweight but strong material"})
contradictions = resp.json()

# Get principle by name
resp = httpx.get("http://localhost:8000/api/v1/principles/by-name/Segmentation")
principle = resp.json()

# Get random principles for inspiration
resp = httpx.get("http://localhost:8000/api/v1/principles/random?limit=5")
random_principles = resp.json()
```

## Key Endpoints

### Parameters
- `GET /parameters/` - List all TRIZ parameters
- `GET /parameters/{id}` - Get parameter by ID
- `GET /parameters/search` - Search parameters by semantic similarity
  - Query parameters: `limit` (1-39, default: 5) - number of results to return

### Principles  
- `GET /principles/` - List all inventive principles
- `GET /principles/{id}` - Get principle by ID
- `GET /principles/by-name/{name}` - Get principle by name
- `GET /principles/search` - Search principles by semantic similarity
  - Query parameters: `limit` (1-40, default: 5) - number of results to return
- `GET /principles/random` - Get random principles for inspiration
  - Query parameters: `limit` (1-40, default: 5) - number of principles to return
- `GET /principles/matrix` - Get principles from contradiction matrix

### Contradictions
- `POST /contradictions/extract-tc` - Extract technical contradictions with full TRIZ analysis
  - Query parameters: `limit` (1-10, default: 3) - limit parameters per effect

### Patents
- `POST /patents/extract` - Extract contradictions from patent content
  - Query parameters: `limit` (1-10, default: 3) - limit parameters per effect
- `POST /patents/classify` - Classify patent solutions to TRIZ principles
  - Query parameters: `limit` (1-40, default: 10) - limit number of principles returned

### Utilities
- `GET /utils/health-check` - API health check endpoint

See `backend/test.http` for complete API examples.

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Citation

If you use TRIZ Contradiction API in your projects, please consider citing the following:

```bibtex
@software{TRIZ_Contradiction_API,
  author = {Mysior, M.},
  title = {TRIZ Contradiction API},
  url = {https://github.com/mmysior/contradictions-api},
  doi = {10.5281/zenodo.17042046},
  version = {0.1.0},
  year = {2025}
}
```

## Funding

This API was developed as part of research supported by the National Science Centre, Poland (grant no. 2024/08/X/ST8/00391).

