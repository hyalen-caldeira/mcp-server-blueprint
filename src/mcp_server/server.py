"""MCP Server setup and configuration."""

import logging

from fastmcp import FastMCP

from src.core.config import get_settings


settings = get_settings()

# Configure logging
logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP(
    name=settings.app_name,
    version=settings.app_version,
)

logger.info(f"MCP Server '{settings.app_name}' v{settings.app_version} initialized")
