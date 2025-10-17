"""Core business logic module.

This module contains transport-agnostic business logic that can be reused
across both MCP and REST API interfaces.

All business logic should be implemented here to maintain a single source of truth.
"""

from src.core.config import Settings, get_settings
from src.core.database import Base, get_session, init_db
from src.core.exceptions import (
    ApplicationError,
    DatabaseError,
    NotFoundError,
    ToolHandlerError,
    ToolHandlerNotFoundError,
    ToolNotFoundError,
    ValidationError,
)


__all__: list[str] = [
    "Settings",
    "get_settings",
    "Base",
    "get_session",
    "init_db",
    "ApplicationError",
    "ValidationError",
    "NotFoundError",
    "ToolNotFoundError",
    "ToolHandlerError",
    "ToolHandlerNotFoundError",
    "DatabaseError",
]
