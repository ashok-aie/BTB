"""Make user_activities.id autoincrement

Revision ID: c24227c7bc74
Revises: 7f1698497b60
Create Date: 2025-10-26 04:44:14.628884

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c24227c7bc74'
down_revision: Union[str, Sequence[str], None] = '7f1698497b60'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
