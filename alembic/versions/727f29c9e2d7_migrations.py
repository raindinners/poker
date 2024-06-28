"""Migrations

Revision ID: 727f29c9e2d7
Revises: init
Create Date: 2024-06-28 14:13:45.738875

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "727f29c9e2d7"
down_revision = "init"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "balances",
        sa.Column("balance", sa.BIGINT(), nullable=False),
        sa.Column("bonus_increment_time_hours", sa.BIGINT(), nullable=False),
        sa.Column("last_time_claimed_bonus", sa.DateTime(), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.BIGINT(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.BIGINT(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("users")
    op.drop_table("balances")
    # ### end Alembic commands ###