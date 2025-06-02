from pyramid.httpexceptions import HTTPUnprocessableEntity
from marshmallow import ValidationError
from ..schemas import IJSONSchema

def json_validator_tween_factory(handler, registry):
    """
    Tween factory for validating JSON input based on registered schemas.
    
    This tween intercepts requests with JSON content and validates them against
    the appropriate schema based on the URL path.
    """
    def json_validator_tween(request):
        if request.method in ['POST', 'PUT', 'PATCH'] and request.content_type == 'application/json':
            try:
                # Extract path components to determine which schema to use
                path_parts = request.path.strip('/').split('/')
                first_path = path_parts[0] if path_parts else ''
                
                # Handle special case for auth routes
                if first_path == 'auth' and len(path_parts) > 1:
                    # For auth routes like /auth/login or /auth/register
                    second_path = path_parts[1]
                    schema_name = f"auth_{second_path}_schema"
                else:
                    # For regular entity routes like /users, /courts, etc.
                    schema_name = f"{first_path}_schema"
                
                # Query the registry for the appropriate schema
                schema = registry.queryUtility(IJSONSchema, name=schema_name)
                
                if schema:
                    # Set schema validation rules based on HTTP method
                    schema.set_schema_by_method(request.method)
                    
                    # Validate the request body
                    schema.load(request.json_body)
            except ValidationError as e:
                # Return 422 Unprocessable Entity for validation errors
                raise HTTPUnprocessableEntity(json={'validation_errors': e.messages})
            except Exception as e:
                # Log the error but don't handle it here
                import logging
                log = logging.getLogger(__name__)
                log.error(f"Error in JSON validation: {str(e)}")
                
        # Continue with the request if validation passes or is not needed
        return handler(request)
    
    return json_validator_tween
