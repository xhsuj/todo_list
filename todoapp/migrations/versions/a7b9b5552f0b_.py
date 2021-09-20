"""empty message

Revision ID: a7b9b5552f0b
Revises: 1d67de549396
Create Date: 2021-08-02 09:30:24.951185

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a7b9b5552f0b'
down_revision = '1d67de549396'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('todos_list_id_fkey', 'todos', type_='foreignkey')
    op.create_foreign_key(None, 'todos', 'todolists', ['list_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'todos', type_='foreignkey')
    op.create_foreign_key('todos_list_id_fkey', 'todos', 'todolists', ['list_id'], ['id'])
    # ### end Alembic commands ###