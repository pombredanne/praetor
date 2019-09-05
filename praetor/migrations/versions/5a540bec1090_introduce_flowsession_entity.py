"""Introduce FlowSession entity

Revision ID: 5a540bec1090
Revises: 631b0f0e272f
Create Date: 2019-08-29 18:31:59.430770

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5a540bec1090'
down_revision = '631b0f0e272f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('flow_session',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.Column('flow_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['flow_id'], ['flow.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('edge', sa.Column('flow_session_id', sa.Integer(), nullable=False))
    op.drop_constraint('edge_flow_id_fkey', 'edge', type_='foreignkey')
    op.create_foreign_key(None, 'edge', 'flow_session', ['flow_session_id'], ['id'])
    op.drop_column('edge', 'flow_id')
    op.add_column('task', sa.Column('flow_session_id', sa.Integer(), nullable=False))
    op.drop_constraint('task_name_flow_id_key', 'task', type_='unique')
    op.create_unique_constraint(None, 'task', ['name', 'flow_session_id'])
    op.drop_constraint('task_flow_id_fkey', 'task', type_='foreignkey')
    op.create_foreign_key(None, 'task', 'flow_session', ['flow_session_id'], ['id'])
    op.drop_column('task', 'flow_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('flow_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'task', type_='foreignkey')
    op.create_foreign_key('task_flow_id_fkey', 'task', 'flow', ['flow_id'], ['id'])
    op.drop_constraint(None, 'task', type_='unique')
    op.create_unique_constraint('task_name_flow_id_key', 'task', ['name', 'flow_id'])
    op.drop_column('task', 'flow_session_id')
    op.add_column('edge', sa.Column('flow_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'edge', type_='foreignkey')
    op.create_foreign_key('edge_flow_id_fkey', 'edge', 'flow', ['flow_id'], ['id'])
    op.drop_column('edge', 'flow_session_id')
    op.drop_table('flow_session')
    # ### end Alembic commands ###