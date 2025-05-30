"""Updated status to condition

Revision ID: ba02c0a34a85
Revises: a5ab4b04f9e1
Create Date: 2025-05-30 02:49:26.936436

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ba02c0a34a85'
down_revision: Union[str, None] = 'a5ab4b04f9e1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.drop_column('complaint', 'status')

def downgrade():
    op.add_column('complaint', sa.Column('status', sa.String(), nullable=True))

