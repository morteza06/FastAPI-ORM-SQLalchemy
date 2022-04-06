"""add content to posts table

Revision ID: 4aa10972e1e6
Revises: 02e4d3c33dd2
Create Date: 2022-04-05 22:50:10.527910

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4aa10972e1e6'
down_revision = '02e4d3c33dd2'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
