"""Tool repository for database operations."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models.tool import Tool
from src.core.repositories.base import BaseRepository


class ToolRepository(BaseRepository[Tool]):
    """Repository for Tool model with specific operations."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize tool repository.

        Args:
            session: Database session
        """
        super().__init__(Tool, session)

    async def get_by_name(self, name: str) -> Tool | None:
        """Get a tool by name.

        Args:
            name: Tool name

        Returns:
            Tool instance or None if not found
        """
        result = await self.session.execute(select(Tool).where(Tool.name == name))
        return result.scalar_one_or_none()  # type: ignore[no-any-return]

    async def list_active(self) -> list[Tool]:
        """List all active tools.

        Returns:
            List of active tool instances
        """
        result = await self.session.execute(select(Tool).where(Tool.is_active == True))  # noqa: E712
        return list(result.scalars().all())

    async def soft_delete(self, id_: int) -> bool:
        """Soft delete a tool by setting is_active to False.

        Args:
            id_: Tool ID

        Returns:
            True if deactivated, False if not found
        """
        tool = await self.get_by_id(id_)
        if not tool:
            return False

        tool.is_active = False
        await self.session.commit()
        return True

    async def activate(self, id_: int) -> bool:
        """Activate a tool by setting is_active to True.

        Args:
            id_: Tool ID

        Returns:
            True if activated, False if not found
        """
        tool = await self.get_by_id(id_)
        if not tool:
            return False

        tool.is_active = True
        await self.session.commit()
        return True
