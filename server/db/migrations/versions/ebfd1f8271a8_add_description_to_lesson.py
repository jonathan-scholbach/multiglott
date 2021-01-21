"""Add description to Lesson

Revision ID: ebfd1f8271a8
Revises: 8aa739deac37
Create Date: 2021-01-21 15:29:11.723327

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ebfd1f8271a8'
down_revision = '8aa739deac37'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('lesson', sa.Column('description', sa.UnicodeText(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('lesson', 'description')
    # ### end Alembic commands ###
