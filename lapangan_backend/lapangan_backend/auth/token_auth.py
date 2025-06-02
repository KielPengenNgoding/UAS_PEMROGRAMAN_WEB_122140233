"""
Token-based authentication policy for Pyramid.
"""
from pyramid.authentication import CallbackAuthenticationPolicy
from pyramid.interfaces import IAuthenticationPolicy
from zope.interface import implementer
import logging
from pyramid.security import Everyone, Authenticated

log = logging.getLogger(__name__)

@implementer(IAuthenticationPolicy)
class TokenAuthenticationPolicy(CallbackAuthenticationPolicy):
    """
    A token-based authentication policy that extracts credentials from
    the Authorization header in the format 'Bearer <token>'.
    
    This policy works alongside the existing AuthTktAuthenticationPolicy
    to provide dual authentication methods.
    """
    
    def __init__(self, callback=None):
        self.callback = callback
    
    def unauthenticated_userid(self, request):
        """
        Extract the userid from the request's Authorization header.
        """
        # Try to get token from Authorization header
        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            token = auth_header[7:]  # Remove 'Bearer ' prefix
            
            # Check if token exists in our simple token store
            from .views import token_store
            if token in token_store:
                # Store the token in the request for later use in effective_principals
                request.token_info = token_store[token]
                log.info(f"Valid token found for user: {token_store[token]['email']} with role: {token_store[token]['role']}")
                # Store both user_id and email in request for proper authentication
                request.user_id = token_store[token]['user_id']
                request.user_email = token_store[token]['email']
                # Return user_id (numeric) for authentication
                return token_store[token]['user_id']
            
            log.warning(f"Invalid token received: {token[:10]}...")
            return None
        
        return None
    
    def remember(self, request, userid, **kw):
        """
        Return headers to remember this user.
        """
        # This policy doesn't set cookies, so return empty list
        return []
    
    def forget(self, request):
        """
        Return headers to forget this user.
        """
        # This policy doesn't set cookies, so return empty list
        return []
        
    def effective_principals(self, request):
        """
        Return a sequence representing the effective principals including the
        userid and any groups belonged to by the current user, including
        'system' groups such as Everyone and Authenticated.
        """
        effective_principals = [Everyone]
        
        try:
            userid = self.unauthenticated_userid(request)
            
            if userid is not None:
                effective_principals.append(Authenticated)
                effective_principals.append(userid)
                
                # If we have token_info stored in the request, use the role directly
                if hasattr(request, 'token_info') and 'role' in request.token_info:
                    role = request.token_info['role']
                    log.info(f"Adding role from token: {role}")
                    effective_principals.append(role)
                    
                    if role == 'admin':
                        log.info("User has admin role, adding admin permission")
                        effective_principals.append('admin')

                elif self.callback is not None:
                    try:
                        groups = self.callback(userid, request)
                        if groups is not None:
                            effective_principals.extend(groups)

                            if 'admin' in groups:
                                log.info("User has admin role from callback, adding admin permission")
                                effective_principals.append('admin')
                    except Exception as e:
                        log.error(f"Error in authentication callback: {str(e)}")
                        # Continue with basic authentication without groups
        except Exception as e:
            log.error(f"Error determining effective principals: {str(e)}")
            # Return only Everyone principal on error
            
        log.info(f"Token effective principals: {effective_principals}")
        return effective_principals


@implementer(IAuthenticationPolicy)
class CustomMultiAuthenticationPolicy(CallbackAuthenticationPolicy):
    """
    Custom implementation of a multi-authentication policy that tries multiple
    authentication policies in order until one succeeds.
    """
    
    def __init__(self, policies, callback=None):
        self.policies = policies
        self.callback = callback
    
    def authenticated_userid(self, request):
        """
        Return the authenticated userid or None if no authenticated userid can
        be found. This method of the policy should ensure that a record exists
        in whatever persistent store is used related to the user (the user
        should not have been deleted); if a record associated with the current
        id does not exist in a persistent store, it should return None.
        """
        for policy in self.policies:
            userid = policy.authenticated_userid(request)
            if userid is not None:
                return userid
        return None
    
    def unauthenticated_userid(self, request):
        """
        Return the unauthenticated userid. This method performs the same
        duty as authenticated_userid but is permitted to return the userid
        based only on data present in the request; it needn't (and shouldn't)
        check any persistent store to ensure that the user record related to
        the request userid exists.
        """
        for policy in self.policies:
            userid = policy.unauthenticated_userid(request)
            if userid is not None:
                return userid
        return None
    
    def effective_principals(self, request):
        """
        Return a sequence representing the effective principals including the
        userid and any groups belonged to by the current user, including
        'system' groups such as Everyone and Authenticated.
        """
        # Intentamos obtener los principales de cada política
        for policy in self.policies:
            principals = policy.effective_principals(request)
            if principals and len(principals) > 1:  # Si hay más que solo Everyone
                log.info(f"Using principals from policy {policy.__class__.__name__}: {principals}")
                return principals
        
        # Si ninguna política devolvió principales útiles, usamos el comportamiento predeterminado
        effective_principals = [Everyone]
        userid = self.authenticated_userid(request)
        if userid is not None:
            effective_principals.append(Authenticated)
            effective_principals.append(userid)
            if self.callback is not None:
                groups = self.callback(userid, request)
                if groups is not None:
                    effective_principals.extend(groups)
                    # Si 'admin' está en los grupos, añadimos explícitamente el permiso 'admin'
                    if 'admin' in groups:
                        log.info("User has admin role from callback in MultiAuth, adding admin permission")
                        effective_principals.append('admin')
        
        log.info(f"MultiAuth effective principals: {effective_principals}")
        return effective_principals
    
    def remember(self, request, userid, **kw):
        """
        Return a set of headers suitable for 'remembering' the userid named
        userid when set in a response. An individual authentication policy
        and its consumers can decide on the composition and meaning of
        **kw.
        """
        headers = []
        for policy in self.policies:
            headers.extend(policy.remember(request, userid, **kw))
        return headers
    
    def forget(self, request):
        """
        Return a set of headers suitable for 'forgetting' the current user
        on subsequent requests.
        """
        headers = []
        for policy in self.policies:
            headers.extend(policy.forget(request))
        return headers
