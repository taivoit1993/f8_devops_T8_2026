"""create posts table and seed data

Revision ID: 001_create_posts_table
Revises:
Create Date: 2026-10-18 01:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '001_create_posts_table'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    posts_table = op.create_table(
        'posts',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('published', sa.Boolean(), server_default=sa.text('true'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_posts_id'), 'posts', ['id'], unique=False)

    # Seed initial data
    op.bulk_insert(
        posts_table,
        [
            {
                'title': 'Getting Started with FastAPI and Docker',
                'content': 'FastAPI is a modern, fast web framework for building APIs with Python based on standard Python type hints.',
                'published': True,
            },
            {
                'title': 'Database Migrations with Alembic',
                'content': 'Alembic is a lightweight database migration tool for usage with the SQLAlchemy Database Toolkit for Python.',
                'published': True,
            },
            {
                'title': 'Containerizing DevOps Applications',
                'content': 'Docker containers wrap up software and its dependencies into a standardized unit for software development.',
                'published': True,
            },
        ]
    )


def downgrade() -> None:
    op.drop_index(op.f('ix_posts_id'), table_name='posts')
    op.drop_table('posts')
