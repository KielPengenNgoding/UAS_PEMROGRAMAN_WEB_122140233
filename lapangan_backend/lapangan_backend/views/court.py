from pyramid.view import view_config, view_defaults
from ..orms.court import CourtORM
from pyramid.httpexceptions import HTTPBadRequest, HTTPNotFound, HTTPUnprocessableEntity
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from ..schemas import CourtSchema

@view_defaults(route_name='court')
class CourtViews:
    def __init__(self, request):
        self.request = request

    @view_config(request_method='GET', renderer='json')
    def list(self):
        query = self.request.dbsession.query(CourtORM)
        
        # Get filter parameters from query string
        category = self.request.params.get('category')
        status = self.request.params.get('status')
        
        # Apply filters if provided
        if category:
            query = query.filter(CourtORM.court_category == category)
        if status:
            query = query.filter(CourtORM.status == status)
            
        courts = query.all()
        
        # Get unique categories for filter options
        categories = self.request.dbsession.query(CourtORM.court_category).distinct().all()
        categories = [cat[0] for cat in categories]
        
        return {
            'data': [self._court_to_dict(court) for court in courts],
            'total': len(courts),
            'categories': categories,
            'statuses': ['available', 'maintenance', 'booked']  # Fixed list of possible statuses
        }

    @view_config(request_method='POST', renderer='json')
    def add(self):
        try:
            # Inisialisasi schema dan atur berdasarkan metode HTTP
            schema = CourtSchema()
            schema.set_schema_by_method('POST')
            
            # Validasi dan deserialisasi input
            validated_data = schema.load(self.request.json_body)
            
            # Buat court baru dengan data yang sudah divalidasi
            new_court = CourtORM(
                court_name=validated_data['court_name'],
                court_category=validated_data['court_category'],
                description=validated_data.get('description', ''),
                status=validated_data.get('status', 'available')
            )
            self.request.dbsession.add(new_court)
            self.request.dbsession.flush()
            
            return {'message': 'Court added successfully', 'id_court': new_court.id_court}
        except ValidationError as e:
            # Tangani error validasi dari Marshmallow
            return HTTPUnprocessableEntity(detail={'validation_errors': e.messages})
        except IntegrityError:
            return HTTPBadRequest(detail='A court with this name already exists')

    def _court_to_dict(self, court):
        return {
            'id_court': court.id_court,
            'court_name': court.court_name,
            'court_category': court.court_category,
            'description': court.description,
            'status': court.status,
            'image_url': court.image_url
        }

@view_defaults(route_name='court_detail')
class CourtDetailViews:
    def __init__(self, request):
        self.request = request

    @view_config(request_method='GET', renderer='json')
    def detail(self):
        court_id = int(self.request.matchdict['id_court'])
        court = self.request.dbsession.query(CourtORM).filter(CourtORM.id_court == court_id).first()
        if court is None:
            return HTTPNotFound(detail='Court not found')
        return self._court_to_dict(court)

    @view_config(request_method='PUT', renderer='json')
    def update(self):
        try:
            court_id = int(self.request.matchdict['id_court'])
            court = self.request.dbsession.query(CourtORM).filter(CourtORM.id_court == court_id).first()
            if court is None:
                return HTTPNotFound(detail='Court not found')
            
            # Inisialisasi schema dan atur berdasarkan metode HTTP
            schema = CourtSchema()
            schema.set_schema_by_method('PUT')  # Ini akan membuat semua field menjadi opsional
            
            # Validasi dan deserialisasi input
            validated_data = schema.load(self.request.json_body)
            
            # Update court dengan data yang sudah divalidasi
            if 'court_name' in validated_data:
                court.court_name = validated_data['court_name']
            if 'court_category' in validated_data:
                court.court_category = validated_data['court_category']
            if 'description' in validated_data:
                court.description = validated_data['description']
            if 'status' in validated_data:
                court.status = validated_data['status']
            
            self.request.dbsession.flush()
            return {'message': 'Court updated successfully', 'id_court': court.id_court}
        except ValidationError as e:
            # Tangani error validasi dari Marshmallow
            return HTTPUnprocessableEntity(detail={'validation_errors': e.messages})
        except IntegrityError:
            return HTTPBadRequest(detail='Update would violate unique constraints')

    @view_config(request_method='DELETE', renderer='json')
    def delete(self):
        court_id = int(self.request.matchdict['id_court'])
        court = self.request.dbsession.query(CourtORM).filter(CourtORM.id_court == court_id).first()
        if court is None:
            return HTTPNotFound(detail='Court not found')
        
        self.request.dbsession.delete(court)
        return {'message': 'Court and related data deleted successfully', 'id_court': court_id}
    
    def _court_to_dict(self, court):
        return {
            'id_court': court.id_court,
            'court_name': court.court_name,
            'court_category': court.court_category,
            'description': court.description,
            'status': court.status,
            'image_url': court.image_url
        }
