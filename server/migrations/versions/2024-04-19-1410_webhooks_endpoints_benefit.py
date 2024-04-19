"""webhooks_endpoints.benefit

Revision ID: c3ef57daff7f
Revises: c4ebdc0f0482
Create Date: 2024-04-19 14:10:07.156448

"""

import sqlalchemy as sa
from alembic import op

# Polar Custom Imports
from polar.kit.extensions.sqlalchemy import PostgresUUID

# revision identifiers, used by Alembic.
revision = "c3ef57daff7f"
down_revision = "c4ebdc0f0482"
branch_labels: tuple[str] | None = None
depends_on: tuple[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "webhook_endpoints",
        sa.Column(
            "event_benefit_created",
            sa.Boolean(),
            server_default="false",
            nullable=False,
        ),
    )
    op.add_column(
        "webhook_endpoints",
        sa.Column(
            "event_benefit_updated",
            sa.Boolean(),
            server_default="false",
            nullable=False,
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("webhook_endpoints", "event_benefit_updated")
    op.drop_column("webhook_endpoints", "event_benefit_created")
    # ### end Alembic commands ###
