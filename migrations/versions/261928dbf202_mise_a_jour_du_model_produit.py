"""Mise a jour du model Produit

Revision ID: 261928dbf202
Revises: c29d13e1849c
Create Date: 2025-02-18 17:06:05.755575

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '261928dbf202'
down_revision = 'c29d13e1849c'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.add_column(sa.Column('unit', sa.String(length=50), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.drop_column('unit')

    # ### end Alembic commands ###
