"""announcement_checksum.checked_at without timezone

Revision ID: 8c60edb390f3
Revises: fb10e089a8c0
Create Date: 2021-04-28 07:59:52.609235

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '8c60edb390f3'
down_revision = 'fb10e089a8c0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("announcement_checksum", "checked_at", type_=sa.DateTime())
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("announcement_checksum", "checked_at", type_=sa.DateTime(timezone=True))
    # ### end Alembic commands ###
