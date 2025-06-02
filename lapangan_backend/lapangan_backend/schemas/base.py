from zope.interface import implementer
from marshmallow import Schema
from .__interface__ import IJSONSchema

@implementer(IJSONSchema)
class BaseSchema(Schema):
    def load(self, data, **kwargs):
        """Validate and deserialize input data."""
        return super().load(data, **kwargs)
        
    def set_schema_by_method(self, method):
        """Adjust schema fields based on HTTP method."""
        # Default implementation — can be overridden
        pass
