"""change product.resale to product.rerelease

Revision ID: 33d0a85ab52f
Revises: 77263c67479f
Create Date: 2022-03-20 02:12:19.621814

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '33d0a85ab52f'
down_revision = '77263c67479f'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('product', 'resale', new_column_name='rerelease')


def downgrade():
    op.alter_column('product', 'rerelease', new_column_name='resale')
