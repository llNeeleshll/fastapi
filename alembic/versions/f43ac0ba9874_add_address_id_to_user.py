"""add address_id to user

Revision ID: f43ac0ba9874
Revises: 4e47e7f8f686
Create Date: 2022-08-26 17:28:05.499593

"""
from tkinter import CASCADE
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f43ac0ba9874'
down_revision = '4e47e7f8f686'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('address_id', sa.Integer(), nullable=True))
    op.create_foreign_key('address_users_fk', source_table="users", 
        referent_table="address", local_cols=['address_id'], remote_cols=['id'],
        ondelete="CASCADE")


def downgrade() -> None:
    op.drop_constraint('address_users_fk',table_name="users")
    op.drop_column('users','phone_number')
