"""mission cat_id nullable

Revision ID: bd3d8b70f20e
Revises: 02eaecf19078
Create Date: 2024-12-12 17:53:41.628312

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bd3d8b70f20e'
down_revision: Union[str, None] = '02eaecf19078'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Alter the column to be nullable
    with op.batch_alter_table('missions') as batch_op:
        batch_op.alter_column('cat_id', nullable=True)

def downgrade():
    # Revert the column to be non-nullable
    with op.batch_alter_table('missions') as batch_op:
        batch_op.alter_column('cat_id', nullable=False)