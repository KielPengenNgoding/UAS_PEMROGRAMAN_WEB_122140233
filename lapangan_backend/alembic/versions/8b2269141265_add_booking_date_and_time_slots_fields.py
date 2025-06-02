"""Add booking_date and time_slots fields

Revision ID: 8b2269141265
Revises: add_image_url_to_courts
Create Date: 2025-06-01 10:13:47.873020

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8b2269141265'
down_revision: Union[str, None] = 'add_image_url_to_courts'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add new columns
    op.add_column('bookings', sa.Column('booking_date', sa.Date(), nullable=True))
    op.add_column('bookings', sa.Column('time_slot', sa.String(20), nullable=True))
    
    # Migrate data from time column to new columns
    conn = op.get_bind()
    bookings = conn.execute(sa.text('SELECT id, time FROM bookings')).fetchall()
    
    for booking_id, booking_time in bookings:
        if booking_time:
            # Update booking_date with the date part of the datetime
            conn.execute(
                sa.text(f"UPDATE bookings SET booking_date = '{booking_time.date()}' WHERE id = {booking_id}")
            )
            
            # Format the time slot based on the hour (assuming 1-hour slots)
            hour = booking_time.hour
            next_hour = hour + 1
            time_slot = f"{hour:02d}.00 - {next_hour:02d}.00"
            
            # Update the time_slot field
            conn.execute(
                sa.text(f"UPDATE bookings SET time_slot = '{time_slot}' WHERE id = {booking_id}")
            )
    
    # Make the new columns non-nullable after data migration
    op.alter_column('bookings', 'booking_date', nullable=False)
    op.alter_column('bookings', 'time_slot', nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    # Drop the new columns
    op.drop_column('bookings', 'time_slot')
    op.drop_column('bookings', 'booking_date')
