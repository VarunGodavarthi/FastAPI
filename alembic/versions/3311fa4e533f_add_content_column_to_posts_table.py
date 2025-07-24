"""add content column to posts table

Revision ID: 3311fa4e533f
Revises: 82bf84f146a6
Create Date: 2025-07-22 20:43:50.265276

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3311fa4e533f'
down_revision: Union[str, Sequence[str], None] = '82bf84f146a6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content',sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
