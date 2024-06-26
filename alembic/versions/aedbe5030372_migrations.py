"""Migrations

Revision ID: aedbe5030372
Revises: 727f29c9e2d7
Create Date: 2024-06-28 15:14:43.622967

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "aedbe5030372"
down_revision = "727f29c9e2d7"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "balances",
        "user_id",
        existing_type=sa.INTEGER(),
        type_=sa.BIGINT(),
        existing_nullable=False,
    )
    op.create_unique_constraint(None, "balances", ["id"])
    op.create_foreign_key(None, "balances", "users", ["user_id"], ["id"])
    op.create_unique_constraint(None, "users", ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "users", type_="unique")
    op.drop_constraint(None, "balances", type_="foreignkey")
    op.drop_constraint(None, "balances", type_="unique")
    op.alter_column(
        "balances",
        "user_id",
        existing_type=sa.BIGINT(),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
    # ### end Alembic commands ###
