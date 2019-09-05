"""Add FlowRun class, updated/created columns

Revision ID: 7c75fab490c8
Revises: c4605236abf7
Create Date: 2019-08-21 12:18:27.723111

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7c75fab490c8'
down_revision = 'c4605236abf7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('flow', sa.Column('created', sa.DateTime(), server_default=sa.text('now()'), nullable=True))
    op.add_column('flow', sa.Column('key', sa.String(length=64), nullable=False))
    op.add_column('flow', sa.Column('updated', sa.DateTime(), nullable=True))
    op.drop_constraint('flow_name_key', 'flow', type_='unique')
    op.create_unique_constraint(None, 'flow', ['key'])
    op.drop_column('flow', 'name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('flow', sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'flow', type_='unique')
    op.create_unique_constraint('flow_name_key', 'flow', ['name'])
    op.drop_column('flow', 'updated')
    op.drop_column('flow', 'key')
    op.drop_column('flow', 'created')
    # ### end Alembic commands ###
