"""Custom exceptions for the application."""


class ApplicationError(Exception):
    """Base exception for all application errors."""

    pass


class ValidationError(ApplicationError):
    """Raised when validation fails."""

    pass


class NotFoundError(ApplicationError):
    """Raised when a resource is not found."""

    pass


class ToolNotFoundError(NotFoundError):
    """Raised when a tool is not found."""

    pass


class ToolHandlerError(ApplicationError):
    """Raised when a tool handler fails to execute."""

    pass


class ToolHandlerNotFoundError(ApplicationError):
    """Raised when a tool handler is not registered."""

    pass


class DatabaseError(ApplicationError):
    """Raised when a database operation fails."""

    pass
