"""add ends_at column to events

Revision ID: 6e73b57f59bf
Revises: 5e7ed52ad806
Create Date: 2025-12-16 21:49:08.862998

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6e73b57f59bf'
down_revision: Union[str, Sequence[str], None] = '5e7ed52ad806'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('events', sa.Column('ends_at', sa.DateTime(), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('events', 'ends_at')
