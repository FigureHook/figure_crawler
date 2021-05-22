"""migrate column data from prodcut_id -> product_id

Revision ID: fbc7fe956e1e
Revises: dc7042a9ce99
Create Date: 2021-05-15 08:26:53.552511

"""
import sqlalchemy as sa
from alembic import op
from figure_hook.Models.relation_table import (product_paintwork_table,
                                               product_sculptor_table)

# revision identifiers, used by Alembic.
revision = 'fbc7fe956e1e'
down_revision = 'dc7042a9ce99'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()

    tables = [
        'product_paintwork',
        'product_sculptor'
    ]

    for t in tables:
        pids = set()
        for r in bind.execute(sa.text(f"SELECT * FROM {t}")):
            pids.add(r['prodcut_id'])

        for pid in pids:
            bind.execute(
                sa.text(
                    f"UPDATE {t} SET product_id={pid} WHERE {t}.prodcut_id={pid}"
                )
            )


def downgrade():
    bind = op.get_bind()
    tables = [
        'product_paintwork',
        'product_sculptor'
    ]

    for t in tables:
        pids = set()
        for r in bind.execute(sa.text(f"SELECT * FROM {t}")):
            pids.add(r['product_id'])

        for pid in pids:
            bind.execute(
                sa.text(
                    f"UPDATE {t} SET prodcut_id={pid} WHERE {t}.product_id={pid}"
                )
            )
