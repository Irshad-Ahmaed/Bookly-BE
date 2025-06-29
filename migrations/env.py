import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context
from sqlmodel import SQLModel

from src.config import config as AppConfig  # Your config with DATABASE_URL
from src.db.models import User
from src.db.models import Book

# Alembic Config
config = context.config

# DO NOT inject via .ini-style config (it misinterprets %)
# Instead, manually override the settings dictionary
configuration = config.get_section(config.config_ini_section)
configuration["sqlalchemy.url"] = AppConfig.DATABASE_URL

# Logging
if config.config_file_name:
    fileConfig(config.config_file_name)

# Metadata for 'autogenerate'
target_metadata = SQLModel.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    context.configure(
        url=AppConfig.DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations():
    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online():
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
