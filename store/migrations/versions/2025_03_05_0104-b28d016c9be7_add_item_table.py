"""add item table

Revision ID: b28d016c9be7
Revises: 564aecc40acd
Create Date: 2025-03-05 01:04:06.915826

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b28d016c9be7"
down_revision: Union[str, None] = "564aecc40acd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "item",
        sa.Column("item_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("info", sa.Text(), nullable=False),
        sa.Column("price", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("category_id", sa.SmallInteger(), nullable=False),
        sa.ForeignKeyConstraint(
            ["category_id"],
            ["category.category_id"],
            name=op.f("fk_item_category_id_category"),
        ),
        sa.PrimaryKeyConstraint("item_id", name=op.f("pk_item")),
    )


def downgrade() -> None:
    op.drop_table("item")
