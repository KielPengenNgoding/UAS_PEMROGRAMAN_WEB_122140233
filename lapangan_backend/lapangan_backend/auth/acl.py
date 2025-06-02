"""
Access Control Lists (ACL) for the application.
"""
from pyramid.security import Allow, Everyone, Authenticated, ALL_PERMISSIONS

class RootFactory:
    """
    Root factory for the application that defines the ACL.
    This controls who can access what resources.
    """
    def __init__(self, request):
        self.request = request
        
    @property
    def __acl__(self):
        """
        Define the access control list.
        Format: (Allow/Deny, Principal, Permission)
        """
        return [
            (Allow, 'admin', 'admin'),           # Admins can access admin resources
            (Allow, Authenticated, 'view'),      # All authenticated users can view
            (Allow, Authenticated, 'create'),    # All authenticated users can create
            (Allow, Authenticated, 'edit_own'),  # All authenticated users can edit their own resources
            (Allow, Everyone, 'public'),         # Everyone can access public resources
        ]
