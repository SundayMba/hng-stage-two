"""Added Organisational Model

Revision ID: 285b6cf88c65
Revises: 7454035112fa
Create Date: 2024-07-05 23:38:01.417899

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '285b6cf88c65'
down_revision = '7454035112fa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('organisations',
    sa.Column('orgId', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('orgId')
    )
    with op.batch_alter_table('organisations', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_organisations_name'), ['name'], unique=True)
        batch_op.create_index(batch_op.f('ix_organisations_orgId'), ['orgId'], unique=True)

    op.create_table('users_organisation',
    sa.Column('organisation_id', sa.String(), nullable=True),
    sa.Column('user_id', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['organisation_id'], ['organisations.orgId'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.userId'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users_organisation')
    with op.batch_alter_table('organisations', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_organisations_orgId'))
        batch_op.drop_index(batch_op.f('ix_organisations_name'))

    op.drop_table('organisations')
    # ### end Alembic commands ###
