from ..orms.booking import BookingORM
from ..orms.user import UserORM
from ..orms.court import CourtORM
from sqlalchemy.orm import Session, joinedload
from datetime import datetime, date
import re

class Booking:
    def __init__(self, id, user_id, court_id, booking_date, time_slot, full_name, phone_number, status, user=None, court=None):
        self.id = id
        self.user_id = user_id
        self.court_id = court_id
        self.booking_date = booking_date
        self.time_slot = time_slot
        self.full_name = full_name
        self.phone_number = phone_number
        self.status = status
        self.user = user
        self.court = court

    @classmethod
    def from_orm(cls, orm_obj, include_relations=False):
        user = None
        court = None
        
        if include_relations:
            if hasattr(orm_obj, 'user') and orm_obj.user:
                from .user import User  # Import here to avoid circular imports
                user = User.from_orm(orm_obj.user)
                
            if hasattr(orm_obj, 'court') and orm_obj.court:
                from .court import Court  # Import here to avoid circular imports
                court = Court.from_orm(orm_obj.court)
        
        return cls(
            id=orm_obj.id,
            user_id=orm_obj.user_id,
            court_id=orm_obj.court_id,
            booking_date=orm_obj.booking_date,
            time_slot=orm_obj.time_slot,
            full_name=orm_obj.full_name,
            phone_number=orm_obj.phone_number,
            status=orm_obj.status,
            user=user,
            court=court
        )

    def to_dict(self, include_relations=False):
        result = {
            'id': self.id,
            'user_id': self.user_id,
            'court_id': self.court_id,
            'booking_date': self.booking_date.isoformat() if isinstance(self.booking_date, date) else self.booking_date,
            'time_slot': self.time_slot,
            'full_name': self.full_name,
            'phone_number': self.phone_number,
            'status': self.status
        }
        
        if include_relations:
            if self.user:
                result['user'] = self.user.to_dict()
            if self.court:
                result['court'] = self.court.to_dict()
                
        return result

    @classmethod
    def get_all(cls, dbsession: Session, include_relations=False):
        query = dbsession.query(BookingORM)
        if include_relations:
            query = query.options(
                joinedload(BookingORM.user),
                joinedload(BookingORM.court)
            )
        bookings_orm = query.all()
        return [cls.from_orm(booking, include_relations) for booking in bookings_orm]

    @classmethod
    def get_by_id(cls, dbsession: Session, booking_id: int, include_relations=False):
        query = dbsession.query(BookingORM).filter(BookingORM.id == booking_id)
        if include_relations:
            query = query.options(
                joinedload(BookingORM.user),
                joinedload(BookingORM.court)
            )
        booking_orm = query.first()
        return cls.from_orm(booking_orm, include_relations) if booking_orm else None

    @classmethod
    def get_by_user(cls, dbsession: Session, user_id: int, include_relations=False):
        query = dbsession.query(BookingORM).filter(BookingORM.user_id == user_id)
        if include_relations:
            query = query.options(
                joinedload(BookingORM.user),
                joinedload(BookingORM.court)
            )
        bookings_orm = query.all()
        return [cls.from_orm(booking, include_relations) for booking in bookings_orm]

    @classmethod
    def get_by_court(cls, dbsession: Session, court_id: int, include_relations=False):
        query = dbsession.query(BookingORM).filter(BookingORM.court_id == court_id)
        if include_relations:
            query = query.options(
                joinedload(BookingORM.user),
                joinedload(BookingORM.court)
            )
        bookings_orm = query.all()
        return [cls.from_orm(booking, include_relations) for booking in bookings_orm]

    @classmethod
    def create(cls, dbsession: Session, data: dict):
        # Verify user exists
        user_id = data['user_id']
        user = dbsession.query(UserORM).filter(UserORM.id == user_id).first()
        if not user:
            raise ValueError(f"User with ID {user_id} not found")
            
        # Verify court exists
        court_id = data['court_id']
        court = dbsession.query(CourtORM).filter(CourtORM.id_court == court_id).first()
        if not court:
            raise ValueError(f"Court with ID {court_id} not found")
        
        # Get booking date and time slot
        booking_date = data['booking_date']
        time_slot = data['time_slot']
        
        # Parse date if it's a string
        if isinstance(booking_date, str):
            try:
                booking_date = date.fromisoformat(booking_date)
            except ValueError:
                raise ValueError("Invalid date format. Use ISO format (YYYY-MM-DD)")
        
        # Validate time slot format
        if not re.match(r'^\d{1,2}\.00 - \d{1,2}\.00$', time_slot):
            raise ValueError("Invalid time slot format. Use 'HH.00 - HH.00' format")
        
        new_booking = BookingORM(
            user_id=user_id,
            court_id=court_id,
            booking_date=booking_date,
            time_slot=time_slot,
            full_name=data.get('full_name', user.full_name),
            phone_number=data['phone_number'],
            status=data.get('status', 'pending')
        )
        dbsession.add(new_booking)
        dbsession.flush()
        return cls.from_orm(new_booking)

    @classmethod
    def update(cls, dbsession: Session, booking_id: int, data: dict):
        booking_orm = dbsession.query(BookingORM).filter(BookingORM.id == booking_id).first()
        if not booking_orm:
            return None
            
        if 'court_id' in data:
            court_id = data['court_id']
            court = dbsession.query(CourtORM).filter(CourtORM.id_court == court_id).first()
            if not court:
                raise ValueError(f"Court with ID {court_id} not found")
            booking_orm.court_id = court_id
            
        if 'booking_date' in data:
            booking_date = data['booking_date']
            if isinstance(booking_date, str):
                try:
                    booking_date = date.fromisoformat(booking_date)
                except ValueError:
                    raise ValueError("Invalid date format. Use ISO format (YYYY-MM-DD)")
            booking_orm.booking_date = booking_date
            
        if 'time_slot' in data:
            time_slot = data['time_slot']
            # Validate time slot format
            if not re.match(r'^\d{1,2}\.00 - \d{1,2}\.00$', time_slot):
                raise ValueError("Invalid time slot format. Use 'HH.00 - HH.00' format")
            booking_orm.time_slot = time_slot
            
        if 'full_name' in data:
            booking_orm.full_name = data['full_name']
            
        if 'phone_number' in data:
            booking_orm.phone_number = data['phone_number']
            
        if 'status' in data:
            booking_orm.status = data['status']
            
        dbsession.flush()
        return cls.from_orm(booking_orm)

    @classmethod
    def delete(cls, dbsession: Session, booking_id: int):
        booking_orm = dbsession.query(BookingORM).filter(BookingORM.id == booking_id).first()
        if booking_orm:
            dbsession.delete(booking_orm)
            return True
        return False
