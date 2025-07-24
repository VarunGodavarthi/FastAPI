"""add foreign key to posts table

Revision ID: db0ed894211f
Revises: 62fd1e1b5958
Create Date: 2025-07-22 21:01:36.340827

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'db0ed894211f'
down_revision: Union[str, Sequence[str], None] = '62fd1e1b5958'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table = "posts", referent_table = "users",
                          local_cols = ['owner_id'], remote_cols = ['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name = "posts")
    op.drop_column('posts','owner_id')
    pass
