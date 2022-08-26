"""create phone number for user table

Revision ID: a154ba15773f
Revises: 
Create Date: 2022-08-26 17:05:17.069500

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a154ba15773f'
down_revision = None
branch_labels = None
depends_on = None

## alembic upgrade a154ba15773f
def upgrade() -> None:
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))

## alembic downgrade -1
def downgrade() -> None:
    op.drop_column('users','phone_number')
