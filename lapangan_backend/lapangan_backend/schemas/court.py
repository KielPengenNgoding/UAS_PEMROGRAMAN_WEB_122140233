from marshmallow import fields, validate, post_load
from .base import BaseSchema

class CourtSchema(BaseSchema):
    id_court = fields.Integer(dump_only=True)
    court_name = fields.String(required=True)
    court_category = fields.String(required=True)
    description = fields.String()
    status = fields.String(validate=validate.OneOf(['available', 'maintenance', 'booked']), required=False)
    image_url = fields.String(required=False)
    
    @post_load
    def set_defaults(self, data, **kwargs):
        """Set default values for fields if not provided."""
        if 'status' not in data or not data['status']:
            data['status'] = 'available'
        return data
    
    def set_schema_by_method(self, method):
        """Adjust schema fields based on HTTP method."""
        if method == 'PUT':
            self.fields['court_name'].required = False
            self.fields['court_category'].required = False
        elif method == 'POST':
            # For POST, all required fields remain required
            pass
