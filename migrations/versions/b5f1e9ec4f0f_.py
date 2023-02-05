"""empty message

Revision ID: b5f1e9ec4f0f
Revises: 13b0f3c9cdd6
Create Date: 2023-02-05 13:28:10.004212

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b5f1e9ec4f0f'
down_revision = '13b0f3c9cdd6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('occupant', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('studentId',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('course',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('level',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('room',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('block',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('roomnumber',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('roomid',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('paid',
               existing_type=sa.VARCHAR(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('occupant', schema=None) as batch_op:
        batch_op.alter_column('paid',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('roomid',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('roomnumber',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('block',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('room',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('level',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('course',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('studentId',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(),
               nullable=False)

    # ### end Alembic commands ###
