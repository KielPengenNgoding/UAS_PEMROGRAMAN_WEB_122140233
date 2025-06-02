from pyramid.config import Configurator
import logging
from .auth.acl import RootFactory
from pyramid.static import static_view
import os

log = logging.getLogger(__name__)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    with Configurator(settings=settings, root_factory=RootFactory) as config:
        # Include pyramid add-ons
        config.include('pyramid_jinja2')
        config.include('pyramid_tm')       # Transaction management
        config.include('pyramid_retry')    # Retry failed transactions
        
        # Include our packages
        config.include('.models')          # Include database models and session factory
        config.include('.auth')            # Include authentication and authorization
        config.include('.middleware')      # Include middleware for JSON validation and CORS
        config.include('.views')           # Include all views
        config.include('.routes')          # Include route definitions

        # Get the absolute path to the images directory
        here = os.path.dirname(os.path.dirname(__file__))
        images_path = os.path.join(here, '..', 'frontend_lapangan', 'public', 'images')
        images_path = os.path.abspath(images_path)
        
        # Ensure the images directory exists
        os.makedirs(images_path, exist_ok=True)
        
        # Add static view for serving uploaded images
        # This will serve files from the images directory at /images URL
        config.add_static_view(name='images', path=images_path)
        
        # Create uploads directory for court images
        uploads_dir = os.path.join(here, 'lapangan_backend', 'static', 'uploads', 'courts')
        os.makedirs(uploads_dir, exist_ok=True)
        log.info(f'Court uploads directory: {uploads_dir}')
        
        # Add static view for serving uploaded court images
        config.add_static_view(name='static', path='lapangan_backend:static')
        
        # Scan for view configurations
        config.scan()
        
        # Admin routes
        config.add_route('admin_courts', '/admin/courts')
        config.add_route('admin_court', '/admin/courts/{id_court}')
        config.add_route('admin_upload_image', '/admin/upload-image')
        config.add_route('admin_bookings', '/admin/bookings')
        
        log.info('Application initialized with authentication and middleware support')
        log.info(f'Images will be served from: {images_path}')
        return config.make_wsgi_app()
