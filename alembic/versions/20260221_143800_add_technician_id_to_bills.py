"""add technician_id to bills

Revision ID: 20260221_143800
Revises: 20260221_143300
Create Date: 2026-02-21

"""

from alembic import op
import sqlalchemy as sa


revision = "20260221_143800"
down_revision = "20260221_143300"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("bills", sa.Column("technician_id", sa.Integer(), nullable=True))
    op.create_foreign_key(
        "bills_technician_id_fkey",
        "bills",
        "technicians",
        ["technician_id"],
        ["id"],
    )
    op.create_index("ix_bills_technician_id", "bills", ["technician_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_bills_technician_id", table_name="bills")
    op.drop_constraint("bills_technician_id_fkey", "bills", type_="foreignkey")
    op.drop_column("bills", "technician_id")
