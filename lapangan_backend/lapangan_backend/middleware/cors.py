def cors_tween_factory(handler, registry):
    """CORS tween factory."""
    
    def cors_tween(request):
        """Handle CORS requests."""
        # Handle OPTIONS request
        if request.method == 'OPTIONS':
            response = request.response
            response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5173'
            response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Origin, Content-Type, Accept, Authorization'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Max-Age'] = '3600'
            return response
            
        response = handler(request)
        
        # Add CORS headers to all responses
        response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5173'
        response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Origin, Content-Type, Accept, Authorization'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        
        # Add cache headers for images
        if request.path.startswith('/images/'):
            response.headers['Cache-Control'] = 'public, max-age=3600'
        
        return response
        
    return cors_tween
