import sys
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import your app modules
from app.db.database import Base
from app.models import user  # import all models here
from app.models.word import Word, UserActivity
from app.core.config import settings  # ✅ use your Pydantic Settings


# Alembic config
config = context.config
fileConfig(config.config_file_name)

# target metadata for autogenerate
target_metadata = Base.metadata

# ✅ Use DATABASE_DIRECT_URL from environment (via settings)
db_url = str(settings.DATABASE_DIRECT_URL)
if not db_url:
    raise ValueError("DATABASE_DIRECT_URL environment variable is not set")

config.set_main_option("sqlalchemy.url", db_url)

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.QueuePool,  # Use QueuePool for Supabase pooler
        pool_size=5,
        max_overflow=10,
        pool_timeout=30,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
