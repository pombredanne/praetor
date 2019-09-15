"""Add map_index to TaskRun

Revision ID: 6985feb1b47d
Revises: 03377d1c7c67
Create Date: 2019-09-14 15:28:16.960467

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "6985feb1b47d"
down_revision = "03377d1c7c67"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("task_run", sa.Column("map_index", sa.Integer(), nullable=True))


def downgrade():
    op.drop_column("task_run", "map_index")
