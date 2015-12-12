"""empty message

Revision ID: 9dedc5d44b9
Revises: None
Create Date: 2015-12-08 18:52:14.353704

"""

# revision identifiers, used by Alembic.
revision = '9dedc5d44b9'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('questions', sa.Column('visited_count', sa.Integer(), nullable=True))
    op.create_unique_constraint(None, 'roles', ['name'])
    op.create_unique_constraint(None, 'tags', ['tag'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tags')
    op.drop_constraint(None, 'roles')
    op.drop_column('questions', 'visited_count')
    ### end Alembic commands ###