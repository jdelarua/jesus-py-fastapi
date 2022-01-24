"""Add Published , Rating & created_at columns to posts table

Revision ID: 21637d647cc2
Revises: f29c43f42780
Create Date: 2022-01-23 12:00:09.552120

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '21637d647cc2'
#Below is the revision id for the previos revision in my case f29c43f42780_create_database_schema.py
down_revision = 'f29c43f42780'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('published', sa.Boolean(), server_default=sa.text('false'), nullable=False))
    op.add_column('posts',sa.Column('rating', sa.Integer(), server_default=sa.text('0'), nullable=False))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'rating')
    op.drop_column('posts', 'created_at')
    pass
