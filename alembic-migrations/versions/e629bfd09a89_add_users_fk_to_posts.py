"""Add users FK to posts

Revision ID: e629bfd09a89
Revises: 4d2c1ecc7eda
Create Date: 2022-01-23 14:52:30.382718

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e629bfd09a89'
down_revision = '4d2c1ecc7eda'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_owner_id_FK', 
                          source_table='posts', 
                          referent_table='users',
                          local_cols=['owner_id'], 
                          remote_cols=['id'],
                          ondelete="CASCADE")


def downgrade():
    op.drop_constraint('post_owner_id_FK', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
