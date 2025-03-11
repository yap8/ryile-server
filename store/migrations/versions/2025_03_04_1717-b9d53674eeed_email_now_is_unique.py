"""email now is unique

Revision ID: b9d53674eeed
Revises: 0deddb744127
Create Date: 2025-03-04 17:17:52.235441

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa  # noqa: F401


# revision identifiers, used by Alembic.
revision: str = "b9d53674eeed"
down_revision: Union[str, None] = "0deddb744127"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(op.f("uq_user_email"), "user", ["email"])


def downgrade() -> None:
    op.drop_constraint(op.f("uq_user_email"), "user", type_="unique")
