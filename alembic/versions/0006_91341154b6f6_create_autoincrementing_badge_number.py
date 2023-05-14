"""create autoincrementing badge_number.

Revision ID: 91341154b6f6
Revises: f51f411a1f4a
Create Date: 2023-05-13 18:41:53.844838

"""
import sqlalchemy as sa

from alembic import op

pass


# revision identifiers, used by Alembic.
revision = "91341154b6f6"
down_revision = "f51f411a1f4a"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade migrations."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "employee",
        sa.Column(
            "badge_number", sa.Integer(), sa.Identity(always=True), nullable=False
        ),
    )
    op.create_index(
        op.f("ix_employee_badge_number"), "employee", ["badge_number"], unique=True
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade migrations."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_employee_badge_number"), table_name="employee")
    op.drop_column("employee", "badge_number")
    # ### end Alembic commands ###