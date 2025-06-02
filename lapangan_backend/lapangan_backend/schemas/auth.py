from marshmallow import Schema, fields, validates, ValidationError, post_load
from .base import BaseSchema

class LoginSchema(BaseSchema):
    """
    Schema for validating login requests.
    """
    email = fields.Email(required=True, error_messages={'required': 'Email is required'})
    password = fields.String(required=True, error_messages={'required': 'Password is required'})
    
    def set_schema_by_method(self, method):
        """
        No changes needed based on HTTP method for login.
        """
        pass

class RegisterSchema(BaseSchema):
    """
    Schema for validating user registration requests.
    """
    full_name = fields.String(required=True, error_messages={'required': 'Full name is required'})
    email = fields.Email(required=True, error_messages={'required': 'Email is required'})
    password = fields.String(required=True, error_messages={'required': 'Password is required'})
    role = fields.String(required=False, validate=lambda x: x in ['user', 'admin'], 
                         error_messages={'validator_failed': 'Role must be either "user" or "admin"'})
    
    @post_load
    def set_defaults(self, data, **kwargs):
        """Set default values for fields if not provided."""
        if 'role' not in data or not data['role']:
            data['role'] = 'user'
        return data
    
    @validates('password')
    def validate_password(self, value, **kwargs):
        """
        Validate that the password meets minimum requirements.
        """
        if len(value) < 8:
            raise ValidationError('Password must be at least 8 characters long')
        
        # Check for at least one digit
        if not any(char.isdigit() for char in value):
            raise ValidationError('Password must contain at least one digit')
        
        # Check for at least one uppercase letter
        if not any(char.isupper() for char in value):
            raise ValidationError('Password must contain at least one uppercase letter')
    
    def set_schema_by_method(self, method):
        """
        No changes needed based on HTTP method for registration.
        """
        pass
