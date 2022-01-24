"""Create Database Schema

Revision ID: f29c43f42780
Revises: 
Create Date: 2022-01-21 19:33:41.138122

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f29c43f42780'
down_revision = None
branch_labels = None
depends_on = None

'''
  __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    rating = Column(Integer, nullable=False, server_default="0")
    create_at = Column(TIMESTAMP(timezone=True), server_default=text('NOW()'), nullable=False)
    #define  posts_orm.owner_id as a FK to users_orm.id
    owner_id = Column(Integer, ForeignKey('users.id',ondelete="CASCADE"), nullable=False)
'''
# https://roman.pt/posts/sqlalchemy-and-alembic/


# Run below upgrade with 
#      > alembic upgrade f29c43f42780
#      where f29c43f42780 is revision number (see revision field on this file)
#  This will create table alembic_version on my PostgreSql database DO NOT DELETE IT.
def upgrade():
    op.create_table(
        'posts', 
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('content', sa.String(), nullable=False)
        )
                    # sa.Column('published', sa.Boolean(), default=False)
                    # sa.Column('create_at', sa.DateTime(), nullable=False, )
                    # sa.Column('owner_id', sa.sa.Integer(), sa.sa.ForeignKey('users.id'))
    pass

def downgrade():
    op.drop_table('posts')
    pass
