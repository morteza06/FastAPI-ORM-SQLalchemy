"""add foreign-key to posts table

Revision ID: 272809280128
Revises: 333895d52193
Create Date: 2022-04-05 23:27:36.852060

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '272809280128'
down_revision = '333895d52193'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users",
                          local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('posts_users.fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
