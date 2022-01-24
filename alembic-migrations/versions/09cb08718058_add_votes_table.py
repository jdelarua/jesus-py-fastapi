"""Add Votes Table

Revision ID: 09cb08718058
Revises: e629bfd09a89
Create Date: 2022-01-23 15:40:36.533381

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '09cb08718058'
down_revision = 'e629bfd09a89'
branch_labels = None
depends_on = None


def upgrade():
     #Create Table votes
     op.create_table('votes',
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('post_id', sa.Integer(), nullable=False)
                    )
     #Add  composite PK
     op.create_primary_key('votes_comp_pkey',
                           'votes',
                           ['user_id','post_id']    
                          )   
     #Add user_id FK
     op.create_foreign_key('votes_user_id_FK', 
                          source_table='votes', 
                          referent_table='users',
                          local_cols=['user_id'], 
                          remote_cols=['id'],
                          ondelete="CASCADE")                                      
     #Add post_id FK
     op.create_foreign_key('votes_post_id_FK', 
                          source_table='votes', 
                          referent_table='posts',
                          local_cols=['post_id'], 
                          remote_cols=['id'],
                          ondelete="CASCADE")                                      
     pass

def downgrade():
    op.drop_table('votes') 
    pass
