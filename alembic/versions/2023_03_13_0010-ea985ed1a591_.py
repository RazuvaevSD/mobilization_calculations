"""empty message

Revision ID: ea985ed1a591
Revises: 
Create Date: 2023-03-13 00:10:59.013125

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea985ed1a591'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('documents',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('doc_type', sa.String(length=50), nullable=True),
    sa.Column('number', sa.String(), nullable=True),
    sa.Column('date', sa.String(), nullable=True),
    sa.Column('org_name', sa.String(length=800), nullable=True),
    sa.Column('pos_head', sa.String(length=450), nullable=True),
    sa.Column('pos_coordinator', sa.String(length=450), nullable=True),
    sa.Column('annex', sa.String(length=2), nullable=True),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['parent_id'], ['documents.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('organizations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('pos_head', sa.String(length=400), nullable=False),
    sa.Column('pos_coordinator', sa.String(length=400), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('amount',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('data_type', sa.String(length=50), nullable=True),
    sa.Column('document_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=450), nullable=True),
    sa.Column('type_expenses', sa.String(length=3), nullable=True),
    sa.Column('amounts_transfer', sa.String(), nullable=True),
    sa.Column('amount_economy', sa.String(), nullable=True),
    sa.Column('total', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['document_id'], ['documents.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('amount')
    op.drop_table('organizations')
    op.drop_table('documents')
    # ### end Alembic commands ###
