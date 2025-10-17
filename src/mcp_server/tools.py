"""MCP tools implementation with dynamic loading."""

import logging
from typing import Any

from src.core.database import async_session_factory
from src.core.services.tool_service import ToolService
from src.mcp_server.server import mcp


logger = logging.getLogger(__name__)


async def load_and_register_tools() -> None:
    """Load active tools from database and register them with MCP server."""
    async with async_session_factory() as session:
        service = ToolService(session)
        tools = await service.list_tools(active_only=True)

        logger.info(f"Loading {len(tools)} active tools from database")

        for tool in tools:
            register_tool(tool.name, tool.description, tool.parameters_schema)
            logger.info(f"Registered tool: {tool.name}")


def register_tool(name: str, description: str, parameters_schema: dict[str, Any]) -> None:  # noqa: ARG001
    """Register a tool with the MCP server.

    Args:
        name: Tool name
        description: Tool description
        parameters_schema: JSON schema for parameters (used by FastMCP internally)
    """

    @mcp.tool(name=name, description=description)  # type: ignore[misc]
    async def dynamic_tool(**kwargs: Any) -> dict[str, Any]:
        """Dynamically created tool that executes via service layer."""
        async with async_session_factory() as session:
            service = ToolService(session)
            try:
                result = await service.execute_tool(name, kwargs)
                return result
            except Exception as e:
                logger.error(f"Tool '{name}' execution failed: {e}")
                return {
                    "success": False,
                    "error": str(e),
                }

    # Set the function name for better debugging
    dynamic_tool.__name__ = name
