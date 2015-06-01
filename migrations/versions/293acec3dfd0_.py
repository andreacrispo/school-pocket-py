"""empty message

Revision ID: 293acec3dfd0
Revises: None
Create Date: 2015-02-28 18:44:05.262391

"""

# revision identifiers, used by Alembic.
revision = '293acec3dfd0'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('confirmed', sa.Boolean(), nullable=True),
    sa.Column('img_profile', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_users_email', 'users', ['email'], unique=True)
    op.create_index('ix_users_username', 'users', ['username'], unique=True)
    op.create_table('subjects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('subject', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_subjects_subject', 'subjects', ['subject'], unique=False)
    op.create_table('homeworks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('homework', sa.String(length=255), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('deadline', sa.Date(), nullable=True),
    sa.Column('completed', sa.Boolean(), nullable=True),
    sa.Column('priority', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('subject_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['subject_id'], ['subjects.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('grades',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('grade', sa.Integer(), nullable=True),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('subject_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['subject_id'], ['subjects.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_grades_date', 'grades', ['date'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_grades_date', 'grades')
    op.drop_table('grades')
    op.drop_table('homeworks')
    op.drop_index('ix_subjects_subject', 'subjects')
    op.drop_table('subjects')
    op.drop_index('ix_users_username', 'users')
    op.drop_index('ix_users_email', 'users')
    op.drop_table('users')
    ### end Alembic commands ###
