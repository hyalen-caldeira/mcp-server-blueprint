"""Initialize database - create tables."""

import asyncio
import logging

from src.core.database import init_db


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main() -> None:
    """Initialize database tables."""
    logger.info("Initializing database...")
    await init_db()
    logger.info("Database initialized successfully!")


if __name__ == "__main__":
    asyncio.run(main())
