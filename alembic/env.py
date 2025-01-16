from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import app.config.config as config  # Import your config module
from app.models.models import Base  # Replace with your actual models module path

# Fetch database URL dynamically
DATABASE_URL = config.get_database_url()

if not DATABASE_URL:
    raise RuntimeError("Failed to retrieve the database URL from SSM.")

# Escape '%' for ConfigParser compatibility
escaped_database_url = DATABASE_URL.replace('%', '%%')

# Set the database URL in Alembic configuration
alembic_config = context.config
alembic_config.set_main_option("sqlalchemy.url", escaped_database_url)

# Interpret the config file for Python logging
if alembic_config.config_file_name is not None:
    fileConfig(alembic_config.config_file_name)

# Set target metadata
target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = alembic_config.get_main_option("sqlalchemy.url")
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
        alembic_config.get_section(alembic_config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
