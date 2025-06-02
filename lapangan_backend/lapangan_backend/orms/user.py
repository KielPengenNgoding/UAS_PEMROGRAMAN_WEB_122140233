from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from .meta import Base

class UserORM(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    role = Column(Enum('admin', 'user', name='user_role_enum'), nullable=False)

    # Relationship
    bookings = relationship("BookingORM", back_populates="user")
