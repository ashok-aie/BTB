"""Make user_activities.id autoincrement

Revision ID: 7f1698497b60
Revises: e8d990827089
Create Date: 2025-10-26 04:42:37.300354

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7f1698497b60'
down_revision: Union[str, Sequence[str], None] = 'e8d990827089'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
