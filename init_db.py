import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.sql import text

from config import POSTGRES_URL, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB


async def init_db():
    engine = create_async_engine(POSTGRES_URL)

    async with engine.begin() as conn:
        result = await conn.execute(
            text("SELECT 1 FROM pg_database WHERE datname=:db_name"),
            {"db_name": POSTGRES_DB},
        )
        if not result.scalar():
            await conn.execute(text(f"CREATE DATABASE {POSTGRES_DB}"))

    db_engine = create_async_engine(POSTGRES_URL)

    async with db_engine.begin() as conn:
        await conn.run_sync(
            lambda sync_conn: alembic.command.upgrade(
                alembic.config.Config("alembic.ini"), "head"
            )
        )

    await engine.dispose()
    await db_engine.dispose()


if __name__ == "__main__":
    import alembic.config
    import alembic.command

    asyncio.run(init_db())
