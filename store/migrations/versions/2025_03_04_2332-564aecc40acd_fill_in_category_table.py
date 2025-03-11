"""fill in category table

Revision ID: 564aecc40acd
Revises: 28a92c16838b
Create Date: 2025-03-04 23:32:44.648121

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "564aecc40acd"
down_revision: Union[str, None] = "28a92c16838b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    insert into category(name_ru, name_en)
    values
        ('одежда', 'clothes'),
        ('украшения', 'jewellery'),
        ('новинки', 'new')
    """)


def downgrade() -> None:
    op.execute("""
    delete from category
    where name_en in ('clothes', 'jewellery', 'new')
    """)
