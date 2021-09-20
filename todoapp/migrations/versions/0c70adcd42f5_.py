"""empty message

Revision ID: 0c70adcd42f5
Revises: 64279f73f801
Create Date: 2021-07-30 14:10:24.742591

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0c70adcd42f5'
down_revision = '64279f73f801'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('todos', sa.Column('completed', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###
    op.execute('update todos set completed=False where completed is null;')
    op.alter_column('todos','completed', nullable=False)
    


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('todos', 'completed')
    # ### end Alembic commands ###
