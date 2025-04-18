"""update: nullable product_id in item_transaction to allow product listing deletion (orphan)

Revision ID: fa445309a086
Revises: f746a23c8085
Create Date: 2025-04-18 22:30:59.206259

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fa445309a086'
down_revision = 'f746a23c8085'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('item_transactions', schema=None) as batch_op:
        batch_op.alter_column('product_id',
                              existing_type=sa.INTEGER(),
                              nullable=True)
        # batch_op.drop_constraint(None, type_='foreignkey')
        # batch_op.create_foreign_key(None, 'products', ['product_id'], ['id'], ondelete='SET NULL')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('item_transactions', schema=None) as batch_op:
        # batch_op.drop_constraint(None, type_='foreignkey')
        # batch_op.create_foreign_key(None, 'products', ['product_id'], ['id'])
        batch_op.alter_column('product_id',
                              existing_type=sa.INTEGER(),
                              nullable=False)

    # ### end Alembic commands ###
