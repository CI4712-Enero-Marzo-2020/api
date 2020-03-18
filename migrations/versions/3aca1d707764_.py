"""empty message

Revision ID: 3aca1d707764
Revises: e9830bfaee9d
Create Date: 2020-02-29 05:02:34.511740

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3aca1d707764'
down_revision = 'e9830bfaee9d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('documentation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('dev_met', sa.Text(), nullable=False),
    sa.Column('version', sa.Float(), nullable=False),
    sa.Column('metaphor', sa.Text(), nullable=True),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('copyR',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('doc_id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['doc_id'], ['documentation.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('copyR')
    op.drop_table('documentation')
    # ### end Alembic commands ###
