"""empty message

Revision ID: 5c452771fc
Revises: a63b187362
Create Date: 2014-09-20 21:26:20.009925

"""

# revision identifiers, used by Alembic.
revision = '5c452771fc'
down_revision = 'a63b187362'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('grades', sa.Column('date', sa.Date(), nullable=True))
    op.create_index(op.f('ix_grades_date'), 'grades', ['date'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_grades_date'), table_name='grades')
    op.drop_column('grades', 'date')
    ### end Alembic commands ###
