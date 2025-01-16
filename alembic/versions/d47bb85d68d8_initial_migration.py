"""Initial migration

Revision ID: d47bb85d68d8
Revises: 
Create Date: 2025-01-15 16:32:53.984602

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd47bb85d68d8'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Create pokemon table
    op.create_table(
        'pokemon',
        sa.Column('pokemon_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('height', sa.Integer, nullable=False),
        sa.Column('weight', sa.Integer, nullable=False),
        sa.Column('xp', sa.Integer, nullable=False),
        sa.Column('image_url', sa.String, nullable=False),
        sa.Column('pokemon_url', sa.String, nullable=False),
    )

    # Create abilities table
    op.create_table(
        'abilities',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('pokemon_id', sa.Integer, sa.ForeignKey('pokemon.pokemon_id'), nullable=False),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('is_hidden', sa.Boolean, nullable=False),
    )

    # Create stats table
    op.create_table(
        'stats',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('pokemon_id', sa.Integer, sa.ForeignKey('pokemon.pokemon_id'), nullable=False),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('base_stat', sa.String, nullable=False),
    )

    # Create types table
    op.create_table(
        'types',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('pokemon_id', sa.Integer, sa.ForeignKey('pokemon.pokemon_id'), nullable=False),
        sa.Column('name', sa.String, nullable=False),
    )


def downgrade():
    # Drop types table
    op.drop_table('types')

    # Drop stats table
    op.drop_table('stats')

    # Drop abilities table
    op.drop_table('abilities')

    # Drop pokemon table
    op.drop_table('pokemon')