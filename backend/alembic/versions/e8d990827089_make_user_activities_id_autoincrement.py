"""Make user_activities.id autoincrement

Revision ID: e8d990827089
Revises: fe1b0efe3141
Create Date: 2025-10-26 04:37:12.347114

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e8d990827089'
down_revision: Union[str, Sequence[str], None] = 'fe1b0efe3141'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
