from zope.interface import Interface

class IJSONSchema(Interface):
    def load(data):
        """Validate and deserialize input data."""

    def set_schema_by_method(method):
        """Adjust schema fields based on HTTP method."""
