"""Tools for interacting with the Contradictions API."""

from app.utils.http import make_request


async def formulate_tc(description: str) -> str:
    """Formulate Technical Contradiction from problem description.

    Extracts technical contradictions from a problem description, identifying
    the action parameter and two evaluation parameters (positive and negative effects).
    This is a simple extraction - use other tools to find matching TRIZ parameters
    and principles based on the effects.

    Args:
        description: Problem description text

    Returns:
        Formatted string with UUID, action parameter, and evaluation parameters
    """
    try:
        data = await make_request(
            method="POST",
            endpoint="/api/v1/contradictions/extract-tc",
            json_data={"description": description},
        )

        # Extract contradictions list from response
        contradictions = data.get("contradictions", [])

        if not contradictions or len(contradictions) == 0:
            return "No technical contradictions found in the description."

        # Format all contradictions
        results = []
        for idx, tc in enumerate(contradictions, 1):
            result = f"--- Technical Contradiction #{idx} ---\n"
            result += f"UUID: {tc['uuid']}\n\n"
            result += f"AP (Action Parameter): {tc['action']}\n"
            result += f"EP1 (Positive Effect): {tc['positive_effect']}\n"
            result += f"EP2 (Negative Effect): {tc['negative_effect']}\n"

            results.append(result)

        return "\n\n".join(results)

    except Exception as e:
        return f"Error formulating technical contradiction: {str(e)}"


async def get_ips_by_matrix(improving_params: list[int], preserving_params: list[int]) -> str:
    """Get Inventive Principles from TRIZ contradiction matrix.

    Looks up applicable Inventive Principles based on parameters to improve
    and parameters to preserve using the classical TRIZ contradiction matrix.

    Args:
        improving_params: List of TRIZ parameter IDs that should be improved
        preserving_params: List of TRIZ parameter IDs that should be preserved

    Returns:
        Formatted string with Inventive Principles and their descriptions
    """
    try:
        # Build query parameters
        payload = {"improving": improving_params, "preserving": preserving_params}

        data = await make_request(
            method="GET", endpoint="/api/v1/principles/matrix", params=payload
        )

        if not data or len(data) == 0:
            return "No Inventive Principles found for the given parameter combination."

        # Format the response
        result = f"Found {len(data)} Inventive Principle(s) from TRIZ Matrix:\n\n"

        for i, principle in enumerate(data, 1):
            result += f"{i}. {principle['name']} (ID: {principle['id']})\n"
            result += f"   {principle['description']}\n\n"

            if principle.get("rules"):
                result += "   Rules:\n"
                for rule in principle["rules"]:
                    result += f"   • {rule}\n"
                result += "\n"

            if principle.get("hints"):
                result += "   Hints:\n"
                for hint in principle["hints"]:
                    result += f"   • {hint}\n"
                result += "\n"

            if principle.get("examples"):
                result += "   Examples:\n"
                for example in principle["examples"]:
                    result += f"   • {example}\n"
                result += "\n"

        return result.strip()

    except Exception as e:
        return f"Error retrieving Inventive Principles: {str(e)}"


async def search_parameter(query: str, limit: int = 5) -> str:
    """Search for matching TRIZ parameters using semantic similarity.

    Finds the most relevant TRIZ parameters based on semantic similarity
    to the provided query text.

    Args:
        query: Search query describing the parameter
        limit: Maximum number of results to return (1-39, default: 1)

    Returns:
        Formatted string with matching parameters and similarity scores
    """
    try:
        # Validate limit
        if limit < 1 or limit > 39:
            return "Error: limit must be between 1 and 39"

        data = await make_request(
            method="GET", endpoint="/api/v1/parameters/search", params={"q": query, "limit": limit}
        )

        if not data or len(data) == 0:
            return "No matching parameters found."

        # Format the response
        result = f"Found {len(data)} matching TRIZ parameter(s):\n\n"

        for i, item in enumerate(data, 1):
            param = item["parameter"]
            score = item["score"]
            result += f"{i}. {param['name']} (ID: {param['id']}) - Similarity: {score:.2%}\n"
            result += f"   {param['description']}\n"
            if param.get("examples"):
                result += f"   Examples: {', '.join(param['examples'][:3])}\n"
            result += "\n"

        return result.strip()

    except Exception as e:
        return f"Error searching parameters: {str(e)}"


