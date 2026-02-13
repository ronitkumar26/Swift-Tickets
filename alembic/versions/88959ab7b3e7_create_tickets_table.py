"""create tickets table

Revision ID: 88959ab7b3e7
Revises: 6cdd5183527e
Create Date: 2026-02-13 11:12:02.208726

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '88959ab7b3e7'
down_revision: Union[str, Sequence[str], None] = '6cdd5183527e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "tickets",
        sa.Column("id", sa.Integer(), nullable=False),

        sa.Column("title", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),

        sa.Column(
            "status",
            sa.Enum("OPEN", "IN_PROGRESS", "RESOLVED", "CLOSED", name="ticketstatus"),
            nullable=False,
            server_default="OPEN",
        ),

        sa.Column(
            "priority",
            sa.Enum("LOW", "MEDIUM", "HIGH", name="ticketpriority"),
            nullable=False,
            server_default="MEDIUM",
        ),

        sa.Column("resolution_note", sa.Text(), nullable=True),

        sa.Column("owner_id", sa.Integer(), nullable=False),
        sa.Column("assigned_to_id", sa.Integer(), nullable=True),

        sa.ForeignKeyConstraint(["owner_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["assigned_to_id"], ["users.id"]),

        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("tickets")

    sa.Enum(name="ticketstatus").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="ticketpriority").drop(op.get_bind(), checkfirst=True)
