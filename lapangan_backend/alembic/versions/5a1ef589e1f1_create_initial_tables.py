"""Create initial tables

Revision ID: 5a1ef589e1f1
Revises: 
Create Date: 2025-06-01 04:02:28.881483

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5a1ef589e1f1'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('courts',
    sa.Column('id_court', sa.Integer(), nullable=False),
    sa.Column('court_name', sa.String(length=100), nullable=False),
    sa.Column('court_category', sa.String(length=50), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('status', sa.Enum('available', 'maintenance', 'booked', name='court_status_enum'), nullable=False),
    sa.PrimaryKeyConstraint('id_court', name=op.f('pk_courts'))
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('full_name', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('role', sa.Enum('admin', 'user', name='user_role_enum'), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_users')),
    sa.UniqueConstraint('email', name=op.f('uq_users_email'))
    )
    op.create_table('bookings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('court_id', sa.Integer(), nullable=False),
    sa.Column('time', sa.DateTime(), nullable=False),
    sa.Column('full_name', sa.String(length=100), nullable=True),
    sa.Column('phone_number', sa.String(length=20), nullable=False),
    sa.Column('status', sa.Enum('pending', 'confirmed', 'cancelled', name='booking_status_enum'), nullable=False),
    sa.ForeignKeyConstraint(['court_id'], ['courts.id_court'], name=op.f('fk_bookings_court_id_courts')),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_bookings_user_id_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_bookings'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bookings')
    op.drop_table('users')
    op.drop_table('courts')
    # ### end Alembic commands ###
