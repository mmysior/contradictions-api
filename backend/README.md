# Backend API

A FastAPI service for TRIZ (Theory of Inventive Problem Solving) analysis with semantic search and LLM-powered contradiction extraction.

## Quick Start

From the project root:

```bash
docker compose up -d
```

API available at `http://localhost:8000` with interactive documentation at `/docs`

## Core Features

- **Semantic Search**: Find relevant TRIZ parameters and inventive principles using natural language
- **Matrix Lookup**: Get principle recommendations from the classical TRIZ contradiction matrix
- **Technical Contradiction Extraction**: Analyze problem descriptions to identify contradictions
- **Patent Analysis**: Extract contradictions and classify solutions from patent content

## API Endpoints

All endpoints are under the `/api/v1/` prefix.

### Parameters
Search and retrieve TRIZ parameters (39 total):
- List all parameters or get by ID
- Search parameters using semantic similarity
- Limit results with `limit` query parameter

### Principles
Work with TRIZ inventive principles (40 total):
- List, search, or get by ID/name
- Get principles from the contradiction matrix
- Generate random principles for inspiration
- Limit results with `limit` query parameter

### Contradictions
Extract technical contradictions from problem descriptions:
- Analyze text to identify action parameters, positive effects, and negative effects

### Patents
Specialized analysis for patent content:
- Extract contradictions from patent text
- Supports OCR processing for patent documents

### Utilities
- Health check endpoint for monitoring

For detailed API usage and examples, visit `/docs` when the API is running.

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

