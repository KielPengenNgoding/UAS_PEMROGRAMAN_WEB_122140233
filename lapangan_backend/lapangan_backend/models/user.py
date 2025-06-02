from ..orms.user import UserORM
from sqlalchemy.orm import Session, joinedload
from .booking import Booking

class User:
    def __init__(self, id, full_name, email, role, bookings=None):
        self.id = id
        self.full_name = full_name
        self.email = email
        self.role = role
        self.bookings = bookings or []

    @classmethod
    def from_orm(cls, orm_obj, include_bookings=False):
        bookings = []
        if include_bookings and hasattr(orm_obj, 'bookings') and orm_obj.bookings:
            from .booking import Booking  # Import here to avoid circular imports
            bookings = [Booking.from_orm(b) for b in orm_obj.bookings]
            
        return cls(
            id=orm_obj.id,
            full_name=orm_obj.full_name,
            email=orm_obj.email,
            role=orm_obj.role,
            bookings=bookings
        )

    def to_dict(self, include_bookings=False):
        result = {
            'id': self.id,
            'full_name': self.full_name,
            'email': self.email,
            'role': self.role
        }
        
        if include_bookings:
            result['bookings'] = [b.to_dict() for b in self.bookings]
            
        return result

    @classmethod
    def get_all(cls, dbsession: Session, include_bookings=False):
        query = dbsession.query(UserORM)
        if include_bookings:
            query = query.options(joinedload(UserORM.bookings))
        users_orm = query.all()
        return [cls.from_orm(user, include_bookings) for user in users_orm]

    @classmethod
    def get_by_id(cls, dbsession: Session, user_id: int, include_bookings=False):
        query = dbsession.query(UserORM).filter(UserORM.id == user_id)
        if include_bookings:
            query = query.options(joinedload(UserORM.bookings))
        user_orm = query.first()
        return cls.from_orm(user_orm, include_bookings) if user_orm else None

    @classmethod
    def create(cls, dbsession: Session, data: dict):
        new_user = UserORM(
            full_name=data['full_name'],
            email=data['email'],
            password=data['password'],  # In production, hash this password
            role=data['role']
        )
        dbsession.add(new_user)
        dbsession.flush()
        return cls.from_orm(new_user)

    @classmethod
    def update(cls, dbsession: Session, user_id: int, data: dict):
        user_orm = dbsession.query(UserORM).filter(UserORM.id == user_id).first()
        if user_orm:
            if 'full_name' in data:
                user_orm.full_name = data['full_name']
            if 'email' in data:
                user_orm.email = data['email']
            if 'password' in data:
                user_orm.password = data['password']  # In production, hash this password
            if 'role' in data:
                user_orm.role = data['role']
                
            dbsession.flush()
            return cls.from_orm(user_orm)
        return None

    @classmethod
    def delete(cls, dbsession: Session, user_id: int):
        user_orm = dbsession.query(UserORM).filter(UserORM.id == user_id).first()
        if user_orm:
            # Note: This will cascade delete all related bookings if configured in ORM
            dbsession.delete(user_orm)
            return True
        return False
