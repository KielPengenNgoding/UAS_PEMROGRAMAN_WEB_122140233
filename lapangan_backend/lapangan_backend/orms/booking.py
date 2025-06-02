from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Date, UniqueConstraint
from sqlalchemy.orm import relationship
from .meta import Base

class BookingORM(Base):
    __tablename__ = 'bookings'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    court_id = Column(Integer, ForeignKey('courts.id_court'), nullable=False)
    booking_date = Column(Date, nullable=False)  # Store only the date
    time_slot = Column(String(20), nullable=False)  # Format: "08.00 - 09.00"
    full_name = Column(String(100))  # Optional, may be redundant with User
    phone_number = Column(String(20), nullable=False)
    status = Column(Enum('pending', 'confirmed', 'cancelled', name='booking_status_enum'), nullable=False)

    # Add a unique constraint to prevent double booking
    __table_args__ = (
        UniqueConstraint('court_id', 'booking_date', 'time_slot', name='unique_booking_constraint'),
    )

    # Relationships
    user = relationship("UserORM", back_populates="bookings")
    court = relationship("CourtORM", back_populates="bookings")
