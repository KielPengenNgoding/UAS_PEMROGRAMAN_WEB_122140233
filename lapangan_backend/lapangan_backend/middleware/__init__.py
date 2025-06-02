from .jv import json_validator_tween_factory
from .cors import cors_tween_factory
from ..schemas import (
    UserSchema,
    CourtSchema,
    BookingSchema,
    LoginSchema,
    RegisterSchema,
    IJSONSchema
)
from pyramid.events import NewResponse

def includeme(config):
    """Initialize middleware configuration."""
    
    # Register the JSON validation tween
    config.add_tween('lapangan_backend.middleware.jv.json_validator_tween_factory')

    # Register schema utilities for main entities
    config.registry.registerUtility(UserSchema(), IJSONSchema, name='users_schema')
    config.registry.registerUtility(CourtSchema(), IJSONSchema, name='courts_schema')
    config.registry.registerUtility(BookingSchema(), IJSONSchema, name='bookings_schema')
    
    # Register schema utilities for authentication
    config.registry.registerUtility(LoginSchema(), IJSONSchema, name='auth_login_schema')
    config.registry.registerUtility(RegisterSchema(), IJSONSchema, name='auth_register_schema')

    # Register CORS middleware
    config.add_tween('lapangan_backend.middleware.cors.cors_tween_factory')
    
    # Add CORS support
    config.add_subscriber(add_cors_headers_response_callback, NewResponse)

def add_cors_headers_response_callback(event):
    """Add CORS headers to every response."""
    request = event.request
    response = event.response
    
    # Allow requests from frontend
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5173'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Content-Type, Accept, Authorization'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Expose-Headers'] = 'Content-Type,Content-Length'
    
    # Special headers for image requests
    if request.path.startswith('/images/'):
        response.headers['Access-Control-Allow-Methods'] = 'GET'
        response.headers['Cache-Control'] = 'public, max-age=3600'
