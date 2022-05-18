"""initial

Revision ID: 8791efc972fe
Revises: 
Create Date: 2022-05-18 22:54:08.243478

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8791efc972fe'
down_revision = None
branch_labels = ('default',)
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('operation_type', sa.String(length=120), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('product_name', sa.String(length=120), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('history')
    # ### end Alembic commands ###