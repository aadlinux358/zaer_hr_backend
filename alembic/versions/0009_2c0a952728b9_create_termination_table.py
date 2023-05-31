"""create termination table.

Revision ID: 2c0a952728b9
Revises: a52ad50c16c2
Create Date: 2023-05-30 19:28:19.919534

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '2c0a952728b9'
down_revision = 'a52ad50c16c2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade termination."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('termination',
    sa.Column('employee_uid', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('termination_date', sa.Date(), nullable=False),
    sa.Column('date_created', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('date_modified', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('uid', sqlmodel.sql.sqltypes.GUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('created_by', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('modified_by', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('hire_date', sa.Date(), nullable=False),
    sa.ForeignKeyConstraint(['employee_uid'], ['employee.uid'], ),
    sa.PrimaryKeyConstraint('uid'),
    sa.UniqueConstraint('employee_uid', 'hire_date', name='emp_hire'),
    sa.UniqueConstraint('employee_uid', 'termination_date', name="emp_term")
    )
    op.create_index(op.f('ix_termination_uid'), 'termination', ['uid'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade termination."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_termination_uid'), table_name='termination')
    op.drop_table('termination')
    # ### end Alembic commands ###
