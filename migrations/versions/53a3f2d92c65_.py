"""empty message

Revision ID: 53a3f2d92c65
Revises: 
Create Date: 2020-02-16 01:20:30.476516

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '53a3f2d92c65'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('books',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('author', sa.String(), nullable=True),
    sa.Column('published', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('userA',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=100), nullable=False),
    sa.Column('first_name', sa.String(length=100), nullable=False),
    sa.Column('last_name', sa.String(length=100), nullable=False),
    sa.Column('role', sa.String(length=100), nullable=False),
    sa.Column('password', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('logger',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user', sa.Integer(), nullable=True),
    sa.Column('event', sa.Enum('add_project', 'update_project', 'activate_project', 'pause_project', 'delete_project', 'search_project', 'user_register', 'user_login', 'user_role_assign', name='loggerevents'), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('loged_module', sa.String(length=100), nullable=False),
    sa.ForeignKeyConstraint(['user'], ['userA.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('projects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('status', sa.Enum('completed', 'paused', 'active', name='projectstatus'), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['userA.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('projects')
    op.drop_table('logger')
    op.drop_table('userA')
    op.drop_table('books')
    # ### end Alembic commands ###