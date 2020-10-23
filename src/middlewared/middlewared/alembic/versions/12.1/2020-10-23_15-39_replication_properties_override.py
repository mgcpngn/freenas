"""Replication properties override

Revision ID: ce614715260a
Revises: 3376b7a70d17
Create Date: 2020-10-23 15:39:42.818433+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ce614715260a'
down_revision = '3376b7a70d17'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('storage_replication', schema=None) as batch_op:
        batch_op.add_column(sa.Column('repl_properties_override', sa.TEXT(), nullable=True))

    op.execute("UPDATE storage_replication SET repl_properties_override = '{}'")

    with op.batch_alter_table('storage_replication', schema=None) as batch_op:
        batch_op.alter_column('repl_properties_override',
               existing_type=sa.TEXT(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('storage_replication', schema=None) as batch_op:
        batch_op.drop_column('repl_properties_override')

    # ### end Alembic commands ###
