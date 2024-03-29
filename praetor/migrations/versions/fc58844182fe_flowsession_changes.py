"""FlowSession changes

Revision ID: fc58844182fe
Revises: 1ae9d395f1ae
Create Date: 2019-08-29 19:55:07.933822

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fc58844182fe'
down_revision = '1ae9d395f1ae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('index', sa.Integer(), nullable=False))
    op.drop_constraint('task_name_flow_id_key', 'task', type_='unique')
    op.create_unique_constraint(None, 'task', ['name', 'flow_session_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'task', type_='unique')
    op.create_unique_constraint('task_name_flow_id_key', 'task', ['name', 'flow_id'])
    op.drop_column('task', 'index')
    # ### end Alembic commands ###
