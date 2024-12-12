"""Initial tables

Revision ID: 02eaecf19078
Revises: 
Create Date: 2024-12-11 17:20:26.857850

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '02eaecf19078'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Create 'spy_cats' table
    op.create_table('spy_cats',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('years_of_experience', sa.Integer(), nullable=False),
        sa.Column('breed', sa.String(), nullable=False),
        sa.Column('salary', sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Create 'missions' table
    op.create_table('missions',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String()),
        sa.Column('cat_id', sa.Integer(), nullable=False),
        sa.Column('is_complete', sa.Integer(), default=0),
        sa.PrimaryKeyConstraint('id'),
    )

    # Create 'targets' table
    op.create_table('targets',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('country', sa.String(), nullable=False),
        sa.Column('notes', sa.String),
        sa.Column('complete', sa.Integer(), default=0),
        sa.Column('mission_id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade():
    op.drop_table('targets')
    op.drop_table('missions')
    op.drop_table('spy_cats')