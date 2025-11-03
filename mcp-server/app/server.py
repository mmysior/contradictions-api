import logging

from mcp.server.fastmcp import FastMCP

from .core.config import settings
from .core.logging import setup_logging
from .tools import contradictions as contradiction_tools

setup_logging()
logger = logging.getLogger(__name__)


def main() -> None:
    """Main entry point for the TRIZ Contradictions MCP server."""
    mcp = FastMCP(
        "TRIZ Contradictions MCP Server",
        host=settings.HOST,
        port=settings.PORT,
        stateless_http=True,
    )

    # Register tools
    @mcp.tool()
    async def formulate_tc(description: str) -> str:
        """Formulate Technical Contradiction from problem description using external LLM.

        Extracts technical contradictions identifying the action parameter
        and two evaluation parameters (positive and negative effects).

        Args:
            description: Problem description text
        """
        return await contradiction_tools.formulate_tc(description)

    @mcp.tool()
    async def get_ips_by_matrix(improving_params: list[int], preserving_params: list[int]) -> str:
        """Get Inventive Principles from TRIZ Contradiction Matrix.

        Looks up applicable Inventive Principles based on parameters to improve
        and parameters to preserve using the classical TRIZ contradiction matrix.

        Args:
            improving_params: List of TRIZ parameter IDs that should be improved
            preserving_params: List of TRIZ parameter IDs that should be preserved
        """
        return await contradiction_tools.get_ips_by_matrix(improving_params, preserving_params)

    @mcp.tool()
    async def search_parameters(query: str, limit: int = 5) -> str:
        """Search for matching TRIZ parameters using Semantic Similarity.

        Finds the most relevant TRIZ parameters based on semantic similarity
        to the provided query text.

        Args:
            query: Search query describing the parameter
            limit: Maximum number of results to return (1-39, default: 5)
        """
        return await contradiction_tools.search_parameter(query, limit)

    @mcp.tool()
    async def search_principles(query: str, limit: int = 5) -> str:
        """Search for Inventive Principles using Semantic Similarity.

        Finds the most relevant Inventive Principles based on semantic similarity
        to the provided problem description or query. Use this to assign the closest
        Inventive Principle based on a problem description.

        Args:
            query: Problem description or search query
            limit: Maximum number of results to return (1-40, default: 5)
        """
        return await contradiction_tools.search_principle(query, limit)

    @mcp.tool()
    async def get_random_ips(limit: int = 5) -> str:
        """Get random Inventive Principles for inspiration.

        Retrieves a random selection of Inventive Principles, useful for
        brainstorming and creative problem-solving.

        Args:
            limit: Number of random principles to return (1-40, default: 5)
        """
        return await contradiction_tools.get_random_principles(limit)

    @mcp.tool()
    async def get_principle_by_id(principle_id: int) -> str:
        """Get a specific Inventive Principle by ID.

        Retrieves the full details of a specific TRIZ Inventive Principle including
        its description, rules, hints, and examples.

        Args:
            principle_id: The ID of the principle to retrieve (1-40)
        """
        return await contradiction_tools.get_principle_by_id(principle_id)

    @mcp.tool()
    async def get_parameter_by_id(parameter_id: int) -> str:
        """Get a specific TRIZ Parameter by ID.

        Retrieves the full details of a specific TRIZ parameter including
        its description and examples.

        Args:
            parameter_id: The ID of the parameter to retrieve (1-39)
        """
        return await contradiction_tools.get_parameter_by_id(parameter_id)

    # Run the server
    logger.info("🚀 Starting traicon MCP Server...")
    try:
        mcp.run(transport="streamable-http")
    except KeyboardInterrupt:
        logger.info("🛑 TRAICon MCP Server shutting down...")
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
    finally:
        logger.info("✅ TRAICon MCP Server exited. Thanks for using TRAICon!")


if __name__ == "__main__":
    main()
