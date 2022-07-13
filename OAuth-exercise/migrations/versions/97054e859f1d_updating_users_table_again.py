"""updating users table again

Revision ID: 97054e859f1d
Revises: a227661d6c1d
Create Date: 2022-07-13 23:15:56.831296

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '97054e859f1d'
down_revision = 'a227661d6c1d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'users', ['email'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    # ### end Alembic commands ###
