import bcrypt
from ..orms.user import UserORM
import logging

log = logging.getLogger(__name__)

def hash_password(password):
    """
    Hash a password using bcrypt.
    
    Args:
        password: The plain text password
        
    Returns:
        Hashed password as a string
    """
    # Convert password to bytes if it's a string
    if isinstance(password, str):
        password = password.encode('utf-8')
        
    # Generate a salt and hash the password
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    
    # Return the hashed password as a string
    return hashed.decode('utf-8')

def check_password(plain_password, hashed_password):
    """
    Check if a plain text password matches a hashed password.
    
    Args:
        plain_password: The plain text password
        hashed_password: The hashed password to compare against
        
    Returns:
        True if the passwords match, False otherwise
    """
    # Convert passwords to bytes if they're strings
    if isinstance(plain_password, str):
        plain_password = plain_password.encode('utf-8')
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode('utf-8')
        
    # Check if the passwords match
    return bcrypt.checkpw(plain_password, hashed_password)

def get_user(identifier, request):
    """
    Get a user by email or user_id from the database.
    
    Args:
        identifier: The user's email or user_id
        request: The current request
        
    Returns:
        The user object if found, None otherwise
    """
    try:
        # Check if identifier is an integer (user_id) or string (email)
        if isinstance(identifier, int) or (isinstance(identifier, str) and identifier.isdigit()):
            # Convert to integer if it's a string containing digits
            user_id = int(identifier) if isinstance(identifier, str) else identifier
            return request.dbsession.query(UserORM).filter(UserORM.id == user_id).first()
        else:
            # Assume it's an email
            return request.dbsession.query(UserORM).filter(UserORM.email == identifier).first()
    except Exception as e:
        log.error(f"Error getting user: {str(e)}")
        # Make sure to abort the transaction on error
        try:
            request.tm.abort()
        except Exception as abort_error:
            log.error(f"Error aborting transaction: {str(abort_error)}")
        return None

def authenticate_user(email, password, request):
    """
    Authenticate a user by email and password.
    
    Args:
        email: The user's email
        password: The user's password
        request: The current request
        
    Returns:
        The user object if authentication is successful, None otherwise
    """
    user = get_user(email, request)
    if user is not None and check_password(password, user.password):
        return user
    return None


def groupfinder(userid, request):
    """
    Callback function used by the authentication policy to determine
    the groups (roles) a user belongs to.
    
    Args:
        userid: The user ID (typically email or username)
        request: The current request
        
    Returns:
        A list of groups the user belongs to, or None if the user doesn't exist
    """
    user = get_user(userid, request)
    if user is not None:
        # Return a list with the user's role
        return [user.role]
    return None
