"""encrypt smbhash

Revision ID: 434ea5397cd3
Revises: 22230265ab30
Create Date: 2020-05-13 12:08:48.976300+00:00

"""
from alembic import op
import sqlalchemy as sa

from middlewared.plugins.pwenc import encrypt


# revision identifiers, used by Alembic.
revision = '434ea5397cd3'
down_revision = '22230265ab30'
branch_labels = None
depends_on = None


def upgrade():
    table = "account_bsdusers"
    conn = op.get_bind()
    for row in conn.execute(f"SELECT id, bsdusr_smbhash FROM {table}").fetchall():
        encrypted_hash = encrypt(row["bsdusr_smbhash"])
        conn.execute(f"UPDATE {table} SET bsdusr_smbhash=? WHERE id = {row['id']}", encrypted_hash)


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###