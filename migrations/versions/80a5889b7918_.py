"""empty message

Revision ID: 80a5889b7918
Revises: 3dafc44f175d
Create Date: 2023-02-04 17:56:15.277801

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '80a5889b7918'
down_revision = '3dafc44f175d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('room_type', schema=None) as batch_op:
        batch_op.add_column(sa.Column('range', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('basic', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('premium', sa.Float(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('room_type', schema=None) as batch_op:
        batch_op.drop_column('premium')
        batch_op.drop_column('basic')
        batch_op.drop_column('range')

    # ### end Alembic commands ###
