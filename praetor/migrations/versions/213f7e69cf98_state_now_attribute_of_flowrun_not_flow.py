"""State now attribute of FlowRun, not Flow

Revision ID: 213f7e69cf98
Revises: ff0715e0a150
Create Date: 2019-08-22 01:28:44.993793

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '213f7e69cf98'
down_revision = 'ff0715e0a150'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('flow', 'state')
    op.add_column('flow_run', sa.Column('state', sa.String(), nullable=True))
    op.add_column('task_run', sa.Column('flow_run_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'task_run', 'flow_run', ['flow_run_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'task_run', type_='foreignkey')
    op.drop_column('task_run', 'flow_run_id')
    op.drop_column('flow_run', 'state')
    op.add_column('flow', sa.Column('state', sa.VARCHAR(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###