"""add role to users

Revision ID: 1cdd4502dff8
Revises:
Create Date: 2026-09-04 19:00:54.787532

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "1cdd4502dff8"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "users",
        sa.Column(
            "role",
            sa.String(length=50),
            nullable=False,
            server_default="customer"
        )
    )

    op.alter_column(
        "users",
        "role",
        server_default=None
    )


def downgrade():
    op.drop_column("users", "role")