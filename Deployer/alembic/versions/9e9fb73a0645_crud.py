"""crud

Revision ID: 9e9fb73a0645
Revises: fc3d481135d4
Create Date: 2023-12-22 14:49:58.714521

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9e9fb73a0645'
down_revision: Union[str, None] = 'fc3d481135d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_table('zno')


def downgrade() -> None:
    pass
