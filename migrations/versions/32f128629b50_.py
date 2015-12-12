"""empty message

Revision ID: 32f128629b50
Revises: 9dedc5d44b9
Create Date: 2015-12-09 11:26:58.135616

"""

# revision identifiers, used by Alembic.
revision = '32f128629b50'
down_revision = '9dedc5d44b9'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('unvotes',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('answer_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['answer_id'], ['answers.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'answer_id')
    )
    op.create_table('votes',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('answer_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['answer_id'], ['answers.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'answer_id')
    )
    op.create_unique_constraint(None, 'roles', ['name'])
    op.create_unique_constraint(None, 'tags', ['tag'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tags')
    op.drop_constraint(None, 'roles')
    op.drop_table('votes')
    op.drop_table('unvotes')
    ### end Alembic commands ###
