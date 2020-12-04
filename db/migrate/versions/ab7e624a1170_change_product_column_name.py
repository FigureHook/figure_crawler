"""Change product column name

Revision ID: ab7e624a1170
Revises: 8302a5abe06e
Create Date: 2020-12-04 04:56:52.684586

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab7e624a1170'
down_revision = '8302a5abe06e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('id_by_official', sa.String(), nullable=True))
    op.drop_column('product', 'maker_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('maker_id', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('product', 'id_by_official')
    # ### end Alembic commands ###
