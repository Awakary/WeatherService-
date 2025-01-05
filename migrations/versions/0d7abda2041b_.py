"""empty message

Revision ID: 0d7abda2041b
Revises: b1ac385459ef
Create Date: 2024-12-02 00:57:55.966603

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0d7abda2041b'
down_revision: Union[str, None] = 'b1ac385459ef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('location', sa.Column('country', sa.String(), nullable=False))
    op.add_column('location', sa.Column('state', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('location', 'state')
    op.drop_column('location', 'country')
    # ### end Alembic commands ###
