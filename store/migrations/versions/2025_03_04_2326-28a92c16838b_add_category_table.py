"""add category table

Revision ID: 28a92c16838b
Revises: b9d53674eeed
Create Date: 2025-03-04 23:26:09.056744

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "28a92c16838b"
down_revision: Union[str, None] = "b9d53674eeed"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "category",
        sa.Column(
            "category_id", sa.SmallInteger(), sa.Identity(always=True), nullable=False
        ),
        sa.Column("name_ru", sa.String(), nullable=False),
        sa.Column("name_en", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("category_id", name=op.f("pk_category")),
    )


def downgrade() -> None:
    op.drop_table("category")
