"""unique together constraints.

Revision ID: 38b4e3ee8414
Revises: 48e844fd72c3
Create Date: 2023-05-13 00:13:05.189109

"""
import sqlalchemy as sa

from alembic import op

pass


# revision identifiers, used by Alembic.
revision = "38b4e3ee8414"
down_revision = "48e844fd72c3"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade migrations."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("t1")
    op.drop_index("ix_department_name", table_name="department")
    op.create_index(op.f("ix_department_name"), "department", ["name"], unique=False)
    op.create_unique_constraint(None, "department", ["division_uid", "name"])
    op.drop_index("ix_section_name", table_name="section")
    op.create_index(op.f("ix_section_name"), "section", ["name"], unique=False)
    op.create_unique_constraint(None, "section", ["department_uid", "name"])
    op.drop_index("ix_unit_name", table_name="unit")
    op.create_index(op.f("ix_unit_name"), "unit", ["name"], unique=False)
    op.create_unique_constraint(None, "unit", ["section_uid", "name"])
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade migrations."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "unit", type_="unique")  # type: ignore
    op.drop_index(op.f("ix_unit_name"), table_name="unit")
    op.create_index("ix_unit_name", "unit", ["name"], unique=False)
    op.drop_constraint(None, "section", type_="unique")  # type: ignore
    op.drop_index(op.f("ix_section_name"), table_name="section")
    op.create_index("ix_section_name", "section", ["name"], unique=False)
    op.drop_constraint(None, "department", type_="unique")  # type: ignore
    op.drop_index(op.f("ix_department_name"), table_name="department")
    op.create_index("ix_department_name", "department", ["name"], unique=False)
    op.create_table(
        "t1",
        sa.Column("name", sa.VARCHAR(length=50), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint("name", name="t1_pkey"),
    )
    # ### end Alembic commands ###
