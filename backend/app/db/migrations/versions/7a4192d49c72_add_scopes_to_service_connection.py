"""add scopes to service_connection

Revision ID: 7a4192d49c72
Revises: 69789f1cfee8
Create Date: 2026-01-05 15:30:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7a4192d49c72"
down_revision: Union[str, Sequence[str], None] = "69789f1cfee8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("service_connection", sa.Column("scopes", sa.JSON(), nullable=True))


def downgrade() -> None:
    op.drop_column("service_connection", "scopes")
