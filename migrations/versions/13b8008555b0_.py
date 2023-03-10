"""empty message

Revision ID: 13b8008555b0
Revises: 2f925417440f
Create Date: 2023-02-04 18:13:44.440494

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '13b8008555b0'
down_revision = '2f925417440f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('room_location',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('floor', sa.String(), nullable=True),
    sa.Column('location', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('room_location')
    # ### end Alembic commands ###
