"""add current_km to bills

Revision ID: 20260313_000000
Revises: 20260221_143800
Create Date: 2026-03-13

"""

from alembic import op
import sqlalchemy as sa

revision = "20260313_000000"
down_revision = "20260221_143800"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("bills", sa.Column("current_km", sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column("bills", "current_km")
