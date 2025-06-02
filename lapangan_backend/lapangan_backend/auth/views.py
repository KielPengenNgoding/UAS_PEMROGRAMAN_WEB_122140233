from pyramid.view import view_config
from pyramid.httpexceptions import HTTPBadRequest, HTTPUnprocessableEntity, HTTPFound
from pyramid.security import remember, forget
from marshmallow import ValidationError
from ..orms.user import UserORM
from .security import authenticate_user, hash_password
from ..schemas.auth import LoginSchema, RegisterSchema
import logging

log = logging.getLogger(__name__)

# Simple in-memory token store (in production, use a database)
token_store = {}

@view_config(route_name='auth.login', request_method='POST', renderer='json')
def login(request):
    """
    Login endpoint that authenticates a user and returns a token.
    """
    try:
        # Get credentials from request
        credentials = request.json_body
        
        # Validate input using LoginSchema
        schema = LoginSchema()
        try:
            validated_data = schema.load(credentials)
        except ValidationError as e:
            return HTTPUnprocessableEntity(json={
                'status': 'error',
                'message': 'Validation error',
                'errors': e.messages
            })
            
        email = validated_data['email']
        password = validated_data['password']
        
        # Authenticate user
        user = authenticate_user(email, password, request)
        if user is None:
            return HTTPUnprocessableEntity(json={
                'status': 'error',
                'message': 'Invalid email or password'
            })
        
        # Create authentication headers
        headers = remember(request, email)
        
        # Extract token from headers for client-side usage
        auth_token = None
        for key, value in headers:
            if key.lower() == 'authorization' or 'auth_tkt' in key.lower():
                auth_token = value
                break
        
        # If no token found in headers, generate a simple token
        if not auth_token:
            import hashlib
            import time
            token_base = f"{email}:{user.role}:{time.time()}"
            auth_token = hashlib.sha256(token_base.encode()).hexdigest()
            
            # Store token in token_store for later validation
            token_store[auth_token] = {
                'email': email,
                'role': user.role,
                'user_id': user.id,
                'created_at': time.time()
            }
        
        # Return success response with user info, token, and headers
        response = {
            'status': 'success',
            'message': 'Login successful',
            'token': auth_token,  # Include token in response body
            'user': {
                'id': user.id,
                'full_name': user.full_name,
                'email': user.email,
                'role': user.role
            }
        }
        request.response.headers.update(headers)
        return response
    except Exception as e:
        log.error(f"Login error: {str(e)}")
        return HTTPBadRequest(json={
            'status': 'error',
            'message': 'An error occurred during login'
        })

@view_config(route_name='auth.register', request_method='POST', renderer='json')
def register(request):
    """
    Register endpoint that creates a new user.
    """
    try:
        # Get user data from request
        user_data = request.json_body
        
        # Validate input data using RegisterSchema
        schema = RegisterSchema()
        try:
            validated_data = schema.load(user_data)
        except ValidationError as e:
            return HTTPUnprocessableEntity(json={
                'status': 'error',
                'message': 'Validation error',
                'errors': e.messages
            })
        
        # Check if user already exists
        existing_user = request.dbsession.query(UserORM).filter(
            UserORM.email == validated_data['email']
        ).first()
        
        if existing_user is not None:
            return HTTPUnprocessableEntity(json={
                'status': 'error',
                'message': 'User with this email already exists'
            })
        
        # Hash the password
        hashed_password = hash_password(validated_data['password'])
        
        # Create new user
        new_user = UserORM(
            full_name=validated_data['full_name'],
            email=validated_data['email'],
            password=hashed_password,
            role=validated_data.get('role', 'user')  # Default role is 'user'
        )
        
        # Add user to database
        request.dbsession.add(new_user)
        request.dbsession.flush()
        
        # Create authentication headers
        headers = remember(request, validated_data['email'])
        
        # Return success response with headers
        response = {
            'status': 'success',
            'message': 'User registered successfully',
            'user': {
                'id': new_user.id,
                'full_name': new_user.full_name,
                'email': new_user.email,
                'role': new_user.role
            }
        }
        request.response.headers.update(headers)
        return response
    except Exception as e:
        log.error(f"Registration error: {str(e)}")
        return HTTPBadRequest(json={
            'status': 'error',
            'message': 'An error occurred during registration'
        })

@view_config(route_name='auth.logout', renderer='json')
def logout(request):
    """
    Logout endpoint that invalidates the user's authentication token.
    """
    headers = forget(request)
    response = {
        'status': 'success',
        'message': 'Logged out successfully'
    }
    request.response.headers.update(headers)
    return response
