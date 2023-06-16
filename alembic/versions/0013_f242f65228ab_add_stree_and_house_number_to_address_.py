"""add stree and house number to address table.

Revision ID: f242f65228ab
Revises: 63b433c7a929
Create Date: 2023-06-03 19:10:12.616120

"""
import sqlalchemy as sa
import sqlmodel

from alembic import op

# revision identifiers, used by Alembic.
revision = "f242f65228ab"
down_revision = "63b433c7a929"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade migrations."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "address",
        sa.Column(
            "street", sqlmodel.sql.sqltypes.AutoString(length=100), nullable=False
        ),
    )
    op.add_column("address", sa.Column("house_number", sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade migrations."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("address", "house_number")
    op.drop_column("address", "street")
    # ### end Alembic commands ###