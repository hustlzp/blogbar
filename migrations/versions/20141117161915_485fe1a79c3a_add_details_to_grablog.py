"""Add details to GrabLog

Revision ID: 485fe1a79c3a
Revises: 2b2a56326a8d
Create Date: 2014-11-17 16:19:15.191461

"""

# revision identifiers, used by Alembic.
revision = '485fe1a79c3a'
down_revision = '2b2a56326a8d'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('grab_log', sa.Column('details', sa.Text(), nullable=True))
    op.add_column('grab_log', sa.Column('message', sa.Text(), nullable=True))
    op.drop_column('grab_log', 'error')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('grab_log', sa.Column('error', mysql.TEXT(), nullable=True))
    op.drop_column('grab_log', 'message')
    op.drop_column('grab_log', 'details')
    ### end Alembic commands ###