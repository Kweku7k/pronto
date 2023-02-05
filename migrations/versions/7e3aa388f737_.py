"""empty message

Revision ID: 7e3aa388f737
Revises: 
Create Date: 2023-02-04 13:37:28.967663

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7e3aa388f737'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('room', schema=None) as batch_op:
        batch_op.alter_column('block',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('maxOccupancy',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('occupancyStatus',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('occupants',
               existing_type=sa.VARCHAR(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('room', schema=None) as batch_op:
        batch_op.alter_column('occupants',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('occupancyStatus',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('maxOccupancy',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('block',
               existing_type=sa.VARCHAR(),
               nullable=False)

    # ### end Alembic commands ###
