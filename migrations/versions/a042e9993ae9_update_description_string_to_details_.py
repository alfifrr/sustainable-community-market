"""update: description(string) to details(json) in transaction_history model

Revision ID: a042e9993ae9
Revises: 73af3fb540e4
Create Date: 2025-04-18 13:23:27.136092

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a042e9993ae9'
down_revision = '73af3fb540e4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('transaction_history', schema=None) as batch_op:
        batch_op.add_column(sa.Column('details', sa.JSON(), nullable=True))
        batch_op.drop_column('description')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('transaction_history', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', sa.VARCHAR(length=255), nullable=True))
        batch_op.drop_column('details')

    # ### end Alembic commands ###
