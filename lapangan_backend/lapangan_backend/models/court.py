from ..orms.court import CourtORM
from sqlalchemy.orm import Session, joinedload

class Court:
    def __init__(self, id_court, court_name, court_category, description, status, image_url=None, bookings=None):
        self.id_court = id_court
        self.court_name = court_name
        self.court_category = court_category
        self.description = description
        self.status = status
        self.image_url = image_url
        self.bookings = bookings or []

    @classmethod
    def from_orm(cls, orm_obj, include_bookings=False):
        bookings = []
        if include_bookings and hasattr(orm_obj, 'bookings') and orm_obj.bookings:
            from .booking import Booking  # Import here to avoid circular imports
            bookings = [Booking.from_orm(b) for b in orm_obj.bookings]
            
        return cls(
            id_court=orm_obj.id_court,
            court_name=orm_obj.court_name,
            court_category=orm_obj.court_category,
            description=orm_obj.description,
            status=orm_obj.status,
            image_url=orm_obj.image_url if hasattr(orm_obj, 'image_url') else None,
            bookings=bookings
        )

    def to_dict(self, include_bookings=False):
        result = {
            'id_court': self.id_court,
            'court_name': self.court_name,
            'court_category': self.court_category,
            'description': self.description,
            'status': self.status,
            'image_url': self.image_url
        }
        
        if include_bookings:
            result['bookings'] = [b.to_dict() for b in self.bookings]
            
        return result

    @classmethod
    def get_all(cls, dbsession: Session, include_bookings=False):
        query = dbsession.query(CourtORM)
        if include_bookings:
            query = query.options(joinedload(CourtORM.bookings))
        courts_orm = query.all()
        return [cls.from_orm(court, include_bookings) for court in courts_orm]

    @classmethod
    def get_by_id(cls, dbsession: Session, court_id: int, include_bookings=False):
        query = dbsession.query(CourtORM).filter(CourtORM.id_court == court_id)
        if include_bookings:
            query = query.options(joinedload(CourtORM.bookings))
        court_orm = query.first()
        return cls.from_orm(court_orm, include_bookings) if court_orm else None

    @classmethod
    def create(cls, dbsession: Session, data: dict):
        new_court = CourtORM(
            court_name=data['court_name'],
            court_category=data['court_category'],
            description=data.get('description', ''),
            status=data['status'],
            image_url=data.get('image_url')
        )
        dbsession.add(new_court)
        dbsession.flush()
        return cls.from_orm(new_court)

    @classmethod
    def update(cls, dbsession: Session, court_id: int, data: dict):
        court_orm = dbsession.query(CourtORM).filter(CourtORM.id_court == court_id).first()
        if court_orm:
            if 'court_name' in data:
                court_orm.court_name = data['court_name']
            if 'court_category' in data:
                court_orm.court_category = data['court_category']
            if 'description' in data:
                court_orm.description = data['description']
            if 'status' in data:
                court_orm.status = data['status']
            if 'image_url' in data:
                court_orm.image_url = data['image_url']
                
            dbsession.flush()
            return cls.from_orm(court_orm)
        return None

    @classmethod
    def delete(cls, dbsession: Session, court_id: int):
        court_orm = dbsession.query(CourtORM).filter(CourtORM.id_court == court_id).first()
        if court_orm:
            # Note: This will cascade delete all related bookings if configured in ORM
            dbsession.delete(court_orm)
            return True
        return False
