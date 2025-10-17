"""Entry point for MCP server in STDIO mode."""

import asyncio
import logging

from src.core.database import close_db, init_db
from src.mcp_server.server import mcp
from src.mcp_server.tools import load_and_register_tools


logger = logging.getLogger(__name__)


async def startup() -> None:
    """Startup tasks for MCP server."""
    logger.info("Starting MCP server...")

    # Initialize database
    logger.info("Initializing database...")
    await init_db()

    # Load and register tools
    logger.info("Loading tools...")
    await load_and_register_tools()

    logger.info("MCP server startup complete")


async def shutdown() -> None:
    """Shutdown tasks for MCP server."""
    logger.info("Shutting down MCP server...")
    await close_db()
    logger.info("MCP server shutdown complete")


def main() -> None:
    """Main entry point for MCP server."""
    try:
        # Run startup tasks
        asyncio.run(startup())

        # Run MCP server with STDIO transport
        logger.info("Running MCP server with STDIO transport...")
        mcp.run(transport="stdio")

    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt")
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        raise
    finally:
        # Run shutdown tasks
        asyncio.run(shutdown())


if __name__ == "__main__":
    main()
