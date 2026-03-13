"""baseline

Revision ID: 20260221_143300
Revises: 
Create Date: 2026-02-21

"""

from alembic import op
import sqlalchemy as sa


revision = "20260221_143300"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "customers",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("phone_number", sa.String(), nullable=False, index=True),
        sa.Column("vehicle_number", sa.String(), nullable=True, index=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
        ),
    )

    op.create_table(
        "technicians",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("phone_number", sa.String(), nullable=True),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true")),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
        ),
    )

    op.create_table(
        "particulars",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("type", sa.String(), nullable=False),
        sa.Column("unit_price", sa.Float(), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true")),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
        ),
    )

    # bills is created WITHOUT technician_id — added in the next migration
    op.create_table(
        "bills",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("bill_number", sa.Integer(), nullable=False, unique=True),
        sa.Column(
            "customer_id",
            sa.Integer(),
            sa.ForeignKey("customers.id"),
            nullable=False,
        ),
        sa.Column("subtotal", sa.Float(), server_default=sa.text("0")),
        sa.Column("total", sa.Float(), server_default=sa.text("0")),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
        ),
    )

    op.create_table(
        "bill_items",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "bill_id",
            sa.Integer(),
            sa.ForeignKey("bills.id"),
            nullable=False,
        ),
        sa.Column(
            "particular_id",
            sa.Integer(),
            sa.ForeignKey("particulars.id"),
            nullable=False,
        ),
        sa.Column("quantity", sa.Float(), server_default=sa.text("1")),
        sa.Column("unit_price", sa.Float(), nullable=False),
        sa.Column("line_total", sa.Float(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("bill_items")
    op.drop_table("bills")
    op.drop_table("particulars")
    op.drop_table("technicians")
    op.drop_table("customers")
