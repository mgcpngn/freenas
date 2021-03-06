"""Replication target dataset encryption

Revision ID: 1a191726e5ea
Revises: a3298f120609
Create Date: 2020-10-07 19:01:33.955108+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1a191726e5ea'
down_revision = 'a3298f120609'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('storage_replication', schema=None) as batch_op:
        batch_op.add_column(sa.Column('repl_encryption', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('repl_encryption_key', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('repl_encryption_key_format', sa.String(length=120), nullable=True))
        batch_op.add_column(sa.Column('repl_encryption_key_location', sa.Text(), nullable=True))

    op.execute('UPDATE storage_replication SET repl_encryption = FALSE')

    with op.batch_alter_table('storage_replication', schema=None) as batch_op:
        batch_op.alter_column('repl_encryption',
               existing_type=sa.BOOLEAN(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('storage_replication', schema=None) as batch_op:
        batch_op.drop_column('repl_encryption_key_location')
        batch_op.drop_column('repl_encryption_key_format')
        batch_op.drop_column('repl_encryption_key')
        batch_op.drop_column('repl_encryption')

    # ### end Alembic commands ###
