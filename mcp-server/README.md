# MCP Server

Model Context Protocol (MCP) server that brings TRIZ analysis tools to AI assistants.

## Quick Start

From the project root:

```bash
docker compose up -d
```

The MCP server will be available at `http://localhost:8001/mcp`

## Installation

### For Claude Desktop

Add to your Claude Desktop config file:

```json
{
  "mcpServers": {
    "traicon": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "http://localhost:8001/mcp"
      ]
    }
  }
}
```

### For LM Studio

Add to your `mcp.json` (Program tab → Install → Edit mcp.json):

```json
{
  "mcpServers": {
    "traicon": {
      "url": "http://127.0.0.1:8001/mcp"
    }
  }
}
```

## Available Tools

### `formulate_technical_contradiction`
Analyzes problem descriptions to extract technical contradictions, identifying:
- Action parameters (what you're trying to change)
- Positive effects (desired improvements)
- Negative effects (unwanted consequences)

Returns matched TRIZ parameters and recommended inventive principles.

### `find_matching_parameter`
Searches for TRIZ parameters using semantic similarity to natural language queries.
- Takes a description and returns the most relevant parameters
- Configurable result limit (1-39)

### `find_matching_principle`
Finds inventive principles relevant to your problem using semantic search.
- Takes a problem description or search query
- Configurable result limit (1-40)

### `get_inventive_principles_by_matrix`
Retrieves principles from the classical TRIZ contradiction matrix.
- Specify parameters to improve and preserve
- Returns recommended principles for resolving the contradiction

### `get_random_inventive_principles`
Generates random inventive principles for creative brainstorming.
- Configurable number of principles (1-40)

## Usage

Once connected, AI assistants can automatically use TRIZ tools to:
1. Analyze problem descriptions and formulate contradictions
2. Search for relevant TRIZ parameters and principles
3. Look up principle recommendations from the contradiction matrix
4. Generate creative solutions based on TRIZ methodology

## Troubleshooting

### "Connection refused" errors
Ensure the services are running:
```bash
docker compose up -d
```

Check server health: `curl http://localhost:8001/health`

### Tools not appearing
1. Restart your AI assistant after adding the configuration
2. Verify the MCP endpoint is accessible: `curl http://localhost:8001/mcp`
3. Check your AI assistant's MCP configuration file for syntax errors

## Related

- [Backend API Documentation](../backend/README.md)
- [Main Documentation](../README.md)
