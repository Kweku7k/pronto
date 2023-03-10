"""empty message

Revision ID: 13b0f3c9cdd6
Revises: 9fe079361871
Create Date: 2023-02-05 13:03:00.674809

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '13b0f3c9cdd6'
down_revision = '9fe079361871'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('room', schema=None) as batch_op:
        batch_op.add_column(sa.Column('bedsAvailable', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('tier', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('room', schema=None) as batch_op:
        batch_op.drop_column('tier')
        batch_op.drop_column('bedsAvailable')

    # ### end Alembic commands ###
