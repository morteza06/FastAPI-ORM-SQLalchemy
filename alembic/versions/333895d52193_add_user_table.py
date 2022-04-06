"""add user table

Revision ID: 333895d52193
Revises: 4aa10972e1e6
Create Date: 2022-04-05 23:10:18.670403

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '333895d52193'
down_revision = '4aa10972e1e6'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('create_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'),nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade():
    op.drop_table('users')
    pass
