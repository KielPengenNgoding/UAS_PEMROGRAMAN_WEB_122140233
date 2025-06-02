from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from .meta import Base

class CourtORM(Base):
    __tablename__ = 'courts'

    id_court = Column(Integer, primary_key=True)
    court_name = Column(String(100), nullable=False)
    court_category = Column(String(50), nullable=False)
    description = Column(String(255))
    status = Column(Enum('available', 'maintenance', 'booked', name='court_status_enum'), nullable=False)
    image_url = Column(String(255), nullable=True)

    # Relationship
    bookings = relationship("BookingORM", back_populates="court")
