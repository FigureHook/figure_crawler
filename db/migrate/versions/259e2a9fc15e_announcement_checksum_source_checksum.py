"""announcement_checksum -> source_checksum

Revision ID: 259e2a9fc15e
Revises: a5f25e7d894f
Create Date: 2022-02-11 15:31:34.377170

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

from figure_hook.constants import SourceSite

# revision identifiers, used by Alembic.
revision = '259e2a9fc15e'
down_revision = 'a5f25e7d894f'
branch_labels = None
depends_on = None

source_site_mapping = {
    'ALTER': SourceSite.ALTER_ANNOUNCEMENT,
    'GSC': SourceSite.GSC_ANNOUNCEMENT,
    'NATIVE': SourceSite.NATIVE_ANNOUNCEMENT
}


def upgrade():
    bind = op.get_bind()
    session = sa.orm.Session(bind=bind)
    old_checksums_result = session.execute(f"SELECT * FROM announcement_checksum;")

    op.create_table('source_checksum',
                    sa.Column('source', sa.String(), nullable=False),
                    sa.Column('checksum', sa.String(), nullable=True),
                    sa.Column('checked_at', sa.DateTime(), nullable=True),
                    sa.PrimaryKeyConstraint('source')
                    )

    for row in old_checksums_result:
        source = source_site_mapping[row[0]]
        checksum_value = row[1]
        checked_at = row[2]
        session.execute(
            f"INSERT INTO source_checksum (source, checksum, checked_at) VALUES ('{source}', '{checksum_value}', '{checked_at}');"
        )

    session.commit()
    session.close()
    op.drop_table('announcement_checksum')


def downgrade():
    bind = op.get_bind()
    session = sa.orm.Session(bind=bind)
    checksums_result = session.execute(f"SELECT * FROM source_checksum;")

    op.create_table('announcement_checksum',
                    sa.Column('site', postgresql.ENUM('GSC', 'ALTER', 'NATIVE',
                              name='sourcesite'), autoincrement=False, nullable=False),
                    sa.Column('checksum', sa.VARCHAR(), autoincrement=False, nullable=True),
                    sa.Column('checked_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
                    sa.PrimaryKeyConstraint('site', name='announcement_checksum_pkey')
                    )

    for row in checksums_result:
        source = row[0]
        for k, y in source_site_mapping.items():
            if y == source:
                source = k
        checksum_value = row[1]
        checked_at = row[2]
        session.execute(
            f"INSERT INTO announcement_checksum (site, checksum, checked_at) VALUES ('{source}', '{checksum_value}', '{checked_at}');"
        )

    session.commit()
    session.close()
    op.drop_table('source_checksum')
