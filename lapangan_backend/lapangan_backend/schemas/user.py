from marshmallow import fields, validate, post_load
from .base import BaseSchema

class UserSchema(BaseSchema):
    id = fields.Integer(dump_only=True)
    full_name = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)
    role = fields.String(validate=validate.OneOf(['admin', 'user']), required=False)
    
    @post_load
    def set_defaults(self, data, **kwargs):
        """Set default values for fields if not provided."""
        if 'role' not in data or not data['role']:
            data['role'] = 'user'
        return data
    
    def set_schema_by_method(self, method):
        """Adjust schema fields based on HTTP method."""
        if method == 'PUT':
            self.fields['full_name'].required = False
            self.fields['email'].required = False
            self.fields['password'].required = False
        elif method == 'POST':
            # For POST, all required fields remain required
            pass
