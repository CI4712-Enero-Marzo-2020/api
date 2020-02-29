"""empty message

Revision ID: 2b8bb5fd4ac4
Revises: 3aca1d707764
Create Date: 2020-02-29 05:06:01.243800

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2b8bb5fd4ac4'
down_revision = '3aca1d707764'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('intro',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('doc_id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['doc_id'], ['documentation.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('purpose',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('doc_id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['doc_id'], ['documentation.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('purpose')
    op.drop_table('intro')
    # ### end Alembic commands ###
