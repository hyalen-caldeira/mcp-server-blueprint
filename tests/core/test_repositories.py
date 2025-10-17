"""Tests for repository layer."""

from typing import Any

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.repositories.tool_repository import ToolRepository


@pytest.mark.asyncio
async def test_create_tool(test_session: AsyncSession, sample_tool_data: dict[str, Any]) -> None:
    """Test creating a tool."""
    repository = ToolRepository(test_session)
    tool = await repository.create(sample_tool_data)

    assert tool.id is not None
    assert tool.name == sample_tool_data["name"]
    assert tool.description == sample_tool_data["description"]
    assert tool.handler_name == sample_tool_data["handler_name"]
    assert tool.is_active is True


@pytest.mark.asyncio
async def test_get_by_id(test_session: AsyncSession, sample_tool_data: dict[str, Any]) -> None:
    """Test getting a tool by ID."""
    repository = ToolRepository(test_session)
    created_tool = await repository.create(sample_tool_data)

    tool = await repository.get_by_id(created_tool.id)

    assert tool is not None
    assert tool.id == created_tool.id
    assert tool.name == sample_tool_data["name"]


@pytest.mark.asyncio
async def test_get_by_id_not_found(test_session: AsyncSession) -> None:
    """Test getting a non-existent tool."""
    repository = ToolRepository(test_session)
    tool = await repository.get_by_id(999)

    assert tool is None


@pytest.mark.asyncio
async def test_get_by_name(test_session: AsyncSession, sample_tool_data: dict[str, Any]) -> None:
    """Test getting a tool by name."""
    repository = ToolRepository(test_session)
    await repository.create(sample_tool_data)

    tool = await repository.get_by_name(sample_tool_data["name"])

    assert tool is not None
    assert tool.name == sample_tool_data["name"]


@pytest.mark.asyncio
async def test_get_by_name_not_found(test_session: AsyncSession) -> None:
    """Test getting a non-existent tool by name."""
    repository = ToolRepository(test_session)
    tool = await repository.get_by_name("nonexistent_tool")

    assert tool is None


@pytest.mark.asyncio
async def test_list_active(test_session: AsyncSession, sample_tool_data: dict[str, Any]) -> None:
    """Test listing active tools."""
    repository = ToolRepository(test_session)

    # Create active tool
    await repository.create(sample_tool_data)

    # Create inactive tool
    inactive_data = sample_tool_data.copy()
    inactive_data["name"] = "inactive_tool"
    inactive_data["is_active"] = False
    await repository.create(inactive_data)

    # List active tools
    active_tools = await repository.list_active()

    assert len(active_tools) == 1
    assert active_tools[0].name == sample_tool_data["name"]
    assert active_tools[0].is_active is True


@pytest.mark.asyncio
async def test_update_tool(test_session: AsyncSession, sample_tool_data: dict[str, Any]) -> None:
    """Test updating a tool."""
    repository = ToolRepository(test_session)
    tool = await repository.create(sample_tool_data)

    updated_tool = await repository.update(tool.id, {"description": "Updated description"})

    assert updated_tool is not None
    assert updated_tool.id == tool.id
    assert updated_tool.description == "Updated description"


@pytest.mark.asyncio
async def test_soft_delete(test_session: AsyncSession, sample_tool_data: dict[str, Any]) -> None:
    """Test soft deleting a tool."""
    repository = ToolRepository(test_session)
    tool = await repository.create(sample_tool_data)

    success = await repository.soft_delete(tool.id)

    assert success is True

    # Verify tool is inactive
    tool = await repository.get_by_id(tool.id)
    assert tool is not None
    assert tool.is_active is False


@pytest.mark.asyncio
async def test_activate(test_session: AsyncSession, sample_tool_data: dict[str, Any]) -> None:
    """Test activating a tool."""
    repository = ToolRepository(test_session)
    sample_tool_data["is_active"] = False
    tool = await repository.create(sample_tool_data)

    success = await repository.activate(tool.id)

    assert success is True

    # Verify tool is active
    tool = await repository.get_by_id(tool.id)
    assert tool is not None
    assert tool.is_active is True
