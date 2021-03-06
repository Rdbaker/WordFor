"""Add the 'runtime' column to the answers table.

Revision ID: db9cebab6ff7
Revises: 634731ff04c2
Create Date: 2016-09-25 18:19:05.739911

"""

# revision identifiers, used by Alembic.
revision = 'db9cebab6ff7'
down_revision = '634731ff04c2'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('answers', sa.Column('runtime', sa.Interval(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('answers', 'runtime')
    ### end Alembic commands ###
