from app.tools.contradictions import (
    formulate_tc,
    get_ips_by_matrix,
    get_random_principles,
    search_parameter,
    search_principle,
)
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("traicon")


# Register tools
@mcp.tool()
async def formulate_technical_contradiction(description: str) -> str:
    """Formulate Technical Contradiction from problem description.

    Extracts technical contradictions identifying the action parameter
    and two evaluation parameters (positive and negative effects).

    Args:
        description: Problem description text
    """
    return await formulate_tc(description)


@mcp.tool()
async def get_inventive_principles_by_matrix(
    improving_params: list[int], preserving_params: list[int]
) -> str:
    """Get Inventive Principles from TRIZ contradiction matrix.

    Looks up applicable Inventive Principles based on parameters to improve
    and parameters to preserve using the classical TRIZ contradiction matrix.

    Args:
        improving_params: List of TRIZ parameter IDs that should be improved
        preserving_params: List of TRIZ parameter IDs that should be preserved
    """
    return await get_ips_by_matrix(improving_params, preserving_params)


@mcp.tool()
async def find_matching_parameter(query: str, limit: int = 1) -> str:
    """Search for matching TRIZ parameters using semantic similarity.

    Finds the most relevant TRIZ parameters based on semantic similarity
    to the provided query text.

    Args:
        query: Search query describing the parameter
        limit: Maximum number of results to return (1-39, default: 1)
    """
    return await search_parameter(query, limit)


@mcp.tool()
async def find_matching_principle(query: str, limit: int = 1) -> str:
    """Search for Inventive Principles using semantic similarity.

    Finds the most relevant Inventive Principles based on semantic similarity
    to the provided problem description or query. Use this to assign the closest
    Inventive Principle based on a problem description.

    Args:
        query: Problem description or search query
        limit: Maximum number of results to return (1-40, default: 1)
    """
    return await search_principle(query, limit)


@mcp.tool()
async def get_random_inventive_principles(limit: int = 5) -> str:
    """Get random Inventive Principles for inspiration.

    Retrieves a random selection of Inventive Principles, useful for
    brainstorming and creative problem-solving.

    Args:
        limit: Number of random principles to return (1-40, default: 5)
    """
    return await get_random_principles(limit)
