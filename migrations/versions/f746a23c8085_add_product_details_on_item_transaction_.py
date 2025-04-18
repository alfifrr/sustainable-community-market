"""add: product_details on item_transaction for tracking product

Revision ID: f746a23c8085
Revises: a042e9993ae9
Create Date: 2025-04-18 21:33:44.304361

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f746a23c8085'
down_revision = 'a042e9993ae9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('item_transactions', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('product_details', sa.JSON(), nullable=True))

    # Update existing records with product data
    op.execute("""
        UPDATE item_transactions 
        SET product_details = json_object(
            'id', p.id,
            'name', p.name,
            'description', p.description,
            'price', p.price,
            'category_id', p.category_id,
            'expiration_date', p.expiration_date
        )
        FROM products p
        WHERE item_transactions.product_id = p.id
    """)

    # Make column non-nullable after data population
    with op.batch_alter_table('item_transactions', schema=None) as batch_op:
        batch_op.alter_column('product_details',
                              existing_type=sa.JSON(),
                              nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('item_transactions', schema=None) as batch_op:
        batch_op.drop_column('product_details')

    # ### end Alembic commands ###
