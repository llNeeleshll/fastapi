"""create address table

Revision ID: 4e47e7f8f686
Revises: a154ba15773f
Create Date: 2022-08-26 17:21:45.982912

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4e47e7f8f686'
down_revision = 'a154ba15773f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("address",
    sa.Column("id", sa.Integer(), nullable=False, primary_key = True),
    sa.Column("address1", sa.String(), nullable=False),
    sa.Column("address2", sa.String(), nullable=False),
    sa.Column("city", sa.String(), nullable=False),
    sa.Column("state", sa.String(), nullable=False),
    sa.Column("country", sa.String(), nullable=False),
    sa.Column("post_code", sa.String(), nullable=False)
    )


def downgrade() -> None:
    op.drop_table('address')
