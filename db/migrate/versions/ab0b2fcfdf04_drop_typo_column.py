"""drop typo column

Revision ID: ab0b2fcfdf04
Revises: fbc7fe956e1e
Create Date: 2021-05-15 09:00:39.368900

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab0b2fcfdf04'
down_revision = 'fbc7fe956e1e'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint('product_paintwork_prodcut_id_fkey', 'product_paintwork', type_='foreignkey')
    op.drop_constraint('product_sculptor_prodcut_id_fkey', 'product_sculptor', type_='foreignkey')
    op.drop_column('product_sculptor', 'prodcut_id')
    op.drop_column('product_paintwork', 'prodcut_id')



def downgrade():
    op.add_column('product_sculptor', sa.Column('prodcut_id', sa.Integer(), nullable=True))
    op.add_column('product_paintwork', sa.Column('prodcut_id', sa.Integer(), nullable=True))
    op.create_foreign_key('product_paintwork_prodcut_id_fkey', 'product_paintwork', 'product', ['prodcut_id'], ['id'])
    op.create_foreign_key('product_sculptor_prodcut_id_fkey', 'product_sculptor', 'product', ['prodcut_id'], ['id'])
