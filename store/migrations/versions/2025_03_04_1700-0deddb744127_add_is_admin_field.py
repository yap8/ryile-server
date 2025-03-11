"""add is_admin_field

Revision ID: 0deddb744127
Revises: dc2475e2891b
Create Date: 2025-03-04 17:00:05.080975

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0deddb744127"
down_revision: Union[str, None] = "dc2475e2891b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "user",
        sa.Column("is_admin", sa.Boolean(), server_default="false", nullable=False),
    )


def downgrade() -> None:
    op.drop_column("user", "is_admin")
