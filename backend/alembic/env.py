import sys
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db.database import Base
from app.models import user  # import all models here
from app.models.word import Word
from app.models.word import UserWordStats 
from app.core.config import settings  # ✅ use your Pydantic Settings

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))  # add project root to path

# Alembic config
config = context.config
fileConfig(config.config_file_name)

# target metadata for autogenerate
target_metadata = Base.metadata

# ✅ Use the DATABASE_URL from your app settings
config.set_main_option("sqlalchemy.url", str(settings.DATABASE_URL))

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
