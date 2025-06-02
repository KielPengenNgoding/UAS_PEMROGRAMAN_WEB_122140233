from pyramid.view import view_config, view_defaults
from ..orms.user import UserORM
from pyramid.httpexceptions import HTTPBadRequest, HTTPNotFound, HTTPUnprocessableEntity
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from ..schemas import UserSchema

@view_defaults(route_name='user')
class UserViews:
    def __init__(self, request):
        self.request = request

    @view_config(request_method='GET', renderer='json')
    def list(self):
        users = self.request.dbsession.query(UserORM).all()
        return {
            'data': [self._user_to_dict(user) for user in users],
            'total': len(users)
        }

    @view_config(request_method='POST', renderer='json')
    def add(self):
        try:
            # Inisialisasi schema dan atur berdasarkan metode HTTP
            schema = UserSchema()
            schema.set_schema_by_method('POST')
            
            # Validasi dan deserialisasi input
            validated_data = schema.load(self.request.json_body)
            
            # Buat user baru dengan data yang sudah divalidasi
            new_user = UserORM(
                full_name=validated_data['full_name'],
                email=validated_data['email'],
                password=validated_data['password'],  # In production, hash this password
                role=validated_data.get('role', 'user')
            )
            self.request.dbsession.add(new_user)
            self.request.dbsession.flush()
            
            return {'message': 'User added successfully', 'id': new_user.id}
        except ValidationError as e:
            # Tangani error validasi dari Marshmallow
            return HTTPUnprocessableEntity(detail={'validation_errors': e.messages})
        except IntegrityError:
            return HTTPBadRequest(detail='A user with this email already exists')

    def _user_to_dict(self, user):
        return {
            'id': user.id,
            'full_name': user.full_name,
            'email': user.email,
            'role': user.role
        }

@view_defaults(route_name='user_detail')
class UserDetailViews:
    def __init__(self, request):
        self.request = request

    @view_config(request_method='GET', renderer='json')
    def detail(self):
        user_id = int(self.request.matchdict['id'])
        user = self.request.dbsession.query(UserORM).filter(UserORM.id == user_id).first()
        if user is None:
            return HTTPNotFound(detail='User not found')
        return self._user_to_dict(user)

    @view_config(request_method='PUT', renderer='json')
    def update(self):
        try:
            user_id = int(self.request.matchdict['id'])
            user = self.request.dbsession.query(UserORM).filter(UserORM.id == user_id).first()
            if user is None:
                return HTTPNotFound(detail='User not found')
            
            # Inisialisasi schema dan atur berdasarkan metode HTTP
            schema = UserSchema()
            schema.set_schema_by_method('PUT')  # Ini akan membuat semua field menjadi opsional
            
            # Validasi dan deserialisasi input
            validated_data = schema.load(self.request.json_body)
            
            # Update user dengan data yang sudah divalidasi
            if 'full_name' in validated_data:
                user.full_name = validated_data['full_name']
            if 'email' in validated_data:
                user.email = validated_data['email']
            if 'password' in validated_data:
                user.password = validated_data['password']  # In production, hash this password
            if 'role' in validated_data:
                user.role = validated_data['role']
            
            self.request.dbsession.flush()
            return {'message': 'User updated successfully', 'id': user.id}
        except ValidationError as e:
            # Tangani error validasi dari Marshmallow
            return HTTPUnprocessableEntity(detail={'validation_errors': e.messages})
        except IntegrityError:
            return HTTPBadRequest(detail='Update would violate unique constraints')

    @view_config(request_method='DELETE', renderer='json')
    def delete(self):
        user_id = int(self.request.matchdict['id'])
        user = self.request.dbsession.query(UserORM).filter(UserORM.id == user_id).first()
        if user is None:
            return HTTPNotFound(detail='User not found')
        
        self.request.dbsession.delete(user)
        return {'message': 'User and related data deleted successfully', 'id': user_id}
    
    def _user_to_dict(self, user):
        return {
            'id': user.id,
            'full_name': user.full_name,
            'email': user.email,
            'role': user.role
        }