async def search_principle(query: str, limit: int = 5) -> str:
    """Search for Inventive Principles using semantic similarity.

    Finds the most relevant Inventive Principles based on semantic similarity
    to the provided problem description or query.

    Args:
        query: Problem description or search query
        limit: Maximum number of results to return (1-40, default: 1)

    Returns:
        Formatted string with matching principles and similarity scores
    """
    try:
        # Validate limit
        if limit < 1 or limit > 40:
            return "Error: limit must be between 1 and 40"

        data = await make_request(
            method="GET", endpoint="/api/v1/principles/search", params={"q": query, "limit": limit}
        )

        if not data or len(data) == 0:
            return "No matching principles found."

        # Format the response
        result = f"Found {len(data)} matching Inventive Principle(s):\n\n"

        for i, item in enumerate(data, 1):
            principle = item["principle"]
            score = item["score"]
            result += (
                f"{i}. {principle['name']} (ID: {principle['id']}) - Similarity: {score:.2%}\n"
            )
            result += f"   {principle['description']}\n\n"

            if principle.get("rules"):
                result += "   Rules:\n"
                for rule in principle["rules"]:
                    result += f"   • {rule}\n"
                result += "\n"

            if principle.get("hints"):
                result += "   Hints:\n"
                for hint in principle["hints"]:
                    result += f"   • {hint}\n"
                result += "\n"

            if principle.get("examples"):
                result += "   Examples:\n"
                for example in principle["examples"]:
                    result += f"   • {example}\n"
                result += "\n"

        return result.strip()

    except Exception as e:
        return f"Error searching principles: {str(e)}"


async def get_principle_by_id(principle_id: int) -> str:
    """Get a specific Inventive Principle by ID.

    Retrieves the full details of a specific TRIZ Inventive Principle including
    its description, rules, hints, and examples.

    Args:
        principle_id: The ID of the principle to retrieve (1-40)

    Returns:
        Formatted string with complete principle information
    """
    try:
        data = await make_request(
            method="GET",
            endpoint=f"/api/v1/principles/{principle_id}",
        )

        if not data:
            return f"Principle with ID {principle_id} not found."

        # Format the response
        result = f"Inventive Principle #{data['id']}: {data['name']}\n\n"
        result += f"{data['description']}\n\n"

        if data.get("rules"):
            result += "Rules:\n"
            for rule in data["rules"]:
                result += f"• {rule}\n"
            result += "\n"

        if data.get("hints"):
            result += "Hints:\n"
            for hint in data["hints"]:
                result += f"• {hint}\n"
            result += "\n"

        if data.get("examples"):
            result += "Examples:\n"
            for example in data["examples"]:
                result += f"• {example}\n"

        return result.strip()

    except Exception as e:
        return f"Error retrieving principle: {str(e)}"


async def get_parameter_by_id(parameter_id: int) -> str:
    """Get a specific TRIZ Parameter by ID.

    Retrieves the full details of a specific TRIZ parameter including
    its description and examples.

    Args:
        parameter_id: The ID of the parameter to retrieve (1-39)

    Returns:
        Formatted string with complete parameter information
    """
    try:
        data = await make_request(
            method="GET",
            endpoint=f"/api/v1/parameters/{parameter_id}",
        )

        if not data:
            return f"Parameter with ID {parameter_id} not found."

        # Format the response
        result = f"TRIZ Parameter #{data['id']}: {data['name']}\n\n"
        result += f"{data['description']}\n"

        if data.get("examples"):
            result += "\nExamples:\n"
            for example in data["examples"]:
                result += f"• {example}\n"

        return result.strip()

    except Exception as e:
        return f"Error retrieving parameter: {str(e)}"


async def get_random_principles(limit: int = 5) -> str:
    """Get random Inventive Principles for inspiration.

    Retrieves a random selection of Inventive Principles, useful for
    brainstorming and creative problem-solving.

    Args:
        limit: Number of random principles to return (1-40, default: 5)

    Returns:
        Formatted string with random principles and their descriptions
    """
    try:
        # Validate limit
        if limit < 1 or limit > 40:
            return "Error: limit must be between 1 and 40"

        data = await make_request(
            method="GET", endpoint="/api/v1/principles/random", params={"limit": limit}
        )

        if not data or len(data) == 0:
            return "No principles returned."

        # Format the response
        result = f"Random Inventive Principles ({len(data)}):\n\n"

        for i, principle in enumerate(data, 1):
            result += f"{i}. {principle['name']} (ID: {principle['id']})\n"
            result += f"   {principle['description']}\n\n"

            if principle.get("rules"):
                result += "   Rules:\n"
                for rule in principle["rules"][:3]:  # Limit to first 3 for brevity
                    result += f"   • {rule}\n"
                result += "\n"

            if principle.get("hints"):
                result += "   Hints:\n"
                for hint in principle["hints"][:2]:  # Limit to first 2 for brevity
                    result += f"   • {hint}\n"
                result += "\n"

            if principle.get("examples"):
                result += f"   Example: {principle['examples'][0]}\n\n"

        return result.strip()

    except Exception as e:
        return f"Error retrieving random principles: {str(e)}"
