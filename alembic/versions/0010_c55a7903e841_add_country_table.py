"""add country table.

Revision ID: c55a7903e841
Revises: 2c0a952728b9
Create Date: 2023-06-02 13:55:49.709450

"""
import sqlalchemy as sa
import sqlmodel

from alembic import op

# revision identifiers, used by Alembic.
revision = "c55a7903e841"
down_revision = "2c0a952728b9"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade migrations."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "country",
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column(
            "date_created",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "date_modified",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "uid",
            sqlmodel.sql.sqltypes.GUID(),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("created_by", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("modified_by", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.PrimaryKeyConstraint("uid"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(op.f("ix_country_uid"), "country", ["uid"], unique=True)
    op.add_column(
        "employee",
        sa.Column("country_uid", sqlmodel.sql.sqltypes.GUID(), nullable=False),
    )
    op.create_foreign_key(None, "employee", "country", ["country_uid"], ["uid"])
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade migrations."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "employee", type_="foreignkey")  # type: ignore
    op.drop_column("employee", "country_uid")
    op.drop_index(op.f("ix_country_uid"), table_name="country")
    op.drop_table("country")
    # ### end Alembic commands ###
