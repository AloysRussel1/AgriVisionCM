"""Ajout de la relation Message-Product

Revision ID: abdca27ca632
Revises: d8f4fc288197
Create Date: 2025-02-18 23:52:01.396053

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'abdca27ca632'
down_revision = 'd8f4fc288197'
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table('messages', schema=None) as batch_op:
        batch_op.add_column(sa.Column('product_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(
            'fk_messages_product',  # Nom de la contrainte
            'products',  # Table référencée
            ['product_id'],  # Colonne locale
            ['id']  # Colonne distante référencée
        )





def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('messages', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('product_id')

    # ### end Alembic commands ###
