"""Add living space type to Room model

Revision ID: 73f6a69f7225
Revises: eb55d30ab582
Create Date: 2025-02-08 16:06:00.740355

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '73f6a69f7225'
down_revision = 'eb55d30ab582'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('room', schema=None) as batch_op:
        batch_op.add_column(sa.Column('living_space_type', sa.String(length=50), server_default='Boarding House', nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('room', schema=None) as batch_op:
        batch_op.drop_column('living_space_type')

    # ### end Alembic commands ###
