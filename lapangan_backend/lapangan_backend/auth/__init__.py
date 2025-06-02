from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
import logging

from .security import groupfinder, get_user
from .token_auth import TokenAuthenticationPolicy, CustomMultiAuthenticationPolicy

log = logging.getLogger(__name__)

def includeme(config):
    """
    Configure authentication and authorization policies
    """
    # Set up cookie-based authentication policy
    cookie_policy = AuthTktAuthenticationPolicy(
        secret=config.registry.settings.get('auth.secret', 'lapangan-secret'),
        callback=groupfinder,
        hashalg='sha512',
        cookie_name='lapangan_auth_tkt',
        timeout=86400,  # 24 hours
    )
    
    # Set up token-based authentication policy
    token_policy = TokenAuthenticationPolicy(callback=groupfinder)
    
    # Combine both policies using CustomMultiAuthenticationPolicy
    # This allows authentication via either cookies or token headers
    multi_policy = CustomMultiAuthenticationPolicy(
        policies=[
            token_policy,  # Try token auth first
            cookie_policy   # Fall back to cookie auth
        ],
        callback=groupfinder
    )
    
    # Set up authorization policy
    authz_policy = ACLAuthorizationPolicy()
    
    # Set the policies
    config.set_authentication_policy(multi_policy)
    config.set_authorization_policy(authz_policy)
    
    # Add routes for authentication
    config.add_route('auth.login', '/auth/login')
    config.add_route('auth.register', '/auth/register')
    config.add_route('auth.logout', '/auth/logout')
    
    # Scan auth views
    config.scan('lapangan_backend.auth.views')
    
    log.info('Authentication configured')
